import polars as pl

def get_raw_sequence_length(data: pl.DataFrame,
                        text_column: str = 'text',
                        ) -> pl.DataFrame:
    data = data.with_columns(
        pl.col(text_column).map_elements(lambda x: len(x),
                                         return_dtype=pl.UInt16
                                         ).alias("raw_seq_len"),
    )
    
    return data

def get_sequence_length(data: pl.DataFrame,
                        backbone: str = 'spacy'
                       ) -> pl.DataFrame:
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

def get_raw_length_per_sentence(data: pl.DataFrame,
                                backbone: str = 'spacy',
                                text_column: str = 'text'
                                ) -> pl.DataFrame:
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