from pathlib import Path
from .engine import compress_image


SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png", ".webp")


def is_image(file_path: Path) -> bool:
    return file_path.suffix.lower() in SUPPORTED_FORMATS


def scan_folder(folder_path: str) -> list:
    folder = Path(folder_path)
    return [p for p in folder.rglob("*") if p.is_file() and is_image(p)]


def compress_batch(files, output_dir, target_kb=500):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    results = []

    for idx, file_path in enumerate(files, start=1):
        output_name = f"{file_path.stem}_compressed_{idx}.jpg"
        output_path = output_dir / output_name

        try:
            success, size = compress_image(
                file_path,
                output_path,
                target_kb=target_kb
            )

            results.append({
                "file": file_path.name,
                "output": output_name,
                "success": success,
                "size_kb": round(size, 2)
            })

        except Exception as e:
            results.append({
                "file": file_path.name,
                "success": False,
                "error": str(e)
            })

    return results
