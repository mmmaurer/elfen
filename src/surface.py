"""
This module contains functions to calculate various surface-level features
from text data.
"""
from collections import Counter
from typing import Any, Tuple

import polars as pl

def get_raw_sequence_length(data: pl.DataFrame,
                            text_column: str = 'text',
                            *_ : Tuple[Any, ...],
                            ) -> pl.DataFrame:
    """
    Calculates the raw text length (number of characters) of a text.
    """
    data = data.with_columns(
        pl.col(text_column).map_elements(lambda x: len(x),
                                         return_dtype=pl.UInt16
                                         ).alias("raw_sequence_length"),
    )
    
    return data

def get_num_tokens(data: pl.DataFrame,
                   backbone: str = 'spacy',
                   *_ : Tuple[Any, ...],
                   ) -> pl.DataFrame:
    """
    Calculates the sequence length (number of tokens) of a text.
    """
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: len(x),
                                       return_dtype=pl.UInt16
                                       ).alias("n_tokens"),
        )
    elif backbone == 'stanza':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: x.num_tokens,
                                       return_dtype=pl.UInt16
                                       ).alias("n_tokens"),
        )
    
    return data

def get_num_sentences(data: pl.DataFrame,
                      backbone: str = 'spacy',
                      *_ : Tuple[Any, ...],
                      ) -> pl.DataFrame:
    """
    Calculates the number of sentences in a text.
    """
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: len(list(x.sents)),
                                         return_dtype=pl.UInt16
                                       ).alias("n_sentences"),
        )
    elif backbone == 'stanza':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: len(x.sentences),
                                       return_dtype=pl.UInt16
                                       ).alias("n_sentences"),
        )
    
    return data

def get_num_tokens_per_sentence(data: pl.DataFrame,
                                backbone: str = 'spacy',
                                *_ : Tuple[Any, ...],
                                ) -> pl.DataFrame:
    """
    Calculates the average number of tokens per sentence in a text.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_sentences' not in data.columns:
        data = get_num_sentences(data, backbone=backbone)

    data = data.with_columns(
        (pl.col("n_tokens") / pl.col("n_sentences")).alias("tokens_per_sentence"),
    )

    return data

def get_num_characters(data: pl.DataFrame,
                    backbone: str = 'spacy',
                    *_ : Tuple[Any, ...],
                    ) -> pl.DataFrame:
        """
        Calculates the number of characters in a text.
        Only takes tokens into account in contrast to get_raw_sequence_length.
        """
        if backbone == 'spacy':
            data = data.with_columns(
                pl.col("nlp").map_elements(lambda x: sum(
                    [len(token.text) for token in x]),
                    return_dtype=pl.UInt16
                    ).alias("n_characters"),
            )
        elif backbone == 'stanza':
            data = data.with_columns(
                pl.col("nlp").map_elements(lambda x: sum(
                    [len(token.text) for sent
                     in x.sentences for token in sent.tokens]),
                    return_dtype=pl.UInt16
                    ).alias("n_characters"),
            )
        
        return data

def get_chars_per_sentence(data: pl.DataFrame,
                            backbone: str = 'spacy',
                            *_ : Tuple[Any, ...],
                            ) -> pl.DataFrame:
    """
    Calculates the average number of characters per sentence in a text.
    """
    if 'n_characters' not in data.columns:
        data = get_num_characters(data, backbone=backbone)
    if 'n_sentences' not in data.columns:
        data = get_num_sentences(data, backbone=backbone)

    data = data.with_columns(
        (
            pl.col("n_characters") / pl.col("n_sentences")
        ).alias("characters_per_sentence"),
    )

    return data

def get_raw_length_per_sentence(data: pl.DataFrame,
                                backbone: str = 'spacy',
                                text_column: str = 'text',
                                *_ : Tuple[Any, ...],
                                ) -> pl.DataFrame:
    """
    Calculates the average number of characters per sentence in a text.
    """
    if 'n_sentences' not in data.columns:
        data = get_num_sentences(data, backbone=backbone)
    if 'raw_sequence_length' not in data.columns:
        data = get_raw_sequence_length(data, text_column=text_column)

    data = data.with_columns(
        (
            pl.col("raw_sequence_length") / pl.col("n_sentences")
        ).alias("raw_length_per_sentence"),
    )

    return data

def get_avg_word_length(data: pl.DataFrame,
                        backbone: str = 'spacy',
                        text_column: str = 'text'
                        ,*_ : Tuple[Any, ...],
                        ) -> pl.DataFrame:
    """
    Calculates the average word length in a text.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_characters' not in data.columns:
        data = get_num_characters(data, text_column=text_column)

    data = data.with_columns(
        (
            pl.col("n_characters") / pl.col("n_tokens")
        ).alias("avg_word_length"),
    )

    return data

def get_num_types(data: pl.DataFrame,
                  backbone: str = 'spacy',
                  *_ : Tuple[Any, ...],
                 ) -> pl.DataFrame:
    """
    Calculates the number of types in a text.
    """
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col("nlp"). \
                map_elements(lambda x: len(set([token.text for token in x])),
                             return_dtype=pl.UInt16
                             ).alias("n_types"),
        )
    elif backbone == 'stanza':
        data = data.with_columns(
            pl.col("nlp"). \
                map_elements(lambda x: len(
                    set([token.text for sent
                         in x.sentences for token in sent.tokens])),
                         return_dtype=pl.UInt16
                         ).alias("n_types"),
        )
        
    return data

def get_num_long_words(data: pl.DataFrame,
                       backbone: str = 'spacy',
                       threshold: int = 6,
                       *_ : Tuple[Any, ...],
                       ) -> pl.DataFrame:
    """
    Calculates the number of long words in a text.
    """
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col("nlp"). \
                map_elements(lambda x: len([token for token in x
                                           if len(token.text) >= threshold]),
                             return_dtype=pl.UInt16
                             ).alias("n_long_words"),
        )
    elif backbone == 'stanza':
        data = data.with_columns(
            pl.col("nlp"). \
                map_elements(lambda x: len([token for sent
                                           in x.sentences for token in sent.tokens
                                           if len(token.text) >= threshold]),
                             return_dtype=pl.UInt16
                             ).alias("n_long_words"),
        )
        
    return data

def get_num_lemmas(data: pl.DataFrame,
                   backbone: str = 'spacy',
                   *_ : Tuple[Any, ...],
                   ) -> pl.DataFrame:
    """
    Calculates the number of unique lemmas in the text.

    Args:
    - data: A Polars DataFrame containing the text data.
    - backbone: The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
    
    Returns:
    - data: A Polars DataFrame containing the number of unique lemmas in the
            text data. The number of unique lemmas is stored in a new column
            named 'n_lemmas'.
    """
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: len(set(
                [token.lemma_ for token in x])),
                return_dtype=pl.UInt16
                ).alias("n_lemmas"),
        )
    elif backbone == 'stanza':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: len(set(
                [token.lemma for sent in x.sentences for token
                 in sent.words])),
                return_dtype=pl.UInt16
                ).alias("n_lemmas"),
        )
    
    return data

