"""
This module contains functions to calculate the VAD dimensions, Plutchik
emotions, the sentiment and emotion intensity of text data.

If you are using this functionality, please cite the original authors of
the resources.

The lexicons used in this module are:

- NRC VAD Lexicon:
    Mohammad, S. M., & Turney, P. D. (2013).
    Crowdsourcing a Word-Emotion Association Lexicon.
    Computational Intelligence, 29(3), 436-465.
- NRC Emotion Intensity Lexicon:
    Mohammad, S. M. (2018).
    Obtaining reliable human ratings of valence, arousal, and dominance
    for 20,000 English words.
    In Proceedings of the 56th Annual Meeting of the Association for
    Computational Linguistics (Volume 1: Long Papers) (pp. 174-184).
- NRC Sentiment Lexicon:
    Mohammad, S.M. (2018).
    Word Affect Intensities.
    In Proceedings of the 11th Edition of the Language Resources and 
    Evaluation Conference (LREC-2018), May 2018, Miyazaki, Japan.

The VAD lexicon contains three dimensions: Valence, Arousal, and Dominance.

The emotion intensity lexicon contains the intensity of eight Plutchik
emotions: Anger, Anticipation, Disgust, Fear, Joy, Sadness, Surprise,
and Trust.

The sentiment lexicon contains the sentiment of words: Positive and
Negative.

The following functions are implemented in this module:

- VAD Dimensions:

    - load_vad_lexicon: 
        Loads the VAD lexicon as a polars DataFrame.
    - get_avg_valence:
        Calculates the average valence of the text.
    - get_avg_arousal:
        Calculates the average arousal of the text.
    - get_avg_dominance:
        Calculates the average dominance of the text.
    - get_n_low_valence
        Calculates the number of words with valence lower than the
        threshold.
    - get_n_high_valence:
        Calculates the number of words with valence higher than the
        threshold.
    - get_n_low_arousal:
        Calculates the number of words with arousal lower than the
        threshold.
    - get_n_high_arousal:
        Calculates the number of words with arousal higher than the
        threshold.
    - get_n_low_dominance:
        Calculates the number of words with dominance lower than the
        threshold.
    - get_n_high_dominance:
        Calculates the number of words with dominance higher than the
        threshold.

- Emotion Intensity:

    - load_intensity_lexicon:
        Loads the emotion intensity lexicon as a polars DataFrame.
    - get_avg_emotion_intensity:
        Calculates the average emotion intensity of the text.
    - get_n_low_intensity:
        Calculates the number of words with emotion intensity lower than
        the threshold.
    - get_n_high_intensity:
        Calculates the number of words with emotion intensity higher than
        the threshold.
    
- Sentiment Analysis:

    - load_sentiment_nrc_lexicon:
        Loads the sentiment NRC lexicon as a polars DataFrame.
    - get_n_positive_sentiment:
        Calculates the number of words with positive sentiment.
    - get_n_negative_sentiment:
        Calculates the number of words with negative sentiment.
"""
import polars as pl

from .preprocess import (
    get_lemmas,
)
from .resources import (
    RESOURCE_MAP,
    LANGUAGES_NRC,
)
from .schemas import (
    VAD_SCHEMA_NRC,
    VAD_SCHEMA_NRC_MULTILINGUAL,
    INTENSITY_SCHEMA,
    INTENSITY_SCHEMA_MULTILINGUAL,
    SENTIMENT_NRC_SCHEMA,
    SENTIMENT_NRC_SCHEMA_MULTILINGUAL,
)
from .surface import (
    get_num_tokens,
)
from .util import (
    filter_lexicon,
)

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

VAD_NRC_PATH = RESOURCE_MAP["vad_nrc"]["filepath"]
INTENSITY_PATH = RESOURCE_MAP["intensity_nrc"]["filepath"]
SENTIWORDNET_PATH = RESOURCE_MAP["sentiwordnet"]["filepath"]
SENTIMENT_NRC_PATH = RESOURCE_MAP["sentiment_nrc"]["filepath"]

# --------------------------------------------------------------------- #
#                           VAD dimensions                              #
# --------------------------------------------------------------------- #

