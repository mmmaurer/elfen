"""
This module contains functions to extract morphological features of text data.
"""
import polars as pl

def get_morph_feats(
        data: pl.DataFrame,
        backbone: str = 'spacy',
        morph_config: dict = None,
        **kwargs: dict[str, str],
        ) -> pl.DataFrame:
    """
    Extracts morphological features from the text data.

    Args:
    - data: A Polars DataFrame containing the text data.
    - backbone: The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
    - morph_config: A dictionary containing the configuration for extracting
                    morphological features. The keys are POS, and the values
                    are dictionaries containing names of features as keys and
                    their configurations as values. The configuration should
                    follow the format:
                    {
                        "VERB": {
                            "VerbForm": ["Inf", "Fin"],
                            ...
                        },
                        ...,
                        "NOUN": {
                            "Number": ["Sing", "Plur"],
                            ...
                        }
                    }
    """
    if morph_config is None:
        print("No morphological features to extract. Returning the input data.")
        return data
    
    # TODO: optimize this function
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
    # TODO: implement for Stanza
    elif backbone == 'stanza':
        print("Morphological features extraction is not implemented yet for Stanza.")
        pass

    return data