import polars as pl

def get_raw_sequence_length(data: pl.DataFrame,
                        text_column: str = 'text',
                        ) -> pl.DataFrame:
    """
    Calculates the raw text length (number of characters) of a text.
    """
    data = data.with_columns(
        pl.col(text_column).map_elements(lambda x: len(x),
                                         return_dtype=pl.UInt16
                                         ).alias("raw_seq_len"),
    )
    
    return data

def get_sequence_length(data: pl.DataFrame,
                        backbone: str = 'spacy'
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
                        backbone: str = 'spacy'
                         ) -> pl.DataFrame:
    """
    Calculates the number of sentences in a text.
    """
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: len(list(x.sents)),
                                         return_dtype=pl.UInt16
                                       ).alias("n_sents"),
        )
    elif backbone == 'stanza':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: len(x.sentences),
                                       return_dtype=pl.UInt16
                                       ).alias("n_sents"),
        )
    
    return data

def get_tokens_per_sentence(data: pl.DataFrame,
                            backbone: str = 'spacy'
                            ) -> pl.DataFrame:
    """
    Calculates the average number of tokens per sentence in a text.
    """
    if 'n_tokens' not in data.columns:
        data = get_sequence_length(data, backbone=backbone)
    if 'n_sents' not in data.columns:
        data = get_num_sentences(data, backbone=backbone)

    data = data.with_columns(
        (pl.col("n_tokens") / pl.col("n_sents")).alias("tokens_per_sent"),
    )

    return data

def get_num_chars(data: pl.DataFrame,
                    backbone: str = 'spacy'
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
                    ).alias("n_chars"),
            )
        elif backbone == 'stanza':
            raise NotImplementedError(
                "Not implemented for Stanza backbone yet."
            )
        
        return data

def get_chars_per_sentence(data: pl.DataFrame,
                            backbone: str = 'spacy'
                            ) -> pl.DataFrame:
    """
    Calculates the average number of characters per sentence in a text.
    """
    if 'n_chars' not in data.columns:
        data = get_num_chars(data, backbone=backbone)
    if 'n_sents' not in data.columns:
        data = get_num_sentences(data, backbone=backbone)

    data = data.with_columns(
        (pl.col("n_chars") / pl.col("n_sents")).alias("chars_per_sent"),
    )

    return data

def get_raw_length_per_sentence(data: pl.DataFrame,
                                backbone: str = 'spacy',
                                text_column: str = 'text'
                                ) -> pl.DataFrame:
    """
    Calculates the average number of characters per sentence in a text.
    """
    if 'n_sents' not in data.columns:
        data = get_num_sentences(data, backbone=backbone)
    if 'raw_seq_len' not in data.columns:
        data = get_raw_sequence_length(data, text_column=text_column)

    data = data.with_columns(
        (pl.col("raw_seq_len") / pl.col("n_sents")).alias("raw_len_per_sent"),
    )

    return data

def get_avg_word_length(data: pl.DataFrame,
                        backbone: str = 'spacy',
                        text_column: str = 'text'
                        ) -> pl.DataFrame:
    """
    Calculates the average word length in a text.
    """
    if 'n_tokens' not in data.columns:
        data = get_sequence_length(data, backbone=backbone)
    if 'raw_seq_len' not in data.columns:
        data = get_raw_sequence_length(data, text_column=text_column)

    data = data.with_columns(
        (pl.col("raw_seq_len") / pl.col("n_tokens")).alias("avg_word_len"),
    )

    return data

def get_num_types(data: pl.DataFrame,
                  backbone: str = 'spacy'
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
        raise NotImplementedError(
            "Not implemented for Stanza backbone yet."
        )
        
    return data