def load_vad_lexicon(path: str = VAD_NRC_PATH,
                     language: str = "en",
                     has_header: bool = True,
                     separator: str = "\t",
                     **kwargs: dict[str, str],
                     ) -> pl.DataFrame:
    """
    Loads the VAD lexicon as a polars DataFrame.

    Args:
        path (str): The path to the VAD lexicon.
        schema (dict): The schema for the VAD lexicon.
        has_header (bool): Whether the lexicon has a header.
        separator (str): The separator used in the lexicon.

    Returns:
        vad_lexicon (pl.DataFrame):
            The VAD lexicon as a polars DataFrame.
    """
    if language != "en":
        schema = VAD_SCHEMA_NRC_MULTILINGUAL
    else:
        schema = VAD_SCHEMA_NRC

    vad_lexicon = pl.read_csv(path,
                              has_header=has_header,
                              schema=schema,
                              separator=separator)
    if "V.Mean" in vad_lexicon.columns: # rename columns for consistency
        vad_lexicon = vad_lexicon.rename(
            {"V.Mean": "valence",
             "A.Mean": "arousal",
             "D.Mean": "dominance"}
        )
    elif "Valence" in vad_lexicon.columns:
        vad_lexicon = vad_lexicon.rename(
            {"Valence": "valence",
             "Arousal": "arousal",
             "Dominance": "dominance"}
        )
    return vad_lexicon

def get_avg_valence(data: pl.DataFrame,
                    lexicon: pl.DataFrame,
                    backbone: str = "spacy",
                    language: str = "en",
                    nan_value: float = 0.0,
                    **kwargs: dict[str, str],
                    ) -> pl.DataFrame:
    """
    Calculates the average valence of the text. Only takes into account
    words in the text that are present in the VAD lexicon.

    The valence of the text is calculated as the mean of the valence
    values of the words in the text.

    NaN/Null values are filled with 0 as the valence is in the range [0,1]
    and 0 is the neutral value in the NRC-VAD lexicon.

    Args:
        data (pl.DataFrame):
            The preprocessed input data. Contains the "nlp" column
            produced by the NLP backbone.
        lexicon (pl.DataFrame): The VAD lexicon.
        backbone (str): The NLP backbone to use.
        nan_value (float): The value to use for NaNs. Defaults to 0.0.

    Returns:
        data (pl.DataFrame):
            The input data with the average valence columns,
            named "avg_valence".
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)

    if language != "en":
        word_column = LANGUAGES_NRC[language]
    else:
        word_column = "word"
    
    data = data.with_columns(
        pl.col("lemmas").map_elements(
            lambda x: filter_lexicon(lexicon=lexicon,
                                     words=x,
                                     word_column=word_column). \
               select("valence").mean().item(),
               return_dtype=pl.Float64
        ).fill_nan(nan_value).fill_null(nan_value).alias("avg_valence")
        # convention to fill NaNs with 0 as valence is in [0,1]
        # and 0 is the neutral value for the NRC-VAD lexicon
    )
    
    return data

def get_avg_arousal(data: pl.DataFrame,
                    lexicon: pl.DataFrame,
                    backbone: str = "spacy",
                    nan_value: float = 0.0,
                    language: str = "en",
                    **kwargs: dict[str, str],
                    ) -> pl.DataFrame:
    """
    Calculates the average arousal of the text. Only takes into account
    words in the text that are present in the VAD lexicon.
    
    The arousal of the text is calculated as the mean of the arousal
    values of the words in the text.

    NaN/Null values are filled with 0 as the arousal is in the range [0,1]
    and 0 is the neutral value in the NRC-VAD lexicon.

    Args:
        data (pl.DataFrame):
            The preprocessed input data. Contains the "nlp" column
            produced by the NLP backbone.
        lexicon (pl.DataFrame): The VAD lexicon.
        backbone (str): The NLP backbone to use.
        nan_value (float): The value to use for NaNs.
                         Defaults to 0.0.
    
    Returns:
        data (pl.DataFrame):
            The input data with the average arousal columns,
            named "avg_arousal".
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)

    if language != "en":
        word_column = LANGUAGES_NRC[language]
    else:
        word_column = "word"
    
    data = data.with_columns(
        pl.col("lemmas").map_elements(
             lambda x: filter_lexicon(lexicon=lexicon,
                                      words=x,
                                      word_column=word_column). \
               select("arousal").mean().item(),
               return_dtype=pl.Float64
        ).fill_nan(nan_value).fill_null(nan_value).alias("avg_arousal")
        # convention to fill NaNs with 0 as arousal is in [0,1]
        # and 0 is the neutral value for the NRC-VAD lexicon
    )
    
    return data

