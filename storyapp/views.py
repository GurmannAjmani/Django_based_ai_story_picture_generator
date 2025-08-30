import os
import json
import shutil
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest
from .storygen import generate_story_and_character_and_background

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# Import your image generation and combination code
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
import time
from PIL import Image

def save_image_from_bytes(image_data: bytes, filename: str):
    with open(filename, 'wb') as f:
        f.write(image_data)

def generate_character_image(character_description: str, out_path: str) -> str:
    # Always request a full-body, toe-to-hair, entire character in the prompt
    image_prompt = f"A photorealistic, full-body, entire character portrait of {character_description}, standing, visible from toe to hair, plain white background, sharp focus, professional photograph, 8k, no cropping, no cut-off, full figure visible, the whole character from feet to top of head, pastel shaded."
    api_key = os.environ.get("CLIPDROP_API_KEY")
    url = "https://clipdrop-api.co/text-to-image/v1"
    headers = { 'x-api-key': api_key }
    response = requests.post(url, files = { 'prompt': (None, image_prompt, 'text/plain') }, headers = headers)
    response.raise_for_status()
    save_image_from_bytes(response.content, out_path)
    return out_path

def generate_background_image(background_description: str, out_path: str) -> str:
    # Always include a road, pavement, or structure in the middle for the character to stand
    image_prompt = f"A highly detailed digital painting of {background_description}, with a road, pavement, or some kind of structure in the middle foreground , pastel shaded, clear space in the center foreground for a person."
    api_key = os.environ.get("CLIPDROP_API_KEY")
    url = "https://clipdrop-api.co/text-to-image/v1"
    headers = { 'x-api-key': api_key }
    response = requests.post(url, files = { 'prompt': (None, image_prompt, 'text/plain') }, headers = headers)
    response.raise_for_status()
    save_image_from_bytes(response.content, out_path)
    return out_path

def remove_white_bg(input_path, output_path, threshold=200):
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()
    new_data = []
    for item in datas:
        if item[0] > threshold and item[1] > threshold and item[2] > threshold:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)
    img.save(output_path)

def overlay_no_bg(fg_path, bg_path, output_path, scale=0.2):
    bg = Image.open(bg_path).convert("RGBA")
    fg = Image.open(fg_path).convert("RGBA")
    new_width = int(bg.width * scale)
    new_height = int(bg.height * scale)
    fg = fg.resize((new_width, new_height), Image.LANCZOS)
    x = (bg.width - fg.width) // 2
    y = bg.height - fg.height
    bg.paste(fg, (x, y), fg)
    bg.save(output_path)

@csrf_exempt
def story_form(request: HttpRequest):
    context = {}
    if request.method == 'POST':
        user_prompt = request.POST.get('prompt', '')
        context['generating'] = True
        if user_prompt:
            # Step 1: Generate story and descriptions
            results = generate_story_and_character_and_background(user_prompt)
            context.update(results)
            context['prompt'] = user_prompt

            # Step 2: Generate images and combine
            char_desc = results.get('char_description', '')
            bg_desc = results.get('bg_img_desc', '')
            media_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media')
            char_img_path = os.path.join(media_dir, 'char_image.png')
            bg_img_path = os.path.join(media_dir, 'bg_img.png')
            no_bg_path = os.path.join(media_dir, 'no_bg.png')
            final_img_path = os.path.join(media_dir, 'final.png')

            try:
                generate_character_image(char_desc, char_img_path)
                generate_background_image(bg_desc, bg_img_path)
                remove_white_bg(char_img_path, no_bg_path)
                overlay_no_bg(no_bg_path, bg_img_path, final_img_path, scale=0.2)  # 20% of bg size
                context['char_image_url'] = '/media/char_image.png'
                context['bg_image_url'] = '/media/bg_img.png'
                context['final_image_url'] = '/media/final.png'
            except Exception as e:
                context['image_error'] = f"Image generation error: {e}"
        context['generating'] = False
    return render(request, 'storyapp/story_form.html', context)
