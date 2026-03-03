"""
This module contains generic functions for computing psycholinguistic
and emotion/sentiment rating-based features. This is primarily intended for
internal use by other modules to avoid code duplication and to make later
extensions, optimizations, or bug fixes easier to implement.
"""
import polars as pl

from .preprocess import get_lemmas

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
    exploded = _explode_and_join(data,
                                 lexicon,
                                 lexicon_word_col,
                                 lexicon_rating_col)

    return _aggregate_and_rejoin(
        data,
        exploded,
        pl.col(lexicon_rating_col).mean(),
        new_col_name,
        fill=None # If no words are found, leave as null
    )

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
    exploded = _explode_and_join(data,
                                 lexicon,
                                 lexicon_word_col,
                                 lexicon_rating_col)
    
    return _aggregate_and_rejoin(
        data,
        exploded,
        (pl.col(lexicon_rating_col) < threshold).sum(),
        new_col_name,
        fill=0 # If no words are found, set count to 0
    )

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
    exploded = _explode_and_join(data,
                                 lexicon,
                                 lexicon_word_col,
                                 lexicon_rating_col)
    
    return _aggregate_and_rejoin(
        data,
        exploded,
        (pl.col(lexicon_rating_col) > threshold).sum(),
        new_col_name,
        fill=0 # If no words are found, set count to 0
    )

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
    exploded = _explode_and_join(data,
                                 lexicon,
                                 lexicon_word_col,
                                 lexicon_sd_col)
    
    return _aggregate_and_rejoin(
        data,
        exploded,
        (pl.col(lexicon_sd_col) > threshold).sum(),
        new_col_name,
        fill=0 # If no words are found, set count to 0
    )

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
    exploded = _explode_and_join(data,
                                 lexicon,
                                 lexicon_word_col,
                                 lexicon_rating_col)
    
    return _aggregate_and_rejoin(
        data,
        exploded,
        pl.col(lexicon_rating_col).max(),
        new_col_name,
        fill=None # If no words are found, leave as null
    )

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
    exploded = _explode_and_join(data,
                                 lexicon,
                                 lexicon_word_col,
                                 lexicon_rating_col)
    
    return _aggregate_and_rejoin(
        data,
        exploded,
        pl.col(lexicon_rating_col).min(),
        new_col_name,
        fill=None # If no words are found, leave as null
    )

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
    exploded = _explode_and_join(data,
                                 lexicon,
                                 lexicon_word_col,
                                 lexicon_rating_col)
    
    return _aggregate_and_rejoin(
        data,
        exploded,
        pl.col(lexicon_rating_col).std(),
        new_col_name,
        fill=None # If no words are found, leave as null
    )

def _explode_and_join(data: pl.DataFrame,
                     lexicon: pl.DataFrame,
                     lexicon_word_col: str,
                     lexicon_rating_col: str,
                     ) -> pl.DataFrame:
    """
    Helper function to explode lemmas and join with lexicon ratings.

    Args:
        data (pl.DataFrame):
            Input DataFrame containing text data.
        lexicon (pl.DataFrame):
            Lexicon DataFrame with word ratings.
        lexicon_word_col (str):
            Column name in lexicon for words.
        lexicon_rating_col (str):
            Column name in lexicon for ratings.

    Returns:
        pl.DataFrame:
            DataFrame with exploded lemmas and joined ratings.
    """
    
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone="spacy")

    return (
        data
        .with_row_index("__row_idx")
        .explode("lemmas")
        .join(
            lexicon.select(
                pl.col(lexicon_word_col).alias("lemmas"),
                pl.col(lexicon_rating_col)
            ),
            on="lemmas",
            how="left"
        )
    )

def _aggregate_and_rejoin(
        data: pl.DataFrame,
        exploded: pl.DataFrame,
        agg_expr: pl.Expr,
        new_col_name: str,
        fill: float | int | None = None
) -> pl.DataFrame:
    """
    Helper function to aggregate exploded data and rejoin with original DataFrame.

    Args:
        data (pl.DataFrame):
            Original DataFrame before exploding.
        exploded (pl.DataFrame):
            DataFrame after exploding and joining with lexicon.
        agg_expr (pl.Expr):
            Polars expression for aggregation (e.g., pl.col("rating").mean()).
        new_col_name (str):
            Name for the new column to store aggregated ratings.
        fill (float | int | None, optional):
            Value to fill for rows with no matching words in lexicon. If None,
            leaves as null. Defaults to None.
    
    Returns:
        pl.DataFrame:
            DataFrame with new column for aggregated ratings.
    """
    result = (
        exploded
        .group_by("__row_idx")
        .agg(agg_expr.alias(new_col_name))
    )

    data = (
        data
        .with_row_index("__row_idx")
        .join(result, on="__row_idx", how="left")
        .drop("__row_idx")
    )

    if fill is not None:
        data = data.with_columns(pl.col(new_col_name).fill_null(fill))

    return data

