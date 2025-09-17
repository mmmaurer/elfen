"""
This module contains functions to download external resources.

If you are using the resources for research, please cite the original
authors.
"""
import requests
import zipfile
import os

from .resource_utils.langs import LANGUAGES_NRC
from .resource_utils.resource_map import RESOURCE_MAP

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def download_lexicon(link: str,
                     path: str,
                     filename: str = None
                     ) -> None:
    """
    Download a lexicon from a link and save it to a path.
    
    Args:
        link (str): Link to the lexicon.
        path (str): Path to save the lexicon.
        filename (str): Name of the file to save the lexicon.

    Returns:
        None
    """
    # Headers to avoid 406 response
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64;"
                      " rv:91.0) Gecko/20100101 Firefox/91.0",
        "Accept": "text/html,application/xhtml+xml,application/"
                  "xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }
    response = requests.get(link, headers=headers)

    if filename is None:
        filename = link.split("/")[-1]

    if link.endswith(".zip"):
        with open("temp.zip", "wb") as f:
            f.write(response.content)
        with zipfile.ZipFile("temp.zip", "r") as zip_ref:
            zip_ref.extractall(path)
        os.remove("temp.zip")
    elif link.endswith(".xlsx"):
        # filename = link.split("/")[-1]
        with open(os.path.join(path, filename), "wb") as f:
            f.write(response.content)
    elif link.endswith(".txt"):
        with open(os.path.join(path, filename), "wb") as f:
            f.write(response.content)
    else:
        with open(os.path.join(path, filename), "wb") as f:
            f.write(response.content)
    
def get_resource(feature: str) -> None:
    """
    Download a resource from the RESOURCE_MAP.

    Args:
        feature (str): Name of the feature to download.

    Returns:
        None
    """
    if feature not in RESOURCE_MAP:
        raise ValueError(f"Feature {feature} not found in RESOURCE_MAP.")

    # Making sure all the necessary directories exist
    os.makedirs(os.path.join(PROJECT_PATH, "elfen_resources",
                             RESOURCE_MAP[feature]["area"],
                             RESOURCE_MAP[feature]["subarea"]),
                             exist_ok=True)
    # Downloading the lexicon if it does not exist
    if not os.path.exists(RESOURCE_MAP[feature]["filepath"]):
        download_lexicon(RESOURCE_MAP[feature]["link"],
                         os.path.join(PROJECT_PATH, "elfen_resources",
                                      RESOURCE_MAP[feature]["area"],
                                      RESOURCE_MAP[feature]["subarea"]),
                                      RESOURCE_MAP[feature]["filename"])

def list_external_resources() -> None:
    """
    List all the external resources available in the RESOURCE_MAP.

    Args:
        None

    Returns:
        None
    """
    for feature in RESOURCE_MAP:
        print(f"Feature: {feature}")
        print("\n")

def get_bibtex() -> str:
    """
    Print the bibtex citation for all the resources in the RESOURCE_MAP,
    and the package itself.

    The citation keys for the lexicons are the names of the lexicons in
    the RESOURCE_MAP.
    The citation key for the package is "maurer-2024-elfen".

    Args:
        None

    Returns:
        bibxtex (str): Bibtex citation for all the resources.
    """

    bibtex = rb"""
    @misc{maurer-2025-elfen,
        author = {Maurer, Maximilian},
        title = {ELFEN - Efficient Linguistic Feature Extraction for Natural Language Datasets},
        year = {2025},
        publisher = {GitHub},
        journal = {GitHub repository},
        howpublished = {\url{https://github.com/mmmaurer/elfen}},
    }
    """
    for feature in RESOURCE_MAP:
        bibtex += RESOURCE_MAP[feature]["bibtex"]

    return bibtex.decode("utf-8")

