import subprocess
import os
import logging
import requests
from bs4 import BeautifulSoup
from rich import print
from rich.console import Console
from rich.text import Text
from rich.panel import Panel

console = Console()


def image_viewer(
    image_path, symbols="all", color_mode="256", color_space="rgb", dithering="none"
):
    """
    Convert an image to terminal-friendly representation using Chafa.

    :param image_path: Path to the image file.
    :param symbols: Symbol set to use (e.g., 'vhalf').
    :param colors: Number of colors to use (e.g., 256).
    :return: The rendered image as text
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
        # Return the output from Chafa
        return result.stdout
    except subprocess.CalledProcessError as e:
        # Log the error
        logging.error(f"An error occurred: {e}")


def fetch_html(url):
    """
    Accepts a URL and returns the HTML content of the page.

    :param url: The URL to fetch the HTML content from.
    :return: The parsed BeautifulSoup object representing the HTML content.
    """
    logging.debug(f"Fetching HTML from URL: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.debug(f"Response status code: {response.status_code}")
        logging.debug(f"Response content: {response.text}")
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching HTML: {e}")
        return BeautifulSoup("", "html.parser")


def parse_html(html):
    """
    Accepts an HTML string and returns a parsed version of it.

    :param html: The HTML content to parse.
    :return: The parsed BeautifulSoup object representing the HTML content.
    """
    logging.debug("Parsing HTML")
    parsed_html = BeautifulSoup(html, "html.parser")
    return parsed_html


def process_html_file(file_path):
    """
    Accepts a file path and returns the HTML content of the file.

    :param file_path: The path to the HTML file.
    """
    logging.debug(f"File path was given: {file_path}")

    html_content = open(file_path).read()
    return parse_html(html_content)


def render_html(soup):

    rendered_text = ""
    print(soup.name)
    if soup.name == "[document]":
        print("document")
        for element in soup.head.descendants:
            print(element.name)
            if element.name == "title":
                print("found title")
                rendered_text += render_element(element)
    return rendered_text
    # print(soup.name)
    # rendered_text = ""
    # if soup.name == "[document]":
    #     for element in soup.body.descendants:
    #         if element.name:
    #             rendered_text += render_element(element)
    # elif soup.name == "div":
    #     for element in soup.descendants:
    #         if element.name:
    #             rendered_text += render_element(element)

    return rendered_text


def render_element(element):
    if element.name == "p":
        return element.get_text() + "\n"
    elif element.name == "title":
        # Place a box around the title
        title = element.get_text()
        return Panel(title) + "\n"
    elif element.name == "a":
        return f"[{element.get_text()}]({element.get('href')})"
    elif element.name in ["h1", "h2", "h3", "h4", "h5", "h6", "title"]:
        return element.get_text().upper() + "\n"
    elif element.name == "div":
        return render_html(element)
    else:
        return element.get_text()


def display_content(content):
    ...
    os.system("clear")
    console.print(content)
