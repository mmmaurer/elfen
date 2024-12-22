"""
This module contains functions to calculate various part-of-speech (POS)-
related features from text data.

The POS-related features implemented in this module are:

- Number of lexical tokens: The number of tokens that are nouns, verbs,
                            adjectives, or adverbs.
- POS variability: The ratio of the number of unique POS tags to the
                   number of tokens.
- Number of tokens per POS tag: The number of tokens for each POS tag.
"""
import polars as pl

from .surface import (
    get_num_tokens,
)

UPOS_TAGS = [
    'ADJ', 'ADP', 'ADV', 'AUX', 'CONJ', 'CCONJ', 'DET', 'INTJ', 'NOUN',
    'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X'
]

def get_num_lexical_tokens(data: pl.DataFrame,
                           backbone: str = 'spacy',
                           **kwargs: dict[str, str],
                           ) -> pl.DataFrame:
    """
    Calculates the number of lexical tokens in the text.

    Lexical tokens are tokens that are nouns, verbs, adjectives, or adverbs.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                        Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the number of lexical tokens
            in the text data. The number of lexical tokens is stored in
            a new column named 'n_lexical_tokens'.
    """
    lex = ["NOUN", "VERB", "ADJ", "ADV"]
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: len(
                [token for token in x if token.pos_ in lex]),
                return_dtype=pl.UInt16
                ).alias("n_lexical_tokens"),
        )
    elif backbone == 'stanza':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: len(
                [token for sent in x.sentences for token
                 in sent.words if token.upos in lex]),
                return_dtype=pl.UInt16
                ).alias("n_lexical_tokens"),
        )
    
    return data

def get_pos_variability(data: pl.DataFrame,
                        backbone: str = 'spacy',
                        **kwargs: dict[str, str],
                        ) -> pl.DataFrame:
    """
    Calculates the variability of part-of-speech tags in the text data.

    The variability is the ratio of the number of unique part-of-speech
    tags to the number of tokens in the text data.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                        Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the variability of
            part-of-speech tags in the text data. The variability
            is stored in a new column named  'pos_variability'.
    """
    if "n_tokens" not in data.columns:
        data = get_num_tokens(data, backbone)
    
    if backbone == 'spacy':
        data = data.with_columns(
            (pl.col("nlp").map_elements(lambda x: len(set(
                [token.pos_ for token in x])),
                return_dtype=pl.UInt16) / 
            pl.col("n_tokens")).alias("pos_variability"),
        )
    elif backbone == 'stanza':
        data = data.with_columns(
            (pl.col("nlp").map_elements(lambda x: len(set(
                [token.upos for sent in x.sentences for token
                 in sent.words])),
                return_dtype=pl.UInt16) / 
            pl.col("n_tokens")).alias("pos_variability"),
        )

    return data

def get_num_per_pos(data: pl.DataFrame,
                    backbone: str = 'spacy',
                    pos_tags: list = UPOS_TAGS,
                    **kwargs: dict[str, str],
                    ) -> pl.DataFrame:
    """
    Calculates the number of tokens per part-of-speech tag in the text data.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
        pos_tags: A list of part-of-speech tags to calculate the number of
                tokens for.
                Default is the Universal POS tagset.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the number of tokens per
            part-of-speech tag in the text data. The number of tokens
            per part-of-speech tag is stored in new columns named
            'n_{pos}' where {pos} is the part-of speech tag.
    """
    if backbone == 'spacy':
        for pos in pos_tags:
            data = data.with_columns(
                pl.col("nlp").map_elements(lambda x: len(
                    [token for token in x if token.pos_ == pos]),
                    return_dtype=pl.UInt16
                    ).alias(f"n_{pos.lower()}"),
            )
    elif backbone == 'stanza':
        for pos in pos_tags:
            data = data.with_columns(
                pl.col("nlp").map_elements(lambda x: len(
                    [token for sent in x.sentences for token
                     in sent.words if token.upos == pos]),
                    return_dtype=pl.UInt16
                    ).alias(f"n_{pos.lower()}"),
            )
    
    return data

