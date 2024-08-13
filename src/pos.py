import polars as pl

from .surface import (
    get_num_tokens,
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
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: len(
                [token for sent in x.sentences for token
                 in sent.words if token.upos in lex]),
                return_dtype=pl.UInt16
                ).alias("n_lexical_tokens"),
        )
    
    return data

def get_pos_variability(data: pl.DataFrame,
                        backbone: str = 'spacy'
                        ) -> pl.DataFrame:
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
        for pos in pos_tags:
            data = data.with_columns(
                pl.col("nlp").map_elements(lambda x: len(
                    [token for sent in x.sentences for token
                     in sent.words if token.upos == pos]),
                    return_dtype=pl.UInt16
                    ).alias(f"n_{pos.lower()}"),
            )
    
    return data

def get_pos_ratio(data: pl.DataFrame,
                           backbone: str = 'spacy',
                           pos_tags: list = UPOS_TAGS
                           ) -> pl.DataFrame:
    if "n_tokens" not in data.columns:
        data = get_num_tokens(data, backbone)

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
        for pos in pos_tags:
            data = data.with_columns(
                pl.col("nlp").map_elements(lambda x: len(
                    [token for sent in x.sentences for token
                     in sent.words if token.upos == pos]),
                    return_dtype=pl.UInt16
                    ).alias(f"n_{pos.lower()}_per_sent"),
            )
    
    return data

def get_num_lemmas(data: pl.DataFrame,
                          backbone: str = 'spacy'
                          ) -> pl.DataFrame:
    """
    Returns the number of unique lemmas in the text.
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

