import numpy as np
import polars as pl

from .features import (
    get_lemmas,
)
from .surface import (
    get_num_tokens,
)
from .schemas import (
    VAD_SCHEMA_NRC,
    INTENSITY_SCHEMA,
    SENTIWORDNET_SCHEMA,
    SENTIMENT_NRC_SCHEMA,
)

from .util import (
    filter_lexicon,
)

# TODO: FIX PATHS ONCE DOWNLOAD UTIL IS IMPLEMENTED
VAD_NRC_PATH = "../resources/VAD/NRC-VAD-Lecixon/NRC-VAD-Lexicon.txt"

INTENSITY_PATH = "../resources/NRC-Emotion-Intensity-Lexicon/" \
    "NRC-Emotion-Intensity-Lexicon-v1.txt"

SENTIWORDNET_PATH = "../resources/Emotion/Sentiment/SentiWordNet_3.0.0.txt"

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

def load_vad_lexicon(path: str = VAD_NRC_PATH,
                     schema: dict = VAD_SCHEMA_NRC,
                     has_header: bool = False,
                     separator: str = "\t",
                     ) -> pl.DataFrame:
    """
    Returns the VAD lexicon as a polars DataFrame.
    """
    vad_lexicon = pl.read_csv(path,
                              has_header=has_header,
                              schema=schema,
                              separator=separator)
    return vad_lexicon

def get_avg_valence(data: pl.DataFrame,
                    vad_lexicon: pl.DataFrame,
                    backbone: str = "spacy",
                    nan_value: float = 0.0
                    ) -> pl.DataFrame:
    """
    Returns the valence of the text.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
    data = data.with_columns(
        pl.col("lemmas").map_elements(
            lambda x: filter_lexicon(lexicon=vad_lexicon,
                                     words=x,
                                     word_column="word"). \
               select("valence").mean().item(),
               return_dtype=pl.Float64
        ).fill_nan(nan_value).fill_null(nan_value).alias("avg_valence")
        # convention to fill NaNs with 0 as valence is in [0,1]
        # and 0 is the neutral value for the NRC-VAD lexicon
    )
    
    return data

def get_avg_arousal(data: pl.DataFrame,
                    vad_lexicon: pl.DataFrame,
                    backbone: str = "spacy",
                    nan_value: float = 0.0
                    ) -> pl.DataFrame:
    """
    Returns the arousal of the text.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
    data = data.with_columns(
        pl.col("lemmas").map_elements(
             lambda x: filter_lexicon(lexicon=vad_lexicon,
                                      words=x,
                                      word_column="word"). \
               select("arousal").mean().item(),
               return_dtype=pl.Float64
        ).fill_nan(nan_value).fill_null(nan_value).alias("avg_arousal")
        # convention to fill NaNs with 0 as arousal is in [0,1]
        # and 0 is the neutral value for the NRC-VAD lexicon
    )
    
    return data

def get_avg_dominance(data: pl.DataFrame,
                      vad_lexicon: pl.DataFrame,
                      backbone: str = "spacy",
                      nan_value: float = 0.0
                      ) -> pl.DataFrame:
    """
    Returns the dominance of the text.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
    data = data.with_columns(
         pl.col("lemmas").map_elements(
          lambda x: filter_lexicon(lexicon=vad_lexicon,
                                   words=x,
                                   word_column="word"). \
                select("dominance").mean().item(),
                return_dtype=pl.Float64
         ).fill_nan(nan_value).fill_null(nan_value).alias("avg_dominance")
         # convention to fill NaNs with 0 as dominance is in [0,1]
         # and 0 is the neutral value for the NRC-VAD lexicon
    )

    return data

def get_n_low_valence(data: pl.DataFrame,
                      vad_lexicon: pl.DataFrame,
                      backbone: str = "spacy",
                      threshold: float = 1.66,
                      nan_value: float = 0.0
                      ) -> pl.DataFrame:
    """
    Returns the number of words with valence lower than the threshold.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
    data = data.with_columns(
        pl.col("lemmas").map_elements(
             lambda x: filter_lexicon(lexicon=vad_lexicon,
                                      words=x,
                                      word_column="word"). \
               select("valence").filter(
                   pl.col("valence") < threshold).shape[0],
               return_dtype=pl.UInt32
        ).fill_nan(nan_value).fill_null(nan_value).alias("n_low_valence")
    )
    
    return data

