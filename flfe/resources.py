"""
This module contains functions to download external resources.

If you are using the resources for research, please cite the original authors.
"""
import requests
import zipfile
import os

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

RESOURCE_MAP = {
    # Hedges, https://github.com/words/hedges
    "hedges": {
        "link": "https://raw.githubusercontent.com/words/hedges/main/data.txt",
        "area": "Semantics",
        "subarea": "Hedges",
        "filename": "hedges.txt",
        "filepath": os.path.join(PROJECT_PATH, "resources", "Semantics",
                                 "Hedges", "hedges.txt")
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
        "filename": "BRM-emot-submit.csv",
        "filepath": os.path.join(PROJECT_PATH, "resources", "Emotion",
                                 "VAD", "BRM-emot-submit.csv")
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
        "filename": "NRC-VAD-Lexicon/NRC-VAD-Lexicon.txt",
        "filepath": os.path.join(PROJECT_PATH, "resources", "Emotion",
                                 "VAD", "NRC-VAD-Lexicon", 
                                 "NRC-VAD-Lexicon.txt"),
        "multilingual_filepath": os.path.join(PROJECT_PATH, "resources", 
                                              "Emotion", "VAD",
                                              "NRC-VAD-Lexicon",
                                              "NRC-VAD-Lexicon-"
                                              "ForVariousLanguages.txt")
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
        "filename": "NRC-Emotion-Intensity-Lexicon/"
                    "NRC-Emotion-Intensity-Lexicon-v1.txt",
        "filepath": os.path.join(PROJECT_PATH, "resources", "Emotion",
                                 "Intensity", "NRC-Emotion-Intensity-Lexicon",
                                 "NRC-Emotion-Intensity-Lexicon-v1.txt"),
        "multilingual_filepath": os.path.join(PROJECT_PATH, "resources",
                                              "Emotion", "Intensity",
                                              "NRC-Emotion-Intensity-Lexicon",
                                              "NRC-Emotion-Intensity-"
                                              "Lexicon-ForVariousLanguages.txt")
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
        "filename": "13428_2013_403_MOESM1_ESM.xlsx",
        "filepath": os.path.join(PROJECT_PATH, "resources", "Psycholinguistics",
                                 "Concreteness", "13428_2013_403_MOESM1_ESM.xlsx")
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
        "filename": "13428_2018_1077_MOESM2_ESM.xlsx",
        "filepath": os.path.join(PROJECT_PATH, "resources", "Psycholinguistics",
                                 "Prevalence", "13428_2018_1077_MOESM2_ESM.xlsx")
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
        "filename": "13428_2013_348_MOESM1_ESM.xlsx",
        "filepath": os.path.join(PROJECT_PATH, "resources", "Psycholinguistics",
                                 "AgeOfAcquisition", "13428_2013_348_MOESM1_ESM.xlsx")
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
        "filename": "SentiWordNet_3.0.0.txt",
        "filepath": os.path.join(PROJECT_PATH, "resources", "Emotion",
                                 "Sentiment", "SentiWordNet_3.0.0.txt")
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
        "filename": "NRC-Emotion-Lexicon/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt",
        "filepath": os.path.join(PROJECT_PATH, "resources", "Emotion",
                                 "Sentiment", "NRC-Emotion-Lexicon",
                                 "NRC-Emotion-Lexicon-Wordlevel-v0.92.txt"),
        "multilingual_filepath": os.path.join(PROJECT_PATH, "resources",
                                              "Emotion", "Sentiment",
                                              "NRC-Emotion-Lexicon",
                                              "NRC-Emotion-Lexicon-"
                                              "ForVariousLanguages.txt")
    },
    # Coso, B., Guasch, M., Buganovic, I., Ferre, P., & Hinojosa, J. A. (2022).
    # CROWD-5e: A croatian psycholinguistic database for affective norms for
    # five discrete emotions.
    # Behavior Research Methods, 55(1), 4018-4034.
    # TODO: Handle processing the data
    "affect_crowd5e": {
        "link": "https://figshare.com/ndownloader/files/36434421",
        "area": "Emotion",
        "subarea": "Affect",
        "filename": "CROWD-5e.xlsx",
        "filepath": os.path.join(PROJECT_PATH, "resources", "Emotion",
                                 "Affect", "CROWD-5e.xlsx")
    },
    # Diveica, V, Pexman, P. M., & Binney, R. J. (2021).
    # Quantifying Social Semantics: an Inclusive Definition
    # of Socialness and Ratings for 8,388 English Words. PsyArXiv.
    # TODO: Handle processing the data
    "socialness": {
        "link": "https://osf.io/download/29eyh/",
        "area": "Psycholinguistics",
        "subarea": "Socialness",
        "filename": "Socialness.xlsx",
        "filepath": os.path.join(PROJECT_PATH, "resources", "Psycholinguistics",
                                 "Socialness", "Socialness.xlsx")
    },
    # TODO: Add Lancaster sensorimotor norms
    # TODO: Add bodo winters iconicity norms
    # TODO: Find and add psycholinguistic norms for other languages?
}

