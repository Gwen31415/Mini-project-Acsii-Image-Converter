# Mini-project-Acsii-Image-Converter
A python converter that take an image file as input and output a text and an image file of the image converted in acsii type art

## acsii-converter.py :
Used to create the acsii images or videos

Launch and input the name of your file (including the extension), it must be located in "resource/".

It will create a txt file and a png file from an image and a mp4 video from a video.
Everything is located in the resource file.

There is configurable option at the top of the file such as :

> FILE_SIZE_RATIO = 0.5 # value from 0 to 1, 0 means that each pixel generate a character ( max quality ), 1 means file size will be as close as possible to the original

## palette_maker.py :
Used to make a palette for the acsii-converter

Launch and input the character you want to use in the palette ( make sure to follow the right format ).

It sorts your characters per brightness and modify palette.json to use them.

Press Enter without answering to generate the default palette.

There is configurable option at the top of the file such as :

>REMOVE_UNDERSCORES = True # remove underscore from the auto-generated palette
>
>USE_UPPER_AND_LOWER = True # allow to also use the upper and the lower version of your characters : a,Z,e → a,z,e,A,Z,E


## palette.json
A simple JSON list with all the characters of the palette sorted in brightness order.

You can totally edit it manually.