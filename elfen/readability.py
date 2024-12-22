"""
This module contains functions to calculate readability scores from text
data. Readability scores are used to assess the readability, i.e., the
complexity, of a text.

The readability scores implemented in this module are:

- Total number of syllables
- Number of monosyllables
- Number of polysyllables
- Flesch Reading Ease
- Flesch-Kincaid Grade Level
- Automated Readability Index (ARI)
- Simple Measure of Gobbledygook (SMOG)
- Coleman-Liau Index (CLI)
- Gunning Fog Index
- LIX
- RIX
"""
import polars as pl

from .surface import (
    get_num_tokens,
    get_num_sentences,
    get_num_characters,
    get_num_long_words
)

def get_num_syllables(data: pl.DataFrame,
                      backbone: str = 'spacy',
                      **kwargs: dict[str, str],
                      ) -> pl.DataFrame:
        """
        Calculates the number of syllables in a text.

        Syllables are calculated using the syllables_count attribute
        of the tokens in the text data.

        Args:
            data (pl.DataFrame):
                A Polars DataFrame containing the text data.
            backbone (str):
                The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
                Not supported for Stanza backbone.

        Returns:
            data (pl.DataFrame):
                A Polars DataFrame containing the number of syllables
                in the text data.
                The number of syllables is stored in a new column
                named 'n_syllables'.
        """
        if backbone == 'spacy':
            data = data.with_columns(
                pl.col("nlp").map_elements(lambda x: sum(
                    [token._.syllables_count for token in x if 
                     token._.syllables_count != None]),
                     return_dtype=pl.UInt16
                    ).alias("n_syllables"),
            )
        elif backbone == 'stanza':
            raise NotImplementedError(
                "Not supported for Stanza backbone."
            )
        
        return data

def get_num_monosyllables(data: pl.DataFrame,
                          backbone: str = 'spacy',
                          **kwargs: dict[str, str],
                          ) -> pl.DataFrame:
    """
    Calculates the number of monosyllables in a text.

    Monosyllables are words with one syllable.

    Args:
        data (pl.DataFrame): APolars DataFrame containing the text data.
        backbone (str):
            The NLP library used to process the text data.
            Either 'spacy' or 'stanza'.
            Not supported for Stanza backbone.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the number of monosyllables
            in the text data.
            The number of monosyllables is stored in a new column
            named 'n_monosyllables'.
    """
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: sum(
                [1 for syllables_count in [
                    token._.syllables_count
                    for token
                    in x
                    if token._.syllables_count != None
                    ] if syllables_count == 1]
                    ), return_dtype=pl.UInt16
                ).alias("n_monosyllables"),
        )
    elif backbone == 'stanza':
        raise NotImplementedError(
            "Not supported for Stanza backbone."
        )

    return data

def get_num_polysyllables(data: pl.DataFrame,
                          backbone: str = 'spacy',
                          **kwargs: dict[str, str],
                          ) -> pl.DataFrame:
    """
    Calculates the number of polysyllables in a text.

    Polysyllables are words with three or more syllables.

    Args:
        data (pl.DataFrame): APolars DataFrame containing the text data.
        backbone (str):
            The NLP library used to process the text data.
            Either 'spacy' or 'stanza'.
            Not supported for Stanza backbone.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the number of polysyllables
            in the text data.
            The number of polysyllables is stored in a new column
            named 'n_polysyllables'.
    """
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: sum(
                [1 for syllables_count in [
                    token._.syllables_count
                    for token
                    in x
                    if token._.syllables_count != None
                    ] if syllables_count >= 3]
                    ), return_dtype=pl.UInt16
                ).alias("n_polysyllables"),
        )
    elif backbone == 'stanza':
        raise NotImplementedError(
            "Not supported for Stanza backbone."
        )

    return data

