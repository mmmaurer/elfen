import polars as pl

from .surface import (
    get_sequence_length,
    get_num_sentences,
)

UPOS_TAGS = [
    'ADJ', 'ADP', 'ADV', 'AUX', 'CONJ', 'CCONJ', 'DET', 'INTJ', 'NOUN',
    'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X'
]

def get_num_lexical_tokens(data: pl.DataFrame,
                            backbone: str = 'spacy'
                            ) -> pl.DataFrame:
    lex = ["NOUN", "VERB", "ADJ", "ADV"]
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: len(
                [token for token in x if token.pos_ in lex]),
                return_dtype=pl.UInt16
                ).alias("n_lexical_tokens"),
        )
    elif backbone == 'stanza':
        raise NotImplementedError(
            "Not implemented for Stanza backbone yet."
        )
    
    return data

def get_num_per_pos(data: pl.DataFrame,
                backbone: str = 'spacy',
                pos_tags: list = UPOS_TAGS
                ) -> pl.DataFrame:
    if backbone == 'spacy':
        for pos in pos_tags:
            data = data.with_columns(
                pl.col("nlp").map_elements(lambda x: len(
                    [token for token in x if token.pos_ == pos]),
                    return_dtype=pl.UInt16
                    ).alias(f"n_{pos.lower()}"),
            )
    elif backbone == 'stanza':
        raise NotImplementedError(
            "Not implemented for Stanza backbone yet."
        )
    
    return data

def get_pos_ratio(data: pl.DataFrame,
                           backbone: str = 'spacy',
                           pos_tags: list = UPOS_TAGS
                           ) -> pl.DataFrame:
    if "n_tokens" not in data.columns:
        data = get_sequence_length(data, backbone)

    for pos in pos_tags:
        if f"n_{pos.lower()}" not in data.columns:
            data = get_num_per_pos(data, backbone, pos_tags)
        data = data.with_columns(
            (
                pl.col(f"n_{pos.lower()}") / pl.col("n_tokens")
            ).alias(f"{pos.lower()}_ratio")
        )
    
    return data

def get_pos_per_sent(data: pl.DataFrame,
                     backbone: str = 'spacy',
                     pos_tags: list = UPOS_TAGS
                     ) -> pl.DataFrame:
    if "n_sentences" not in data.columns:
        data = get_num_sentences(data, backbone)
    
    if backbone == 'spacy':
        for pos in pos_tags:
            data = data.with_columns(
                pl.col("nlp").map_elements(lambda x: len(
                    [token for token in x if token.pos_ == pos]),
                    return_dtype=pl.UInt16
                    ).alias(f"n_{pos.lower()}_per_sent"),
            )
    elif backbone == 'stanza':
        raise NotImplementedError(
            "Not implemented for Stanza backbone yet."
        )
    
    return data