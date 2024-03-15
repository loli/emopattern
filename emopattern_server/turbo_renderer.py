#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from diffusers import AutoPipelineForText2Image, AutoPipelineForImage2Image
import torch
import sys

#sys.path.append("/home/lunar/git/coupling_diffusion")
from diffusers import AutoencoderTiny
from sfast.compilers.stable_diffusion_pipeline_compiler import (compile, CompilationConfig)
from diffusers.utils import load_image
import lunar_tools as lt
import numpy as np
from PIL import Image
from lunar_tools.comms import OSCSender, OSCReceiver
from lunar_tools.control_input import MidiInput
from prompt_blender import PromptBlender


#%%
ip_server = '10.50.10.15'
ip_viewer = "10.50.10.17"

akai_lpd8 = MidiInput(device_name="akai_lpd8")

    

torch.set_grad_enabled(False)
torch.backends.cuda.matmul.allow_tf32 = False
torch.backends.cudnn.allow_tf32 = False

use_maxperf = False
use_image_mode = False

pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16")

pipe.to("cuda")
pipe.vae = AutoencoderTiny.from_pretrained('madebyollin/taesdxl', torch_device='cuda', torch_dtype=torch.float16)
pipe.vae = pipe.vae.cuda()
pipe.set_progress_bar_config(disable=True)

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
    
blender = PromptBlender(pipe, use_compel=True)
comm_server = lt.ZMQPairEndpoint(is_server=True, ip=ip_server, port='5556')
comm_viewer = lt.ZMQPairEndpoint(is_server=False, ip=ip_viewer, port='5557')

#%%
fract_increment = 0.003
sz = (512*2, 512*2)
renderer = lt.Renderer(width=sz[1], height=sz[0])
latents = torch.randn((1,4,64,64)).half().cuda() # 64 is the fastest
# latents_additive = torch.randn((1,4,64,64)).half().cuda() # 64 is the fastest

prompt_last = "photo of a house"
prompt_next = "photo of a sad house"

embeds_last = blender.get_prompt_embeds(prompt_last)
embeds_current = embeds_last # temp solution
embeds_next = blender.get_prompt_embeds(prompt_next)
fract = 0

while True:
    fract_increment = akai_lpd8.get("H0", val_min=0.001, val_max=0.05)
    # Check if there was something new being sent
    server_msgs = comm_server.get_messages()
    if len(server_msgs) > 0:
        # Find a new target
        try:
            prompt_next = server_msgs[0]['prompt']
            print(f"got new prompt: {prompt_next}")
        except Exception as e:
            print(f"bad message caused exception: {e}")
        embeds_next = blender.get_prompt_embeds(prompt_next)
        embeds_last = embeds_current
        fract = 0
    else:
        fract = np.clip(fract, 0, 1)
        embeds_current = blender.blend_prompts(embeds_last, embeds_next, fract)
        prompt_embeds, negative_prompt_embeds, pooled_prompt_embeds, negative_pooled_prompt_embeds = embeds_current
        
        image = pipe(guidance_scale=0.0, num_inference_steps=1, latents=latents, prompt_embeds=prompt_embeds, negative_prompt_embeds=negative_prompt_embeds, pooled_prompt_embeds=pooled_prompt_embeds, negative_pooled_prompt_embeds=negative_pooled_prompt_embeds).images[0]
        
        # Render the image
        image = np.asanyarray(image)
        image = np.uint8(image)
        renderer.render(image)
        #comm_viewer.send_img(image)
        fract += fract_increment