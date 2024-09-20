import torch
import numpy as np
from PIL import Image, ImageOps


class ResizeImage:
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "resizeImage"
    CATEGORY = "burak/image_utils/resize"
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE", {}),
            }
        }

    @staticmethod
    def validate(image):
        if isinstance(image, torch.Tensor):
            if image.ndim == 4:  # in comfyui, IMAGE datatype is torch.Tensor with shape [B,H,W,C]
                return True
            else:
                raise ValueError("Input doesn't has property shape.")
        else:
            raise TypeError("Input should be torch.tensor")

    # Tensor to PIL
    def tensor2pil(self, image):
        return Image.fromarray(np.clip(255.0 * image.cpu().numpy(), 0, 255).astype(np.uint8))  # H,W,C

    # Convert PIL to Tensor
    def pil2tensor(self, image):
        return torch.from_numpy(np.array(image).astype(np.float32) / 255.0)

    def resizeImage(self, image):
        self.validate(image)
        tensor_list = [self.pil2tensor(self.tensor2pil(image[i, :, :, :]).resize((128, 128), Image.LANCZOS)) for i in range(image.size(0))]
        # self.tensor2pil(torch.stack(tensor_list).squeeze()).save("debug.jpeg") # DEBUG
        return torch.stack(tensor_list)

    def split_image_with_alpha(self, image: torch.Tensor):
        out_images = [i[:, :, :3] for i in image]
        out_alphas = [i[:, :, 3] if i.shape[2] > 3 else torch.ones_like(i[:, :, 0]) for i in image]
        result = (torch.stack(out_images), 1.0 - torch.stack(out_alphas))
        return result


NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAMES_MAPPINGS = {}
