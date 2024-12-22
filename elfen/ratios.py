import polars as pl

from .surface import (
    get_num_tokens,
    get_num_sentences,
    get_num_types
)

def get_feature_token_ratio(data: pl.DataFrame,
                            features: list[str],
                            backbone: str = 'spacy',
                            **kwargs: dict[str, str],
                            ) -> pl.DataFrame:
    """
    Gets the ratio of given features to the total number of tokens.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        features (list[str]):
            A list of features to calculate the ratio for.
            Note that the features should be present in the data
            as column names.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the ratio of the given features
            to the total number of tokens. The ratios are stored in new
            columns with the feature names suffixed by '_token_ratio'. 
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone)

    data = data.with_columns(
        (pl.col(features) / pl.col("n_tokens")). \
            name.map(lambda x: f"{x}_token_ratio")
    )

    return data

def get_feature_type_ratio(data: pl.DataFrame,
                            features: list[str],
                            backbone: str = 'spacy',
                            **kwargs: dict[str, str],
                            ) -> pl.DataFrame:
    """
    Gets the ratio of given features to the total number of types.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        features (list[str]):
            A list of features to calculate the ratio for.
            Note that the features should be present in the data
            as column names.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the ratio of the given features
            to the total number of types. The ratios are stored in new
            columns with the feature names suffixed by '_type_ratio'.
    """
    if 'n_types' not in data.columns:
        data = get_num_types(data, backbone)
    
    data = data.with_columns(
        (pl.col(features) / pl.col("n_types")). \
            name.map(lambda x: f"{x}_type_ratio")
    )

    return data

def get_feature_sentence_ratio(data: pl.DataFrame,
                               features: list[str],
                               backbone: str = 'spacy',
                               **kwargs: dict[str, str],
                               ) -> pl.DataFrame:
    """
    Gets the ratio of given features to the total number of sentences.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        features (list[str]):
            A list of features to calculate the ratio for.
            Note that the features should be present in the data
            as column names.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the ratio of the given features
            to the total number of sentences. The ratios are stored in new
            columns with the feature names suffixed by '_sentence_ratio'. 
    """
    if 'n_sentences' not in data.columns:
        data = get_num_sentences(data, backbone)

    data = data.with_columns(
        (pl.col(features) / pl.col("n_sentences")). \
            name.map(lambda x: f"{x}_sentence_ratio")
    )

    return data 

