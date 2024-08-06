import bz2

import polars as pl
import numpy as np

def get_compressibility(data: pl.DataFrame,
                        text_column: str = 'text',
                        ) -> pl.DataFrame:
    """
    Calculates the compressibility of a text.
    """
    data = data.with_columns(
        pl.col(text_column).map_elements(
            lambda x: len(bz2.compress(x.encode('utf-8'))) / len(x),
            return_dtype=pl.UInt16
            ).alias("compressibility"),
    )
    
    return data

def get_entropy(data: pl.DataFrame,
                text_column: str = 'text',
                ) -> pl.DataFrame:
    """
    Calculates the Shannon entropy of a text.
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
    """
    chars = np.array(list(string))

    _, counts = np.unique(chars, return_counts=True)
    prob = counts / len(string)
    entropy = -np.sum(prob * np.log2(prob))
    
    return entropy

