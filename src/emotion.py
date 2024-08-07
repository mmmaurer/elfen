import numpy as np
import polars as pl

from .surface import (
    get_num_tokens,
)

VAD_PATH = "../resources/NRC-VAD-Lecixon/NRC-VAD-Lexicon.txt"
VAD_SCHEMA = {
    "word": pl.String,
    "valence": pl.Float32,
    "arousal": pl.Float32,
    "dominance": pl.Float32,
}

INTENSITY_PATH = "../resources/NRC-Emotion-Intensity-Lexicon/" \
    "NRC-Emotion-Intensity-Lexicon-v1.txt"

INTENSITY_SCHEMA = {
    "word": pl.String,
    "emotion": pl.String,
    "emotion_intensity": pl.Float32,
}

EMOTIONS = [
    "anger",
    "anticipation",
    "disgust",
    "fear",
    "joy",
    "sadness",
    "surprise",
    "trust"
]


# --------------------------------------------------------------------- #
#                           VAD dimensions                              #
# --------------------------------------------------------------------- #

def load_vad_lexicon(path: str = VAD_PATH,
                     schema: dict = VAD_SCHEMA,
                     has_header: bool = False,
                     separator: str = "\t",
                     ) -> pl.DataFrame:
    """
    Returns the VAD lexicon as a polars DataFrame.
    """
    vad_lexicon = pl.read_csv(path = path,
                              has_header=has_header,
                              schema=schema,
                              separator=separator)
    return vad_lexicon

def get_avg_valence(data: pl.DataFrame,
                vad_lexicon: pl.DataFrame,
                backbone: str = "spacy",
                ) -> pl.DataFrame:
    """
    Returns the valence of the text.
    """
    if backbone == "spacy":
        data = data.with_columns(
             pl.col("nlp").map_elements(
                  lambda x: np.mean(
                       [vad_lexicon.filter(pl.col("word") == lemma). \
                        select("valence").item()
                        for lemma 
                        in [
                             token.lemma_ 
                             for token
                             in x
                        ]
                        if vad_lexicon.filter(pl.col("word") == lemma). \
                            shape[0]==1]
                 )
             ).alias("avg_valence")
        )
    elif backbone == "stanza":
        raise NotImplementedError("VAD calculation is not "
                                  "implemented for Stanza yet.")

    return data

def get_avg_arousal(data: pl.DataFrame,
                    vad_lexicon: pl.DataFrame,
                    backbone: str = "spacy",
                    ) -> pl.DataFrame:
    """
    Returns the arousal of the text.
    """
    if backbone == "spacy":
        data = data.with_columns(
             pl.col("nlp").map_elements(
                  lambda x: np.mean(
                       [vad_lexicon.filter(pl.col("word") == lemma). \
                        select("arousal").item()
                        for lemma 
                        in [
                             token.lemma_ 
                             for token
                             in x
                        ]
                        if vad_lexicon.filter(pl.col("word") == lemma). \
                            shape[0]==1]
                 )
             ).alias("avg_arousal")
        )
    elif backbone == "stanza":
        raise NotImplementedError("VAD calculation is not "
                                  "implemented for Stanza yet.")

    return data

def get_avg_dominance(data: pl.DataFrame,
                      vad_lexicon: pl.DataFrame,
                      backbone: str = "spacy",
                      ) -> pl.DataFrame:
        """
        Returns the dominance of the text.
        """
        if backbone == "spacy":
            data = data.with_columns(
                 pl.col("nlp").map_elements(
                    lambda x: np.mean(
                         [vad_lexicon.filter(pl.col("word") == lemma). \
                            select("dominance").item()
                            for lemma 
                            in [
                                 token.lemma_ 
                                 for token
                                 in x
                            ]
                            if vad_lexicon.filter(pl.col("word") == lemma). \
                                shape[0]==1]
                     )
                 ).alias("avg_dominance")
            )
        elif backbone == "stanza":
            raise NotImplementedError("VAD calculation is not "
                                      "implemented for Stanza yet.")
    
        return data

def get_n_low_valence(data: pl.DataFrame,
                      vad_lexicon: pl.DataFrame,
                      backbone: str = "spacy",
                      threshold: float = 1.66
                      ) -> pl.DataFrame:
    """
    Returns the number of words with valence lower than the threshold.
    """
    if backbone == "spacy":
        data = data.with_columns(
             pl.col("nlp").map_elements(
                  lambda x: np.sum(
                       [vad_lexicon.filter(pl.col("word") == lemma). \
                        select("valence").item() < threshold
                        for lemma 
                        in [
                             token.lemma_ 
                             for token
                             in x
                        ]
                        if vad_lexicon.filter(pl.col("word") == lemma). \
                            shape[0]==1]
                 )
             ).alias("n_low_valence")
        )
    elif backbone == "stanza":
        raise NotImplementedError("VAD calculation is not "
                                  "implemented for Stanza yet.")

    return data

