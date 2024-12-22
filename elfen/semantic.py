"""
This module provides functions to extract semantic features from text.

The WordNet features are collected using the `wn` package. It uses Open
Multilingual WordNet to provide information about words in different
languages.

If you are using the resources for research, please cite the original
authors of Open Multilingual WordNet. 

The semantic features implemented in this module are:
- Number of hedge words
- Ratio of hedge words
- Average number of synsets
- Average number of synsets per POS tag
- Number of words with a low number of synsets
- Number of words with a high number of synsets
- Number of words with a low number of synsets per POS tag
- Number of words with a high number of synsets per POS tag
"""
import polars as pl
import wn

from .surface import (
    get_num_tokens,
)
from .util import (
    upos_to_wn,
)

# ------------------------------------------------------------------- #
#                            Hedges                                   #
# ------------------------------------------------------------------- #

def load_hedges(hedges_file: str) -> list[str]:
    """
    Loads the hedges from the given file.

    Args:
        hedges_file (str): Path to the file containing the hedges.

    Returns:
        hedges (list[str]):
            List of hedge words.
    """
    with open(hedges_file, 'r') as f:
        raw = f.readlines()
        hedges = []
        for line in raw:
            if not line.startswith("%") and line.strip() != "\n" and \
                line.strip() != "":
                hedges.append(line.strip())
    
    return hedges

def get_num_hedges(data: pl.DataFrame,
                   lexicon: list[str],
                   text_column: str = 'text',
                   **kwargs: dict[str, str],
                   ) -> pl.DataFrame:
    """
    Calculates the number of hedges in a text.

    Args:
        data (pl.DataFrame): Polars DataFrame.
        lexicon (list[str]): List of hedges.
        text_column (str): Name of the column containing the text.

    Returns:
        data (pl.DataFrame):
            Polars DataFrame with the number of hedges.
    """
    def n_matches(string: str, patterns: list[str]) -> int:
        """
        Helper function.
        Returns the number of matches of the patterns in the string.
        """
        total_matches = 0
        for pattern in patterns:
            total_matches += string.count(pattern)
        return total_matches
    
    data = data.with_columns(
        pl.col(text_column).map_elements(lambda x: 
                                         n_matches(x, lexicon),
            return_dtype=pl.UInt16
            ).alias("n_hedges"),
    )
    
    return data

def get_hedges_ratio(data: pl.DataFrame,
                     lexicon: list[str],
                     text_column: str = 'text',
                     backbone: str = 'spacy',
                     **kwargs: dict[str, str],
                     ) -> pl.DataFrame:
    """
    Calculates the ratio of hedges in a text.

    Args:
        data (pl.DataFrame): Polars DataFrame.
        hedges (list[str]): List of hedges.
        text_column (str): Name of the column containing the text.
        backbone (str): NLP library used.

    Returns:
        data (pl.DataFrame):
            Polars DataFrame with the hedges ratio.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    
    if 'n_hedges' not in data.columns:
        data = get_num_hedges(data, lexicon, text_column)
    
    data = data.with_columns(
        (pl.col("n_hedges") / pl.col("n_tokens")
         ).alias("hedges_ratio"),
    )
    
    return data

# --------------------------------------------------------------------- #
#                       Ambiguity, Polysemy                             #
# --------------------------------------------------------------------- #

def get_synsets(data: pl.DataFrame,
                backbone: str = 'spacy',
                language: str = 'en',
                pos_tags: list[str] = [
                    'NOUN', 'VERB', 'ADJ', 'ADV'
                    ],
                **kwargs: dict[str, str],
                ) -> pl.DataFrame:
    """
    Calculates the number of synsets in a text per token.

    WordNet synsets serve as a proxy for the ambiguity/polysemy of a word.

    Args:
        data (pl.DataFrame): Polars DataFrame.
        backbone (str): NLP library used.
        language (str): Language of the text.
                Defaults to English ('en').
        pos_tags (list[str]): List of POS tags to consider.
                Defaults to lexical tokens.

    Returns:
        data (pl.DataFrame):
            Polars DataFrame with the numbers of synsets per text.
            The columns are named 'synsets' and 'synsets_{pos}'.
    """
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x:
                                        [len(wn.synsets(
                                            token.text,
                                            lang=language,
                                            pos=upos_to_wn(token.pos_)))
                                         for token in x
                                         if token.pos_ in pos_tags],
                return_dtype=pl.List(pl.Int64)).alias("synsets")
        )
        for pos in pos_tags:
            data = data.with_columns(
                pl.col("nlp").map_elements(lambda x:
                                            [len(wn.synsets(
                                                token.text,
                                                lang=language,
                                                pos=upos_to_wn(token.pos_)
                                                ))
                                             for token in x
                                             if token.pos_ == pos],
                    return_dtype=pl.List(pl.Int64)). \
                        alias(f"synsets_{pos.lower()}")
            )
    elif backbone == 'stanza':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x:
                                        [len(wn.synsets(
                                            word.text,
                                            lang=language,
                                            pos=upos_to_wn(word.upos)))
                                         for sent in x.sentences
                                         for word in sent.words
                                         if word.upos in pos_tags],
                return_dtype=pl.List(pl.Int64)).alias("synsets")
        )
        for pos in pos_tags:
            data = data.with_columns(
                pl.col("nlp").map_elements(lambda x:
                                            [len(wn.synsets(
                                                word.text,
                                                lang=language,
                                                pos=upos_to_wn(word.upos)))
                                             for sent in x.sentences
                                             for word in sent.words
                                             if word.upos == pos],
                    return_dtype=pl.List(pl.Int64)). \
                        alias(f"synsets_{pos.lower()}")
            )

    return data

def get_avg_num_synsets(data: pl.DataFrame,
                        backbone: str = 'spacy',
                        language: str = 'en',
                        pos_tags: list[str] = [
                            'NOUN', 'VERB', 'ADJ', 'ADV'
                            ],
                        **kwargs: dict[str, str],
                        ) -> pl.DataFrame:
    """
    Calculates the average number of synsets in a text.

    WordNet synsets serve as a proxy for the ambiguity/polysemy of a word.

    Args:
        data (pl.DataFrame): Polars DataFrame.
        backbone (str): NLP library used.
                'spacy' or 'stanza'.
        language (str): Language of the text.
                Defaults to English ('en').
        pos_tags (list[str]): List of POS tags to consider.
                Defaults to lexical tokens.

    Returns:
        data (pl.DataFrame):
            Polars DataFrame with the average number of synsets.
            The column is named 'avg_n_synsets'.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'synsets' not in data.columns:
        data = get_synsets(data, backbone=backbone,
                           language=language,
                           pos_tags=pos_tags)
    
    data = data.with_columns(
        pl.col("synsets").list.mean().alias("avg_n_synsets")
    )
    
    
    return data

