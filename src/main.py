import os, sys, random
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

def sepia(image: ImageFile.ImageFile) -> Image.Image:
    DEPTH = 30

    processed_image = Image.new("RGB", image.size)
    (width, height) = image.size
    for x in range(width):
        for y in range(height):
            (r, g, b) = image.getpixel((x, y))
            avg = (r + g + b) // 3
            a = min(avg + DEPTH * 2, 255)
            b = min(avg + DEPTH, 255)
            c = avg
            processed_image.putpixel((x, y), (a, b, c))
    return processed_image

def negative(image: ImageFile.ImageFile) -> Image.Image:
    processed_image = Image.new("RGB", image.size)
    (width, height) = image.size
    for x in range(width):
        for y in range(height):
            (r, g, b) = image.getpixel((x, y))
            processed_image.putpixel((x, y), (255 - r, 255 - g, 255 - b))
    return processed_image

def noise(image: ImageFile.ImageFile) -> Image.Image:
    FACTOR = 60

    processed_image = Image.new("RGB", image.size)
    (width, height) = image.size
    for x in range(width):
        for y in range(height):
            (r, g, b) = image.getpixel((x, y))

            rand = random.randint(-FACTOR, FACTOR)
            color = [r + rand, g + rand, b + rand]
            for index, gradient in enumerate(color):
                if gradient < 0:
                    color[index] = 0
                elif gradient > 255:
                    color[index] = 255
            processed_image.putpixel((x, y), tuple(color))
    return processed_image

def main(transform: Callable[[ImageFile.ImageFile], Image.Image]):
    shrek_image = os.path.join(RESOURCES_DIR, "shrek.jpg")
    with Image.open(shrek_image) as image:
        processed_image = transform(image)
        image.show("Original")
        processed_image.show("Processed")


if __name__ == "__main__":
    transforms = (shades_of_gray, sepia, negative, noise)
    try:
        main(transforms[3])
    except Exception as exception:
        print(f"Error occured: {exception}", file=sys.stderr)
