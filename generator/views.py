from django.shortcuts import render
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('STABILITY_API_KEY')
URL = "https://api.stability.ai/v2beta/stable-image/generate/sd3"

def home(request):
    image_data = None
    error_message = None

    if request.method == "POST":
        prompt = request.POST.get("prompt", "").strip()
        if not prompt:
            error_message = "Please enter a prompt."
        elif not API_KEY:
            error_message = "API key missing — check your .env file"
        else:
            print(f"Generating: {prompt}")

            # THIS IS THE CORRECT WAY — multipart/form-data
            headers = {
                "Accept": "application/json",
                "Authorization": f"Bearer {API_KEY}",
            }

            data = {
                "prompt": prompt,
                "model": "sd3-turbo",           # fastest & cheapest
                "aspect_ratio": "1:1",
                "output_format": "png",
            }


            response = requests.post(
                URL,
                headers=headers,
                files={
                    "prompt": (None, prompt),
                    "model": (None, "sd3-turbo"),
                    "aspect_ratio": (None, "1:1"),
                    "output_format": (None, "png"),
                }
            )

            print(f"Status code: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                image_data = result["image"]   # base64 string ready to use
                print("Image generated successfully!")
            else:
                try:
                    error_detail = response.json().get("errors", [response.text])[0]
                except:
                    error_detail = response.text
                error_message = f"API Error {response.status_code}: {error_detail}"
                print(error_message)

    return render(request, "generator/home.html", {
        "image_data": image_data,
        "error_message": error_message
    })