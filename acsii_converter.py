from PIL import Image, ImageDraw, ImageFont
from json import load

with open("palette.json") as file:
    color_table = load(file)

file_name = input("Enter file name: ")

img = Image.open(f"resources/{file_name}")

new_img_char = []

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 10)
bbox = font.getbbox("#")
char_w = bbox[2] - bbox[0]
char_h = bbox[3] - bbox[1]
ratio = char_h/char_w

new_height = round(img.size[1] / ratio)
img = img.resize((img.size[0], new_height))

width = img.size[0] * char_w
height = img.size[1] * char_h

new_img = Image.new("RGB", (width, height), "black")
draw = ImageDraw.Draw(new_img)

img_brightness = []
for x in range(img.size[0]):
    for y in range(img.size[1]):
        pixel = img.getpixel((x, y))
        img_brightness.append(sum(pixel))

brighter = max(img_brightness)/(len(color_table)-1)
percent = 0
for y in range(img.size[1]):
    row = ""
    for x in range(img.size[0]):
        i = x * img.size[1] + y
        img_brightness[i] = round(img_brightness[i]/brighter)

        row +=  color_table[img_brightness[i]]

    draw.text((0, y  * char_h), row, font=font, fill="white")
    new_img_char.append(row)

new_img.save(f"resources/{file_name.split(".")[0]}_acsii.png")

with open(f"resources/{file_name.split(".")[0]}.txt", "w") as file:
    file.write("\n".join(new_img_char))