def get_n_high_valence(data: pl.DataFrame,
                       vad_lexicon: pl.DataFrame,
                       backbone: str = "spacy",
                       threshold: float = 3.33
                       ) -> pl.DataFrame:
    """
    Returns the number of words with valence higher than the threshold.
    """
    if backbone == "spacy":
        data = data.with_columns(
             pl.col("nlp").map_elements(
                  lambda x: np.sum(
                       [vad_lexicon.filter(pl.col("word") == lemma). \
                        select("valence").item() > threshold
                        for lemma 
                        in [
                             token.lemma_ 
                             for token
                             in x
                        ]
                        if vad_lexicon.filter(pl.col("word") == lemma). \
                            shape[0]==1]
                 )
             ).alias("n_high_valence")
        )
    elif backbone == "stanza":
        raise NotImplementedError("VAD calculation is not "
                                  "implemented for Stanza yet.")

    return data

def get_n_low_arousal(data: pl.DataFrame,
                      vad_lexicon: pl.DataFrame,
                      backbone: str = "spacy",
                      threshold: float = 1.66
                      ) -> pl.DataFrame:
    """
    Returns the number of words with arousal lower than the threshold.
    """
    if backbone == "spacy":
        data = data.with_columns(
             pl.col("nlp").map_elements(
                  lambda x: np.sum(
                       [vad_lexicon.filter(pl.col("word") == lemma). \
                        select("arousal").item() < threshold
                        for lemma 
                        in [
                             token.lemma_ 
                             for token
                             in x
                        ]
                        if vad_lexicon.filter(pl.col("word") == lemma). \
                            shape[0]==1]
                 )
             ).alias("n_low_arousal")
        )
    elif backbone == "stanza":
        raise NotImplementedError("VAD calculation is not "
                                  "implemented for Stanza yet.")

    return data

def get_n_high_arousal(data: pl.DataFrame,
                       vad_lexicon: pl.DataFrame,
                       backbone: str = "spacy",
                       threshold: float = 3.33
                       ) -> pl.DataFrame:
    """
    Returns the number of words with arousal higher than the threshold.
    """
    if backbone == "spacy":
        data = data.with_columns(
             pl.col("nlp").map_elements(
                  lambda x: np.sum(
                       [vad_lexicon.filter(pl.col("word") == lemma). \
                        select("arousal").item() > threshold
                        for lemma 
                        in [
                             token.lemma_ 
                             for token
                             in x
                        ]
                        if vad_lexicon.filter(pl.col("word") == lemma). \
                            shape[0]==1]
                 )
             ).alias("n_high_arousal")
        )
    elif backbone == "stanza":
        raise NotImplementedError("VAD calculation is not "
                                  "implemented for Stanza yet.")

    return data

def get_n_low_dominance(data: pl.DataFrame,
                        vad_lexicon: pl.DataFrame,
                        backbone: str = "spacy",
                        threshold: float = 1.66
                        ) -> pl.DataFrame:
    """
    Returns the number of words with dominance lower than the threshold.
    """
    if backbone == "spacy":
        data = data.with_columns(
             pl.col("nlp").map_elements(
                  lambda x: np.sum(
                       [vad_lexicon.filter(pl.col("word") == lemma). \
                        select("dominance").item() < threshold
                        for lemma 
                        in [
                             token.lemma_ 
                             for token
                             in x
                        ]
                        if vad_lexicon.filter(pl.col("word") == lemma). \
                            shape[0]==1]
                 )
             ).alias("n_low_dominance")
        )
    elif backbone == "stanza":
        raise NotImplementedError("VAD calculation is not "
                                  "implemented for Stanza yet.")
    
    return data

def get_n_high_dominance(data: pl.DataFrame,
                         vad_lexicon: pl.DataFrame,
                         backbone: str = "spacy",
                         threshold: float = 3.33
                         ) -> pl.DataFrame:
    """
    Returns the number of words with dominance higher than the threshold.
    """
    if backbone == "spacy":
        data = data.with_columns(
             pl.col("nlp").map_elements(
                  lambda x: np.sum(
                       [vad_lexicon.filter(pl.col("word") == lemma). \
                        select("dominance").item() > threshold
                        for lemma 
                        in [
                             token.lemma_ 
                             for token
                             in x
                        ]
                        if vad_lexicon.filter(pl.col("word") == lemma). \
                            shape[0]==1]
                 )
             ).alias("n_high_dominance")
        )
    elif backbone == "stanza":
        raise NotImplementedError("VAD calculation is not "
                                  "implemented for Stanza yet.")
    
    return data

