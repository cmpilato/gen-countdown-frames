# gen-countdown-frames
Python script for generating still image frames useful for creating a countdown video

# Requirements
`gen-countdown-frames` requires:

* Python - the script is written in this language
* Pillow - the Python imaging library

# Usage
Run `gen-countdown-frames` as you would any other Python script on your system.  The command-line looks like this:

`$ gen-countdown-frame [OPTIONS] NUM_MINUTES`

## Options
* **-h, --help** - Display the usage message
* **--width=PX** - Generate image frames whose width is _PX_ pixels [_default: 1280_]
* **--height=PX** - Generate image frames whose height is _PX_ pixels [_default: 720_]
* **--font-file=FILENAME** - TrueType font file to use for countdown text [_default: arial.ttf_]
* **--font-size=PX** - Font size (in pixels) of countdown text [_default: 10% of the image width_]
* **--font-color=HEX** - Font color (as an RGB hex triplet) of countdown text [_default: FFFFFF_]
* **--position=LOC** - Rough location of text (with padding) [_default: c_]:
    * `tl`: top-left
    * `t`: top-center
    * `tr`: top-right
    * `l`: middle-left
    * `c`: middle-center
    * `r`: middle-right
    * `bl`: bottom-left
    * `b`: bottom-center
    * `br`: bottom-right

## Examples

### Generate 1280x720 images for 5 minutes of countdown, using white 128pt Arial, positioned in the center of the frame
`$ gen-countdown-frames 5`

### Generate 1280x720 images for 5 minutes of countdown, using yellow 128pt Arial, positioned in the bottom-left of the frame
`$ gen-countdown-frames --font-color FFFF00 --position bl 5`

### Generate 640x480 images for 1 minute of countdown, using white 24pt Centory Gothic, positioned in the bottom-right corner of the frame.
`$ gen-countdown-frames --width 640 --height 480 --font-file GOTHIC.TTF --font-size 24 --position br 1`

# License
MIT License
