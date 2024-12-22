"""
This module contains functions for calculating information-theoretic
metrics.

The information-theoretic metrics implemented in this module are:

- Compressibility:
    The ratio of the length of the compressed text to the length of the
    original text.
- Shannon Entropy:
    The Shannon entropy of the text data.
"""
import bz2

import numpy as np
import polars as pl

def get_compressibility(data: pl.DataFrame,
                        text_column: str = 'text',
                        **kwargs: dict[str, str],
                        ) -> pl.DataFrame:
    """
    Calculates the compressibility of the texts in the text column.

    The compressibility is the ratio of the length of the compressed text
    to the length of the original text. This is used as a proxy for the
    Kolmogorov complexity of the text.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        text_column (str): The name of the column containing the text data.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the compressibility of the text
            data. The compressibility is stored in a new column named
            'compressibility'.
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
                **kwargs: dict[str, str],
                ) -> pl.DataFrame:
    """
    Calculates the Shannon entropy of the texts in the text column.

    The Shannon entropy is a measure of the uncertainty in a random variable.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        text_column (str): The name of the column containing the text data.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the Shannon entropy of the text
            data. The Shannon entropy is stored in a new column named
            'entropy'.
    """
    data = data.with_columns(
        pl.col(text_column).map_elements(
            entropy,
            return_dtype=pl.Float64
            ).alias("entropy"),
    )

    return data

def entropy(string: str,
            **kwargs: dict[str, str],
            ) -> float:
    """
    Calculate the Shannon entropy of a string.
    Helper function for get_entropy.

    Args:
        string( str): The input string.

    Returns:
        entropy (float): The Shannon entropy of the input string.
    """
    chars = np.array(list(string))

    _, counts = np.unique(chars, return_counts=True)
    prob = counts / len(string)
    entropy = -np.sum(prob * np.log2(prob))
    
    return entropy