def get_n_high_valence(data: pl.DataFrame,
                       vad_lexicon: pl.DataFrame,
                       backbone: str = "spacy",
                       threshold: float = 0.66,
                       nan_value: float = 0.0
                       ) -> pl.DataFrame:
    """
    Returns the number of words with valence higher than the threshold.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
    data = data.with_columns(
        pl.col("lemmas").map_elements(
            lambda x: filter_lexicon(lexicon=vad_lexicon,
                                      words=x,
                                      word_column="word"). \
               select("valence").filter(
                   pl.col("valence") > threshold).shape[0],
               return_dtype=pl.UInt32
        ).fill_nan(nan_value).fill_null(nan_value).alias("n_high_valence")
    )
    
    return data

def get_n_low_arousal(data: pl.DataFrame,
                      vad_lexicon: pl.DataFrame,
                      backbone: str = "spacy",
                      threshold: float = 0.33,
                      nan_value: float = 0.0
                      ) -> pl.DataFrame:
    """
    Returns the number of words with arousal lower than the threshold.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
    data = data.with_columns(
        pl.col("lemmas").map_elements(
             lambda x: filter_lexicon(lexicon=vad_lexicon,
                                      words=x,
                                      word_column="word"). \
               select("arousal").filter(
                   pl.col("arousal") < threshold).shape[0],
               return_dtype=pl.UInt32
        ).fill_nan(nan_value).fill_null(nan_value).alias("n_low_arousal")
    )
    
    return data

