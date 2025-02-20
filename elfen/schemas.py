"""
This module contains schema definitions for the different external
resources. These schemas are used in Polars to enable type-safe and
fast data manipulation.
"""
import polars as pl

# ======================================== #
#              General Blocks              #
# ======================================== #

LANGS_NRC = {
    'Afrikaans': pl.String,
    'Albanian': pl.String,
    'Amharic': pl.String,
    'Arabic': pl.String,
    'Armenian': pl.String,
    'Azerbaijani': pl.String,
    'Basque': pl.String,
    'Belarusian': pl.String,
    'Bengali': pl.String,
    'Bosnian': pl.String,
    'Bulgarian': pl.String,
    'Catalan': pl.String,
    'Cebuano': pl.String,
    'Chichewa': pl.String,
    'Chinese-Simplified': pl.String,
    'Chinese-Traditional': pl.String,
    'Corsican': pl.String,
    'Croatian': pl.String,
    'Czech': pl.String,
    'Danish': pl.String,
    'Dutch': pl.String,
    'Esperanto': pl.String,
    'Estonian': pl.String,
    'Filipino': pl.String,
    'Finnish': pl.String,
    'French': pl.String,
    'Frisian': pl.String,
    'Galician': pl.String,
    'Georgian': pl.String,
    'German': pl.String,
    'Greek': pl.String,
    'Gujarati': pl.String,
    'Haitian-Creole': pl.String,
    'Hausa': pl.String,
    'Hawaiian': pl.String,
    'Hebrew': pl.String,
    'Hindi': pl.String,
    'Hmong': pl.String,
    'Hungarian': pl.String,
    'Icelandic': pl.String,
    'Igbo': pl.String,
    'Indonesian': pl.String,
    'Irish': pl.String,
    'Italian': pl.String,
    'Japanese': pl.String,
    'Javanese': pl.String,
    'Kannada': pl.String,
    'Kazakh': pl.String,
    'Khmer': pl.String,
    'Kinyarwanda': pl.String,
    'Korean': pl.String,
    'Kurdish-Kurmanji': pl.String,
    'Kyrgyz': pl.String,
    'Lao': pl.String,
    'Latin': pl.String,
    'Latvian': pl.String,
    'Lithuanian': pl.String,
    'Luxembourgish': pl.String,
    'Macedonian': pl.String,
    'Malagasy': pl.String,
    'Malay': pl.String,
    'Malayalam': pl.String,
    'Maltese': pl.String,
    'Maori': pl.String,
    'Marathi': pl.String,
    'Mongolian': pl.String,
    'Myanmar-Burmese': pl.String,
    'Nepali': pl.String,
    'Norwegian': pl.String,
    'Odia': pl.String,
    'Pashto': pl.String,
    'Persian': pl.String,
    'Polish': pl.String,
    'Portuguese': pl.String,
    'Punjabi': pl.String,
    'Romanian': pl.String,
    'Russian': pl.String,
    'Samoan': pl.String,
    'Scots-Gaelic': pl.String,
    'Serbian': pl.String,
    'Sesotho': pl.String,
    'Shona': pl.String,
    'Sindhi': pl.String,
    'Sinhala': pl.String,
    'Slovak': pl.String,
    'Slovenian': pl.String,
    'Somali': pl.String,
    'Spanish': pl.String,
    'Sundanese': pl.String,
    'Swahili': pl.String,
    'Swedish': pl.String,
    'Tajik': pl.String,
    'Tamil': pl.String,
    'Tatar': pl.String,
    'Telugu': pl.String,
    'Thai': pl.String,
    'Turkish': pl.String,
    'Turkmen': pl.String,
    'Ukrainian': pl.String,
    'Urdu': pl.String,
    'Uyghur': pl.String,
    'Uzbek': pl.String,
    'Vietnamese': pl.String,
    'Welsh': pl.String,
    'Xhosa': pl.String,
    'Yiddish': pl.String,
    'Yoruba': pl.String,
    'Zulu': pl.String,
}

# ======================================== #
#        Sentiment/Emotion Analysis        #
# ======================================== #

# ---------------------------------------- #
#                   VAD                    #
# ---------------------------------------- #

VAD_SCHEMA_NRC = {
    "word": pl.String,
    "valence": pl.Float32,
    "arousal": pl.Float32,
    "dominance": pl.Float32,
}

VAD_SCHEMA_NRC_MULTILINGUAL = {
    'English Word': pl.String,
    'Valence': pl.Float32,
    'Arousal': pl.Float32,
    'Dominance': pl.Float32,
}.update(LANGS_NRC)

