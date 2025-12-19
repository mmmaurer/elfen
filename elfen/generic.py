"""
This module contains generic functions for computing psycholinguistic
and emotion/sentiment rating-based features. This is primarily intended for
internal use by other modules to avoid code duplication and to make later
extensions, optimizations, or bug fixes easier to implement.
"""
import polars as pl

from .preprocess import get_lemmas
from .util import filter_lexicon

def get_avg(data: pl.DataFrame,
            lexicon: pl.DataFrame,
            lexicon_word_col: str,
            lexicon_rating_col: str,
            new_col_name: str,
            backbone: str = "spacy",
            **kwargs: dict[str, str]
            ) -> pl.DataFrame:
    """
    Generic function to compute average psycholinguistic or emotion/
    sentiment ratings.

    Args:
        data (pl.DataFrame):
            Input DataFrame containing text data.
        lexicon (pl.DataFrame):
            Lexicon DataFrame with word ratings.
        lexicon_word_col (str):
            Column name in lexicon for words.
        lexicon_rating_col (str):
            Column name in lexicon for ratings.
        new_col_name (str):
            Name for the new column to store average ratings.
        backbone (str, optional):
            NLP backbone to use. Defaults to "spacy".

    Returns:
        pl.DataFrame:
            DataFrame with new column for average ratings.
            Named as specified by `new_col_name`.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)

    data = data.with_columns(
        pl.col("lemmas").map_elements(
            lambda x: filter_lexicon(lexicon=lexicon,
                                     words=x,
                                     word_column=lexicon_word_col). \
                select(pl.col(lexicon_rating_col)).mean().item(),
                return_dtype=pl.Float64
                ).alias(new_col_name)
    )

    return data

def get_n_low(data: pl.DataFrame,
              lexicon: pl.DataFrame,
              lexicon_word_col: str,
              lexicon_rating_col: str,
              threshold: float,
              new_col_name: str,
              backbone: str = "spacy",
              **kwargs: dict[str, str]
              ) -> pl.DataFrame:
    """
    Generic function to compute the number of words with low
    psycholinguistic or emotion/sentiment ratings.

    Args:
        data (pl.DataFrame):
            Input DataFrame containing text data.
        lexicon (pl.DataFrame):
            Lexicon DataFrame with word ratings.
        lexicon_word_col (str):
            Column name in lexicon for words.
        lexicon_rating_col (str):
            Column name in lexicon for ratings.
        threshold (float):
            Threshold below which a rating is considered "low".
        new_col_name (str):
            Name for the new column to store the count of low ratings.
        backbone (str, optional):
            NLP backbone to use. Defaults to "spacy".
    Returns:
        pl.DataFrame:
            DataFrame with new column for count of low ratings.
            Named as specified by `new_col_name`.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)

    data = data.with_columns(
        pl.col("lemmas").map_elements(
            lambda x: filter_lexicon(lexicon=lexicon,
                                     words=x,
                                     word_column=lexicon_word_col). \
                select(pl.col(lexicon_rating_col)).filter(
                    pl.col(lexicon_rating_col) < threshold).shape[0],
                return_dtype=pl.Int64
                ).alias(new_col_name)
    ).fill_null(0) # If no words are found, count is 0

    return data

def get_n_high(data: pl.DataFrame,
               lexicon: pl.DataFrame,
               lexicon_word_col: str,
               lexicon_rating_col: str,
               threshold: float,
               new_col_name: str,
               backbone: str = "spacy",
               **kwargs: dict[str, str]
               ) -> pl.DataFrame:
    """
    Generic function to compute the number of words with high
    psycholinguistic or emotion/sentiment ratings.

    Args:
        data (pl.DataFrame):
            Input DataFrame containing text data.
        lexicon (pl.DataFrame):
            Lexicon DataFrame with word ratings.
        lexicon_word_col (str):
            Column name in lexicon for words.
        lexicon_rating_col (str):
            Column name in lexicon for ratings.
        threshold (float):
            Threshold above which a rating is considered "high".
        new_col_name (str):
            Name for the new column to store the count of high ratings.
        backbone (str, optional):
            NLP backbone to use. Defaults to "spacy".
    Returns:
        pl.DataFrame:
            DataFrame with new column for count of high ratings.
            Named as specified by `new_col_name`.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)

    data = data.with_columns(
        pl.col("lemmas").map_elements(
            lambda x: filter_lexicon(lexicon=lexicon,
                                     words=x,
                                     word_column=lexicon_word_col). \
                select(pl.col(lexicon_rating_col)).filter(
                    pl.col(lexicon_rating_col) > threshold).shape[0],
                return_dtype=pl.Int64
                ).alias(new_col_name)
    ).fill_null(0) # If no words are found, set count to 0

    return data

def get_n_controversial(data: pl.DataFrame,
                    lexicon: pl.DataFrame,
                    lexicon_word_col: str,
                    lexicon_sd_col: str,
                    threshold: float,
                    new_col_name: str,
                    backbone: str = "spacy",
                    **kwargs: dict[str, str]
                    ) -> pl.DataFrame:
    """
    Generic function to compute the number of words with controversial
    psycholinguistic or emotion/sentiment ratings.

    Args:
        data (pl.DataFrame):
            Input DataFrame containing text data.
        lexicon (pl.DataFrame):
            Lexicon DataFrame with word ratings.
        lexicon_word_col (str):
            Column name in lexicon for words.
        lexicon_sd_col (str):
            Column name for the standard deviation of ratings.
        threshold (float):
            Threshold above which a rating is considered "controversial".
        new_col_name (str):
            Name for the new column to store the count of controversial
            ratings.
        backbone (str, optional):
            NLP backbone to use. Defaults to "spacy".
    
    Returns:
        pl.DataFrame:
            DataFrame with new column for count of controversial ratings.
            Named as specified by `new_col_name`.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)

    data = data.with_columns(
        pl.col("lemmas").map_elements(
            lambda x: filter_lexicon(lexicon=lexicon,
                                     words=x,
                                     word_column=lexicon_word_col). \
                select(pl.col(lexicon_sd_col)).filter(
                    pl.col(lexicon_sd_col) > threshold).shape[0],
                return_dtype=pl.Int64
                ).alias(new_col_name)
    ).fill_null(0) # If no words are found, set count to 0

    return data

