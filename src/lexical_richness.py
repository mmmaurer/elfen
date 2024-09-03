"""
This module contains functions to calculate various lexical richness
metrics from text data.
"""
import numpy as np
import polars as pl

from .surface import (
    get_num_tokens,
    get_num_types,
    get_num_lemmas
)
from .pos import (
    get_num_lexical_tokens,
)

def get_lemma_token_ratio(data: pl.DataFrame,
                            backbone: str = 'spacy'
                            ) -> pl.DataFrame:
    """
    Calculates the lemma/token ratio of a text:
    N_lemmas / N_tokens.

    Args:
    - data: A Polars DataFrame containing the text data.
    - backbone: The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
    - data: A Polars DataFrame containing the lemma/token ratio of the
            text data.
            The lemma/token ratio is stored in a new column named
            'lemma_token_ratio'.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_lemmas' not in data.columns:
        data = get_num_lexical_tokens(data, backbone=backbone)
    
    data = data.with_columns(
        (pl.col("n_lemmas") / pl.col("n_tokens")
         ).alias("lemma_token_ratio"),
    )

    return data

def get_ttr(data: pl.DataFrame,
            backbone: str = 'spacy'
            ) -> pl.DataFrame:
    """
    Calculates the type-token ratio (TTR) of a text:
    N_types / N_tokens.

    Args:
    - data: A Polars DataFrame containing the text data.
    - backbone: The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
    - data: A Polars DataFrame containing the type-token ratio of the
            text data.
            The type-token ratio is stored in a new column named 'ttr'.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_types' not in data.columns:
        data = get_num_types(data, backbone=backbone)
    
    data = data.with_columns(
        (pl.col("n_types") / pl.col("n_tokens")).alias("ttr"),
    )

    return data

def get_rttr(data: pl.DataFrame,
             backbone: str = 'spacy'
             ) -> pl.DataFrame:
    """
    Calculates the root type-token ratio (RTTR) of a text:
    N_types / sqrt(N_tokens).
    Args:
    - data: A Polars DataFrame containing the text data.
    - backbone: The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
    Returns:
    - data: A Polars DataFrame containing the root type-token ratio
            of the text data.
            The root type-token ratio is stored in a new column named
            'rttr'.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_types' not in data.columns:
        data = get_num_types(data, backbone=backbone)
    
    data = data.with_columns(
        (
            pl.col("n_types") / pl.col("n_tokens") **0.5
         ).alias("rttr"),
    )

    return data

def get_cttr(data: pl.DataFrame,
             backbone: str = 'spacy'
             ) -> pl.DataFrame:
    """
    Calculates the corrected type-token ratio (CTTR) of a text:
    N_types / sqrt(2*N_tokens).
    Args:
    - data: A Polars DataFrame containing the text data.
    - backbone: The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
    Returns:
    - data: A Polars DataFrame containing the corrected type-token ratio
            of the text data.
            The corrected type-token ratio is stored in a new column named
            'cttr'.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_types' not in data.columns:
        data = get_num_types(data, backbone=backbone)
    
    data = data.with_columns(
        (
            pl.col("n_types") / ((2 * pl.col("n_tokens")) ** 0.5)
        ).alias("cttr"),
    )

    return data

def get_herdan_c(data: pl.DataFrame,
                 backbone: str = 'spacy'
                 ) -> pl.DataFrame:
    """
    Calculates the Herdan's C of a text:
    log(N_types) / log(N_tokens).

    Args:
    - data: A Polars DataFrame containing the text data.
    - backbone: The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
    
    Returns:
    - data: A Polars DataFrame containing the Herdan's C of the text data.
            The Herdan's C is stored in a new column named 'herdan_c'.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_types' not in data.columns:
        data = get_num_types(data, backbone=backbone)
    
    data = data.with_columns(
        (
            pl.col("n_types").log() / pl.col("n_tokens").log()
         ).fill_nan(1).alias("herdan_c")
         # convention to fill NaNs with 1 as log(1) = 0 and 
         # division by 0 is not defined.
    )

    return data

def get_summer_index(data: pl.DataFrame,
                    backbone: str = 'spacy'
                    ) -> pl.DataFrame:
    """
    Calculates the Summer's TTR of a text:
    log(log(N_types)) / log(log(N_tokens)).

    Args:
    - data: A Polars DataFrame containing the text data.
    - backbone: The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
    - data: A Polars DataFrame containing the Summer's TTR of the text data.
            The Summer's TTR is stored in a new column named 'summer_index'.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_types' not in data.columns:
        data = get_num_types(data, backbone=backbone)
    
    data = data.with_columns(
        (pl.col("n_types").log().log() / pl.col("n_tokens").log().log()
         ).fill_nan(1).alias("summer_index")
         # convention to fill NaNs with 1 as log(1) = 0 and
         # division by 0 is not defined.
    )

    return data

