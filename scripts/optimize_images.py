#!/usr/bin/env python3
"""Generate optimized thumbnails for gallery images."""

from PIL import Image
from pathlib import Path

IMAGES_DIR = Path("docs/images")
THUMBNAILS_DIR = IMAGES_DIR / "thumbnails"
MAX_WIDTH = 800
QUALITY = 85

def optimize_image(image_path):
    """Create optimized thumbnail for an image."""
    # Skip if already a thumbnail
    if "thumbnails" in str(image_path):
        return

    # Create thumbnails directory
    THUMBNAILS_DIR.mkdir(exist_ok=True)

    # Output path
    thumb_path = THUMBNAILS_DIR / image_path.name

    # Skip if thumbnail already exists and is newer
    if thumb_path.exists() and thumb_path.stat().st_mtime > image_path.stat().st_mtime:
        print(f"✓ Skipping {image_path.name} (thumbnail up to date)")
        return

    # Open and optimize
    try:
        img = Image.open(image_path)

        # Convert to RGB if needed
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background

        # Resize if needed
        if img.width > MAX_WIDTH:
            ratio = MAX_WIDTH / img.width
            new_height = int(img.height * ratio)
            img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)

        # Save optimized
        img.save(thumb_path, "PNG", optimize=True, quality=QUALITY)

        # Print size reduction
        original_size = image_path.stat().st_size / 1024 / 1024
        thumb_size = thumb_path.stat().st_size / 1024 / 1024
        reduction = (1 - thumb_size / original_size) * 100
        print(f"✓ {image_path.name}: {original_size:.1f}MB → {thumb_size:.1f}MB ({reduction:.0f}% smaller)")

    except Exception as e:
        print(f"✗ Error processing {image_path.name}: {e}")

def main():
    """Process all images in docs/images."""
    print("🖼️  Optimizing images for gallery...\n")

    image_files = [f for f in IMAGES_DIR.glob("*.png") if f.is_file()]

    if not image_files:
        print("No images found to optimize")
        return

    for image_path in sorted(image_files):
        optimize_image(image_path)

    print(f"\n✅ Processed {len(image_files)} images")

if __name__ == "__main__":
    main()