def get_flesch_reading_ease(data: pl.DataFrame,
                            backbone: str = 'spacy',
                            **kwargs: dict[str, str],
                            ) -> pl.DataFrame:
    """
    Calculates the Flesch Reading Ease score of a text.

    Args:
        data (pl.DataFrame): APolars DataFrame containing the text data.
        backbone (str):
            The NLP library used to process the text data.
            Either 'spacy' or 'stanza'.
            Not supported for Stanza backbone.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the Flesch Reading Ease score
            of the text data. The Flesch Reading Ease score is stored
            in a new column named 'flesch_reading_ease'.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_sentences' not in data.columns:
        data = get_num_sentences(data, backbone=backbone)
    if 'n_syllables' not in data.columns:
        data = get_num_syllables(data, backbone=backbone)

    data = data.with_columns(
        (206.835 - (1.015 * (pl.col("n_tokens") / \
                             pl.col("n_sentences"))) - \
         (84.6 * (pl.col("n_syllables") / pl.col("n_sentences")))
         ).alias("flesch_reading_ease"),
    )

    return data

def get_flesch_kincaid_grade(data: pl.DataFrame,
                            backbone: str = 'spacy',
                            **kwargs: dict[str, str],
                            ) -> pl.DataFrame:
    """
    Calculates the Flesch-Kincaid Grade Level of a text.

    Args:
        data (pl.DataFrame): APolars DataFrame containing the text data.
        backbone (str):
            The NLP library used to process the text data.
            Either 'spacy' or 'stanza'.
            Not supported for Stanza backbone.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the Flesch-Kincaid Grade Level
            of the text data. The Flesch-Kincaid Grade Level is stored
            in a new column named 'flesch_kincaid_grade'.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_sentences' not in data.columns:
        data = get_num_sentences(data, backbone=backbone)
    if 'n_syllables' not in data.columns:
        data = get_num_syllables(data, backbone=backbone)

    data = data.with_columns(
        (0.39 * (pl.col("n_tokens") / pl.col("n_sentences")) + \
         11.8 * (pl.col("n_syllables") / pl.col("n_sentences")) - 15.59
         ).alias("flesch_kincaid_grade"),
    )

    return data