def get_max(data: pl.DataFrame,
            lexicon: pl.DataFrame,
            lexicon_word_col: str,
            lexicon_rating_col: str,
            new_col_name: str,
            backbone: str = "spacy",
            **kwargs: dict[str, str]
            ) -> pl.DataFrame:
    """
    Generic function to compute maximum psycholinguistic or emotion/
    sentiment ratings.

    Args:
        data (pl.DataFrame):
            Input DataFrame containing text data.
        lexicon (pl.DataFrame):
            Lexicon DataFrame with word ratings.
        lexicon_word_col (str):
            Column name in lexicon for words.
        lexicon_rating_col (str):
            Column name in lexicon for ratings.
        new_col_name (str):
            Name for the new column to store maximum ratings.
        backbone (str, optional):
            NLP backbone to use. Defaults to "spacy".

    Returns:
        pl.DataFrame:
            DataFrame with new column for maximum ratings.
            Named as specified by `new_col_name`.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)

    data = data.with_columns(
        pl.col("lemmas").map_elements(
            lambda x: filter_lexicon(lexicon=lexicon,
                                     words=x,
                                     word_column=lexicon_word_col). \
                select(pl.col(lexicon_rating_col)).max().item(),
                return_dtype=pl.Float64
                ).alias(new_col_name)
    )

    return data

def get_min(data: pl.DataFrame,
            lexicon: pl.DataFrame,
            lexicon_word_col: str,
            lexicon_rating_col: str,
            new_col_name: str,
            backbone: str = "spacy",
            **kwargs: dict[str, str]
            ) -> pl.DataFrame:
    """
    Generic function to compute minimum psycholinguistic or emotion/
    sentiment ratings.

    Args:
        data (pl.DataFrame):
            Input DataFrame containing text data.
        lexicon (pl.DataFrame):
            Lexicon DataFrame with word ratings.
        lexicon_word_col (str):
            Column name in lexicon for words.
        lexicon_rating_col (str):
            Column name in lexicon for ratings.
        new_col_name (str):
            Name for the new column to store minimum ratings.
        backbone (str, optional):
            NLP backbone to use. Defaults to "spacy".

    Returns:
        pl.DataFrame:
            DataFrame with new column for minimum ratings.
            Named as specified by `new_col_name`.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)

    data = data.with_columns(
        pl.col("lemmas").map_elements(
            lambda x: filter_lexicon(lexicon=lexicon,
                                     words=x,
                                     word_column=lexicon_word_col). \
                select(pl.col(lexicon_rating_col)).min().item(),
                return_dtype=pl.Float64
                ).alias(new_col_name)
    )

    return data

def get_sd(data: pl.DataFrame,
           lexicon: pl.DataFrame,
           lexicon_word_col: str,
           lexicon_rating_col: str,
           new_col_name: str,
           backbone: str = "spacy",
           **kwargs: dict[str, str]
           ) -> pl.DataFrame:
    """
    Generic function to compute standard deviation of psycholinguistic
    or emotion/sentiment ratings.

    Args:
        data (pl.DataFrame):
            Input DataFrame containing text data.
        lexicon (pl.DataFrame):
            Lexicon DataFrame with word ratings.
        lexicon_word_col (str):
            Column name in lexicon for words.
        lexicon_rating_col (str):
            Column name in lexicon for ratings.
        new_col_name (str):
            Name for the new column to store standard deviation of ratings.
        backbone (str, optional):
            NLP backbone to use. Defaults to "spacy".

    Returns:
        pl.DataFrame:
            DataFrame with new column for standard deviation of ratings.
            Named as specified by `new_col_name`.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)

    data = data.with_columns(
        pl.col("lemmas").map_elements(
            lambda x: filter_lexicon(lexicon=lexicon,
                                     words=x,
                                     word_column=lexicon_word_col). \
                select(pl.col(lexicon_rating_col)).std().item(),
                return_dtype=pl.Float64
                ).alias(new_col_name)
    )

    return data

