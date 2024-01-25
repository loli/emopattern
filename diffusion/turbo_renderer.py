#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from diffusers import AutoPipelineForText2Image, AutoPipelineForImage2Image
import torch
import sys

sys.path.append("/home/lunar/git/coupling_diffusion")
from diffusers import AutoencoderTiny
from sfast.compilers.stable_diffusion_pipeline_compiler import (compile, CompilationConfig)
from diffusers.utils import load_image
import lunar_tools as lt
import numpy as np
from PIL import Image
from lunar_tools.comms import OSCSender, OSCReceiver
from lunar_tools.control_input import MidiInput
sys.path.append("")
from prompt_blender import PromptBlender


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
    
blender = PromptBlender(pipe)
#%%

sz = (512*2, 512*2)
renderer = lt.Renderer(width=sz[1], height=sz[0])
latents = torch.randn((1,4,64,64)).half().cuda() # 64 is the fastest
# latents_additive = torch.randn((1,4,64,64)).half().cuda() # 64 is the fastest

prompt1 = "photo of a house"
prompt2 = "photo of a sad house"

embeds1 = blender.get_prompt_embeds(prompt1)
embeds2 = blender.get_prompt_embeds(prompt2)

while True:
    fract = akai_lpd8.get("E0", val_min=0, val_max=1)
    blended = blender.blend_prompts(embeds1, embeds2, fract)

    prompt_embeds, negative_prompt_embeds, pooled_prompt_embeds, negative_pooled_prompt_embeds = blended
    
    image = pipe(guidance_scale=0.0, num_inference_steps=1, latents=latents, prompt_embeds=prompt_embeds, negative_prompt_embeds=negative_prompt_embeds, pooled_prompt_embeds=pooled_prompt_embeds, negative_pooled_prompt_embeds=negative_pooled_prompt_embeds).images[0]
    
    # Render the image
    image = np.asanyarray(image)
    image = np.uint8(image)
    renderer.render(image)