def get_avg_dominance(data: pl.DataFrame,
                      lexicon: pl.DataFrame,
                      backbone: str = "spacy",
                      nan_value: float = 0.0,
                      language: str = "en",
                      **kwargs: dict[str, str],
                      ) -> pl.DataFrame:
    """
    Calculates the average dominance of the text. Only takes into account
    words in the text that are present in the VAD lexicon.

    The dominance of the text is calculated as the mean of the dominance
    values of the words in the text.

    NaN/Null values are filled with 0 as the dominance is in the range
    [0,1] and 0 is the neutral value in the NRC-VAD lexicon.

    Args:
        data (pl.DataFrame):
            The preprocessed input data. Contains the "nlp" column
            produced by the NLP backbone.
        lexicon (pl.DataFrame): The VAD lexicon.
        backbone (str): The NLP backbone to use.
        nan_value (float): The value to use for NaNs.
                         Defaults to 0.0.

    Returns:
        data (pl.DataFrame):
            The input data with the average dominance columns,
            named "avg_dominance".
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)

    if language != "en":
        word_column = LANGUAGES_NRC[language]
    else:
        word_column = "word"
    
    data = data.with_columns(
         pl.col("lemmas").map_elements(
          lambda x: filter_lexicon(lexicon=lexicon,
                                   words=x,
                                   word_column=word_column). \
                select("dominance").mean().item(),
                return_dtype=pl.Float64
         ).fill_nan(nan_value).fill_null(nan_value).alias("avg_dominance")
         # convention to fill NaNs with 0 as dominance is in [0,1]
         # and 0 is the neutral value for the NRC-VAD lexicon
    )

    return data

def get_n_low_valence(data: pl.DataFrame,
                      lexicon: pl.DataFrame,
                      backbone: str = "spacy",
                      threshold: float = 0.33,
                      nan_value: float = 0.0,
                      language: str = "en",
                      **kwargs: dict[str, str],
                      ) -> pl.DataFrame:
    """
    Calculates the number of words with valence lower than the threshold.

    Args:
        data (pl.DataFrame):
            The preprocessed input data. Contains the
            "nlp" column produced by the NLP backbone.
        lexicon (pl.DataFrame): The VAD lexicon.
        backbone (str): The NLP backbone to use.
        threshold (float): The threshold for low valence.
                            Defaults to 0.33.
        nan_value (float): The value to use for NaNs.
                            Defaults to 0.0.

    Returns:
        data (pl.DataFrame):
            The input data with the low valence count column,
            named "n_low_valence".
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)

    if language != "en":
        word_column = LANGUAGES_NRC[language]
    else:
        word_column = "word"
    
    data = data.with_columns(
        pl.col("lemmas").map_elements(
             lambda x: filter_lexicon(lexicon=lexicon,
                                      words=x,
                                      word_column=word_column). \
               select("valence").filter(
                   pl.col("valence") < threshold).shape[0],
               return_dtype=pl.UInt32
        ).fill_nan(nan_value).fill_null(nan_value).alias("n_low_valence")
    )
    
    return data

