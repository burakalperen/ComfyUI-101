from .resize_image import ResizeImage

NODE_CLASS_MAPPINGS = {
    "resizeImage": ResizeImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "resizeImage": "resize image to (128,128)",
}

WEB_DIRECTORY = "js"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