def get_avg_num_synsets_per_pos(data: pl.DataFrame,
                                backbone: str = 'spacy',
                                language: str = 'en',
                                pos_tags: list[str] = [
                                    'NOUN', 'VERB', 'ADJ', 'ADV'
                                    ],
                                nan_value: float = 0,
                                **kwargs: dict[str, str],
                                ) -> pl.DataFrame:
    """
    Calculates the average number of synsets per POS in a text.

    Args:
        data (pl.DataFrame): Polars DataFrame.
        backbone (str): NLP library used.
                'spacy' or 'stanza'.
        language (str): Language of the text.
                Defaults to English ('en').
        pos_tags (list[str]): List of POS tags to consider.
                Defaults to lexical tokens.
        nan_value: Value to fill NaNs with.
                    Defaults to 0.

    Returns:
        data (pl.DataFrame):
            Polars DataFrame with the average number of synsets per POS.
            The columns are named 'avg_n_synsets_{pos}'.
    """
    if "synsets" not in data.columns:  # ensures all synsets are calculated
        data = get_synsets(data, backbone=backbone,
                           language=language,
                           pos_tags=pos_tags)
    for pos_tag in pos_tags:
        if backbone == 'spacy':
            data = data.with_columns(
                pl.col("synsets_" + pos_tag.lower()).list.mean(). \
                fill_nan(nan_value).fill_null(nan_value). \
                    alias(f"avg_n_synsets_{pos_tag.lower()}")
            )
        elif backbone == 'stanza':
            data = data.with_columns(
                pl.col("synsets_" + pos_tag.lower()).list.mean(). \
                fill_nan(nan_value).fill_null(nan_value). \
                    alias(f"avg_n_synsets_{pos_tag.lower()}")
            )

    return data

def get_num_low_synsets(data: pl.DataFrame,
                        backbone: str = 'spacy',
                        language: str = 'en',
                        pos_tags: list[str] = [
                            'NOUN', 'VERB', 'ADJ', 'ADV'
                            ],
                        threshold: int = 2,
                        **kwargs: dict[str, str],
                        ) -> pl.DataFrame:
    """
    Calculates the number of words with a low number of synsets in a text.

    Args:
        data (pl.DataFrame): Polars DataFrame.
        backbone (str): NLP library used.
                'spacy' or 'stanza'.
        language (str): Language of the text.
                Defaults to English ('en').
        pos_tags (list[str]): List of POS tags to consider.
                Defaults to lexical tokens.
        threshold: Threshold for the number of synsets.
                    Defaults to 2.

    Returns:
        data (pl.DataFrame):
            Polars DataFrame with the number of low synsets.
            The column is named 'n_low_synsets'.
    """
    if "synsets" not in data.columns:
        data = get_synsets(data, backbone=backbone,
                           language=language,
                           pos_tags=pos_tags)
    
    data = data.with_columns(
        pl.col("synsets").map_elements(lambda x:
                                       [
                                           1 for synset in x
                                           if synset <= threshold
                                       ],
        return_dtype=pl.List(pl.Int64)).list.len().alias("n_low_synsets")
    )


    return data