def get_n_high_valence(data: pl.DataFrame,
                       lexicon: pl.DataFrame,
                       backbone: str = "spacy",
                       threshold: float = 0.66,
                       nan_value: float = 0.0,
                       language: str = "en",
                       **kwargs: dict[str, str],
                       ) -> pl.DataFrame:
    """
    Calculates the number of words with valence higher than the threshold.

    Args:
        data (pl.DataFrame):
            The preprocessed input data. Contains the "nlp" column
            produced by the NLP backbone.
        lexicon (pl.DataFrame): The VAD lexicon.
        backbone (str): The NLP backbone to use.
        threshold (float): The threshold for high valence.
                         Defaults to 0.66.
        nan_value (float): The value to use for NaNs.
                         Defaults to 0.0.

    Returns:
        data (pl.DataFrame):
            The input data with the high valence count column,
            named "n_high_valence".
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)

    if language != "en":
        word_column = LANGUAGES_NRC[language]
    else:
        word_column = "word"
    
    data = data.with_columns(
        pl.col("lemmas").map_elements(
            lambda x: filter_lexicon(lexicon=lexicon,
                                      words=x,
                                      word_column=word_column). \
               select("valence").filter(
                   pl.col("valence") > threshold).shape[0],
               return_dtype=pl.UInt32
        ).fill_nan(nan_value).fill_null(nan_value).alias("n_high_valence")
    )
    
    return data

def get_n_low_arousal(data: pl.DataFrame,
                      lexicon: pl.DataFrame,
                      backbone: str = "spacy",
                      threshold: float = 0.33,
                      nan_value: float = 0.0,
                      language: str = "en",
                      **kwargs: dict[str, str],
                      ) -> pl.DataFrame:
    """
    Calculates the number of words with arousal lower than the threshold.

    Args:
        data (pl.DataFrame): 
            The preprocessed input data. Contains the
            "nlp" column produced by the NLP backbone.
        lexicon (pl.DataFrame): The VAD lexicon.
        backbone (str): The NLP backbone to use.
        threshold (float): The threshold for low arousal.
                         Defaults to 0.33.
        nan_value (float): The value to use for NaNs.
                         Defaults to 0.0.

    Returns:
        data (pl.DataFrame):
            The input data with the low arousal count column, named
            "n_low_arousal".
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
        
    if language != "en":
        word_column = LANGUAGES_NRC[language]
    else:
        word_column = "word"
    
    data = data.with_columns(
        pl.col("lemmas").map_elements(
             lambda x: filter_lexicon(lexicon=lexicon,
                                      words=x,
                                      word_column=word_column). \
               select("arousal").filter(
                   pl.col("arousal") < threshold).shape[0],
               return_dtype=pl.UInt32
        ).fill_nan(nan_value).fill_null(nan_value).alias("n_low_arousal")
    )
    
    return data

def get_n_high_arousal(data: pl.DataFrame,
                       lexicon: pl.DataFrame,
                       backbone: str = "spacy",
                       threshold: float = 0.66,
                       nan_value: float = 0.0,
                       language: str = "en",
                       **kwargs: dict[str, str],
                       ) -> pl.DataFrame:
    """
    Calculates the number of words with arousal higher than the threshold.

    Args:
        data (pl.DataFrame):
            The preprocessed input data. Contains the
            "nlp" column produced by the NLP backbone.
        lexicon (pl.DataFrame): The VAD lexicon.
        backbone (str): The NLP backbone to use.
        threshold (float): The threshold for high arousal.
                         Defaults to 0.66.
        nan_value (float): The value to use for NaNs.
                            Defaults to 0.0.

    Returns:
        data (pl.DataFrame):
            The input data with the high arousal count column. The
            column name is "n_high_arousal".
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
        
    if language != "en":
        word_column = LANGUAGES_NRC[language]
    else:
        word_column = "word"
    
    data = data.with_columns(
        pl.col("lemmas").map_elements(
             lambda x: filter_lexicon(lexicon=lexicon,
                                      words=x,
                                      word_column=word_column). \
               select("arousal").filter(
                   pl.col("arousal") > threshold).shape[0],
               return_dtype=pl.UInt32
        ).fill_nan(nan_value).fill_null(nan_value).alias("n_high_arousal")
    )
    
    return data

def get_n_low_dominance(data: pl.DataFrame,
                        lexicon: pl.DataFrame,
                        backbone: str = "spacy",
                        threshold: float = 0.33,
                        nan_value: float = 0.0,
                        language: str = "en",
                        **kwargs: dict[str, str],
                        ) -> pl.DataFrame:
    """
    Calculates the number of words with dominance lower than the threshold.

    Args:
        data (pl.DataFrame): 
            The preprocessed input data. Contains the
            "nlp" column produced by the NLP backbone.
        lexicon (pl.DataFrame): The VAD lexicon.
        backbone (str): The NLP backbone to use.
        threshold (float): The threshold for low dominance.
                         Defaults to 0.33.
        nan_value (float): The value to use for NaNs.
                            Defaults to 0.0.

    Returns:
        data (pl.DataFrame):
            The input data with the low dominance count column. The
            column name is "n_low_dominance".
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
        
    if language != "en":
        word_column = LANGUAGES_NRC[language]
    else:
        word_column = "word"
    
    data = data.with_columns(
        pl.col("lemmas").map_elements(
             lambda x: filter_lexicon(lexicon=lexicon,
                                      words=x,
                                      word_column=word_column). \
               select("dominance").filter(
                   pl.col("dominance") < threshold).shape[0],
               return_dtype=pl.UInt32
        ).fill_nan(nan_value).fill_null(nan_value).alias("n_low_dominance")
    )
    
    return data

