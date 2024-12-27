"""
This module contains functions to calculate various surface-level features
from text data.

The surface-level features implemented in this module are:

- Raw Sequence Length:
    The number of characters in the text including whitespaces.
- Number of Tokens: The number of tokens in the text.
- Number of Sentences: The number of sentences in the text.
- Number of Tokens per Sentence: The average number of tokens per sentence.
- Number of Characters:
    The number of characters in the text excluding whitespaces.
- Number of Characters per Sentence:
    The average number of characters per sentence.
- Raw Length per Sentence:
    The average number of characters per sentence including whitespaces.
- Average Word Length: The average length of a word in the text.
- Number of Types: The number of unique tokens in the text.
- Number of Long Words: The number of words longer than a threshold.
- Number of Lemmas: The number of unique lemmas in the text.
- Token Frequencies: The frequency of each token in the text.
"""

from collections import Counter

import polars as pl

def get_raw_sequence_length(data: pl.DataFrame,
                            text_column: str = 'text',
                            **kwargs: dict[str, str],
                            ) -> pl.DataFrame:
    """
    Calculates the raw text length (number of characters) of a text.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        text_column (str): The name of the column containing the text data.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the raw text length of the text
            data. The raw text length is stored in a new column named
            'raw_sequence_length'.
    """
    data = data.with_columns(
        pl.col(text_column).map_elements(lambda x: len(x),
                                         return_dtype=pl.UInt16
                                         ).alias("raw_sequence_length"),
    )
    
    return data

def get_num_tokens(data: pl.DataFrame,
                   backbone: str = 'spacy',
                   **kwargs: dict[str, str],
                   ) -> pl.DataFrame:
    """
    Calculates the sequence length (number of tokens) of a text.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the sequence length of the text
            data. The sequence length is stored in a new column named
            'n_tokens'.
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
                      **kwargs: dict[str, str],
                      ) -> pl.DataFrame:
    """
    Calculates the number of sentences in a text.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
    
    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the number of sentences in the
            text data. The number of sentences is stored in a new column
            named 'n_sentences'.
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
                                **kwargs: dict[str, str],
                                ) -> pl.DataFrame:
    """
    Calculates the average number of tokens per sentence in a text.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
    
    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the average number of tokens per
            sentence in the text data. The average number of tokens per
            sentence is stored in a new column named 'tokens_per_sentence'.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_sentences' not in data.columns:
        data = get_num_sentences(data, backbone=backbone)

    data = data.with_columns(
        (pl.col("n_tokens") / pl.col("n_sentences")). \
            alias("tokens_per_sentence"),
    )

    return data

def get_num_characters(data: pl.DataFrame,
                    backbone: str = 'spacy',
                    **kwargs: dict[str, str],
                    ) -> pl.DataFrame:
        """
        Calculates the number of characters in a text.
        Only takes tokens into account in contrast to
        get_raw_sequence_length.

        Args:
            data (pl.DataFrame):
                A Polars DataFrame containing the text data.
            backbone (str): The NLP library used to process the text data.
                    Either 'spacy' or 'stanza'.
        
        Returns:
            data (pl.DataFrame):
                A Polars DataFrame containing the number of characters in 
                the text data. The number of characters is stored in a new
                column named 'n_characters'.
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
                            **kwargs: dict[str, str],
                            ) -> pl.DataFrame:
    """
    Calculates the average number of characters per sentence in a text.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the average number of characters
            per sentence in the text data. The average number of
            characters per sentence is stored in a new column named
            'characters_per_sentence'.
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
                                **kwargs: dict[str, str],
                                ) -> pl.DataFrame:
    """
    Calculates the average number of characters per sentence in a text.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the average number of characters
            per sentence in the text data. The average number of
            characters per sentence is stored in a new column named
            'raw_length_per_sentence'.
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
                        ,**kwargs: dict[str, str],
                        ) -> pl.DataFrame:
    """
    Calculates the average word length in a text.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the average word length in the
            text data.
            The average word length is stored in a new column named
            'avg_word_length'.
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
                  **kwargs: dict[str, str],
                 ) -> pl.DataFrame:
    """
    Calculates the number of types in a text.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame): 
            A Polars DataFrame containing the number of types in the text 
            data.
            The number of types is stored in a new column named 'n_types'.
    """
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col("nlp"). \
                map_elements(lambda x: len(
                    set([token.text for token in x])),
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
                       **kwargs: dict[str, str],
                       ) -> pl.DataFrame:
    """
    Calculates the number of long words in a text.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
        threshold (int):
            The minimum length of a word to be considered long.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the number of long words in the 
            text data.
            The number of long words is stored in a new column named 
            'n_long_words'.
    """
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col("nlp"). \
                map_elements(lambda x: len(
                    [token for token in x if len(token.text) >= threshold]),
                             return_dtype=pl.UInt16
                             ).alias("n_long_words"),
        )
    elif backbone == 'stanza':
        data = data.with_columns(
            pl.col("nlp"). \
                map_elements(lambda x: len(
                    [token for sent
                     in x.sentences for token in sent.tokens
                     if len(token.text) >= threshold]),
                             return_dtype=pl.UInt16
                             ).alias("n_long_words"),
        )
        
    return data

def get_num_lemmas(data: pl.DataFrame,
                   backbone: str = 'spacy',
                   **kwargs: dict[str, str],
                   ) -> pl.DataFrame:
    """
    Calculates the number of unique lemmas in the text.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
    
    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the number of unique lemmas in
            the text data. The number of unique lemmas is stored in a new 
            column named 'n_lemmas'.
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

