from setuptools import find_packages, setup

setup(
    name="pyweb",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4",
        "pillow",
        "rich",
        "colorama",
    ],
    entry_points={
        "console_scripts": [
            "pyweb=pyweb.main:main",
        ],
    },
)
