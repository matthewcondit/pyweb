# pyweb/main.py
import argparse


def main():
    parser = argparse.ArgumentParser(description="pyweb - CLI HTML Browser")
    parser.add_argument("url", help="URL to fetch and display")
    args = parser.parse_args()
    print(f"Fetching URL: {args.url}")


if __name__ == "__main__":
    main()
