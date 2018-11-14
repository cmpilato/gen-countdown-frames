# gen-countdown-frames
Python script for generating still image frames useful for creating a countdown video

# Requirements
`gen-countdown-frames` requires:

* Python - the script is written in this language
* Pillow - the Python imaging library

_### TODO: Determine supported/required versions of these things_

# Usage
Run `gen-countdown-frames` as you would any other Python script on your system.  The command-line looks like this:

`$ gen-countdown-frame [OPTIONS] NUM_MINUTES`

The result of a successful invocation of the script is a collection of PNG image files in the current working directory whose names derive from the time displayed in the image, and which begin with an index that allows them to be easily sorted from _starting value_ to _0:00_:

    $ gen-countdown-frame --verbose 1
    Create file '00-countdown-0_59.png' ... done.
    Create file '01-countdown-0_58.png' ... done.
    Create file '02-countdown-0_57.png' ... done.
    ...
    Create file '57-countdown-0_02.png' ... done.
    Create file '58-countdown-0_01.png' ... done.
    Create file '59-countdown-0_00.png' ... done.
    $ ls -1
    59-countdown-0_00.png
    58-countdown-0_01.png
    57-countdown-0_02.png
    ...

## Options
* **-h, --help** - Display the usage message
* **--width=PX** - Generate image frames whose width is _PX_ pixels [_default: 1280_]
* **--height=PX** - Generate image frames whose height is _PX_ pixels [_default: 720_]
* **--font-file=FILENAME** - TrueType font file to use for countdown text [_default: arial.ttf_]
* **--font-size=PX** - Font size (in pixels) of countdown text [_default: 10% of the image width_]
* **--font-color=HEX** - Text color (as an RGB or RGBA hex value) [_default: FFFFFFFF_]
* **--no-zeroes** - Omit leading zeroes from single-digit minutes (when NUM_MINUTES is greater than 9)
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
* **--shadow-color=HEX** - Drop shadow color (as an RGB or RGBA hex value, if any)
* **-v, --verbose** - Show verbose output

## Examples
1280x720 images for 5 minutes of countdown, using white 128pt Arial, positioned in the center of the frame:

`$ gen-countdown-frames 5`

1280x720 images for 5 minutes of countdown, using yellow 128pt Arial, positioned in the bottom-left of the frame:

`$ gen-countdown-frames --font-color FFFF00 --position bl 5`

640x480 images for 1 minute of countdown, using white 24pt Century Gothic, positioned in the bottom-right corner of the frame:

`$ gen-countdown-frames --width 640 --height 480 --font-file GOTHIC.TTF --font-size 24 --position br 1`

# License
MIT License