LANGUAGES_NRC = {
    "af": "Afrikaans",
    "sq": "Albanian",
    "am": "Amharic",
    "ar": "Arabic",
    "hy": "Armenian",
    "az": "Azerbaijani",
    "eu": "Basque",
    "be": "Belarusian",
    "bn": "Bengali",
    "bs": "Bosnian",
    "bg": "Bulgarian",
    "ca": "Catalan",
    "ceb": "Cebuano",
    "ny": "Chichewa",
    "zh": "Chinese-Simplified",
    "zh-TW": "Chinese-Traditional",
    "co": "Corsican",
    "hr": "Croatian",
    "cs": "Czech",
    "da": "Danish",
    "nl": "Dutch",
    "eo": "Esperanto",
    "et": "Estonian",
    "fil": "Filipino",
    "fi": "Finnish",
    "fr": "French",
    "fy": "Frisian",
    "gl": "Galician",
    "ka": "Georgian",
    "de": "German",
    "el": "Greek",
    "gu": "Gujarati",
    "ht": "Haitian-Creole",
    "ha": "Hausa",
    "haw": "Hawaiian",
    "he": "Hebrew",
    "hi": "Hindi",
    "hmn": "Hmong",
    "hu": "Hungarian",
    "is": "Icelandic",
    "ig": "Igbo",
    "id": "Indonesian",
    "ga": "Irish",
    "it": "Italian",
    "ja": "Japanese",
    "jv": "Javanese",
    "kn": "Kannada",
    "kk": "Kazakh",
    "km": "Khmer",
    "rw": "Kinyarwanda",
    "ko": "Korean",
    "ku": "Kurdish-Kurmanji",
    "ky": "Kyrgyz",
    "lo": "Lao",
    "la": "Latin",
    "lv": "Latvian",
    "lt": "Lithuanian",
    "lb": "Luxembourgish",
    "mk": "Macedonian",
    "mg": "Malagasy",
    "ms": "Malay",
    "ml": "Malayalam",
    "mt": "Maltese",
    "mi": "Maori",
    "mr": "Marathi",
    "mn": "Mongolian",
    "my": "Myanmar-Burmese",
    "ne": "Nepali",
    "no": "Norwegian",
    "or": "Odia",
    "ps": "Pashto",
    "fa": "Persian",
    "pl": "Polish",
    "pt": "Portuguese",
    "pa": "Punjabi",
    "ro": "Romanian",
    "ru": "Russian",
    "sm": "Samoan",
    "gd": "Scots-Gaelic",
    "sr": "Serbian",
    "st": "Sesotho",
    "sn": "Shona",
    "sd": "Sindhi",
    "si": "Sinhala",
    "sk": "Slovak",
    "sl": "Slovenian",
    "so": "Somali",
    "es": "Spanish",
    "su": "Sundanese",
    "sw": "Swahili",
    "sv": "Swedish",
    "tg": "Tajik",
    "ta": "Tamil",
    "tt": "Tatar",
    "te": "Telugu",
    "th": "Thai",
    "tr": "Turkish",
    "tk": "Turkmen",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "ug": "Uyghur",
    "uz": "Uzbek",
    "vi": "Vietnamese",
    "cy": "Welsh",
    "xh": "Xhosa",
    "yi": "Yiddish",
    "yo": "Yoruba",
    "zu": "Zulu"
}


def download_lexicon(link: str,
                     path: str,
                     filename: str = None
                     ) -> None:
    """
    Download a lexicon from a link and save it to a path.
    
    Args:
    - link: Link to the lexicon.
    - path: Path to save the lexicon.
    - filename: Name of the file to save the lexicon.

    Returns:
    - None
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

    Args:
    - feature: Name of the feature to download.

    Returns:
    - None
    """
    if feature not in RESOURCE_MAP:
        raise ValueError(f"Feature {feature} not found in RESOURCE_MAP.")

    # Making sure all the necessary directories exist
    os.makedirs(os.path.join(PROJECT_PATH, "resources",
                              RESOURCE_MAP[feature]["area"],
                              RESOURCE_MAP[feature]["subarea"]),
                              exist_ok=True)
    # Downloading the lexicon if it does not exist
    if not os.path.exists(os.path.join(PROJECT_PATH, "resources",
                                      RESOURCE_MAP[feature]["area"],
                                      RESOURCE_MAP[feature]["subarea"],
                                      RESOURCE_MAP[feature]["filename"])):
        download_lexicon(RESOURCE_MAP[feature]["link"],
                        os.path.join(PROJECT_PATH, "resources",
                                    RESOURCE_MAP[feature]["area"],
                                    RESOURCE_MAP[feature]["subarea"]),
                                    RESOURCE_MAP[feature]["filename"])

def list_external_resources() -> None:
    """
    List all the external resources available in the RESOURCE_MAP.

    Args:
    - None

    Returns:
    - None
    """
    for feature in RESOURCE_MAP:
        print(f"Feature: {feature}")
        print("\n")
