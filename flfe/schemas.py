"""
This module contains schema definitions for the different external
resources. These schemas are used in Polars to enable type-safe and
fast data manipulation.
"""
import polars as pl


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

# ======================================== #
#        Psycholinguistic Features         #
# ======================================== #