def get_n_high_dominance(data: pl.DataFrame,
                         lexicon: pl.DataFrame,
                         backbone: str = "spacy",
                         threshold: float = 0.66,
                         nan_value: float = 0.0,
                         language: str = "en",
                         **kwargs: dict[str, str],
                         ) -> pl.DataFrame:
    """
    Calculates the number of words with dominance higher than the
    threshold.

    Args:
        data (pl.DataFrame):
            The preprocessed input data. Contains the
            "nlp" column produced by the NLP backbone.
        lexicon (pl.DataFrame): The VAD lexicon.
        backbone (str): The NLP backbone to use.
        threshold (float): The threshold for high dominance.
                            Defaults to 0.66.
        nan_value (float): The value to use for NaNs.
                            Defaults to 0.0.

    Returns:
        data (pl.DataFrame):
            The input data with the high dominance count column. The
            column name is "n_high_dominance".
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
    
    if language != "en":
        word_column = LANGUAGES_NRC[language]
    else:
        word_column = "word"
    
    data = data.with_columns(
        pl.col("lemmas").map_elements(
             lambda x: filter_lexicon(lexicon=lexicon,
                                      words=x,
                                      word_column=word_column). \
               select("dominance").filter(
                   pl.col("dominance") > threshold).shape[0],
               return_dtype=pl.UInt32
        ).fill_nan(nan_value).fill_null(nan_value).alias("n_high_dominance")
    )
    
    return data

# --------------------------------------------------------------------- #
#                           EMOTION INTENSITY                           #
# --------------------------------------------------------------------- #

def load_intensity_lexicon(path: str = INTENSITY_PATH,
                           language: str = "en",
                           has_header: bool = True,
                           separator: str = "\t",
                           **kwargs: dict[str, str],
                           ) -> pl.DataFrame:
    """
    Loads the intensity lexicon as a polars DataFrame.

    Args:
        path (str): The path to the intensity lexicon.
        schema (dict): The schema for the intensity lexicon.
        has_header (bool): Whether the lexicon has a header.

    Returns:
        intensity_lexicon (pl.DataFrame):
            The intensity lexicon as a polars DataFrame.
    """
    if language != "en":
        schema = INTENSITY_SCHEMA_MULTILINGUAL
    else:
        schema = INTENSITY_SCHEMA

    intensity_lexicon = pl.read_csv(path,
                                    has_header=has_header,
                                    schema=schema,
                                    separator=separator)
    # rename columns for consistency
    if "Emotion-Intensity-Score" in intensity_lexicon.columns:
        intensity_lexicon = intensity_lexicon.rename(
            {"Emotion-Intensity-Score": "emotion_intensity",
             "Emotion": "emotion"}
        )
    return intensity_lexicon

def filter_intensity_lexicon(lexicon: pl.DataFrame,
                             words: list,
                             emotion: str,
                             word_column: str = "word",
                             **kwargs: dict[str, str],
                             ) -> pl.DataFrame:
    """
    Filters the intensity lexicon for the given words and emotions.

    Args:
        lexicon (pl.DataFrame): The emotion intensity lexicon.
        words (list): The list of words to filter.
        emotion (str): The emotion to filter for.

    Returns:
        filtered_intensity_lexicon (pl.DataFrame):
            The filtered emotion intensity lexicon.
    """
    filtered_intensity_lexicon = lexicon.filter(
        (pl.col(word_column).is_in(words)) &
        (pl.col("emotion") == emotion)
    )
    
    return filtered_intensity_lexicon

def get_avg_emotion_intensity(data: pl.DataFrame,
                              lexicon: pl.DataFrame,
                              backbone: str = "spacy",
                              emotions: list = EMOTIONS,
                              nan_value: float = 0.0,
                              language: str = "en",
                              **kwargs: dict[str, str],
                              ) -> pl.DataFrame:
    """
    Calculates the average emotion intensity of the text. Only takes into
    account words in the text that are present in the emotion intensity
    lexicon.

    The average emotion intensity is calculated as the mean of the emotion
    intensity values of the words in the text.

    NaN/Null values are filled with 0 as the emotion intensity is in the
    range [0,1] and 0 is the neutral value in the NRC emotion intensity
    lexicon.

    Args:
        data (pl.DataFrame):
            The preprocessed input data. Contains the
            "nlp" column produced by the NLP backbone.
        lexicon (pl.DataFrame): The emotion intensity lexicon.
        backbone (str): The NLP backbone to use.
        emotions (list): The list of emotions to consider.
                       Defaults to the Plutchik emotions.
        nan_value (float): The value to use for NaNs.
                            Defaults to 0.0.

    Returns:
        data (pl.DataFrame):
            The input data with the average emotion intensity columns
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
        
    if language != "en":
        word_column = LANGUAGES_NRC[language]
    else:
        word_column = "word"
    
    for emotion in emotions:
        data = data.with_columns(
            pl.col("lemmas").map_elements(
                lambda x: filter_intensity_lexicon(lexicon,
                    x, emotion, word_column=word_column). \
                    select("emotion_intensity").mean().item(),
                return_dtype=pl.Float64
            ).fill_nan(nan_value).fill_null(nan_value). \
                alias(f"avg_intensity_{emotion}")
        )

    return data

