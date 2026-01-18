"""Generate PNG images for each second of a countdown clock beginning just
under a given number of minutes and counting down to 0:00.  Files will be
created in the current working directory with names that derive from the
time values they contain and contain a sort-friendly initial numeric
index ("002-countdown-4_57.png", "290-countdown-0_09.png", etc.).

Usage:  __FILE__ [OPTIONS] NUM_MINUTES

Options:
   -h, --help        Display this help message
   --width=          Width (in pixels) of the generated images [1280]
   --height=         Height (in pixels) of the generated images [720]
   --font-file=      TrueType font file to use for countdown text [arial.ttf]
   --font-size=      Font size (in pixels) of countdown text [width / 10]
   --font-color=     Text color (as an RGB or RGBA hex value) [FFFFFFFF]
   --position=       Location of text (with proportional padding) [c]:
                        tl (top-left), t (top-centered), tr (top-right),
                        l (middle-left), c (middle-centered), r (middle-right),
                        bl (bottom-left), b (bottom-centered), br (bottom-right)
   --no-zeroes       Omit leading zeroes in minutes remaining
   --shadow-color=   Drop shadow color (as an RGB or RGBA hex value, if any)
   --baseline=       Vertical adjustment in pixels (positive=up, negative=down) [0]
   --ring-height=    Outer diameter (in pixels) of disappearing ring [min(width, height) * 0.8]
   --ring-thickness= Thickness (in pixels) of the ring [ring-height / 10]
   --ring-color=     Ring color (as an RGB or RGBA hex value) [font-color]
   --enable-ring     Enable ring generation (in addition to numeric countdown)
   --disable-text    Disable text generation (show only ring countdown)
   --rotate          Rotate the generated images 180 degrees
   -v, --verbose     Be noisy about what we're doing

Example(s):
   # 5-minute countdown 640x480 with centered Arial 24-point font
   gen-countdown-frames --width 640 --height 480 --font-size 24 5

   # 1-minute countdown 1280x720 with Century Gothic 120-point font
   # positioned in the bottom-right corner
   gen-countdown-frames --font-file GOTHIC.TTF --position br 1

   # 2-minute countdown with both numeric text and disappearing ring
   gen-countdown-frames --enable-ring --ring-height 500 --ring-thickness 40 2
"""

import sys
import getopt
import os
import re
from PIL import Image, ImageFont, ImageDraw


def usage_and_exit(msg=None):
    exit_code = 0
    stream = sys.stdout
    if msg:
        stream = sys.stderr
        stream.write("ERROR: %s\n\n" % msg)
        exit_code = 1
    stream.write(__doc__.replace("__FILE__", os.path.basename(sys.argv[0])))
    raise SystemExit(exit_code)


