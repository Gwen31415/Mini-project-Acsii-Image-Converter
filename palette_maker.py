from PIL import Image, ImageDraw, ImageFont
from json import *

###

REMOVE_UNDERSCORES = True # remove underscore from the auto-generated palette

USE_UPPER_AND_LOWER = True # allow to also use the upper and the lower version of your characters : a,Z,e -> a,z,e,A,Z,E

###

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 10)
bbox = font.getbbox("#")
char_w = bbox[2] - bbox[0]
char_h = bbox[3] - bbox[1]

letter_img = Image.new("RGB", (char_w, char_h), "black")
draw = ImageDraw.Draw(letter_img)

table = input("Enter the char for the palette (format : #,@,e) (leave empty to auto generate) : ")

if table == "":
    table = [chr(index) for index in range(32, 127)]
    if REMOVE_UNDERSCORES:
        table.remove("_")
else:
    table = table.lower().split(",")
    table += [char.upper() for char in table if char.isalpha()]
    table = list(dict.fromkeys(table))

print(table)

brightness_table = []

for letter in table:
    letter_img.paste('black',(0,0,char_w,char_h))
    draw.text((0,-3), text=letter, font=font, fill="white")
    brightness = 0
    for x in range(0, char_w):
        for y in range(0, char_h):
            brightness += sum(letter_img.getpixel((x, y)))
    brightness_table.append(brightness)

palette = []

for _ in range(len(brightness_table)):
    i = brightness_table.index(min(brightness_table))
    brightness_table.pop(i)
    palette.append(table.pop(i))

with open('palette.json', 'w') as outfile:
    dump(palette, outfile)

print(palette)