def get_high_valence_ratio(data: pl.DataFrame,
                            vad_lexicon: pl.DataFrame,
                            backbone: str = "spacy",
                            threshold: float = 3.33
                            ) -> pl.DataFrame:
     """
     Returns the ratio of words with valence higher than the threshold.
     """
     if 'n_tokens' not in data.columns:
          data = get_num_tokens(data, backbone=backbone)
     if 'n_high_valence' not in data.columns:
          data = get_n_high_valence(data, vad_lexicon,
                                    threshold=threshold,
                                    backbone=backbone)
     
     data = data.with_columns(
          (pl.col("n_high_valence") / pl.col("n_tokens")
            ).alias("high_valence_ratio"),
     )
    
     return data

def get_low_valence_ratio(data: pl.DataFrame,
                          vad_lexicon: pl.DataFrame,
                          backbone: str = "spacy",
                          threshold: float = 1.66
                          ) -> pl.DataFrame:
    """
    Returns the ratio of words with valence lower than the threshold.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_low_valence' not in data.columns:
        data = get_n_low_valence(data, vad_lexicon, 
                                 threshold=threshold,
                                 backbone=backbone)
    
    data = data.with_columns(
        (pl.col("n_low_valence") / pl.col("n_tokens")
            ).alias("low_valence_ratio"),
    )
    
    return data

def get_high_arousal_ratio(data: pl.DataFrame,
                           vad_lexicon: pl.DataFrame,
                           backbone: str = "spacy",
                           threshold: float = 3.33
                           ) -> pl.DataFrame:
    """
    Returns the ratio of words with arousal higher than the threshold.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_high_arousal' not in data.columns:
        data = get_n_high_arousal(data, vad_lexicon, 
                                  threshold=threshold,
                                  backbone=backbone)
    
    data = data.with_columns(
        (pl.col("n_high_arousal") / pl.col("n_tokens")
            ).alias("high_arousal_ratio"),
    )
    
    return data

def get_low_arousal_ratio(data: pl.DataFrame,
                          vad_lexicon: pl.DataFrame,
                          backbone: str = "spacy",
                          threshold: float = 1.66
                          ) -> pl.DataFrame:
    """
    Returns the ratio of words with arousal lower than the threshold.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_low_arousal' not in data.columns:
        data = get_n_low_arousal(data, vad_lexicon, 
                                 threshold=threshold,
                                 backbone=backbone)
    
    data = data.with_columns(
        (pl.col("n_low_arousal") / pl.col("n_tokens")
            ).alias("low_arousal_ratio"),
    )
    
    return data

def get_high_dominance_ratio(data: pl.DataFrame,
                             vad_lexicon: pl.DataFrame,
                             backbone: str = "spacy",
                             threshold: float = 3.33
                             ) -> pl.DataFrame:
    """
    Returns the ratio of words with dominance higher than the threshold.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_high_dominance' not in data.columns:
        data = get_n_high_dominance(data, vad_lexicon, 
                                    threshold=threshold,
                                    backbone=backbone)
    
    data = data.with_columns(
        (pl.col("n_high_dominance") / pl.col("n_tokens")
            ).alias("high_dominance_ratio"),
    )

    return data