def gen_timestamp_image(
    width,
    height,
    font,
    font_color,
    shadow_color,
    shadow_offset,
    timestamp,
    position,
    baseline,
    ring_height,
    ring_thickness,
    ring_color,
    arc_fraction,
    enable_ring,
    disable_text,
    file_name,
    rotate=False,
):
    # New image
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    # New drawing canvas
    draw = ImageDraw.Draw(img)

    # Draw the ring if enabled (before text so text appears on top).
    if enable_ring and arc_fraction > 0:
        # Calculate the bounding box for the outer circle (centered).
        center_x = width / 2
        center_y = height / 2
        outer_radius = ring_height / 2

        outer_bbox = [
            center_x - outer_radius,
            center_y - outer_radius,
            center_x + outer_radius,
            center_y + outer_radius,
        ]

        # Calculate the bounding box for the inner circle.
        inner_radius = outer_radius - ring_thickness
        inner_bbox = [
            center_x - inner_radius,
            center_y - inner_radius,
            center_x + inner_radius,
            center_y + inner_radius,
        ]

        # Calculate arc angle based on remaining fraction.
        arc_degrees = 360 * arc_fraction
        start_angle = 270  # Start at top (12 o'clock position)
        end_angle = start_angle + arc_degrees

        # Draw shadow ring if shadow is enabled.
        if shadow_color is not None:
            shadow_outer_bbox = [
                outer_bbox[0] + shadow_offset,
                outer_bbox[1] + shadow_offset,
                outer_bbox[2] + shadow_offset,
                outer_bbox[3] + shadow_offset,
            ]
            shadow_inner_bbox = [
                inner_bbox[0] + shadow_offset,
                inner_bbox[1] + shadow_offset,
                inner_bbox[2] + shadow_offset,
                inner_bbox[3] + shadow_offset,
            ]
            draw.pieslice(shadow_outer_bbox, start_angle, end_angle, fill=shadow_color)
            if inner_radius > 0:
                draw.pieslice(shadow_inner_bbox, start_angle, end_angle, fill=(0, 0, 0, 0))

        # Draw outer arc (filled pieslice)
        draw.pieslice(outer_bbox, start_angle, end_angle, fill=ring_color)

        # Draw inner arc (transparent pieslice) to create the ring effect
        if inner_radius > 0:
            draw.pieslice(inner_bbox, start_angle, end_angle, fill=(0, 0, 0, 0))

    # Calculate the size required by the timestamp text.  We're going
    # to use the actual width of the timestamp text, but for the height
    # we'll normalize on the height needed to represent all the characters
    # we might use.
    if not disable_text:
        bbox = draw.textbbox((0, 0), timestamp, font)
        text_width = bbox[2] - bbox[0]
        bbox = draw.textbbox((0, 0), "0123456789:", font)
        text_height = bbox[3] - bbox[1]

        # Calculate the position of the text.  For a border on
        # edge-snapped positions, we'll use 5% of the smaller dimension.
        #
        # FIXME: Probably should do some bounds-checking here, handling
        #        rendered text that's too big to fit the image.
        border = min(width, height) * 0.05
        if position in ["tl", "l", "bl"]:
            # horizonally left-snapped
            text_x = border
        elif position in ["tr", "r", "br"]:
            # horizonally right-snapped
            text_x = width - text_width - border
        else:
            # horizontally centered
            text_x = (width - text_width) / 2
        if position in ["tl", "t", "tr"]:
            # vertically top-snapped
            text_y = border
        elif position in ["bl", "b", "br"]:
            # vertically bottom-snapped
            text_y = height - text_height - border
        else:
            # vertically centered
            text_y = (height - text_height) / 2

        # At least have the text begin in the frame...
        text_x = max(0, text_x)
        text_y = max(0, text_y)

        # Apply baselinement (positive moves up, negative moves down).
        text_y -= baseline

        # Draw the shadow (if any).
        if shadow_color is not None:
            draw.text(
                (text_x + shadow_offset, text_y + shadow_offset),
                timestamp,
                shadow_color,
                font,
            )

        # Draw the text.
        draw.text((text_x, text_y), timestamp, font_color, font)

    # Rotate the image if requested.
    if rotate:
        img = img.rotate(180)

    # Save the file.
    img.save(file_name)


def color_hex_to_tuple(color):
    regexp = r"^#?(([0-9a-fA-F]{2}){3,4})$"
    match = re.match(regexp, color)
    hex = match.group(1)
    r = int(hex[0:2], 16)
    g = int(hex[2:4], 16)
    b = int(hex[4:6], 16)
    a = 255
    if len(hex) > 6:
        a = int(hex[6:8], 16)
    return (r, g, b, a)


