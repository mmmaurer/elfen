"""
This module contains functions to extract morphological features of text
data.

The morphological features implemented in this module are:

- Number of tokens with a specific morphological feature: The number of
    tokens that have a specific morphological feature, such as VerbForm,
    Number, etc.
"""
import polars as pl

from .configs.morphological_config import MORPH_CONFIG

def get_morph_feats(
        data: pl.DataFrame,
        backbone: str = 'spacy',
        morph_config: dict = MORPH_CONFIG,
        **kwargs: dict[str, str],
        ) -> pl.DataFrame:
    """
    Extracts morphological features from the text data.

    Args:
        data (pl.DataFrame): 
            A Polars DataFrame containing the text data.
        backbone (str): 
            The NLP library used to process the text data.
            Either 'spacy' or 'stanza'.
        morph_config (dict[str, str]):
            A dictionary containing the configuration for extracting
            morphological features. The keys are POS, and the values
            are dictionaries containing names of features as keys and
            their configurations as values. The configuration should
            follow the format as in the MORPH_CONFIG dictionary in
            elfen/configs/morphological_config.py.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the morphological features of
            the text data.
    """
    if morph_config is None:
        print("No morphological features to extract. Returning the input"
              " data.")
        return data
    
    if backbone == 'spacy':
        for pos, feats in morph_config.items():
            for feat, values in feats.items():
                for val in values:
                    data = data.with_columns(
                        pl.col("nlp").map_elements(lambda x: len(
                            [token for token in x if token.pos_ == pos and
                            val in token.morph.get(feat)]),
                            return_dtype=pl.UInt16
                            ).alias(f"n_{pos}_{feat}_{val}"),
                    )
    elif backbone == 'stanza':
        for pos, feats in morph_config.items():
            for feat, values in feats.items():
                for val in values:
                    data = data.with_columns(
                        pl.col("nlp").map_elements(lambda x: len(
                            [1 for token in [token for sent in \
                                             x.sentences for token in \
                                             sent.words if \
                                             token.upos == pos and \
                                             token.feats]
                             if f"{feat}={val}" in token.feats]),
                            return_dtype=pl.UInt16
                            ).alias(f"n_{pos}_{feat}_{val}"),
                    )

    return data