def get_dougast_u(data: pl.DataFrame,
                    backbone: str = 'spacy'
                    ) -> pl.DataFrame:
    """
    Calculates the Dougast's Uber index of a text:
    log(N_types)^2 / (N_tokens - N_types).

    Args:
    - data: A Polars DataFrame containing the text data.
    - backbone: The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
    - data: A Polars DataFrame containing the Dougast's Uber index of the
            text data.
            The Dougast's Uber index is stored in a new column named
            'dougast_u'.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_types' not in data.columns:
        data = get_num_types(data, backbone=backbone)
    
    data = data.with_columns(
        (pl.col("n_types").log()**2 / (pl.col("n_tokens") - pl.col("n_types"))
         ).fill_nan(1).alias("dougast_u")
         # convention to fill NaNs with 1 as log(1) = 0 and
         # division by 0 is not defined.
    )

    return data

def get_maas_index(data: pl.DataFrame,
                    backbone: str = 'spacy'
                    ) -> pl.DataFrame:
    """
    Calculates the Maas' TTR of a text:
    (N_tokens - N_types) / log(N_types)^2.

    Args:
    - data: A Polars DataFrame containing the text data.
    - backbone: The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
    - data: A Polars DataFrame containing the Maas' TTR of the text data.
            The Maas' TTR is stored in a new column named 'maas_index'.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_types' not in data.columns:
        data = get_num_types(data, backbone=backbone)
    
    data = data.with_columns(
        ((pl.col("n_tokens") - pl.col("n_types")) / pl.col("n_types").log()**2 
         ).fill_nan(1).alias("maas_index")
         # convention to fill NaNs with 1 as log(1) = 0 and
         # division by 0 is not defined.
    )

    return data

def get_n_hapax_legomena(data: pl.DataFrame,
                        backbone: str = 'spacy'
                        ) -> pl.DataFrame:
    """
    Calculates the number of hapax legomena in a text: words that occur
    only once.

    Args:
    - data: A Polars DataFrame containing the text data.
    - backbone: The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
    - data: A Polars DataFrame containing the number of hapax legomena in the
            text data.
            The number of hapax legomena is stored in a new column named
            'n_hapax_legomena'.
    """
    if backbone == 'spacy':
        data = data.with_columns(
             pl.col("nlp").map_elements(lambda x: np.sum(
                  np.unique(np.array([token.text for token in x]),
                            return_counts=True)[1] == 1),
                            return_dtype=pl.UInt32).alias("n_hapax_legomena")
        )

    elif backbone == 'stanza':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: np.sum(
                np.unique(np.array([token.text 
                                    for sent 
                                    in x.sentences 
                                    for token in sent.tokens]),
                          return_counts=True)[1] == 1),
                          return_dtype=pl.UInt32).alias("n_hapax_legomena")
        )
    
    return data

def get_lexical_density(data: pl.DataFrame,
                        backbone: str = 'spacy'
                        ) -> pl.DataFrame:
    """
    Calculates the lexical density of a text:
    N_lex / N_tokens.

    Args:
    - data: A Polars DataFrame containing the text data.
    - backbone: The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
    - data: A Polars DataFrame containing the lexical density of the
            text data.
            The lexical density is stored in a new column named
            'lexical_density'.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_lexical_tokens' not in data.columns:
        data = get_num_lexical_tokens(data, backbone=backbone)
    
    data = data.with_columns(
        (pl.col("n_lexical_tokens") / pl.col("n_tokens")
         ).alias("lexical_density"),
    )

    return data

def get_giroud_index(data: pl.DataFrame,
                    backbone: str = 'spacy'
                    ) -> pl.DataFrame:
    """
    Calculates the Giroud's index of a text:
    N_types / sqrt(N_tokens).

    Args:
    - data: A Polars DataFrame containing the text data.
    - backbone: The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
    - data: A Polars DataFrame containing the Giroud's C of the text data.
            The Giroud's C is stored in a new column named 'giroud_c'.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_types' not in data.columns:
        data = get_num_types(data, backbone=backbone)
    
    data = data.with_columns(
        (pl.col("n_types") / pl.col("n_tokens").sqrt()
         ).alias("giroud_index"),
    )

    return data

def get_mtld(data: pl.DataFrame,
            threshold: int = 0.72
            ) -> pl.DataFrame:
    """
    Calculates the Measure of Textual Lexical Diversity (MTLD) of a text.

    Args:
    - data: A Polars DataFrame containing the text data.
    - threshold: The threshold value for the MTLD.
                 The default value is 0.72.

    Returns:
    - data: A Polars DataFrame containing the MTLD of the text data.
            The MTLD is stored in a new column named 'mtld'.
    """
    pass
    # TODO, for reference https://link.springer.com/article/10.3758/BRM.42.2.381


def get_hdd(data: pl.DataFrame,
            threshold: int = 0.72
            ) -> pl.DataFrame:
    """
    Calculates the Hypergeometric Distribution D (HDD) of a text.

    Args:
    - data: A Polars DataFrame containing the text data.
    - threshold: The threshold value for the HDD.
                 The default value is 0.72.

    Returns:
    - data: A Polars DataFrame containing the HDD of the text data.
            The HDD is stored in a new column named 'hdd'.
    """
    pass
    # TODO, for reference https://link.springer.com/article/10.3758/BRM.42.2.381

def get_mattr(data: pl.DataFrame,
            threshold: int = 0.72
            ) -> pl.DataFrame:
    """
    Calculates the Moving-Average Type-Token Ratio (MATTR) of a text.

    Args:
    - data: A Polars DataFrame containing the text data.
    - threshold: The threshold value for the MATTR.
                 The default value is 0.72.

    Returns:
    - data: A Polars DataFrame containing the MATTR of the text data.
            The MATTR is stored in a new column named 'mattr'.
    """
    pass
    # TODO

def get_msttr(data: pl.DataFrame,
            threshold: int = 0.72
            ) -> pl.DataFrame:
    """
    Calculates the Mean Segmental Type-Token Ratio (MSTTR) of a text.

    Args:
    - data: A Polars DataFrame containing the text data.
    - threshold: The threshold value for the MSTTR.
                 The default value is 0.72.

    Returns:
    - data: A Polars DataFrame containing the MSTTR of the text data.
            The MSTTR is stored in a new column named 'msttr'.
    """
    pass
    # TODO