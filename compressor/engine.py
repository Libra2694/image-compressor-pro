from PIL import Image
import os


def compress_image(
    input_path,
    output_path,
    target_kb=500,
    min_quality=30,
    resize_step=0.9
):
    img = Image.open(input_path)

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    quality = 95

    # QUALITY LOOP
    while quality >= min_quality:
        img.save(
            output_path,
            format="JPEG",
            quality=quality,
            optimize=True
        )

        size_kb = os.path.getsize(output_path) / 1024
        if size_kb <= target_kb:
            return True, size_kb

        quality -= 5

    # RESIZE LOOP
    width, height = img.size
    for _ in range(5):
        width = int(width * resize_step)
        height = int(height * resize_step)

        img = img.resize((width, height), Image.LANCZOS)
        img.save(
            output_path,
            format="JPEG",
            quality=min_quality,
            optimize=True
        )

        size_kb = os.path.getsize(output_path) / 1024
        if size_kb <= target_kb:
            return True, size_kb

    return False, size_kb