def get_n_high_arousal(data: pl.DataFrame,
                       vad_lexicon: pl.DataFrame,
                       backbone: str = "spacy",
                       threshold: float = 0.66,
                       nan_value: float = 0.0
                       ) -> pl.DataFrame:
    """
    Returns the number of words with arousal higher than the threshold.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
    data = data.with_columns(
        pl.col("lemmas").map_elements(
             lambda x: filter_lexicon(lexicon=vad_lexicon,
                                      words=x,
                                      word_column="word"). \
               select("arousal").filter(
                   pl.col("arousal") > threshold).shape[0],
               return_dtype=pl.UInt32
        ).fill_nan(nan_value).fill_null(nan_value).alias("n_high_arousal")
    )
    
    return data

def get_n_low_dominance(data: pl.DataFrame,
                        vad_lexicon: pl.DataFrame,
                        backbone: str = "spacy",
                        threshold: float = 0.33,
                        nan_value: float = 0.0
                        ) -> pl.DataFrame:
    """
    Returns the number of words with dominance lower than the threshold.
    """
    data = data.with_columns(
        pl.col("nlp").map_elements(
             lambda x: filter_lexicon(lexicon=vad_lexicon,
                                      words=x,
                                      word_column="word"). \
               select("dominance").filter(
                   pl.col("dominance") < threshold).shape[0],
               return_dtype=pl.UInt32
        ).fill_nan(nan_value).fill_null(nan_value).alias("n_low_dominance")
    )
    
    return data

def get_n_high_dominance(data: pl.DataFrame,
                         vad_lexicon: pl.DataFrame,
                         backbone: str = "spacy",
                         threshold: float = 0.66,
                         nan_value: float = 0.0
                         ) -> pl.DataFrame:
    """
    Returns the number of words with dominance higher than the threshold.
    """
    data = data.with_columns(
        pl.col("nlp").map_elements(
             lambda x: filter_lexicon(lexicon=vad_lexicon,
                                      words=x,
                                      word_column="word"). \
               select("dominance").filter(pl.col("dominance") > threshold),
               return_dtype=pl.UInt32
        ).fill_nan(nan_value).fill_null(nan_value).alias("n_high_dominance")
    )
    
    return data

def get_high_valence_ratio(data: pl.DataFrame,
                            vad_lexicon: pl.DataFrame,
                            backbone: str = "spacy",
                            threshold: float = 0.66,
                            nan_value: float = 0.0
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
            ).fill_nan(nan_value).fill_null(nan_value). \
                alias("high_valence_ratio"),
     )
    
     return data

def get_low_valence_ratio(data: pl.DataFrame,
                          vad_lexicon: pl.DataFrame,
                          backbone: str = "spacy",
                          threshold: float = 0.33,
                          nan_value: float = 0.0
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
            ).fill_nan(nan_value).fill_null(nan_value). \
                alias("low_valence_ratio"),
    )
    
    return data

def get_high_arousal_ratio(data: pl.DataFrame,
                           vad_lexicon: pl.DataFrame,
                           backbone: str = "spacy",
                           threshold: float = 0.66,
                           nan_value: float = 0.0
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
            ).fill_nan(nan_value).fill_null(nan_value). \
                alias("high_arousal_ratio"),
    )
    
    return data

def get_low_arousal_ratio(data: pl.DataFrame,
                          vad_lexicon: pl.DataFrame,
                          backbone: str = "spacy",
                          threshold: float = 0.33,
                          nan_value: float = 0.0
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
            ).fill_nan(nan_value).fill_null(nan_value). \
                alias("low_arousal_ratio"),
    )
    
    return data

def get_high_dominance_ratio(data: pl.DataFrame,
                             vad_lexicon: pl.DataFrame,
                             backbone: str = "spacy",
                             threshold: float = 0.66,
                             nan_value: float = 0.0
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
            ).fill_nan(nan_value).fill_null(nan_value) \
                .alias("high_dominance_ratio"),
    )

    return data

def get_low_dominance_ratio(data: pl.DataFrame,
                            vad_lexicon: pl.DataFrame,
                            backbone: str = "spacy",
                            threshold: float = 0.33,
                            nan_value: float = 0.0
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
            ).fill_nan(nan_value).fill_null(nan_value). \
                alias("low_dominance_ratio"),
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
    intensity_lexicon = pl.read_csv(path,
                                    has_header=has_header,
                                    schema=schema,
                                    separator=separator)
    return intensity_lexicon

def filter_intensity_lexicon(intensity_lexicon: pl.DataFrame,
                             words: list,
                             emotion: str
                             ) -> pl.DataFrame:
    """
    Filters the intensity lexicon for the given words and emotions.
    """
    filtered_intensity_lexicon = intensity_lexicon.filter(
        (pl.col("word").is_in(words)) &
        (pl.col("emotion") == emotion)
    )
    
    return filtered_intensity_lexicon

def get_avg_emotion_intensity(data: pl.DataFrame,
                              intensity_lexicon: pl.DataFrame,
                              backbone: str = "spacy",
                              emotions: list = EMOTIONS,
                              nan_value: float = 0.0
                              ) -> pl.DataFrame:
    """
    Returns the average emotion intensity of the text.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
    for emotion in emotions:
        data = data.with_columns(
            pl.col("lemmas").map_elements(
                lambda x: filter_intensity_lexicon(
                    intensity_lexicon, x, emotion). \
                    select("emotion_intensity").mean().item(),
                return_dtype=pl.Float64
            ).fill_nan(nan_value).fill_null(nan_value). \
                alias(f"avg_intensity_{emotion}")
        )

    return data

def get_n_low_intensity(data: pl.DataFrame,
                        intensity_lexicon: pl.DataFrame,
                        backbone: str = "spacy",
                        emotions: list = EMOTIONS,
                        threshold: float = 0.33,
                        nan_value: float = 0.0
                        ) -> pl.DataFrame:
    """
    Returns the number of words with emotion intensity lower than the threshold.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
    for emotion in emotions:
        data = data.with_columns(
            pl.col("lemmas").map_elements(
                lambda x: filter_intensity_lexicon(
                    intensity_lexicon, x, emotion). \
                    select("emotion_intensity").filter(
                        pl.col("emotion_intensity") < threshold).shape[0],
                return_dtype=pl.UInt32
            ).fill_null(nan_value).fill_nan(nan_value). \
                alias(f"n_low_intensity_{emotion}")
        )

    return data

def get_n_high_intensity(data: pl.DataFrame,
                         intensity_lexicon: pl.DataFrame,
                         backbone: str = "spacy",
                         emotions: list = EMOTIONS,
                         threshold: float = 0.66,
                         nan_value: float = 0.0
                         ) -> pl.DataFrame:
    """
    Returns the number of words with emotion intensity higher than the threshold.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
    for emotion in emotions:
        data = data.with_columns(
            pl.col("lemmas").map_elements(
                lambda x: filter_intensity_lexicon(
                    intensity_lexicon, x, emotion). \
                    select("emotion_intensity").filter(
                        pl.col("emotion_intensity") > threshold).shape[0],
                return_dtype=pl.UInt32
            ).fill_nan(nan_value).fill_null(nan_value). \
                alias(f"n_high_{emotion}_intensity")
        )

    return data

