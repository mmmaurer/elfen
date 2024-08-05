import polars as pl

from .surface import (
    get_sequence_length,
    get_num_sentences,
    get_num_chars
)

def get_num_syllables(data: pl.DataFrame,
                        backbone: str = 'spacy'
                        ) -> pl.DataFrame:
        """
        Calculates the number of syllables in a text.
        """
        if backbone == 'spacy':
            data = data.with_columns(
                pl.col("nlp").map_elements(lambda x: sum(
                    [token._.syllables_count for token in x]),
                                         return_dtype=pl.UInt16
                                         ).alias("n_syllables"),
            )
        elif backbone == 'stanza':
            raise NotImplementedError(
                "Not implemented for Stanza backbone yet."
            )
        
        return data

def get_num_polysyllables(data: pl.DataFrame,
                          backbone: str = 'spacy'
                          ) -> pl.DataFrame:
    """
    Calculates the number of polysyllables in a text.
    Polysyllables are words with three or more syllables.
    """
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: sum(
                [1 for token in x if token._.syllables_count >= 3]),
                                        return_dtype=pl.UInt16
                                        ).alias("n_polysyllables"),
        )
    elif backbone == 'stanza':
        raise NotImplementedError(
            "Not implemented for Stanza backbone yet."
        )

    return data

def get_flesch_reading_ease(data: pl.DataFrame,
                            backbone: str = 'spacy'
                            ) -> pl.DataFrame:
    """
    Calculates the Flesch Reading Ease score of a text.
    """
    if 'n_tokens' not in data.columns:
        data = get_sequence_length(data, backbone=backbone)
    if 'n_sents' not in data.columns:
        data = get_num_sentences(data, backbone=backbone)
    if 'n_syllables' not in data.columns:
        data = get_num_syllables(data, backbone=backbone)

    data = data.with_columns(
        (206.835 - 1.015 * (pl.col("n_tokens") / pl.col("n_sents")) - \
         84.6 * (pl.col("n_syllables") / pl.col("n_sents"))
         ).alias("flesch_reading_ease"),
    )

    return data

def get_flesch_kincaid_grade(data: pl.DataFrame,
                            backbone: str = 'spacy'
                            ) -> pl.DataFrame:
    """
    Calculates the Flesch-Kincaid Grade Level of a text.
    """
    if 'n_tokens' not in data.columns:
        data = get_sequence_length(data, backbone=backbone)
    if 'n_sents' not in data.columns:
        data = get_num_sentences(data, backbone=backbone)
    if 'n_syllables' not in data.columns:
        data = get_num_syllables(data, backbone=backbone)

    data = data.with_columns(
        (0.39 * (pl.col("n_tokens") / pl.col("n_sents")) + \
         11.8 * (pl.col("n_syllables") / pl.col("n_sents")) - 15.59
         ).alias("flesch_kincaid_grade"),
    )

    return data

def get_ari(data: pl.DataFrame,
            backbone: str = 'spacy',
            ) -> pl.DataFrame:
    """
    Calculates the Automated Readability Index (ARI) of a text.
    """
    if 'n_tokens' not in data.columns:
        data = get_sequence_length(data, backbone=backbone)
    if 'n_sents' not in data.columns:
        data = get_num_sentences(data, backbone=backbone)
    if 'n_chars' not in data.columns:
        data = get_num_chars(data, backbone=backbone)

    data = data.with_columns(
        (4.71 * (pl.col("n_chars") / pl.col("n_tokens")) + \
         0.5 * (pl.col("n_tokens") / pl.col("n_sents")) - 21.43
         ).alias("ari"),
    )

    return data

def get_smog(data: pl.DataFrame,
            backbone: str = 'spacy',
            ) -> pl.DataFrame:
    """
    Calculates the Simple Measure of Gobbledygook (SMOG) of a text.
    """
    if 'n_sents' not in data.columns:
        data = get_num_sentences(data, backbone=backbone)
    if 'n_polysyllables' not in data.columns:
        data = get_num_polysyllables(data, backbone=backbone)

    data = data.with_columns(
        (1.0430 * (30 * pl.col("n_polysyllables") / pl.col("n_sents"))**0.5 + 3.1291
         ).alias("smog"),
    )

    return data

def get_cli(data: pl.DataFrame,
            backbone: str = 'spacy',
            ) -> pl.DataFrame:
    """
    Calculates the Coleman-Liau Index (CLI) of a text.
    """
    if 'n_sents' not in data.columns:
        data = get_num_sentences(data, backbone=backbone)
    if 'n_chars' not in data.columns:
        data = get_num_chars(data, backbone=backbone)
    if 'n_tokens' not in data.columns:
        data = get_sequence_length(data, backbone=backbone)

    data = data.with_columns(
        (0.0588 * (pl.col("n_chars") / pl.col("n_tokens") * 100) - \
         0.296 * (pl.col("n_sents") / pl.col("n_tokens") * 100) - 15.8
         ).alias("cli"),
    )

    return data

def get_gunning_fog(data: pl.DataFrame,
                    backbone: str = 'spacy',
                    ) -> pl.DataFrame:
    """
    Calculates the Gunning Fog Index of a text.
    """
    if 'n_sents' not in data.columns:
        data = get_num_sentences(data, backbone=backbone)
    if 'n_polysyllables' not in data.columns:
        data = get_num_polysyllables(data, backbone=backbone)
    if 'n_tokens' not in data.columns:
        data = get_sequence_length(data, backbone=backbone)

    data = data.with_columns(
        (0.4 * ((pl.col("n_tokens") / pl.col("n_sents")) + \
                100 * (pl.col("n_polysyllables") / pl.col("n_tokens")))
                ).alias("gunning_fog"),
    )

    return data