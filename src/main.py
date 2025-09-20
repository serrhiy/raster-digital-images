import os, sys
from collections.abc import Callable
from PIL import Image, ImageFile

RESOURCES_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "resources")
)


def shades_of_gray(image: ImageFile.ImageFile) -> Image.Image:
    processed_image = Image.new("RGB", image.size)
    (width, height) = image.size
    for x in range(width):
        for y in range(height):
            (r, g, b) = image.getpixel((x, y))
            avg = (r + g + b) // 3
            processed_image.putpixel((x, y), (avg, avg, avg))
    return processed_image


def main(transform: Callable[[ImageFile.ImageFile], Image.Image]):
    shrek_image = os.path.join(RESOURCES_DIR, "shrek.jpg")
    with Image.open(shrek_image) as image:
        processed_image = transform(image)
        image.show("Original")
        processed_image.show("Processed")


if __name__ == "__main__":
    transforms = (shades_of_gray,)
    try:
        main(transforms[0])
    except Exception as exception:
        print(f"Error occured: {exception}", file=sys.stderr)