def get_low_intensity_ratio(data: pl.DataFrame,
                            intensity_lexicon: pl.DataFrame,
                            backbone: str = "spacy",
                            emotions: list = EMOTIONS,
                            threshold: float = 0.33,
                            nan_value: float = 0.0
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
                ).fill_nan(nan_value).fill_null(nan_value). \
                    alias(f"low_intensity_{emotion}_ratio"),
        )
    
    return data

def get_high_intensity_ratio(data: pl.DataFrame,
                             intensity_lexicon: pl.DataFrame,
                             backbone: str = "spacy",
                             emotions: list = EMOTIONS,
                             threshold: float = 0.66,
                             nan_value: float = 0.0
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
                ).fill_nan(nan_value).fill_null(nan_value). \
                    alias(f"high_intensity_ratio_{emotion}"),
        )
    
    return data

# --------------------------------------------------------------------- #
#                           SENTIMENT ANALYSIS                          #
# --------------------------------------------------------------------- #

# ---------------------------- SentiWordNet --------------------------- #

def load_sentiwordnet(path: str = SENTIWORDNET_PATH,
                      schema: dict = SENTIWORDNET_SCHEMA,
                      has_header: bool = False,
                      separator: str = "\t",
                      ) -> pl.DataFrame:
    """
    Returns the SentiWordNet lexicon as a polars DataFrame.
    """
    sentiwordnet = pl.read_csv(path,
                              has_header=has_header,
                              schema=schema,
                              separator=separator,
                              # First 26 rows are comments/documentation
                              skip_rows=27)
    return sentiwordnet

# ---------------------------- Sentiment NRC --------------------------- #

def load_sentiment_nrc_lexicon(path: str,
                               schema: dict = SENTIMENT_NRC_SCHEMA,
                               has_header: bool = False,
                               separator: str = "\t",
                               ) -> pl.DataFrame:
    """
    Returns the sentiment NRC lexicon as a polars DataFrame.
    """
    sentiment_nrc = pl.read_csv(path,
                               has_header=has_header,
                               schema=schema,
                               separator=separator)
    return sentiment_nrc

def filter_sentiment_nrc_lexicon(sentiment_nrc: pl.DataFrame,
                                 words: list,
                                 sentiment: str
                                 ) -> pl.DataFrame:
    """
    Filters the sentiment NRC lexicon for the given words and emotions.
    """
    filtered_sentiment_nrc = sentiment_nrc.filter(
        (pl.col("emotion") == sentiment) &
        (pl.col("label") == 1) &
        (pl.col("word").is_in(words))
    )
    
    return filtered_sentiment_nrc

def get_n_positive_sentiment(data: pl.DataFrame,
                            sentiment_nrc: pl.DataFrame,
                            backbone: str = "spacy",
                            nan_value: float = 0.0
                            ) -> pl.DataFrame:
        """
        Returns the number of words with positive sentiment.

        Args:
        - data (pl.DataFrame): The preprocessed input data. Contains the
                               "nlp" column produced by the NLP backbone.
        - sentiment_nrc (pl.DataFrame): The sentiment NRC lexicon.
        - backbone (str): The NLP backbone to use.
        - nan_value (float): The value to use for NaNs.

        """
        if "lemmas" not in data.columns:
            data = get_lemmas(data, backbone=backbone)
        data = data.with_columns(
            pl.col("lemmas").map_elements(
                lambda x: filter_sentiment_nrc_lexicon(
                    sentiment_nrc, x, sentiment="positive").shape[0],
                return_dtype=pl.UInt32
            ).fill_nan(nan_value).fill_null(nan_value). \
            # convention to fill NaNs with 0 as this maps to
            # the absence of positive sentiment words
                alias("n_positive_sentiment")
        )
    
        return data

