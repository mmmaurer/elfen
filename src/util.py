import polars as pl

def rescale_column(df: pl.DataFrame,
                   column: str,
                   minimum: float = None,
                   maximum: float = None) -> pl.DataFrame:
    """
    Rescale a column to a range of [0, 1].
    """
    if minimum is None:
        minimum = df[column].min()
    if maximum is None:
        maximum = df[column].max()
    
    rescaled_df = df.with_columns([
        ((pl.col(column) - minimum) / (maximum - minimum)).alias(column)
    ])

    return rescaled_df

def normalize_column(df: pl.DataFrame,
                     column: str) -> pl.DataFrame:
    """
    Normalize a column to have a mean of 0 and a standard deviation of 1.
    """
    mean = df[column].mean()
    std = df[column].std()

    normalized_df = df.with_columns([
        ((pl.col(column) - mean) / std).alias(column)
    ])

    return normalized_df

def filter_lexicon(lexicon: pl.DataFrame,
                   words: pl.Series,
                   word_column: str = "Word"
                   ) -> pl.DataFrame:
    """
    Filter a lexicon to only include the words in a list.
    """
    return lexicon.filter(pl.col(word_column).is_in(words))

def upos_to_swn(upos_tag: str) -> str:
    """
    Convert a Universal POS tag to a SentiWordNet POS tag.
    """
    if upos_tag in {"NOUN", "PROPN"}:
        return "n"
    elif upos_tag in {"VERB", "AUX"}:
        return "v"
    elif upos_tag in {"ADV"}:
        return "r"
    elif upos_tag in {"ADJ"}:
        return "a"
    else:
        return None