from PIL import Image
import os
from app.config import settings


def validate_image(file_path: str) -> bool:
    """Validate if the file is a valid image."""
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception:
        return False


def get_image_info(file_path: str) -> dict:
    """Get basic information about an image."""
    try:
        with Image.open(file_path) as img:
            return {
                "format": img.format,
                "mode": img.mode,
                "size": img.size,
                "width": img.width,
                "height": img.height
            }
    except Exception as e:
        return {"error": str(e)}


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in settings.ALLOWED_EXTENSIONS