def get_ari(data: pl.DataFrame,
            backbone: str = 'spacy',
            **kwargs: dict[str, str],
            ) -> pl.DataFrame:
    """
    Calculates the Automated Readability Index (ARI) of a text.

    Args:
        data (pl.DataFrame): APolars DataFrame containing the text data.
        backbone (str):
            The NLP library used to process the text data.
            Either 'spacy' or 'stanza'.
            Not supported for Stanza backbone.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the Automated Readability Index
            of the text data. The Automated Readability Index is stored
            in a new column named 'ari'.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_sentences' not in data.columns:
        data = get_num_sentences(data, backbone=backbone)
    if 'n_characters' not in data.columns:
        data = get_num_characters(data, backbone=backbone)

    data = data.with_columns(
        (4.71 * (pl.col("n_characters") / pl.col("n_tokens")) + \
         0.5 * (pl.col("n_tokens") / pl.col("n_sentences")) - 21.43
         ).alias("ari"),
    )

    return data

def get_smog(data: pl.DataFrame,
            backbone: str = 'spacy',
            **kwargs: dict[str, str],
            ) -> pl.DataFrame:
    """
    Calculates the Simple Measure of Gobbledygook (SMOG) of a text.

    Args:
        data (pl.DataFrame): APolars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
                Not supported for Stanza backbone.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the Simple Measure of
            Gobbledygook of the text data. The Simple Measure of
            Gobbledygook is stored in a new column named 'smog'.
    """
    if 'n_sentences' not in data.columns:
        data = get_num_sentences(data, backbone=backbone)
    if 'n_polysyllables' not in data.columns:
        data = get_num_polysyllables(data, backbone=backbone)

    data = data.with_columns(
        (1.0430 * (30 * pl.col("n_polysyllables") /  \
                   pl.col("n_sentences"))**0.5 + 3.1291
         ).alias("smog"),
    )

    return data

def get_cli(data: pl.DataFrame,
            backbone: str = 'spacy',
            **kwargs: dict[str, str],
            ) -> pl.DataFrame:
    """
    Calculates the Coleman-Liau Index (CLI) of a text.

    Args:
        data (pl.DataFrame): APolars DataFrame containing the text data.
        backbone (str):
            The NLP library used to process the text data.
            Either 'spacy' or 'stanza'.
            Not supported for Stanza backbone.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the Coleman-Liau Index
            of the text data. The Coleman-Liau Index is stored
            in a new column named 'cli'.
    """
    if 'n_sentences' not in data.columns:
        data = get_num_sentences(data, backbone=backbone)
    if 'n_characters' not in data.columns:
        data = get_num_characters(data, backbone=backbone)
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)

    data = data.with_columns(
        (0.0588 * (pl.col("n_characters") / pl.col("n_tokens") * 100) - \
         0.296 * (pl.col("n_sentences") / pl.col("n_tokens") * 100) - 15.8
         ).alias("cli"),
    )

    return data

def get_gunning_fog(data: pl.DataFrame,
                    backbone: str = 'spacy',
                    **kwargs: dict[str, str],
                    ) -> pl.DataFrame:
    """
    Calculates the Gunning Fog Index of a text.

    Args:
        data (pl.DataFrame): APolars DataFrame containing the text data.
        backbone (str):
            The NLP library used to process the text data.
            Either 'spacy' or 'stanza'.
            Not supported for Stanza backbone.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the Gunning Fog Index
            of the text data. The Gunning Fog Index is stored
            in a new column named 'gunning_fog'.
    """
    if 'n_sentences' not in data.columns:
        data = get_num_sentences(data, backbone=backbone)
    if 'n_polysyllables' not in data.columns:
        data = get_num_polysyllables(data, backbone=backbone)
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)

    data = data.with_columns(
        (0.4 * ((pl.col("n_tokens") / pl.col("n_sentences")) + \
                100 * (pl.col("n_polysyllables") / pl.col("n_tokens")))
                ).alias("gunning_fog"),
    )

    return data

def get_lix(data: pl.DataFrame,
            backbone: str = 'spacy',
            **kwargs: dict[str, str],
            ) -> pl.DataFrame:
    """
    Calculates the LIX of a text.

    Args:
        data (pl.DataFrame): APolars DataFrame containing the text data.
        backbone (str):
            The NLP library used to process the text data.
            Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the LIX of the text data.
            The LIX is stored in a new column named 'lix'.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_sentences' not in data.columns:
        data = get_num_sentences(data, backbone=backbone)
    if 'n_long_words' not in data.columns:
        data = get_num_long_words(data, backbone=backbone)

    data = data.with_columns(
        (pl.col("n_tokens") / pl.col("n_sentences") + \
         100 * pl.col("n_long_words") / pl.col("n_tokens")
         ).alias("lix"),
    )

    return data

def get_rix(data: pl.DataFrame,
            backbone: str = 'spacy',
            **kwargs: dict[str, str],
            ) -> pl.DataFrame:
    """
    Calculates the RIX of a text.

    Args:
        data (pl.DataFrame): APolars DataFrame containing the text data.
        backbone (str):
            The NLP library used to process the text data.
            Either 'spacy' or 'stanza'.
            Not supported for Stanza backbone.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the RIX of the text data.
            The RIX is stored in a new column named 'rix'.
    """
    if 'n_sentences' not in data.columns:
        data = get_num_sentences(data, backbone=backbone)
    if 'n_long_words' not in data.columns:
        data = get_num_long_words(data, backbone=backbone)

    data = data.with_columns(
        (pl.col("n_long_words") / pl.col("n_sentences")
         ).alias("rix"),
    )

    return data

