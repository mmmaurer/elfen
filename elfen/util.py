"""
This module contains utility functions for working with Polars DataFrames.
"""
import polars as pl

def rescale_column(data: pl.DataFrame,
                   column: str,
                   minimum: float = 0.0,
                   maximum: float = 1.0) -> pl.DataFrame:
    """
    Rescales a column to a custom range. Defaults to [0, 1].

    Args:
        data (pl.DataFrame): A Polars DataFrame.
        column (str): The name of the column to rescale.
        minimum (float): 
            The desired minimum value of the column.
            Defaults to 0.
        maximum (float):
            The desired maximum value of the column.
            Defaults to 1.

    Returns:
        rescaled_data (pl.DataFrame):
            A Polars DataFrame with the column rescaled to
            [minimum, maximum].
    """
    inner_minimum = data[column].min()
    inner_maximum = data[column].max()
    
    # Rescale to [0, 1]
    if minimum == 0.0 and maximum == 1.0:
        rescaled_data = data.with_columns([
            ((pl.col(column) - inner_minimum) / 
            (inner_maximum - inner_minimum)).alias(column)
        ])
    # Rescale to [minimum, maximum]
    else:
        rescaled_data = data.with_columns([
            (((pl.col(column) - inner_minimum) / 
            (inner_maximum - inner_minimum)) * 
            (maximum - minimum) + minimum).alias(column)
        ])

    return rescaled_data

def normalize_column(data: pl.DataFrame,
                     column: str) -> pl.DataFrame:
    """
    Normalizes a column to have a mean of 0 and a standard deviation of 1.

    Args:
        data (pl.DataFrame): A Polars DataFrame.
        column (str): The name of the column to normalize.
    
    Returns:
        normalized_data (pl.DataFrame):
            A Polars DataFrame with the column normalized
    """
    mean = data[column].mean()
    std = data[column].std()

    normalized_data = data.with_columns([
        ((pl.col(column) - mean) / std).alias(column)
    ])

    return normalized_data

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

