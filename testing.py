from PIL import Image
from io import BytesIO
from os import listdir
from random import choice

import settings as s


# def create_userpic():
#     size = 320, 320
#     output = BytesIO()
#     image_filename = open((s.image_path + choice(listdir(s.image_path))), 'rb')
#     image = Image.open(image_filename)
#     image = image.convert('RGB')
#     image = image.resize(size)
#     image.save(output, format='JPEG', quality=80)
#     image.show()


def create_userpic():
    size = 320, 320
    output = BytesIO()
    image_filename = open((s.image_path + choice(listdir(s.image_path))), 'rb')
    image = Image.open(image_filename)
    bg = Image.new("RGB", image.size, (255, 255, 255))
    bg.paste(image, image)
    image.save(output, format='JPEG', quality=80)
    image.show()

def create_userpic_2():
    size = 320, 320
    output = BytesIO()
    image_filename = open((s.image_path + choice(listdir(s.image_path))), 'rb')
    image = Image.open(image_filename)
    new_image = Image.new('RGBA', image.size, 'white')
    new_image.paste(image, image)
    image = new_image.convert('RGB')
    image = image.resize(size)
    image.save(output, format='JPEG', quality=80)
    image.show()


create_userpic()
