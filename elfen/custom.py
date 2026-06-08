"""
Generic functions for custom lexicon feature extraction. These functions
allow the user to extract features from a custom lexicon. The lexicon
should be a DataFrame with with the tokens or lemmas in one column and
the features (e.g. concreteness; only if thresholds are to be applied) in
another column.

Functions:
    get_n_custom: Get the number of occurences of words in a custom lexicon
        in the text.
    get_occurs_custom: Binary feature indicating if any word from a custom
        lexicon occurs in the text.
    get_n_custom_low: Get the number of occurences of words with a low
        given feature (e.g. concreteness) from a custom lexicon in the
        text.
    get_n_custom_high: Get the number of occurences of words with a high
        given feature (e.g. concreteness) from a custom lexicon in the
        text.
"""

import polars as pl

from .generic import (
    get_avg,
    get_n_low,
    get_n_high,
)


def get_n_custom(data: pl.DataFrame,
                 lexicon: pl.DataFrame,
                 feature_name: str = 'n_custom',
                 word_column: str = 'word',
                 measurement_level: str = 'tokens',
                 ) -> pl.DataFrame:
    """
    Get the number of occurences of words in a custom lexicon in the text.

    Args:
        data (pl.DataFrame):
            The data to process. Should contain the preprocessed column
            'nlp'.
        lexicon (pl.DataFrame): The lexicon to use.
        feature_name (str): The name of the feature to create.
        word_column (str): The column the words occur in in the lexicon.
        measurement_level (str):
            The measurement level of the lexicon; either 'tokens' or
            'lemmas'.

    Returns:
        data (pl.DataFrame): 
            The data with the new feature.
    """
    raise NotImplementedError('This function is not implemented yet. Please use get_n_custom_low and get_n_custom_high instead.')
    
def get_occurs_custom(data: pl.DataFrame,
                      lexicon: pl.DataFrame,
                      feature_name: str = 'occurs_custom',
                      word_column: str = 'word',
                      measurement_level: str = 'tokens',
                      ) -> pl.DataFrame:
    """
    Binary feature indicating if any word from a custom lexicon occurs in
    the text.

    Args:
        data (pl.DataFrame):
            The data to process. Should contain the preprocessed column
            'nlp'.
        lexicon (pl.DataFrame): The lexicon to use.
        feature_name (str): The name of the feature to create.
        word_column (str): The column the words occur in in the lexicon.

    Returns:
        data (pl.DataFrame): 
            The data with the new feature.
    """
    raise NotImplementedError('This function is not implemented yet. Please use get_n_custom_low and get_n_custom_high instead.')

def get_n_custom_low(data: pl.DataFrame,
                     lexicon: pl.DataFrame,
                     threshold: int,
                     feature_name: str,
                     word_column: str = 'word',
                     feature_column: str = 'feature',
                     ) -> pl.DataFrame:
    """
    Get the number of occurences of words in a custom lexicon in the text
    with a given feature (e.g. concreteness) below a threshold.

    Args:
        data (pl.DataFrame):
            The data to process. Should contain the preprocessed column
            'nlp'.
        lexicon (pl.DataFrame): The lexicon to use.
        feature_name (str): The name of the feature to create.
        threshold (int): The threshold to use.
        word_column (str): The column the words occur in in the lexicon.
        feature_column (str):
            The column the feature occurs in in the lexicon.

    Returns:
        data (pl.DataFrame): 
            The data with the new feature in the column specified by 
            `feature_name`.
    """
    data = get_n_low(data=data,
                     lexicon=lexicon,
                     threshold=threshold,
                     lexicon_rating_col=feature_column,
                     lexicon_word_col=word_column,
                     new_col_name=feature_name,
    )

    return data

def get_n_custom_high(data: pl.DataFrame,
                      lexicon: pl.DataFrame,
                      threshold: int,
                      feature_name: str = 'n_custom_high',
                      word_column: str = 'word',
                      feature_column: str = 'feature',
                      ) -> pl.DataFrame:
    """
    Get the number of occurences of words in a custom lexicon in the text
    with a given feature (e.g. concreteness) above a threshold.

    Args:
        data (pl.DataFrame):
            The data to process. Should contain the preprocessed column
            'nlp'.
        lexicon (pl.DataFrame): The lexicon to use.
        threshold (int): The threshold to use.
        feature_name (str): The name of the feature to create.
        word_column (str): The column the words occur in in the lexicon.
        feature_column (str):
            The column the feature occurs in in the lexicon.
        measurement_level (str):
            The measurement level of the lexicon; either 'tokens' or
            'lemmas'.

    Returns:
        data (pl.DataFrame): 
            The data with the new feature.
    """
    data = get_n_high(data=data,
                      lexicon=lexicon,
                      threshold=threshold,
                      lexicon_rating_col=feature_column,
                      lexicon_word_col=word_column,
                      new_col_name=feature_name,
    )

    return data


def get_avg_custom(data: pl.DataFrame,
                   lexicon: pl.DataFrame,
                   feature_name: str = 'avg_custom',
                   word_column: str = 'word',
                   feature_column: str = 'feature',
                   ) -> pl.DataFrame:
    """
    Get the average feature value of words in a custom lexicon in the text.

    Args:
        data (pl.DataFrame):
            The data to process. Should contain the preprocessed column
            'nlp'.
        lexicon (pl.DataFrame): The lexicon to use.
        feature_name (str): The name of the feature to create.
        word_column (str): The column the words occur in in the lexicon.
        feature_column (str):
            The column the feature occurs in in the lexicon.
        measurement_level (str):
            The measurement level of the lexicon; either 'tokens' or
            'lemmas'.

    Returns:
        data (pl.DataFrame): 
            The data with the new feature.
    """
    data = get_avg(data=data,
                   lexicon=lexicon,
                   lexicon_word_col=word_column,
                   lexicon_rating_col=feature_column,
                   new_col_name=feature_name,
    )

    return data

