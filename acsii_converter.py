import av

from PIL import Image, ImageDraw, ImageFont
from json import load

###

FILE_SIZE_RATIO = 1 # value from 0 to 1, 0 means that each pixel generate a character ( max quality ), 1 means file size will be as close as possible to the original

###

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 10)
bbox = font.getbbox("#")
char_w = bbox[2] - bbox[0]
char_h = bbox[3] - bbox[1]
ratio = char_h/char_w

valid_video_files = [
    "mp4",
    "mkv",
    "avi",
    "mjpeg",
    "m4a",
    "mov"
]

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

def convert(img, file_size_ratio=FILE_SIZE_RATIO):

    global font, char_h, char_w


    new_img_char = []

    new_height = round(img.size[1] / ratio)
    img = img.resize((img.size[0], new_height))

    ratio_width = max(1, char_w * file_size_ratio)
    ratio_height = max(1,char_h * file_size_ratio)
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
        file.write("\n".join(img_char))

elif file_format in valid_video_files:
    content = av.open(f"resources/{file_name}")
    input_stream = content.streams.video[0]
    fps = input_stream.average_rate

    output_file = av.open(f"resources/{file_name.split('.')[0]}_acsii.mp4","w")

    stream = output_file.add_stream("libx264", rate=fps)
    stream.pix_fmt = "yuv420p"
    stream.width = 0
    stream.height = 0

    for frame in content.decode(video=0):
        acsii_image = convert(frame.to_image(), 1)[1]
        if stream.width == 0:
            w, h = acsii_image.size

            stream.width = w - (w % 2)
            stream.height = h - (h % 2)

        if acsii_image.size != (stream.width, stream.height):
            acsii_image = acsii_image.crop((0, 0, stream.width, stream.height))

        acsii_frame = av.VideoFrame.from_image(acsii_image)

        for packet in stream.encode(acsii_frame):
            output_file.mux(packet)

    for packet in stream.encode():
        output_file.mux(packet)

    output_file.close()

else :
    print("Invalid file name")