def get_n_low_intensity(data: pl.DataFrame,
                        lexicon: pl.DataFrame,
                        backbone: str = "spacy",
                        emotions: list = EMOTIONS,
                        threshold: float = 0.33,
                        nan_value: float = 0.0,
                        language: str = "en",
                        **kwargs: dict[str, str],
                        ) -> pl.DataFrame:
    """
    Calculates the number of words with emotion intensity lower than the
    threshold.

    Args:
        data (pl.DataFrame): The preprocessed input data. Contains the
                           "nlp" column produced by the NLP backbone.
        lexicon (pl.DataFrame): The emotion intensity lexicon.
        backbone (str): The NLP backbone to use.
        emotions (list): The list of emotions to consider.
        threshold (float): The threshold for low intensity.
                         Defaults to 0.33.
        nan_value (float): The value to use for NaNs.
                         Defaults to 0.0.

    Returns:
        data (pl.DataFrame):
            The input data with the low intensity count column for each
            emotion. The column names are in the format
            "n_low_intensity_{emotion}".
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
        
    if language != "en":
        word_column = LANGUAGES_NRC[language]
    else:
        word_column = "word"
    
    for emotion in emotions:
        data = data.with_columns(
            pl.col("lemmas").map_elements(
                lambda x: filter_intensity_lexicon(
                    lexicon, x, emotion, word_column=word_column). \
                    select("emotion_intensity").filter(
                        pl.col("emotion_intensity") < threshold).shape[0],
                return_dtype=pl.UInt32
            ).fill_null(nan_value).fill_nan(nan_value). \
                alias(f"n_low_intensity_{emotion}")
        )

    return data

def get_n_high_intensity(data: pl.DataFrame,
                         lexicon: pl.DataFrame,
                         backbone: str = "spacy",
                         emotions: list = EMOTIONS,
                         threshold: float = 0.66,
                         nan_value: float = 0.0,
                         language: str = "en",
                         **kwargs: dict[str, str],
                         ) -> pl.DataFrame:
    """
    Calculates the number of words with emotion intensity higher than the
    threshold.

    Args:
        data (pl.DataFrame):
            The preprocessed input data. Contains the
            "nlp" column produced by the NLP backbone.
        lexicon (pl.DataFrame): The emotion intensity lexicon.
        backbone (str): The NLP backbone to use.
        emotions (list): The list of emotions to consider.
        threshold (float): The threshold for high intensity.
                            Defaults to 0.66.
        nan_value (float): The value to use for NaNs.
                            Defaults to 0.0.

    Returns:
        data (pl.DataFrame):
            The input data with the high intensity count column for each
            emotion. The column names are in the format
            "n_high_intensity_{emotion}".
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
    
    if language != "en":
        word_column = LANGUAGES_NRC[language]
    else:
        word_column = "word"
    
    for emotion in emotions:
        data = data.with_columns(
            pl.col("lemmas").map_elements(
                lambda x: filter_intensity_lexicon(
                    lexicon, x, emotion, word_column=word_column). \
                    select("emotion_intensity").filter(
                        pl.col("emotion_intensity") > threshold).shape[0],
                return_dtype=pl.UInt32
            ).fill_nan(nan_value).fill_null(nan_value). \
                alias(f"n_high_intensity_{emotion}")
        )

    return data

