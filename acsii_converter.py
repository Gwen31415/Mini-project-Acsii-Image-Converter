from PIL import Image, ImageDraw, ImageFont

color_table = [
    "#",
    "%",
    "$",
    "[",
    "/",
    "|",
    "t",
    "l",
    "*",
    "^",
    "a",
    "e",
    "n",
    "u",
    "r",
    "=",
    "+",
    ";",
    ":",
    ".",
    " "
]

color_table.reverse()

file_name = input("Enter file name: ")

img = Image.open(f"resources/{file_name}")

new_img_char = []
img_brightness = []

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 10)
char_w, char_h = 6, 10
width = img.size[0] * char_w * 2
height = img.size[1] * char_h

new_img = Image.new("RGB", (width, height), "black")
draw = ImageDraw.Draw(new_img)

for x in range(img.size[0]):
    for y in range(img.size[1]):
        pixel = img.getpixel((x, y))
        img_brightness.append(sum(pixel))

brighter = max(img_brightness)/(len(color_table)-1)
for y in range(img.size[1]):
    row = ""
    for x in range(img.size[0]):
        i = x * img.size[1] + y
        img_brightness[i] = round(img_brightness[i]/brighter)

        row += " " + color_table[img_brightness[i]]

    draw.text((0, y  * char_h), row, font=font, fill="white")
    new_img_char.append(row)

new_img.save(f"resources/{file_name.split(".")[0]}_acsii.png")

with open(f"resources/{file_name.split(".")[0]}.txt", "w") as file:
    file.write("\n".join(new_img_char))


