import subprocess


def chafa_convert(
    image_path, symbols="all", color_mode="256", color_space="rgb", dithering="none"
):
    """
    Convert an image to terminal-friendly representation using Chafa.

    :param image_path: Path to the image file.
    :param symbols: Symbol set to use (e.g., 'vhalf').
    :param colors: Number of colors to use (e.g., 256).
    :return: None
    """
    try:
        # Run Chafa command
        result = subprocess.run(
            ["chafa", image_path],
            # ["chafa", f"--symbols={symbols}", f"--colors={color_mode}", image_path],
            capture_output=True,
            text=True,
            check=True,
        )
        # Print the output from Chafa to the terminal
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


# Example usage
if __name__ == "__main__":
    image_path = "png_test.png"  # Replace with your image path
    chafa_convert(image_path)
    # chafa_convert(image_path, symbols="all", color_mode="full")