VAD_SCHEMA_WARRINER = {
    '': pl.UInt32,
    'Word': pl.String,
    "V.Mean.Sum": pl.Float32,
    "V.SD.Sum": pl.Float32,
    "V.Rat.Sum": pl.Float32,
    "A.Mean.Sum": pl.Float32,
    "A.SD.Sum": pl.Float32,
    "A.Rat.Sum": pl.Float32,
    "D.Mean.Sum": pl.Float32,
    "D.SD.Sum": pl.Float32,
    "D.Rat.Sum": pl.Float32,
    "V.Mean.M": pl.Float32,
    "V.SD.M": pl.Float32,
    "V.Rat.M": pl.Float32,
    "V.Mean.F": pl.Float32,
    "V.SD.F": pl.Float32,
    "V.Rat.F": pl.Float32,
    "A.Mean.M": pl.Float32,
    "A.SD.M": pl.Float32,
    "A.Rat.M": pl.Float32,
    "A.Mean.F": pl.Float32,
    "A.SD.F": pl.Float32,
    "A.Rat.F": pl.Float32,
    "D.Mean.M": pl.Float32,
    "D.SD.M": pl.Float32,
    "D.Rat.M": pl.Float32,
    "D.Mean.F": pl.Float32,
    "D.SD.F": pl.Float32,
    "D.Rat.F": pl.Float32,
    "V.Mean.Y": pl.Float32,
    "V.SD.Y": pl.Float32,
    "V.Rat.Y": pl.Float32,
    "V.Mean.O": pl.Float32,
    "V.SD.O": pl.Float32,
    "V.Rat.O": pl.Float32,
    "A.Mean.Y": pl.Float32,
    "A.SD.Y": pl.Float32,
    "A.Rat.Y": pl.Float32,
    "A.Mean.O": pl.Float32,
    "A.SD.O": pl.Float32,
    "A.Rat.O": pl.Float32,
    "D.Mean.Y": pl.Float32,
    "D.SD.Y": pl.Float32,
    "D.Rat.Y": pl.Float32,
    "D.Mean.O": pl.Float32,
    "D.SD.O": pl.Float32,
    "D.Rat.O": pl.Float32,
    "V.Mean.L": pl.Float32,
    "V.SD.L": pl.Float32,
    "V.Rat.L": pl.Float32,
    "V.Mean.H": pl.Float32,
    "V.SD.H": pl.Float32,
    "V.Rat.H": pl.Float32,
    "A.Mean.L": pl.Float32,
    "A.SD.L": pl.Float32,
    "A.Rat.L": pl.Float32,
    "A.Mean.H": pl.Float32,
    "A.SD.H": pl.Float32,
    "A.Rat.H": pl.Float32,
    "D.Mean.L": pl.Float32,
    "D.SD.L": pl.Float32,
    "D.Rat.L": pl.Float32,
    "D.Mean.H": pl.Float32,
    "D.SD.H": pl.Float32,
    "D.Rat.H": pl.Float32,
}

# ---------------------------------------- #
#           Emotion Intensity              #
# ---------------------------------------- #

INTENSITY_SCHEMA = {
    "word": pl.String,
    "emotion": pl.String,
    "emotion_intensity": pl.Float32,
}

INTENSITY_SCHEMA_MULTILINGUAL = {
    'English Word': pl.String,
    'Emotion': pl.String,
    'Emotion-Intensity Score': pl.Float32,
}.update(LANGS_NRC)

# ---------------------------------------- #
#               Sentiment                  #
# ---------------------------------------- #

SENTIWORDNET_SCHEMA = {
    "POS": pl.String,
    "ID": pl.UInt32,
    "PosScore": pl.Float32,
    "NegScore": pl.Float32,
    "SynsetTerms": pl.String,
    "Gloss": pl.String,
}

SENTIMENT_NRC_SCHEMA = {
    "word": pl.String,
    "emotion": pl.String,
    "label": pl.UInt8,
}

SENTIMENT_NRC_SCHEMA_MULTILINGUAL = {
    "English Word": pl.String,
    "anger": pl.UInt8,
    "anticipation": pl.UInt8,
    "disgust": pl.UInt8,
    "fear": pl.UInt8,
    "joy": pl.UInt8,
    "negative": pl.UInt8,
    "positive": pl.UInt8,
    "sadness": pl.UInt8,
    "surprise": pl.UInt8,
    "trust": pl.UInt8,
}.update(LANGS_NRC)

# ======================================== #
#        Psycholinguistic Features         #
# ======================================== #