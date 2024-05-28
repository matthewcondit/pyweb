import argparse
import logging
from pyweb.utils import (
    image_viewer,
    fetch_html,
    process_html_file,
    render_html,
    display_content,
)

# Set up logging
logging.basicConfig(level=logging.ERROR)


def main() -> str:
    parser = argparse.ArgumentParser(description="Render content in the terminal.")
    parser.add_argument("input", help="URL or .html file path")
    parser.add_argument(
        "--image", help="Image file path to render in the terminal", action="store_true"
    )
    args = parser.parse_args()

    # Display image if only an image is requested
    if args.image:
        return image_viewer(args.input)

    # TODO: Add code to handle different types of input

    # If image only was not specified, that means the input is a URL or html path.

    # If URL, do a request to get the html content
    if args.input.startswith("http://") or args.input.startswith("https://"):
        # URL was given, do a request to get the HTML content
        logging.debug("URL was given")
        html_content = fetch_html(args.input)
    else:
        # Assume a file path was given
        html_content = process_html_file(args.input)

    # TODO: Process the HTML content as needed
    rendered_content = render_html(html_content)

    return rendered_content  # Return an empty string if no output is generated


if __name__ == "__main__":
    output = main()
    display_content(output)