# --------------------------------------------------------------------- #
#                           SENTIMENT ANALYSIS                          #
# --------------------------------------------------------------------- #

# ---------------------------- SentiWordNet --------------------------- #
# NOTE: SentiWordNet is not used in the current implementation

# def load_sentiwordnet(path: str = SENTIWORDNET_PATH,
#                       schema: dict = SENTIWORDNET_SCHEMA,
#                       has_header: bool = False,
#                       separator: str = "\t",
#                       **kwargs: dict[str, str],
#                       ) -> pl.DataFrame:
#     """
#     Loads the SentiWordNet lexicon as a polars DataFrame.

#     Args:
#         path (str): The path to the SentiWordNet lexicon.
#         schema (dict): The schema for the SentiWordNet lexicon.
#         has_header (bool): Whether the lexicon has a header.
#         separator (str): The separator used in the lexicon.

#     Returns:
#         sentiwordnet (pl.DataFrame):
#           The SentiWordNet lexicon as a polars DataFrame.
#     """
#     sentiwordnet = pl.read_csv(path,
#                               has_header=has_header,
#                               schema=schema,
#                               separator=separator,
#                               # First 26 rows are comments/documentation
#                               skip_rows=27)
#     return sentiwordnet

# ---------------------------- Sentiment NRC --------------------------- #

def load_sentiment_nrc_lexicon(path: str = SENTIMENT_NRC_PATH,
                               language: str = "en",
                               has_header: bool = True,
                               separator: str = "\t",
                               **kwargs: dict[str, str],
                               ) -> pl.DataFrame:
    """
    Loads the sentiment NRC lexicon as a polars DataFrame.

    Args:
        path (str): The path to the sentiment NRC lexicon.
        schema (dict): The schema for the sentiment NRC lexicon.
        has_header (bool): Whether the lexicon has a header.
        separator (str): The separator used in the lexicon.

    Returns:
        sentiment_nrc (pl.DataFrame):
            The sentiment NRC lexicon as a polars DataFrame.
    """
    if language != "en":
        schema = SENTIMENT_NRC_SCHEMA_MULTILINGUAL
    else:
        schema = SENTIMENT_NRC_SCHEMA
    
    sentiment_nrc = pl.read_csv(path,
                               has_header=has_header,
                               schema=schema,
                               separator=separator)
    return sentiment_nrc

def filter_sentiment_lexicon(lexicon: pl.DataFrame,
                             words: list,
                             sentiment: str,
                             word_column: str = "word",
                             **kwargs: dict[str, str],
                             ) -> pl.DataFrame:
    """
    Filters the sentiment NRC lexicon for the given words and emotions.

    Args:
        lexicon (pl.DataFrame): The sentiment lexicon.
        words (list): The list of words to filter.
        sentiment (str): The sentiment to filter for.

    Returns:
        filtered_sentiment_nrc (pl.DataFrame):
            The filtered sentiment NRC lexicon.
    """
    if "label" in lexicon.columns:
        filtered_sentiment_nrc = lexicon.filter(
            (pl.col("emotion") == sentiment) &
            (pl.col("label") == 1) &
            (pl.col(word_column).is_in(words))
        )
    elif "Afrikaans" in lexicon.columns:
        filtered_sentiment_nrc = lexicon.filter(
            (pl.col(sentiment) == 1) &
            (pl.col(word_column).is_in(words))
        )
    
    return filtered_sentiment_nrc

