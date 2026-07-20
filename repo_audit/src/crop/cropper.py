from PIL import Image


class Cropper:

    def crop(self, image_path, box):

        img = Image.open(image_path)

        return img.crop(
            (
                box.x1,
                box.y1,
                box.x2,
                box.y2,
            )
        )