def get_low_dominance_ratio(data: pl.DataFrame,
                            vad_lexicon: pl.DataFrame,
                            backbone: str = "spacy",
                            threshold: float = 1.66
                            ) -> pl.DataFrame:
    """
    Returns the ratio of words with dominance lower than the threshold.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_low_dominance' not in data.columns:
        data = get_n_low_dominance(data, vad_lexicon, 
                                   threshold=threshold,
                                   backbone=backbone)
    
    data = data.with_columns(
        (pl.col("n_low_dominance") / pl.col("n_tokens")
            ).alias("low_dominance_ratio"),
    )

    return data

# --------------------------------------------------------------------- #
#                           EMOTION INTENSITY                           #
# --------------------------------------------------------------------- #

def load_intensity_lexicon(path: str = INTENSITY_PATH,
                           schema: dict = INTENSITY_SCHEMA,
                           has_header: bool = False,
                           separator: str = "\t",
                           ) -> pl.DataFrame:
    """
    Returns the intensity lexicon as a polars DataFrame.
    """
    intensity_lexicon = pl.read_csv(path = path,
                                    has_header=has_header,
                                    schema=schema,
                                    separator=separator)
    return intensity_lexicon

def get_avg_emotion_intensity(data: pl.DataFrame,
                              intensity_lexicon: pl.DataFrame,
                              backbone: str = "spacy",
                              emotions: list = EMOTIONS
                              ) -> pl.DataFrame:
    """
    Returns the average emotion intensity of the text.
    """
    if backbone == "spacy":
        for emotion in emotions:
            data = data.with_columns(
                pl.col("nlp").map_elements(
                    lambda x: np.mean(
                        [intensity_lexicon.filter(
                            (pl.col("word") == lemma) & 
                            (pl.col("emotion") == emotion)
                        ).select("emotion_intensity").item()
                        for lemma
                        in [
                            token.lemma_
                            for token
                            in x
                        ]
                        if intensity_lexicon.filter(
                            (pl.col("word") == lemma) &
                            (pl.col("emotion") == emotion)
                        ).shape[0] == 1]
                    )
                ).alias(f"avg_intensity_{emotion}")
            )
    elif backbone == "stanza":
        raise NotImplementedError("Emotion intensity calculation is not "
                                  "implemented for Stanza.")
    
    return data

def get_n_low_intensity(data: pl.DataFrame,
                        intensity_lexicon: pl.DataFrame,
                        backbone: str = "spacy",
                        emotions: list = EMOTIONS,
                        threshold: float = 0.33
                        ) -> pl.DataFrame:
    """
    Returns the number of words with emotion intensity lower than the threshold.
    """
    if backbone == "spacy":
        for emotion in emotions:
            data = data.with_columns(
                pl.col("nlp").map_elements(
                    lambda x: np.sum(
                        [intensity_lexicon.filter(
                            (pl.col("word") == lemma) &
                            (pl.col("emotion") == emotion)
                        ).select("emotion_intensity").item() < threshold
                        for lemma
                        in [
                            token.lemma_
                            for token
                            in x
                        ]
                        if intensity_lexicon.filter(
                            (pl.col("word") == lemma) &
                            (pl.col("emotion") == emotion)
                        ).shape[0] == 1]
                    )
                ).alias(f"n_low_intensity_{emotion}")
            )
    elif backbone == "stanza":
        raise NotImplementedError("Emotion intensity calculation is not "
                                  "implemented for Stanza.")
    
    return data

def get_n_high_intensity(data: pl.DataFrame,
                         intensity_lexicon: pl.DataFrame,
                         backbone: str = "spacy",
                         emotions: list = EMOTIONS,
                         threshold: float = 0.66
                         ) -> pl.DataFrame:
    """
    Returns the number of words with emotion intensity higher than the threshold.
    """
    if backbone == "spacy":
        for emotion in emotions:
            data = data.with_columns(
                pl.col("nlp").map_elements(
                    lambda x: np.sum(
                        [intensity_lexicon.filter(
                            (pl.col("word") == lemma) &
                            (pl.col("emotion") == emotion)
                        ).select("emotion_intensity").item() > threshold
                        for lemma
                        in [
                            token.lemma_
                            for token
                            in x
                        ]
                        if intensity_lexicon.filter(
                            (pl.col("word") == lemma) &
                            (pl.col("emotion") == emotion)
                        ).shape[0] == 1]
                    )
                ).alias(f"n_high_{emotion}_intensity")
            )
    elif backbone == "stanza":
        raise NotImplementedError("Emotion intensity calculation is not "
                                  "implemented for Stanza.")
    
    return data

def get_low_intensity_ratio(data: pl.DataFrame,
                            intensity_lexicon: pl.DataFrame,
                            backbone: str = "spacy",
                            emotions: list = EMOTIONS,
                            threshold: float = 0.33
                            ) -> pl.DataFrame:
    """
    Returns the ratio of words with emotion intensity lower than the threshold.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_low_intensity' not in data.columns:
        data = get_n_low_intensity(data, intensity_lexicon,
                                   threshold=threshold,
                                   backbone=backbone)
    
    for emotion in emotions:
        data = data.with_columns(
            (pl.col(f"n_low_{emotion}_intensity") / pl.col("n_tokens")
                ).alias(f"low_intensity_{emotion}_ratio"),
        )
    
    return data

def get_high_intensity_ratio(data: pl.DataFrame,
                             intensity_lexicon: pl.DataFrame,
                             backbone: str = "spacy",
                             emotions: list = EMOTIONS,
                             threshold: float = 0.66
                             ) -> pl.DataFrame:
    """
    Returns the ratio of words with emotion intensity higher than the threshold.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_high_intensity' not in data.columns:
        data = get_n_high_intensity(data, intensity_lexicon,
                                    threshold=threshold,
                                    backbone=backbone)
    
    for emotion in emotions:
        data = data.with_columns(
            (pl.col(f"n_high_{emotion}_intensity") / pl.col("n_tokens")
                ).alias(f"high_intensity_ratio_{emotion}"),
        )
    
    return data

# --------------------------------------------------------------------- #
#                           SENTIMENT ANALYSIS                          #
# --------------------------------------------------------------------- #