def get_n_positive_sentiment(data: pl.DataFrame,
                            lexicon: pl.DataFrame,
                            backbone: str = "spacy",
                            nan_value: float = 0.0,
                            language: str = "en",
                            **kwargs: dict[str, str],
                            ) -> pl.DataFrame:
    """
    Calculates the number of words with positive sentiment.
    
    Args:
        data (pl.DataFrame): 
            The preprocessed input data. Contains the
            "nlp" column produced by the NLP backbone.
        lexicon (pl.DataFrame): The sentiment lexicon.
        backbone (str): The NLP backbone to use.
        nan_value (float): The value to use for NaNs.
                         Defaults to 0.0.
    
    Returns:
        data (pl.DataFrame):
            The input data with the positive sentiment count column.
            The column name is "n_positive_sentiment".
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)

    if language != "en":
        word_column = LANGUAGES_NRC[language]
    else:
        word_column = "word"
    
    # ensure that the column is not already present;
    # this may happen if sentiment_score is called before
    # n_negative_sentiment or n_positive_sentiment
    if "n_positive_sentiment" not in data.columns:
        data = data.with_columns(
            pl.col("lemmas").map_elements(
                lambda x: filter_sentiment_lexicon(
                    lexicon, x, sentiment="positive",
                    word_column=word_column).shape[0],
                return_dtype=pl.UInt32
            ).fill_nan(nan_value).fill_null(nan_value). \
            # convention to fill NaNs with 0 as this maps to
            # the absence of positive sentiment words
                alias("n_positive_sentiment")
        )

    return data

def get_n_negative_sentiment(data: pl.DataFrame,
                            lexicon: pl.DataFrame,
                            backbone: str = "spacy",
                            nan_value: float = 0.0,
                            language: str = "en",
                            **kwargs: dict[str, str],
                            ) -> pl.DataFrame:
    """
    Calculates the number of words with negative sentiment.

    Args:
        data (pl.DataFrame):
            The preprocessed input data. Contains the
            "nlp" column produced by the NLP backbone.
        lexicon (pl.DataFrame): The sentiment lexicon.
        backbone (str): The NLP backbone to use.
        nan_value (float): The value to use for NaNs.
                            Defaults to 0.0.

    Returns:
        data (pl.DataFrame):
            The input data with the negative sentiment count column.
            The column name is "n_negative_sentiment".
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
    
    if language != "en":
        word_column = LANGUAGES_NRC[language]
    else:
        word_column = "word"
    
    # ensure that the column is not already present;
    # this may happen if sentiment_score is called before
    # n_negative_sentiment or n_positive_sentiment
    if "n_negative_sentiment" not in data.columns:
        data = data.with_columns(
            pl.col("lemmas").map_elements(
                lambda x: filter_sentiment_lexicon(
                    lexicon, x, sentiment="negative",
                    word_column=word_column).shape[0],
                return_dtype=pl.UInt32
            ).fill_nan(nan_value).fill_null(nan_value). \
            # convention to fill NaNs with 0 as this maps to
            # the absence of negative sentiment words
                alias("n_negative_sentiment")
        )

    return data

def get_sentiment_score(data: pl.DataFrame,
                        lexicon: pl.DataFrame,
                        backbone: str = "spacy",
                        nan_value: float = 0.0,
                        language: str = "en",
                        **kwargs: dict[str, str],
                        ) -> pl.DataFrame:
    """
    Calculates the sentiment score of the text.

    The sentiment score is calculated as the difference between the number
    of positive and negative sentiment words divided by the number of
    tokens. The sentiment score is in the range [-1, 1], where -1
    indicates negative sentiment, 0 indicates neutral sentiment, and 1 
    indicates positive sentiment.

    Args:
        data (pl.DataFrame): 
            The preprocessed input data. Contains the
            "nlp" column produced by the NLP backbone.
        lexicon (pl.DataFrame): The sentiment lexicon.
        backbone (str): The NLP backbone to use.
        nan_value (float): The value to use for NaNs.
                            Defaults to 0.0.

    Returns:
        data (pl.DataFrame): 
            The input data with the sentiment score column. The column
            name is "sentiment_score".
    """
    if language != "en":
        word_column = LANGUAGES_NRC[language]
    else:
        word_column = "word"

    if "n_positive_sentiment" not in data.columns:
        data = get_n_positive_sentiment(data,
                                        lexicon=lexicon,
                                        language=language,
                                        backbone=backbone)
    if "n_negative_sentiment" not in data.columns:
        data = get_n_negative_sentiment(data,
                                        lexicon=lexicon,
                                        language=language,
                                        backbone=backbone)
    if "n_tokens" not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    
    data = data.with_columns(
        ((pl.col("n_positive_sentiment") - pl.col("n_negative_sentiment")) /
         pl.col("n_tokens")).fill_nan(nan_value).fill_null(nan_value). \
         alias("sentiment_score")
    )

    return data

