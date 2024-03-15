#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import torch
import numpy as np
import lunar_tools as lt
from diffusers import AutoencoderTiny, AutoPipelineForText2Image
from sfast.compilers.stable_diffusion_pipeline_compiler import (
    compile,
    CompilationConfig,
)

from prompt_blender import PromptBlender


# settings
use_maxperf = False  # whether to compile the model
fract_increment = (
    0.003  # usually 0.001 to 0.05; speed of transition between prompts (0 to 1)
)
ip_server = "10.50.10.15"  # ip of this machine, queque listens for new prompt
send = True  # whether to send generated images to render app's machine
ip_viewer = "10.50.10.17"  # ip of render app's machine, generated images are send there
render = False  # whether to render generated images also on this machine
render_size = (512, 512)  # (height, width) of rendered images on this machine

# initial prompts
prompt_last = "photo of a house"
prompt_next = "photo of a sad house"

# init torch
torch.set_grad_enabled(False)
torch.backends.cuda.matmul.allow_tf32 = False
torch.backends.cudnn.allow_tf32 = False

# init pipeline
pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16"
)
pipe.to("cuda")
pipe.vae = AutoencoderTiny.from_pretrained(
    "madebyollin/taesdxl", torch_device="cuda", torch_dtype=torch.float16
)
pipe.vae = pipe.vae.cuda()
pipe.set_progress_bar_config(disable=True)

# compile pipeline
if use_maxperf:
    config = CompilationConfig.Default()
    config.enable_xformers = True
    config.enable_triton = True
    config.enable_cuda_graph = True
    config.enable_jit = True
    config.enable_jit_freeze = True
    config.trace_scheduler = True
    config.enable_cnn_optimization = True
    config.preserve_parameters = False
    config.prefer_lowp_gemm = True

    pipe = compile(pipe, config)

# init objects
blender = PromptBlender(pipe)
comm_server = lt.ZMQPairEndpoint(is_server=True, ip=ip_server, port="5556")
if send:
    comm_viewer = lt.ZMQPairEndpoint(is_server=False, ip=ip_viewer, port="5557")
if render:
    renderer = lt.Renderer(width=render_size[1], height=render_size[0])

# network inits
latents = torch.randn((1, 4, 64, 64)).half().cuda()  # 64 is the fastest

# loop vars
embeds_last = blender.get_prompt_embeds(prompt_last)
embeds_current = embeds_last  # temp solution
embeds_next = blender.get_prompt_embeds(prompt_next)
fract = 0.0

while True:
    # check for ne wprompt received
    server_msgs = comm_server.get_messages()
    if len(server_msgs) > 0:
        # set embedding of newly received prompt as new target
        try:
            prompt_next = server_msgs[0]["prompt"]
            print(f"got new prompt: {prompt_next}")
        except Exception as e:
            print(f"bad message caused exception: {e}")
        embeds_next = blender.get_prompt_embeds(prompt_next)
        embeds_last = embeds_current
        fract = 0.0
    else:
        # generate next image, {fract} percentage towards the goal prompt
        fract = np.clip(fract, 0, 1)
        embeds_current = blender.blend_prompts(embeds_last, embeds_next, fract)
        (
            prompt_embeds,
            negative_prompt_embeds,
            pooled_prompt_embeds,
            negative_pooled_prompt_embeds,
        ) = embeds_current

        image = pipe(
            guidance_scale=0.0,
            num_inference_steps=1,
            latents=latents,
            prompt_embeds=prompt_embeds,
            negative_prompt_embeds=negative_prompt_embeds,
            pooled_prompt_embeds=pooled_prompt_embeds,
            negative_pooled_prompt_embeds=negative_pooled_prompt_embeds,
        ).images[0]

        # send image to client
        if send:
            comm_viewer.send_img(image)

        # tender the image
        if render:
            renderer.render(np.uint8(np.asanyarray(image)))

        fract += fract_increment
