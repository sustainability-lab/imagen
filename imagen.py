import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io
import json
from datetime import datetime
from pathlib import Path

st.title("Imagen / Gemini Image Generator")

# Create docs/images directory if it doesn't exist
Path("docs/images").mkdir(parents=True, exist_ok=True)

prompt = st.text_area("Prompt", height=150)
filename = st.text_input("Save as filename", "output.png")

if st.button("Generate Image") and prompt.strip():
    with st.spinner("Generating image..."):
        client = genai.Client()

        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[{"google_search": {}}],
                image_config=types.ImageConfig(
                    aspect_ratio="16:9",
                    image_size="4K"
                )
            )
        )

        # extract inline_data bytes
        part = next((p for p in response.parts if getattr(p, "inline_data", None)), None)

        if part:
            raw_bytes = part.inline_data.data

            # Convert bytes → PIL Image (with format detection)
            img = Image.open(io.BytesIO(raw_bytes)).convert("RGB")

            # Save to docs/images directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_filename = f"{timestamp}_{filename}"
            image_path = f"docs/images/{image_filename}"
            img.save(image_path)

            # Update gallery.json
            gallery_path = "docs/gallery.json"
            try:
                with open(gallery_path, "r") as f:
                    gallery_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                gallery_data = {"images": []}

            gallery_data["images"].insert(0, {
                "image": f"images/{image_filename}",
                "prompt": prompt,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            with open(gallery_path, "w") as f:
                json.dump(gallery_data, f, indent=2)

            # Show in streamlit - use the PIL Image object
            st.image(img, caption=f"Saved as {image_path}")
            st.success(f"Image generated and saved to gallery!")

        else:
            st.error("No image returned.")
