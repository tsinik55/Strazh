from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO

back_ground_color = (50, 50, 50)

# unicode_text = "some test\U0001f602"
unicode_text = '\U0001f602'
emoji = Image.new("RGB", (160, 160))
draw = ImageDraw.Draw(emoji)

draw.text((0, 0), '\U0001f602', font=ImageFont.truetype('AppleColorEmoji.ttf', 137), embedded_color=True,
          transparency=0)

emoji.show()

buffered = BytesIO()
emoji.save(buffered, format='JPG')
img_str = base64.b64encode(buffered.getvalue())

print(img_str)

bytes_decoded = base64.b64decode(img_str)
img = Image.open(BytesIO(bytes_decoded))
img.show()

out_img = img.convert("RGB")

# save file
out_img.save("saved_img.jpg")