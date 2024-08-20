"""
This module contains functions for calculating information-theoretic metrics.
"""
import bz2

import polars as pl
import numpy as np

def get_compressibility(data: pl.DataFrame,
                        text_column: str = 'text',
                        ) -> pl.DataFrame:
    """
    Calculates the compressibility of the texts in the text column.

    The compressibility is the ratio of the length of the compressed text to
    the length of the original text. This is used as a proxy for the
    kolmogorov complexity of the text.

    Args:
    - data: A Polars DataFrame containing the text data.
    - text_column: The name of the column containing the text data.

    Returns:
    - data: A Polars DataFrame containing the compressibility of the text data.
            The compressibility is stored in a new column named 'compressibility'.
    """
    data = data.with_columns(
        pl.col(text_column).map_elements(
            lambda x: len(bz2.compress(x.encode('utf-8'))) / len(x),
            return_dtype=pl.Float64
            ).alias("compressibility"),
    )
    
    return data

def get_entropy(data: pl.DataFrame,
                text_column: str = 'text',
                ) -> pl.DataFrame:
    """
    Calculates the Shannon entropy of the texts in the text column.

    The Shannon entropy is a measure of the uncertainty in a random variable.

    Args:
    - data: A Polars DataFrame containing the text data.
    - text_column: The name of the column containing the text data.

    Returns:
    - data: A Polars DataFrame containing the Shannon entropy of the text data.
            The Shannon entropy is stored in a new column named 'entropy'.
    """
    data = data.with_columns(
        pl.col(text_column).map_elements(
            entropy,
            return_dtype=pl.Float64
            ).alias("entropy"),
    )

    return data

def entropy(string: str) -> float:
    """
    Calculate the Shannon entropy of a string.
    Helper function for get_entropy.

    Args:
    - string: The input string.

    Returns:
    - entropy: The Shannon entropy of the input string.
    """
    chars = np.array(list(string))

    _, counts = np.unique(chars, return_counts=True)
    prob = counts / len(string)
    entropy = -np.sum(prob * np.log2(prob))
    
    return entropy