def get_num_high_synsets(data: pl.DataFrame,
                         backbone: str = 'spacy',
                         language: str = 'en',
                         pos_tags: list[str] = [
                             'NOUN', 'VERB', 'ADJ', 'ADV'
                             ],
                        threshold: int = 5,
                        **kwargs: dict[str, str],
                        ) -> pl.DataFrame:
    """
    Calculates the number of words with a high number of synsets in a text.

    Args:
        data (pl.DataFrame): Polars DataFrame.
        backbone (str): NLP library used.
                'spacy' or 'stanza'.
        language (str): Language of the text.
                Defaults to English ('en').
        pos_tags (list[str]): List of POS tags to consider.
                Defaults to lexical tokens.
        threshold: Threshold for the number of synsets.
                    Defaults to 5.

    Returns:
        data (pl.DataFrame):
            Polars DataFrame with the number of high synsets.
            The column is named 'n_high_synsets'.
    """
    if "synsets" not in data.columns:
        data = get_synsets(data, backbone=backbone,
                           language=language,
                           pos_tags=pos_tags)
    
    data = data.with_columns(
        pl.col("synsets").map_elements(lambda x:
                                       [
                                           1 for synset in x
                                           if synset >= threshold
                                       ],
        return_dtype=pl.List(pl.Int64)).list.len().alias("n_high_synsets")
    )

    return data

def get_low_synsets_per_pos(data: pl.DataFrame,
                            backbone: str = 'spacy',
                            language: str = 'en',
                            pos_tags: list[str] = [
                                'NOUN', 'VERB', 'ADJ', 'ADV'
                                ],
                            threshold: int = 2,
                            **kwargs: dict[str, str],
                            ) -> pl.DataFrame:
    """
    Calculates the number of words with a low number of synsets per POS in
    a text.

    Args:
        data (pl.DataFrame): Polars DataFrame.
        backbone (str): NLP library used.
                'spacy' or 'stanza'.
        language (str): Language of the text.
                Defaults to English ('en').
        pos_tags (list[str]): List of POS tags to consider.
                Defaults to lexical tokens.
        threshold: Threshold for the number of synsets.
                 Defaults to 2.
    
    Returns:
        data (pl.DataFrame):
            Polars DataFrame with the number of low synsets per POS.
            The columns are named 'n_low_synsets_{pos}'.
    """
    for pos_tag in pos_tags:
        if "synsets_" + pos_tag.lower() not in data.columns:
            data = get_synsets(data, backbone=backbone,
                               language=language,
                               pos_tags=[pos_tag])
        data = data.with_columns(
            pl.col("synsets_" + pos_tag.lower()).map_elements(
                lambda x: [1 for synset in x if synset <= threshold],
            return_dtype=pl.List(pl.Int64)).list.len(). \
                alias(f"n_low_synsets_{pos_tag.lower()}")
        )

    return data

def get_high_synsets_per_pos(data: pl.DataFrame,
                             backbone: str = 'spacy',
                             language: str = 'en',
                             pos_tags: list[str] = [
                                 'NOUN', 'VERB', 'ADJ', 'ADV'
                                 ],
                             threshold: int = 5,
                             **kwargs: dict[str, str],
                             ) -> pl.DataFrame:
    """
    Calculates the number of words with a high number of synsets per POS
    in a text.

    Args:
        data (pl.DataFrame): Polars DataFrame.
        backbone (str): NLP library used.
                'spacy' or 'stanza'.
        language (str): Language of the text.
                Defaults to English ('en').
        pos_tags (list[str]): List of POS tags to consider.
                Defaults to lexical tokens.
        threshold: Threshold for the number of synsets.
                 Defaults to 5.
    
    Returns:
        data (pl.DataFrame):
            Polars DataFrame with the number of high synsets per POS.
            The columns are named 'n_high_synsets_{pos}'.
    """
    for pos_tag in pos_tags:
        if "synsets_" + pos_tag.lower() not in data.columns:
            data = get_synsets(data, backbone=backbone,
                               language=language,
                               pos_tags=[pos_tag])
        data = data.with_columns(
            pl.col("synsets_" + pos_tag.lower()).map_elements(
                lambda x: [1 for synset in x if synset >= threshold],
            return_dtype=pl.List(pl.Int64)).list.len(). \
                alias(f"n_high_synsets_{pos_tag.lower()}")
        )

    return data

