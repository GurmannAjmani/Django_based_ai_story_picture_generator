# Story & Character Generator Django App

This Django web application generates a short story, a detailed character description, and a background description using Gemini AI, then creates AI-generated images for the character and background, and combines them visually. All images are pastel shaded and the character is always full-body, placed on a suitable structure in the background.

## Features
- Generate a 200-word story, 100-word character description, and 100-word background description from a prompt
- Generate a pastel-shaded, full-body character image (head to toe)
- Generate a pastel-shaded background image with a road/pavement/structure in the foreground for the character to stand
- Combine the character and background images, placing the character at the bottom center (20% of background size)
- View all images and text in a simple web interface

## Requirements
- Python 3.8+
- pip
- [Google Gemini API Key](https://aistudio.google.com/app/apikey)
- [Clipdrop API Key](https://clipdrop.co/apis)

## Setup Instructions

1. **Clone or Download the Repository**

2. **Create and Activate a Virtual Environment**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

3. **Install Dependencies**

```powershell
pip install -r requirements.txt
```

4. **Configure API Keys**

Create a `.env` file in the project root with the following content:

```
GOOGLE_API_KEY=your_google_api_key_here
CLIPDROP_API_KEY=your_clipdrop_api_key_here
```

Replace the values with your actual API keys.

5. **Apply Migrations**

```powershell
python manage.py migrate --settings=storyweb.settings
```

6. **Run the Development Server**

```powershell
python manage.py runserver --settings=storyweb.settings
```

7. **Open the App**

Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## How It Works
- Enter a prompt describing the story/character you want.
- The app uses Gemini AI to generate the story, character, and background descriptions.
- It then uses the Clipdrop API to generate a character image (full body, pastel shaded) and a background image (with a structure for the character to stand on, pastel shaded).
- The character image is processed to remove the white background and is overlaid on the background image at the bottom center (20% of background size).
- All results are displayed on the web page.

## Environment Variables
- `GOOGLE_API_KEY`: Your Google Gemini API key
- `CLIPDROP_API_KEY`: Your Clipdrop API key

## Notes
- All images are saved in the `media/` directory and served via Django's development server.
- For production, configure static/media file serving and use a secure method for managing secrets.

## Troubleshooting
- If you see errors about missing API keys, check your `.env` file.
- If image generation fails, check your API quota and network connection.
- For Windows, always use the provided PowerShell commands.

## License
This project is for educational/demo purposes only.
