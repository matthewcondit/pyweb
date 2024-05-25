import argparse
import logging
import shutil
import sys
import traceback

import numpy as np
from PIL import Image
from termcolor import colored

# Configure Logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Constants for terminal character size in pixels
CHAR_WIDTH = 8
CHAR_HEIGHT = 16

# Use a set of block elements and box-drawing characters
UNICODE_BLOCKS = [
    " ",
    "░",
    "▒",
    "▓",
    "█",
    "▌",
    "▐",
    "▀",
    "▄",
    "▖",
    "▗",
    "▘",
    "▝",
    "▞",
    "▟",
    "▙",
    "▚",
    "▛",
]


def get_terminal_size():
    """
    Get the current size of the terminal in columns and lines.
    Returns a tuple (columns, lines).
    """
    size = shutil.get_terminal_size()
    return size.columns, size.lines


def rgb_to_grayscale(rgb):
    """
    Convert an RGB tuple to a grayscale value using the formula:
    0.299 * R + 0.587 * G + 0.114 * B
    """
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]


def rgb_to_ansi(rgb):
    """
    Convert an RGB tuple to an ANSI color code.
    """
    r, g, b = rgb
    return f"\033[38;2;{r};{g};{b}m"


def chunk_to_unicode(chunk):
    """
    Convert a chunk of the image (8x16 pixels) to a corresponding Unicode character.
    """
    # Convert the RGB values to grayscale
    grayscale_chunk = np.array([rgb_to_grayscale(pixel) for pixel in chunk])
    avg_brightness = np.mean(grayscale_chunk)
    shade_index = int((avg_brightness / 255) * (len(UNICODE_BLOCKS) - 1))
    return UNICODE_BLOCKS[shade_index]


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Convert an image to ASCII art")
    parser.add_argument("image_path", help="Path to the image file")
    parser.add_argument(
        "--grayscale", action="store_true", help="Convert image to grayscale"
    )
    parser.add_argument(
        "--width", type=int, default=None, help="Resize image to this width in pixels"
    )
    parser.add_argument(
        "--height", type=int, default=None, help="Resize image to this height in pixels"
    )

    # Parse arguments
    args = parser.parse_args()
    image_path = args.image_path
    convert_to_grayscale = args.grayscale
    width = args.width
    height = args.height

    try:
        # Open the image
        image = Image.open(image_path)

        # Resize the image if width and/or height are specified
        if width or height:
            original_size = image.size
            if width and height:
                new_size = (width, height)
            elif width:
                aspect_ratio = image.height / image.width
                new_size = (width, int(width * aspect_ratio))
            elif height:
                aspect_ratio = image.width / image.height
                new_size = (int(height * aspect_ratio), height)

            image = image.resize(new_size)
            logging.info(f"Image resized from {original_size} to {image.size}")

        # Convert to grayscale if requested
        if convert_to_grayscale:
            image = image.convert("L")
            logging.info(f"Image converted to grayscale: {image_path}")
        else:
            logging.info(f"Successfully opened image: {image_path}")

        # Get the image size
        img_width, img_height = image.size

        # Debug output: size of the rendered image
        logging.debug(
            f"Rendered image size: {img_width} pixels width, {img_height} pixels height"
        )

        # Debug output: size of each Unicode block
        logging.debug(
            f"Unicode block size: {CHAR_WIDTH} pixels width, {CHAR_HEIGHT} pixels height"
        )

        # Initialize an empty list to store the rows of characters
        output = []

        # Loop through the image in 8x16 chunks
        for y in range(0, img_height, CHAR_HEIGHT):
            row = []
            for x in range(0, img_width, CHAR_WIDTH):
                # Crop the 8x16 chunk
                chunk = image.crop((x, y, x + CHAR_WIDTH, y + CHAR_HEIGHT))

                # Convert chunk to a numpy array of pixel values
                pixels = np.array(chunk.getdata())
                print(pixels)
                # Convert the chunk to a Unicode character
                unicode_char = chunk_to_unicode(pixels)

                # If in grayscale mode, get the average grayscale value for coloring
                if convert_to_grayscale:
                    avg_grayscale = int(np.mean(pixels))
                    row.append(
                        colored(unicode_char, "white", "on_grey", attrs=["bold"])
                    )
                else:
                    # Get the average color for the chunk
                    avg_color = np.mean(pixels, axis=0).astype(int)
                    ansi_color = rgb_to_ansi(avg_color)
                    row.append(f"{ansi_color}{unicode_char}\033[0m")

            # Append the row to the output
            output.append("".join(row))

        # Print the resulting ASCII art
        print("\n".join(output))

    except Exception as e:
        logging.error(f"Error processing image: {e}")
        logging.error(traceback.format_exc())


if __name__ == "__main__":
    main()
