import requests
import zipfile
import os

import polars as pl


RESOURCE_MAP = {
    # Hedges, https://github.com/words/hedges
    "hedges": {
        "link": "https://raw.githubusercontent.com/words/hedges/main/data.txt",
        "area": "Semantics",
        "subarea": "Hedges",
        "filename": "hedges.txt"
    },
    # Warriner, A. B., Kuperman, V., & Brysbaert, M. (2013).
    # Norms of valence, arousal, and dominance for 13,915 English lemmas.
    # Behavior Research Methods, 45(4), 1191-1207.
    "vad_warriner": {
        "link": "https://static-content.springer.com/esm/"
                "art%3A10.3758%2Fs13428-012-0314-x/MediaObjects/"
                "13428_2012_314_MOESM1_ESM.zip",
        "area": "Emotion",
        "subarea": "VAD",
        "filename": "BRM-emot-submit.xlsx"
    },
    # Mohammad, S. M. (2018).
    # Obtaining reliable human ratings of valence, arousal, and dominance for 
    # 20,000 English words.
    # In Proceedings of the 56th Annual Meeting of the Association for
    # Computational Linguistics (Volume 1: Long Papers) (pp. 174-184).
    "vad_nrc": {
        "link": "https://saifmohammad.com/WebDocs/Lexicons/"
                "NRC-VAD-Lexicon.zip",
        "area": "Emotion",
        "subarea": "VAD",
        "filename": "NRC-VAD-Lexicon/NRC-VAD-Lexicon.txt"
    },
    # Mohammad, S. M. (2018)
    # Word affect intensity.
    # In Proceedings of the 56th Annual Meeting of the Association for
    # Computational Linguistics (Volume 1: Long Papers) (pp. 1609-1619).
    "intensity_nrc": {
        "link": "https://saifmohammad.com/WebDocs/Lexicons/"
                "NRC-Emotion-Intensity-Lexicon.zip",
        "area": "Emotion",
        "subarea": "Intensity",
        "filename": "NRC-Emotion-Intensity/"
                    "NRC-Emotion-Intensity-Lexicon-v1.txt"
    },
    # Brysbaert, M., Warriner, A. B., & Kuperman, V. (2014).
    # Concreteness ratings for 40 thousand generally known English word lemmas.
    # Behavior Research Methods, 46(3), 904-911.
    "concreteness_brysbaert": {
        "link": "https://static-content.springer.com/esm/"
                "art%3A10.3758%2Fs13428-013-0403-5/MediaObjects/"
                "13428_2013_403_MOESM1_ESM.xlsx",
        "area": "Psycholinguistics",
        "subarea": "Concreteness",
        "filename": "13428_2013_403_MOESM1_ESM.xlsx"
    },
    # Brysbaert, M., Mandera, P., McCormick, S. F., & Keuleers, E. (2019).
    # Word prevalence norms for 62,000 English lemmas.
    # Behavior Research Methods, 51(2), 467-479.
    "prevalence_brysbaert": {
        "link": "https://static-content.springer.com/"
                "esm/art%3A10.3758%2Fs13428-018-1077-9/"
                "MediaObjects/13428_2018_1077_MOESM2_ESM.xlsx",
        "area": "Psycholinguistics",
        "subarea": "Prevalence",
        "filename": "13428_2018_1077_MOESM2_ESM.xlsx"
    },
    # Kuperman, V., Stadthagen-Gonzalez, H., & Brysbaert, M. (2013).
    # Age-of-acquisition ratings for 30,000 English words.
    # Behavior Research Methods, 45(4), 1191-1207.
    "aoa_kuperman": {
        "link": "https://static-content.springer.com/esm/"
                "art%3A10.3758%2Fs13428-013-0348-8/"
                "MediaObjects/13428_2013_348_MOESM1_ESM.xlsx",
        "area": "Psycholinguistics",
        "subarea": "AgeOfAcquisition",
        "filename": "13428_2013_348_MOESM1_ESM.xlsx"
    },
    # Baccianella, S., Esuli, A., & Sebastiani, F. (2010).
    # SentiWordNet 3.0: An enhanced lexical resource for sentiment
    # analysis and opinion mining.
    # In LREC (Vol. 10, pp. 2200-2204).
    "sentiwordnet": {
        "link": "https://raw.githubusercontent.com/aesuli/SentiWordNet/"
                "master/data/SentiWordNet_3.0.0.txt",
        "area": "Emotion",
        "subarea": "Sentiment",
        "filename": "SentiWordNet_3.0.0.txt"
    },
    # Mohammad, S. M., & Turney, P. D. (2013).
    # Emotions evoked by common words and phrases:
    # Using Mechanical Turk to create an emotion lexicon.
    # In Proceedings of the NAACL HLT 2013 Workshop on
    # Computational Approaches to Analysis and Generation
    # of Emotion in Text (pp. 26-34).
    "sentiment_nrc": {
        "link": "https://saifmohammad.com/WebDocs/Lexicons/NRC-Emotion-Lexicon.zip",
        "area": "Emotion",
        "subarea": "Sentiment",
        "filename": "NRC-Emotion-Lexicon/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt"
    },
}


def download_lexicon(link: str,
                     path: str,
                     filename: str = None
                     ) -> None:
    """
    Download a lexicon from a link and save it to a path.
    
    Parameters
    ----------
    link : str
        The link to the lexicon.
    path : str
        The path to save the lexicon.
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
        filename = link.split("/")[-1]
        with open(os.path.join(path, filename), "wb") as f:
            f.write(response.content)
    elif link.endswith(".txt"):
        with open(os.path.join(path, filename), "wb") as f:
            f.write(response.content)
    
def get_resource(feature: str) -> None:
    """
    Download a resource from the RESOURCE_MAP.
    """
    if feature not in RESOURCE_MAP:
        raise ValueError(f"Feature {feature} not found in RESOURCE_MAP.")
    
    project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Making sure all the necessary directories exist
    os.makedirs(os.path.join(project_path, "resources",
                              RESOURCE_MAP[feature]["area"],
                              RESOURCE_MAP[feature]["subarea"]),
                              exist_ok=True)
    # Downloading the lexicon if it does not exist
    if not os.path.exists(os.path.join(project_path, "resources",
                                      RESOURCE_MAP[feature]["area"],
                                      RESOURCE_MAP[feature]["subarea"],
                                      RESOURCE_MAP[feature]["filename"])):
        download_lexicon(RESOURCE_MAP[feature]["link"],
                        os.path.join(project_path, "resources",
                                    RESOURCE_MAP[feature]["area"],
                                    RESOURCE_MAP[feature]["subarea"]),
                                    RESOURCE_MAP[feature]["filename"])

