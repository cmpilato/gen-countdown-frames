# gen-countdown-frames
Python package for generating still image frames useful for creating a countdown video

# Installation

## From source
```bash
pip install -e .
```

## With development dependencies
```bash
pip install -e ".[dev]"
```

See [INSTALL.md](INSTALL.md) for more detailed installation and development instructions.

# Requirements
`gen-countdown-frames` requires:

* Python 3.8 or later
* Pillow - the Python imaging library

# Usage
After installation, use the `gen-countdown-frames` command:

`$ gen-countdown-frames [OPTIONS] NUM_MINUTES`

The result of a successful invocation is a collection of PNG image files in the current working directory whose names derive from the time displayed in the image, and which begin with an index that allows them to be easily sorted from _starting value_ to _0:00_:

    $ gen-countdown-frames --verbose 1
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
* **--baseline=PX** - Vertical adjustment in pixels (positive values move text up, negative values move text down) [_default: 0_]
* **--ring-height=PX** - Outer diameter (in pixels) of disappearing ring [_default: 80% of the smaller dimension_]
* **--ring-thickness=PX** - Thickness (in pixels) of the ring [_default: 10% of ring-height_]
* **--ring-color=HEX** - Ring color (as an RGB or RGBA hex value) [_default: same as font-color_]
* **--enable-ring** - Enable ring generation (in addition to numeric countdown)
* **--disable-text** - Disable text generation (show only ring countdown)
* **--rotate** - Rotate the generated images 180 degrees
* **-v, --verbose** - Show verbose output

## Examples
1280x720 images for 5 minutes of countdown, using white 128pt Arial, positioned in the center of the frame:

`$ gen-countdown-frames 5`

1280x720 images for 5 minutes of countdown, using yellow 128pt Arial, positioned in the bottom-left of the frame:

`$ gen-countdown-frames --font-color FFFF00 --position bl 5`

640x480 images for 1 minute of countdown, using white 24pt Century Gothic, positioned in the bottom-right corner of the frame:

`$ gen-countdown-frames --width 640 --height 480 --font-file GOTHIC.TTF --font-size 24 --position br 1`

1280x720 images for 2 minutes of countdown, rotated 180 degrees:

`$ gen-countdown-frames --rotate 2`

1280x720 images for 3 minutes of countdown with both numeric text and disappearing ring:

`$ gen-countdown-frames --enable-ring 3`

1280x720 images for 1 minute of countdown with custom ring size and color:

`$ gen-countdown-frames --enable-ring --ring-height 500 --ring-thickness 40 --ring-color FF0000 1`

1280x720 images for 2 minutes with only the disappearing ring (no text):

`$ gen-countdown-frames --enable-ring --disable-text 2`

640x480 images for 5 minutes with only numeric text (default behavior):

`$ gen-countdown-frames --width 640 --height 480 5`

# License
MIT License
