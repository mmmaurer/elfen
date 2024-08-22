"""
This module contains functions to calculate the VAD dimensions, Plutchik
emotions, the sentiment and emotion intensity of text data.

If you are using this functionality, please cite the original authors of
the resources.

The lexicons used in this module are:
- NRC VAD Lexicon: Mohammad, S. M., & Turney, P. D. (2013).
    Crowdsourcing a Word-Emotion Association Lexicon.
    Computational Intelligence, 29(3), 436-465.
- NRC Emotion Intensity Lexicon: Mohammad, S. M. (2018).
    Obtaining reliable human ratings of valence, arousal, and dominance for
    20,000 English words.
    In Proceedings of the 56th Annual Meeting of the Association for
    Computational Linguistics (Volume 1: Long Papers) (pp. 174-184).
- SentiWordNet: Esuli, A., & Sebastiani, F. (2006).
    SentiWordNet: A publicly available lexical resource for opinion mining.
    In Proceedings of the 5th Conference on Language Resources and Evaluation
    (LREC'06) (pp. 417-422).
"""
import polars as pl

from .features import (
    get_lemmas,
)
from .surface import (
    get_num_tokens,
    get_num_sentences
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
    Loads the VAD lexicon as a polars DataFrame.

    Args:
    - path (str): The path to the VAD lexicon.
    - schema (dict): The schema for the VAD lexicon.
    - has_header (bool): Whether the lexicon has a header.
    - separator (str): The separator used in the lexicon.

    Returns:
    - vad_lexicon (pl.DataFrame): The VAD lexicon as a polars DataFrame.
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
    Calculates the valence of the text.

    The valence of the text is calculated as the mean of the valence
    values of the words in the text.

    Args:
    - data (pl.DataFrame): The preprocessed input data. Contains the
                           "nlp" column produced by the NLP backbone.
    - vad_lexicon (pl.DataFrame): The VAD lexicon.
    - backbone (str): The NLP backbone to use.
    - nan_value (float): The value to use for NaNs.
                            Defaults to 0.0.

    Returns:
    - data (pl.DataFrame): The input data with the average
                           valence columns.
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
    Calculates the arousal of the text.

    The arousal of the text is calculated as the mean of the arousal
    values of the words in the text.

    Args:
    - data (pl.DataFrame): The preprocessed input data. Contains the
                           "nlp" column produced by the NLP backbone.
    - vad_lexicon (pl.DataFrame): The VAD lexicon.
    - backbone (str): The NLP backbone to use.
    - nan_value (float): The value to use for NaNs.
                         Defaults to 0.0.
    
    Returns:
    - data (pl.DataFrame): The input data with the average
                           arousal columns.
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
    Calculates the dominance of the text.

    The dominance of the text is calculated as the mean of the dominance
    values of the words in the text.

    Args:
    - data (pl.DataFrame): The preprocessed input data. Contains the
                           "nlp" column produced by the NLP backbone.
    - vad_lexicon (pl.DataFrame): The VAD lexicon.
    - backbone (str): The NLP backbone to use.
    - nan_value (float): The value to use for NaNs.
                         Defaults to 0.0.

    Returns:
    - data (pl.DataFrame): The input data with the average
                           dominance columns.
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
    Calculates the number of words with valence lower than the threshold.

    Args:
    - data (pl.DataFrame): The preprocessed input data. Contains the
                           "nlp" column produced by the NLP backbone.
    - vad_lexicon (pl.DataFrame): The VAD lexicon.
    - backbone (str): The NLP backbone to use.
    - threshold (float): The threshold for low valence.
                            Defaults to 0.33.
    - nan_value (float): The value to use for NaNs.
                            Defaults to 0.0.

    Returns:
    - data (pl.DataFrame): The input data with the low
                           valence count column.
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
    Calculates the number of words with valence higher than the threshold.

    Args:
    - data (pl.DataFrame): The preprocessed input data. Contains the
                           "nlp" column produced by the NLP backbone.
    - vad_lexicon (pl.DataFrame): The VAD lexicon.
    - backbone (str): The NLP backbone to use.
    - threshold (float): The threshold for high valence.
                         Defaults to 0.66.
    - nan_value (float): The value to use for NaNs.
                         Defaults to 0.0.

    Returns:
    - data (pl.DataFrame): The input data with the high
                           valence count column.
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
    Calculates the number of words with arousal lower than the threshold.

    Args:
    - data (pl.DataFrame): The preprocessed input data. Contains the
                           "nlp" column produced by the NLP backbone.
    - vad_lexicon (pl.DataFrame): The VAD lexicon.
    - backbone (str): The NLP backbone to use.
    - threshold (float): The threshold for low arousal.
                         Defaults to 0.33.
    - nan_value (float): The value to use for NaNs.
                         Defaults to 0.0.

    Returns:
    - data (pl.DataFrame): The input data with the low
                           arousal count column
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
    Calculates the number of words with arousal higher than the threshold.

    Args:
    - data (pl.DataFrame): The preprocessed input data. Contains the
                           "nlp" column produced by the NLP backbone.
    - vad_lexicon (pl.DataFrame): The VAD lexicon.
    - backbone (str): The NLP backbone to use.
    - threshold (float): The threshold for high arousal.
                         Defaults to 0.66.
    - nan_value (float): The value to use for NaNs.
                            Defaults to 0.0.

    Returns:
    - data (pl.DataFrame): The input data with the high
                           arousal count column.
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
                        threshold: float = 0.33,
                        nan_value: float = 0.0
                        ) -> pl.DataFrame:
    """
    Calculates the number of words with dominance lower than the threshold.

    Args:
    - data (pl.DataFrame): The preprocessed input data. Contains the
                           "nlp" column produced by the NLP backbone.
    - vad_lexicon (pl.DataFrame): The VAD lexicon.
    - backbone (str): The NLP backbone to use.
    - threshold (float): The threshold for low dominance.
                         Defaults to 0.33.
    - nan_value (float): The value to use for NaNs.
                            Defaults to 0.0.

    Returns:
    - data (pl.DataFrame): The input data with the low
                           dominance count column.
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
                         threshold: float = 0.66,
                         nan_value: float = 0.0
                         ) -> pl.DataFrame:
    """
    Calculates the number of words with dominance higher than the
    threshold.

    Args:
    - data (pl.DataFrame): The preprocessed input data. Contains the
                           "nlp" column produced by the NLP backbone.
    - vad_lexicon (pl.DataFrame): The VAD lexicon.
    - backbone (str): The NLP backbone to use.
    - threshold (float): The threshold for high dominance.
                            Defaults to 0.66.
    - nan_value (float): The value to use for NaNs.
                            Defaults to 0.0.

    Returns:
    - data (pl.DataFrame): The input data with the high
                           dominance count column.
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

