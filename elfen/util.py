"""
This module contains utility functions for working with Polars DataFrames.
"""
import polars as pl

def rescale_column(df: pl.DataFrame,
                   column: str,
                   minimum: float | None = None,
                   maximum: float | None = None) -> pl.DataFrame:
    """
    Rescales a column to a range of [0, 1].

    Args:
        df (pl.DataFrame): A Polars DataFrame.
        column (str): The name of the column to rescale.
        minimum (float): 
            The minimum value of the column.
            If None, the minimum value of the
            column is used.
        maximum (float):
            The maximum value of the column.
            If None, the maximum value of the
            column is used.

    Returns:
        rescaled_df (pl.DataFrame):
            A Polars DataFrame with the column rescaled to [0, 1].
    """
    if minimum is None:
        minimum = df[column].min()
    if maximum is None:
        maximum = df[column].max()
    
    rescaled_df = df.with_columns([
        ((pl.col(column) - minimum) / (maximum - minimum)).alias(column)
    ])

    return rescaled_df

def normalize_column(df: pl.DataFrame,
                     column: str) -> pl.DataFrame:
    """
    Normalizes a column to have a mean of 0 and a standard deviation of 1.

    Args:
        df (pl.DataFrame): A Polars DataFrame.
        column (str): The name of the column to normalize.
    
    Returns:
        normalized_df (pl.DataFrame):
            A Polars DataFrame with the column normalized
    """
    mean = df[column].mean()
    std = df[column].std()

    normalized_df = df.with_columns([
        ((pl.col(column) - mean) / std).alias(column)
    ])

    return normalized_df

def filter_lexicon(lexicon: pl.DataFrame,
                   words: pl.Series,
                   word_column: str = "Word"
                   ) -> pl.DataFrame:
    """
    Filters a lexicon to only include the words in a list.

    Args:
        lexicon (pl.DataFrame): A Polars DataFrame containing the lexicon.
        words (pl.Series): A Polars Series containing the words to include.
        word_column (str):
            The name of the column containing the words in the lexicon.

    Returns:
        filtered_lexicon (pl.DataFrame):
            A Polars DataFrame containing only the words in the list.
    """
    return lexicon.filter(pl.col(word_column).is_in(words))

def upos_to_wn(upos_tag: str) -> str:
    """
    Converts a Universal POS tag to a (Senti)WordNet POS tag.

    Args:
        upos_tag (str): A Universal POS tag.

    Returns:
        wn_tag (str): A WordNet POS tag.
    """
    if upos_tag in {"NOUN", "PROPN"}:
        return "n"
    elif upos_tag in {"VERB", "AUX"}:
        return "v"
    elif upos_tag in {"ADV"}:
        return "r"
    elif upos_tag in {"ADJ"}:
        return "a"
    else:
        return None

