#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 11:20:08 2024

@author: hasti
"""

# reads the YAML file and returns its content. The main loop of the program runs indefinitely, 
# picking a random prompt from the YAML file's contents every 15 seconds, until the program is interrupted (e.g., by pressing Ctrl+C).

import yaml
import random
import time

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    yaml_file_path = '../resources/emoprompts.yaml'  # Replace with your YAML file path
    prompts = read_yaml(yaml_file_path)

    try:
        while True:
            prompt = random.choice(list(prompts.values()))
            print(f"Selected prompt: {prompt}")
            time.sleep(15)
    except KeyboardInterrupt:
        print("Program terminated by user.")

if __name__ == "__main__":
    main()