# --------------------------------------------------------------------- #
#                           EMOTION INTENSITY                           #
# --------------------------------------------------------------------- #

def load_intensity_lexicon(path: str = INTENSITY_PATH,
                           schema: dict = INTENSITY_SCHEMA,
                           has_header: bool = False,
                           separator: str = "\t",
                           ) -> pl.DataFrame:
    """
    Loads the intensity lexicon as a polars DataFrame.

    Args:
    - path (str): The path to the intensity lexicon.
    - schema (dict): The schema for the intensity lexicon.
    - has_header (bool): Whether the lexicon has a header.

    Returns:
    - intensity_lexicon (pl.DataFrame): The intensity lexicon as a polars
                                        DataFrame.
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

    Args:
    - intensity_lexicon (pl.DataFrame): The emotion intensity lexicon.
    - words (list): The list of words to filter.
    - emotion (str): The emotion to filter for.

    Returns:
    - filtered_intensity_lexicon (pl.DataFrame): The filtered emotion
                                                 intensity lexicon.
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
    Calculates the average emotion intensity of the text.

    The average emotion intensity is calculated as the mean of the emotion
    intensity values of the words in the text.

    Args:
    - data (pl.DataFrame): The preprocessed input data. Contains the
                           "nlp" column produced by the NLP backbone.
    - intensity_lexicon (pl.DataFrame): The emotion intensity lexicon.
    - backbone (str): The NLP backbone to use.
    - emotions (list): The list of emotions to consider.
                       Defaults to the Plutchik emotions.
    - nan_value (float): The value to use for NaNs.
                            Defaults to 0.0.

    Returns:
    - data (pl.DataFrame): The input data with the average
                           emotion intensity columns
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
    Calculates the number of words with emotion intensity lower than the threshold.

    Args:
    - data (pl.DataFrame): The preprocessed input data. Contains the
                           "nlp" column produced by the NLP backbone.
    - intensity_lexicon (pl.DataFrame): The emotion intensity lexicon.
    - backbone (str): The NLP backbone to use.
    - emotions (list): The list of emotions to consider.
    - threshold (float): The threshold for low intensity.
                         Defaults to 0.33.
    - nan_value (float): The value to use for NaNs.
                         Defaults to 0.0.

    Returns:
    - data (pl.DataFrame): The input data with the low
                           intensity count columns
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
    Calculates the number of words with emotion intensity higher than the threshold.

    Args:
    - data (pl.DataFrame): The preprocessed input data. Contains the
                           "nlp" column produced by the NLP backbone.
    - intensity_lexicon (pl.DataFrame): The emotion intensity lexicon.
    - backbone (str): The NLP backbone to use.
    - emotions (list): The list of emotions to consider.
    - threshold (float): The threshold for high intensity.
                            Defaults to 0.66.
    - nan_value (float): The value to use for NaNs.
                            Defaults to 0.0.

    Returns:
    - data (pl.DataFrame): The input data with the high
                           intensity count columns
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
    Loads the SentiWordNet lexicon as a polars DataFrame.

    Args:
    - path (str): The path to the SentiWordNet lexicon.
    - schema (dict): The schema for the SentiWordNet lexicon.
    - has_header (bool): Whether the lexicon has a header.
    - separator (str): The separator used in the lexicon.

    Returns:
    - sentiwordnet (pl.DataFrame): The SentiWordNet lexicon as a polars
                                   DataFrame.
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
    Loads the sentiment NRC lexicon as a polars DataFrame.

    Args:
    - path (str): The path to the sentiment NRC lexicon.
    - schema (dict): The schema for the sentiment NRC lexicon.
    - has_header (bool): Whether the lexicon has a header.
    - separator (str): The separator used in the lexicon.

    Returns:
    - sentiment_nrc (pl.DataFrame): The sentiment NRC lexicon as a polars
                                    DataFrame.
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

    Args:
    - sentiment_nrc (pl.DataFrame): The sentiment NRC lexicon.
    - words (list): The list of words to filter.
    - sentiment (str): The sentiment to filter for.

    Returns:
    - filtered_sentiment_nrc (pl.DataFrame): The filtered sentiment NRC lexicon.
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
    Calculates the number of words with positive sentiment.
    Args:
    - data (pl.DataFrame): The preprocessed input data. Contains the
                           "nlp" column produced by the NLP backbone.
    - sentiment_nrc (pl.DataFrame): The sentiment NRC lexicon.
    - backbone (str): The NLP backbone to use.
    - nan_value (float): The value to use for NaNs.
                         Defaults to 0.0.
    
    Returns:
    - data (pl.DataFrame): The input data with the positive
                           sentiment count column.
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
    Calculates the number of words with negative sentiment.

    Args:
    - data (pl.DataFrame): The preprocessed input data. Contains the
                           "nlp" column produced by the NLP backbone.
    - sentiment_nrc (pl.DataFrame): The sentiment NRC lexicon.
    - backbone (str): The NLP backbone to use.
    - nan_value (float): The value to use for NaNs.
                            Defaults to 0.0.

    Returns:
    - data (pl.DataFrame): The input data with the negative
                           sentiment count column.
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

def get_sentiment_score(data: pl.DataFrame,
                        sentiment_nrc: pl.DataFrame,
                        backbone: str = "spacy",
                        nan_value: float = 0.0
                        ) -> pl.DataFrame:
    """
    Calculates the sentiment score of the text.

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
                            Defaults to 0.0.

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

