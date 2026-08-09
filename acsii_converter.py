from PIL import Image, ImageDraw, ImageFont
from json import load

###

FILE_SIZE_RATIO = 0 # value from 0 to 1, 1 means that the output will be as close as possible to the original size, 0 means that each pixel generate a character

###

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 10)
bbox = font.getbbox("#")
char_w = bbox[2] - bbox[0]
char_h = bbox[3] - bbox[1]
ratio = char_h/char_w


valid_image_files = [
    "jpg",
    "jpe",
    "jpeg",
    "jfif",
    "png",
    "apng",
    "bmp",
    "dib",
    "gif",
    "tif",
    "tiff",
    "webp",
    "ico",
    "icns",
    "eps",
    "ps",
    "pbm",
    "pgm",
    "pnm",
    "ppm",
    "pcx",
    "tga",
    "icb",
    "vda",
    "vst",
    "sgi",
    "bw",
    "rgb",
    "rgba",
    "xbm",
    "dds",
    "msp",
    "wmf",
    "emf",
    "jp2",
    "j2k",
    "jpc",
    "jpf",
    "jpx",
    "h5",
    "hdf"
]

def convert(img):

    global font, char_h, char_w


    new_img_char = []

    new_height = round(img.size[1] / ratio)
    img = img.resize((img.size[0], new_height))

    ratio_width = max(1, char_w * FILE_SIZE_RATIO)
    ratio_height = max(1,char_h * FILE_SIZE_RATIO)
    new_width = int(img.size[0] // ratio_width)
    new_height = int(img.size[1] // ratio_height)
    img = img.resize((new_width, new_height))

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
    for y in range(img.size[1]):
        row = ""
        for x in range(img.size[0]):
            i = x * img.size[1] + y
            img_brightness[i] = round(img_brightness[i]/brighter)

            row +=  color_table[img_brightness[i]]

        draw.text((0, y  * char_h), row, font=font, fill="white")
        new_img_char.append(row)

    return new_img_char, new_img


with open("palette.json") as file:
    color_table = load(file)

file_name = input("Enter file name: ")
file_format = file_name.split(".")[-1]
if file_format in valid_image_files:
    content = Image.open(f"resources/{file_name}")

    img_char, new_img_file = convert(content)
    new_img_file.save(f"resources/{file_name.split(".")[0]}_acsii.png")

    with open(f"resources/{file_name.split(".")[0]}.txt", "w") as file:
        file.write("\n".join(new_img_char))
        file.write("\n".join(img_char))

else :
    print("Invalid file name")