def main():
    opts, args = getopt.getopt(
        sys.argv[1:],
        "hv",
        [
            "help",
            "width=",
            "height=",
            "font-file=",
            "font-size=",
            "font-color=",
            "no-zeroes",
            "position=",
            "shadow-color=",
            "baseline=",
            "ring-height=",
            "ring-thickness=",
            "ring-color=",
            "enable-ring",
            "disable-text",
            "rotate",
            "verbose",
        ],
    )

    width = 1280
    height = 720
    font_file = "arial.ttf"
    font_size = None
    font_color = (255, 255, 255, 255)
    shadow_color = None
    position = "c"
    baseline = 0
    ring_height = None
    ring_thickness = None
    ring_color = None
    enable_ring = False
    disable_text = False
    zeroes = True
    rotate = False
    verbose = False

    # Parse options.
    for option, value in opts:
        if option in ["-h", "--help"]:
            usage_and_exit()
        elif option in ["--height"]:
            try:
                height = int(value)
            except Exception:
                usage_and_exit("Invalid value for --height")
        elif option in ["--width"]:
            try:
                width = int(value)
            except Exception:
                usage_and_exit("Invalid value for --width")
        elif option in ["--font-size"]:
            try:
                font_size = int(value)
            except Exception:
                usage_and_exit("Invalid value for --font-size")
        elif option in ["--font-file"]:
            font_file = value
        elif option in ["--font-color"]:
            try:
                font_color = color_hex_to_tuple(value)
            except Exception:
                usage_and_exit("Invalid value for --font-color")
        elif option in ["--no-zeroes"]:
            zeroes = False
        elif option in ["--position"]:
            if value not in ["tl", "t", "tr", "l", "c", "r", "bl", "b", "br"]:
                usage_and_exit("Invalid value for --position")
            position = value
        elif option in ["--shadow-color"]:
            try:
                shadow_color = color_hex_to_tuple(value)
            except Exception:
                usage_and_exit("Invalid value for --shadow-color")
        elif option in ["--baseline"]:
            try:
                baseline = int(value)
            except Exception:
                usage_and_exit("Invalid value for --baseline")
        elif option in ["--ring-height"]:
            try:
                ring_height = int(value)
            except Exception:
                usage_and_exit("Invalid value for --ring-height")
        elif option in ["--ring-thickness"]:
            try:
                ring_thickness = int(value)
            except Exception:
                usage_and_exit("Invalid value for --ring-thickness")
        elif option in ["--ring-color"]:
            try:
                ring_color = color_hex_to_tuple(value)
            except Exception:
                usage_and_exit("Invalid value for --ring-color")
        elif option in ["--enable-ring"]:
            enable_ring = True
        elif option in ["--disable-text"]:
            disable_text = True
        elif option in ["--rotate"]:
            rotate = True
        elif option in ["-v", "--verbose"]:
            verbose = True
        else:
            usage_and_exit(f"Unexpected option '{option}'")

    # Only non-optional argument is the number of minutes.
    if len(args) != 1:
        usage_and_exit("Not enough arguments")
    try:
        num_minutes = int(args[0])
        if num_minutes > 60:
            usage_and_exit("Maximum number of minutes is 60")
    except Exception:
        usage_and_exit("Invalid value for number of minutes")

    # If any ring option was explicitly specified, enable ring mode.
    if ring_height is not None or ring_thickness is not None or ring_color is not None:
        enable_ring = True

    # If there's no font size, we use text that's 10% of the width.
    if font_size is None:
        font_size = int(width / 10)

    # Calculate the would-be drop shadow offset.
    shadow_offset = int(font_size * 0.03)

    # Set default ring_height if not specified (80% of the smaller dimension).
    if ring_height is None:
        ring_height = int(min(width, height) * 0.8)

    # Handle ring mode settings.
    if enable_ring:
        if ring_thickness is None:
            ring_thickness = int(ring_height / 10)
        if ring_thickness * 2 >= ring_height:
            usage_and_exit("Thickness is too large for the given ring height")
        if ring_color is None:
            ring_color = font_color

    # Validate that at least one mode is enabled.
    if not enable_ring and disable_text:
        usage_and_exit("Cannot disable text without enabling ring")

    # Try to load the font.
    try:
        font = ImageFont.truetype(font_file, font_size)
    except Exception:
        usage_and_exit(f"Unable to load font file '{font_file}' and size {font_size}")

    format = "%d:%02d"
    if num_minutes >= 10 and zeroes:
        format = "%02d:%02d"
    num_images = num_minutes * 60
    filename_fmt = "%%0%dd-countdown-%%s.png" % (len(str(num_images)))
    index = 0
    for minute in range(num_minutes - 1, -1, -1):
        for second in range(59, -1, -1):
            timestamp = format % (minute, second)
            filename = filename_fmt % (index, timestamp.replace(":", "_"))
            arc_fraction = 1.0 - (
                (index + 1) / num_images
            )  # (first frame missing 1 arc, last frame empty)
            if verbose:
                sys.stdout.write(f"Create file '{filename}' ... ")
            gen_timestamp_image(
                width,
                height,
                font,
                font_color,
                shadow_color,
                shadow_offset,
                timestamp,
                position,
                baseline,
                ring_height,
                ring_thickness,
                ring_color,
                arc_fraction,
                enable_ring,
                disable_text,
                filename,
                rotate,
            )
            if verbose:
                sys.stdout.write("done.\n")
            index += 1
    if verbose:
        sys.stdout.write("Finished!\n")


if __name__ == "__main__":
    main()