def get_token_freqs(data: pl.DataFrame,
                    backbone: str = 'spacy',
                    **kwargs: dict[str, str],
                    ) -> pl.DataFrame:
    """
    Calculates the frequency of each token in the text.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
    
    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the frequency of each token in
            the text data. The frequency of each token is stored in a new 
            column named 'token_freqs'.
    """
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: dict(
                Counter([token.text for token in x])),
                return_dtype=pl.Object
                ).alias("token_freqs"),
        )
    elif backbone == 'stanza':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: dict(
                Counter([token.text for sent in x.sentences for token
                         in sent.tokens])),
                return_dtype=pl.Object
                ).alias("token_freqs"),
        )
    
    return data

def get_global_token_frequencies(data: pl.DataFrame,
                                 backbone: str = 'spacy',
                                 **kwargs: dict[str, str],
                                 ) -> dict[str, int]:
    """
    Calculates the global frequency of each token in the text.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
        token_freqs (dict[str, int]):
            A dictionary containing the frequency of each token in the text.
    """
    if backbone == 'spacy':
        token_freqs = dict(Counter([token.text for text in 
                                    data["nlp"].to_list() for 
                                    token in text]
        ))
    elif backbone == 'stanza':
        token_freqs = dict(Counter([token.text for text in
                                    data["nlp"].to_list() for
                                    sent in text.sentences for 
                                    token in sent.tokens]
        ))

    return token_freqs

def get_global_lemma_frequencies(data: pl.DataFrame,
                                 backbone: str = 'spacy',
                                 **kwargs: dict[str, str],
                                 ) -> dict[str, int]:
    """
    Calculates the global frequency of each lemma in the text.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
        lemma_freqs (dict[str, int]):
            A dictionary containing the frequency of each lemma in the text.
    """
    if backbone == 'spacy':
        lemma_freqs = dict(Counter([token.lemma_ for text in
                                    data["nlp"].to_list() for
                                    token in text]
        ))
    elif backbone == 'stanza':
        lemma_freqs = dict(Counter([token.lemma for text in
                                    data["nlp"].to_list() for
                                    sent in text.sentences for
                                    token in sent.tokens]
        ))

    return lemma_freqs