def get_n_negative_sentiment(data: pl.DataFrame,
                            sentiment_nrc: pl.DataFrame,
                            backbone: str = "spacy",
                            nan_value: float = 0.0
                            ) -> pl.DataFrame:
        """
        Returns the number of words with negative sentiment.
        """
        if "lemmas" not in data.columns:
            data = get_lemmas(data, backbone=backbone)
        data = data.with_columns(
            pl.col("lemmas").map_elements(
                lambda x: filter_sentiment_nrc_lexicon(
                    sentiment_nrc, x, sentiment="negative").shape[0],
                return_dtype=pl.UInt32
            ).fill_nan(nan_value).fill_null(nan_value). \
            # convention to fill NaNs with 0 as this maps to
            # the absence of negative sentiment words
                alias("n_negative_sentiment")
        )
    
        return data

def get_positive_sentiment_ratio(data: pl.DataFrame,
                                sentiment_nrc: pl.DataFrame,
                                backbone: str = "spacy",
                                nan_value: float = 0.0
                                ) -> pl.DataFrame:
        """
        Returns the ratio of words with positive sentiment.
        """
        if 'n_tokens' not in data.columns:
            data = get_num_tokens(data, backbone=backbone)
        if 'n_positive_sentiment' not in data.columns:
            data = get_n_positive_sentiment(data, sentiment_nrc,
                                            backbone=backbone)
        
        data = data.with_columns(
            (pl.col("n_positive_sentiment") / pl.col("n_tokens")
                ).fill_nan(nan_value).fill_null(nan_value). \
                # convention to fill NaNs with 0 as this maps to
                # the absence of positive sentiment words
                    alias("positive_sentiment_ratio"),
        )
        
        return data

def get_negative_sentiment_ratio(data: pl.DataFrame,
                                sentiment_nrc: pl.DataFrame,
                                backbone: str = "spacy",
                                nan_value: float = 0.0
                                ) -> pl.DataFrame:
        """
        Returns the ratio of words with negative sentiment.
        """
        if 'n_tokens' not in data.columns:
            data = get_num_tokens(data, backbone=backbone)
        if 'n_negative_sentiment' not in data.columns:
            data = get_n_negative_sentiment(data, sentiment_nrc,
                                            backbone=backbone)
        
        data = data.with_columns(
            (pl.col("n_negative_sentiment") / pl.col("n_tokens")
                ).fill_nan(nan_value).fill_null(nan_value). \
                # convention to fill NaNs with 0 as this maps to
                # the absence of negative sentiment words
                    alias("negative_sentiment_ratio"),
        )
        
        return data

def get_sentiment_score(data: pl.DataFrame,
                        sentiment_nrc: pl.DataFrame,
                        backbone: str = "spacy",
                        nan_value: float = 0.0
                        ) -> pl.DataFrame:
    """
    Returns the sentiment score of the text.

    The sentiment score is calculated as the difference between the number of
    positive and negative sentiment words divided by the number of tokens.
    The sentiment score is in the range [-1, 1], where -1 indicates negative
    sentiment, 0 indicates neutral sentiment, and 1 indicates positive sentiment.

    Args:
    - data (pl.DataFrame): The preprocessed input data. Contains the
                           "nlp" column produced by the NLP backbone.
    - sentiment_nrc (pl.DataFrame): The sentiment NRC lexicon.
    - backbone (str): The NLP backbone to use.
    - nan_value (float): The value to use for NaNs.

    Returns:
    - data (pl.DataFrame): The input data with the sentiment score column.
    """
    if "n_positive_sentiment" not in data.columns:
        data = get_n_positive_sentiment(data,
                                        sentiment_nrc,
                                        backbone=backbone)
    if "n_negative_sentiment" not in data.columns:
        data = get_n_negative_sentiment(data,
                                        sentiment_nrc,
                                        backbone=backbone)
    if "n_tokens" not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    
    data = data.with_columns(
        ((pl.col("n_positive_sentiment") - pl.col("n_negative_sentiment")) /
         pl.col("n_tokens")).fill_nan(nan_value).fill_null(nan_value). \
         alias("sentiment_score")
    )

    return data