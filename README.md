# Imagen Gallery

A Streamlit app for generating images using Google's Gemini Imagen model, with automatic gallery publishing to GitHub Pages.

## Features

- Generate images using Gemini 3 Pro Image Preview
- Clean, responsive gallery interface
- Automatic deployment to GitHub Pages
- Stores prompts alongside generated images

## Setup

1. Install dependencies:
```bash
pip install streamlit google-genai pillow
```

2. Run the Streamlit app:
```bash
streamlit run imagen.py
```

3. Generate images - they'll automatically be saved to `docs/images/` and added to the gallery

## GitHub Pages

The gallery is automatically deployed to GitHub Pages whenever you push images to the `docs/` directory.

To enable GitHub Pages:
1. Go to your repository Settings
2. Navigate to Pages
3. Set Source to "GitHub Actions"

Your gallery will be available at: `https://<username>.github.io/<repo-name>/`

## How it Works

1. Enter a prompt in the Streamlit app
2. Click "Generate Image"
3. Image is saved to `docs/images/` with timestamp
4. `docs/gallery.json` is updated with prompt and metadata
5. Commit and push changes
6. GitHub Actions deploys to Pages automatically
