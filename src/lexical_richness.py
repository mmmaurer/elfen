import numpy as np
import polars as pl

from .surface import (
    get_num_tokens,
    get_num_types
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
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_lex_tokens' not in data.columns:
        data = get_num_lexical_tokens(data, backbone=backbone)
    
    data = data.with_columns(
        (pl.col("n_lex_tokens") / pl.col("n_tokens")
         ).alias("lemma_token_ratio"),
    )

    return data

def get_ttr(data: pl.DataFrame,
            backbone: str = 'spacy'
            ) -> pl.DataFrame:
    """
    Calculates the type-token ratio (TTR) of a text:
    N_types / N_tokens.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_types' not in data.columns:
        data = get_num_types(data)
    
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
    Calculates the number of hapax legomena in a text: words that occur only once.
    """
    if backbone == 'spacy':
        data = data.with_columns(
             pl.col("nlp").map_elements(lambda x: np.sum(
                  np.unique(np.array([token.text for token in x]),
                            return_counts=True)[1] == 1),
                            return_dtype=pl.UInt32).alias("n_hapax_legomena")
        )

    elif backbone == 'stanza':
        raise NotImplementedError("Hapax legomena calculation is not "
                                  "implemented for Stanza.")
    
    return data

def get_hapax_legomena_ratio(data: pl.DataFrame,
                            backbone: str = 'spacy'
                            ) -> pl.DataFrame:
    """
    Calculates the ratio of hapax legomena in a text:
    N_hapax_legomena / N_tokens.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_hapax_legomena' not in data.columns:
        data = get_n_hapax_legomena(data, backbone=backbone)
    
    data = data.with_columns(
        (pl.col("n_hapax_legomena") / pl.col("n_tokens")
         ).alias("hapax_legomena_ratio"),
    )

    return data

def get_hapax_legomenat_type_ratio(data: pl.DataFrame,
            backbone: str = 'spacy'
            ) -> pl.DataFrame:
    """
    Calculates the hapax legomena/type ratio of a text:
    N_hapax_legomena / N_types.
    """
    if 'n_types' not in data.columns:
        data = get_num_types(data, backbone=backbone)
    if 'n_hapax_legomena' not in data.columns:
        data = get_n_hapax_legomena(data, backbone=backbone)
    
    data = data.with_columns(
        (pl.col("n_hapax_legomena") / pl.col("n_types")
         ).alias("hapax_legomena_type_ratio"),
    )

    return data

def get_lexical_density(data: pl.DataFrame,
                        backbone: str = 'spacy'
                        ) -> pl.DataFrame:
    """
    Calculates the lexical density of a text:
    N_lex / N_tokens.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_lex_tokens' not in data.columns:
        data = get_num_lexical_tokens(data, backbone=backbone)
    
    data = data.with_columns(
        (pl.col("n_lex_tokens") / pl.col("n_tokens")
         ).alias("lexical_density"),
    )

    return data

