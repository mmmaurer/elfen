"""
This module contains functions to calculate various lexical richness
metrics from text data.

The lexical richness metrics implemented in this module are:

- Lemma/Token Ratio: 
    The ratio of the number of lemmas to the number of tokens in the text.
- Type/Token Ratio: 
    The ratio of the number of types to the number of tokens in the text.
- Root Type/Token Ratio: 
    The ratio of the number of types to the square root of the number of
    tokens in the text.
- Corrected Type/Token Ratio: 
    The ratio of the number of types to the square root of twice the 
    number of tokens in the text.
- Herdan's C: 
    The logarithm of the number of types divided by the logarithm of the
    number of tokens.
- Summer's TTR:
    The logarithm of the logarithm of the number of types divided by the
    logarithm of the logarithm of the number of tokens.
- Dugast's Uber Index:
    The square of the logarithm of the number of tokens divided by the
    logarithm of the number of tokens minus the logarithm of the number
    of types.
- Maas' TTR:
    The number of tokens minus the number of types divided
    by the square of the logarithm of the number of types.
- Number of Hapax Legomena:
    The number of words that occur only once in the text.
- Number of Global Token Hapax Legomena:
    The number of words that occur only once in the entire corpus.
- Number of Global Lemma Hapax Legomena:
    The number of lemmas that occur only once in the entire corpus.
- Number of Hapax Dislegomena:
    The number of words that occur only once or twice in the text.
- Number of Global Token Hapax Dislegomena:
    The number of words that occur only once or twice in the entire
    corpus.
- Number of Global Lemma Hapax Dislegomena:
    The number of lemmas that occur only once or twice in the entire
    corpus.
- Sichel's S:
    The number of hapax dislegomena divided by the number of types in the
    text.
- Global Sichel's S:
    The number of global token hapax dislegomena divided by the number of
    types in the text.
- Lexical Density:
    The ratio of the number of lexical tokens to the number of tokens in
    the text.
- Giroud's Index:
    The number of types divided by the square root of the number of tokens
    in the text.
- Measure of Textual Lexical Diversity (MTLD)
- Hypergeometric Distribution Diversity (HD-D)
- Moving-Average Type-Token Ratio (MATTR)
- Mean Segmental Type-Token Ratio (MSTTR)
- Yule's K
- Simpson's D
- Herdan's Vm
"""
from collections import Counter

import numpy as np
import polars as pl
from scipy.stats import hypergeom

from .surface import (
    get_num_tokens,
    get_num_types,
    get_token_freqs,
    get_global_token_frequencies,
    get_global_lemma_frequencies,
    get_num_lemmas
)
from .pos import (
    get_num_lexical_tokens,
)
from .preprocess import (
    get_tokens,
)

def get_lemma_token_ratio(data: pl.DataFrame,
                          backbone: str = 'spacy',
                          **kwargs: dict[str, str],
                          ) -> pl.DataFrame:
    """
    Calculates the lemma/token ratio of a text:

    N_lemmas / N_tokens.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the lemma/token ratio of the
            text data. The lemma/token ratio is stored in a new column
            named 'lemma_token_ratio'.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_lemmas' not in data.columns:
        data = get_num_lemmas(data, backbone=backbone)
    
    data = data.with_columns(
        (pl.col("n_lemmas") / pl.col("n_tokens")
         ).alias("lemma_token_ratio"),
    )

    return data

def get_ttr(data: pl.DataFrame,
            backbone: str = 'spacy',
            **kwargs: dict[str, str],
            ) -> pl.DataFrame:
    """
    Calculates the type-token ratio (TTR) of a text:

    N_types / N_tokens.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the type-token ratio of the text
            data. The type-token ratio is stored in a new column named
            'ttr'.
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
             backbone: str = 'spacy',
             **kwargs: dict[str, str],
             ) -> pl.DataFrame:
    """
    Calculates the root type-token ratio (RTTR) of a text:

    N_types / sqrt(N_tokens).

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the root type-token ratio of the
            text data. The root type-token ratio is stored in a new column
            named 'rttr'.
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
             backbone: str = 'spacy',
             **kwargs: dict[str, str],
             ) -> pl.DataFrame:
    """
    Calculates the corrected type-token ratio (CTTR) of a text:

    N_types / sqrt(2*N_tokens).

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                        Either 'spacy' or 'stanza'.
    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the corrected type-token ratio
            of the text data. The corrected type-token ratio is stored in
            a new column named 'cttr'.
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
                 backbone: str = 'spacy',
                 **kwargs: dict[str, str],
                 ) -> pl.DataFrame:
    """
    Calculates the Herdan's C of a text:

    log(N_types) / log(N_tokens).

    Note that the convention is to fill NaNs with 1 as log(1) = 0.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
    
    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing Herdan's C of the text data.
            Herdan's C is stored in a new column named 'herdan_c'.
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
                    backbone: str = 'spacy',
                    **kwargs: dict[str, str],
                    ) -> pl.DataFrame:
    """
    Calculates the Summer's TTR of a text:

    log(log(N_types)) / log(log(N_tokens)).

    Note that the convention is to fill NaNs with 1 as log(1) = 0.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the Summer's TTR of the text
            data. Summer's TTR is stored in a new column named
            'summer_index'.
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

def get_dugast_u(data: pl.DataFrame,
                  backbone: str = 'spacy',
                  **kwargs: dict[str, str],
                  ) -> pl.DataFrame:
    """
    Calculates the Dougast's Uber index of a text:
    log(N_tokens)^2 / (log(N_tokens) - log(N_types)).

    Note that the convention is to fill NaNs with 1 as log(1) = 0.
    For texts with N_types = N_tokens, this will output Inf as division by
    0 is not defined.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame): A Polars DataFrame containing Dugast's Uber
        index of the text data. Dugast's Uber index is stored in a new
        column named 'dugast_u'.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_types' not in data.columns:
        data = get_num_types(data, backbone=backbone)
    
    data = data.with_columns(
        (pl.col("n_tokens").log()**2 / (pl.col("n_tokens").log() - \
                                       pl.col("n_types").log())
         ).fill_nan(1).alias("dugast_u")
         # convention to fill NaNs with 1 as log(1) = 0 and
         # division by 0 is not defined.
    )

    return data

def get_maas_index(data: pl.DataFrame,
                   backbone: str = 'spacy',
                   **kwargs: dict[str, str],
                   ) -> pl.DataFrame:
    """
    Calculates the Maas' TTR of a text:
    (N_tokens - N_types) / log(N_types)^2.

    Note that the convention is to fill NaNs with 1 as log(1) = 0.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing Maas' TTR of the text data.
            Maas' TTR is stored in a new column named 'maas_index'.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_types' not in data.columns:
        data = get_num_types(data, backbone=backbone)
    
    data = data.with_columns(
        ((pl.col("n_tokens") - pl.col("n_types")) / \
            pl.col("n_types").log()**2 
         ).fill_nan(1).alias("maas_index")
         # convention to fill NaNs with 1 as log(1) = 0 and
         # division by 0 is not defined.
    )

    return data

def get_n_hapax_legomena(data: pl.DataFrame,
                         backbone: str = 'spacy',
                         **kwargs: dict[str, str],
                         ) -> pl.DataFrame:
    """
    Calculates the number of hapax legomena in a text: words that occur
    only once.

    TODO: Add global hapax legomena calculation.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the number of hapax legomena in
            the text data. The number of hapax legomena is stored in a new
            column named 'n_hapax_legomena'.
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

def get_n_global_token_hapax_legomena(data: pl.DataFrame,
                                      backbone: str = 'spacy',
                                      **kwargs: dict[str, str],
                                      ) -> pl.DataFrame:
    """
    Calculates the number of global hapax legomena in a text: words that
    occur only once in the entire corpus.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
    
    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the number of global hapax
            legomena in the text data. The number of global hapax legomena
            is stored in a new column named 'n_global_hapax_legomena'.
    """
    token_freqs = get_global_token_frequencies(data, backbone=backbone)
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: len(
                [token for token in x if token_freqs[token.text] == 1]),
                return_dtype=pl.UInt32). \
                    alias("n_global_token_hapax_legomena")
        )
    elif backbone == 'stanza':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: len(
                [token for sent in x.sentences for token in sent.tokens
                 if token_freqs[token.text] == 1]),
                return_dtype=pl.UInt32). \
                    alias("n_global_token_hapax_legomena")
        )

    return data

def get_n_global_lemma_hapax_legomena(data: pl.DataFrame,
                                      backbone: str = 'spacy',
                                      **kwargs: dict[str, str],
                                      ) -> pl.DataFrame:
    """
    Calculates the number of global hapax legomena in a text: lemmas that
    occur only once in the entire corpus.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the number of global hapax
            legomena in the text data. The number of global hapax legomena
            is stored in a new column named 'n_global_lemma_hapax_legomena'.
    """
    lemma_freqs = get_global_lemma_frequencies(data, backbone=backbone)
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: len(
                [token.lemma_ for token in x if 
                 lemma_freqs[token.lemma_] == 1]),
                return_dtype=pl.UInt32). \
                    alias("n_global_lemma_hapax_legomena")
        )
    elif backbone == 'stanza':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: len(
                [token.lemma for sent in x.sentences for 
                 token in sent.tokens
                 if lemma_freqs[token.lemma] == 1]),
                return_dtype=pl.UInt32). \
                    alias("n_global_lemma_hapax_legomena")
        )

    return data

def get_n_hapax_dislegomena(data: pl.DataFrame,
                            backbone: str = 'spacy',
                            **kwargs: dict[str, str],
                            ) -> pl.DataFrame:
    """
    Calculates the number of hapax dislegomena in a text: words that occur
    only once or twice.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the number of hapax dislegomena
            in the text data. The number of hapax dislegomena is stored in
            a new column named 'n_hapax_dislegomena'.
    """
    if backbone == 'spacy':
        data = data.with_columns(
             pl.col("nlp").map_elements(lambda x: np.sum(
                  np.unique(np.array([token.text for token in x]),
                            return_counts=True)[1] <= 2),
                            return_dtype=pl.UInt32). \
                                alias("n_hapax_dislegomena")
        )

    elif backbone == 'stanza':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: np.sum(
                np.unique(np.array([token.text 
                                    for sent 
                                    in x.sentences 
                                    for token in sent.tokens]),
                          return_counts=True)[1] <= 2),
                          return_dtype=pl.UInt32). \
                            alias("n_hapax_dislegomena")
        )
    
    return data

def get_n_global_token_hapax_dislegomena(data: pl.DataFrame,
                                       backbone: str = 'spacy',
                                       **kwargs: dict[str, str],
                                       ) -> pl.DataFrame:
    """
    Calculates the number of global hapax dislegomena in a text: words that
    occur only once or twice in the entire corpus.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                        Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the number of global hapax
            dislegomena in the text data. The number of global hapax
            dislegomena is stored in a new column named
            'n_global_token_hapax_dislegomena'.
    """
    token_freqs = get_global_token_frequencies(data, backbone=backbone)

    if backbone == 'spacy':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: len(
                [token for token in x if token_freqs[token.text] <= 2]),
                return_dtype=pl.UInt32). \
                    alias("n_global_token_hapax_dislegomena")
        )
    elif backbone == 'stanza':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: len(
                [token for sent in x.sentences for token in sent.tokens
                 if token_freqs[token.text] <= 2]),
                return_dtype=pl.UInt32). \
                    alias("n_global_token_hapax_dislegomena")
        )

    return data

def get_n_global_lemma_hapax_dislegomena(data: pl.DataFrame,
                                       backbone: str = 'spacy',
                                       **kwargs: dict[str, str],
                                       ) -> pl.DataFrame:
    """
    Calculates the number of global hapax dislegomena in a text: lemmas that
    occur only once or twice in the entire corpus.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                        Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the number of global hapax
            dislegomena in the text data. The number of global hapax
            dislegomena is stored in a new column named
            'n_global_lemma_hapax_dislegomena'.
    """
    lemma_freqs = get_global_lemma_frequencies(data, backbone=backbone)

    if backbone == 'spacy':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: len(
                [token.lemma_ for token in x if 
                 lemma_freqs[token.lemma_] <= 2]),
                return_dtype=pl.UInt32). \
                    alias("n_global_lemma_hapax_dislegomena")
        )
    elif backbone == 'stanza':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: len(
                [token.lemma for sent in x.sentences for 
                 token in sent.tokens
                 if lemma_freqs[token.lemma] <= 2]),
                return_dtype=pl.UInt32). \
                    alias("n_global_lemma_hapax_dislegomena")
        )

    return data

def get_sichel_s(data: pl.DataFrame,
                 backbone: str = 'spacy',
                 **kwargs: dict[str, str],
                 ) -> pl.DataFrame:
    """
    Calculates the Sichel's S of a text:
    N_hapax_dislegomena / N_types.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
    
    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing Sichel's S of the text data.
            Sichel's S is stored in a new column named 'sichel_s'.
    """
    if 'n_types' not in data.columns:
        data = get_num_types(data, backbone=backbone)
    if 'n_hapax_dislegomena' not in data.columns:
        data = get_n_hapax_dislegomena(data, backbone=backbone)

    data = data.with_columns(
        (pl.col("n_hapax_dislegomena") / pl.col("n_types")
         ).alias("sichel_s"),
    )

    return data

def get_global_sichel_s(data: pl.DataFrame,
                        backbone: str = 'spacy',
                        **kwargs: dict[str, str],
                        ) -> pl.DataFrame:
    """
    Calculates the global Sichel's S of a text:
    N_global_token_hapax_dislegomena / N_types.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                        Either 'spacy' or 'stanza'.
    
    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the global Sichel's S of the
            text data. The global Sichel's S is stored in a new column
            named 'global_sichel_s'.
    """
    if 'n_types' not in data.columns:
        data = get_num_types(data, backbone=backbone)
    if 'n_global_token_hapax_dislegomena' not in data.columns:
        data = get_n_global_token_hapax_dislegomena(data,
                                                    backbone=backbone)

    data = data.with_columns(
        (pl.col("n_global_token_hapax_dislegomena") / pl.col("n_types")
         ).alias("global_sichel_s"),
    )

    return data

def get_lexical_density(data: pl.DataFrame,
                        backbone: str = 'spacy',
                        **kwargs: dict[str, str],
                        ) -> pl.DataFrame:
    """
    Calculates the lexical density of a text:

    N_lex / N_tokens.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the lexical density of the text
            data. The lexical density is stored in a new column named
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
                     backbone: str = 'spacy',
                     **kwargs: dict[str, str],
                     ) -> pl.DataFrame:
    """
    Calculates the Giroud's index of a text:

    N_types / sqrt(N_tokens).

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing Giroud's C of the text data.
            Giroud's C is stored in a new column named 'giroud_c'.
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
             threshold: float = 0.72,
             backbone: str = 'spacy',
             **kwargs: dict[str, str],
             ) -> pl.DataFrame:
    """
    Calculates the Measure of Textual Lexical Diversity (MTLD) of a text.

    For reference https://link.springer.com/article/10.3758/BRM.42.2.381 

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
        threshold: The threshold value for the MTLD.
                 The default value is 0.72.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the MTLD of the text data.
            The MTLD is stored in a new column named 'mtld'.
    """
    def sub_mtld(tokens: list[str],
                 forward: bool = True,
                 threshold: float = 0.72
                 ) -> float:
        """
        Calculate the MTLD of a text using a forward or backward approach.
        For reference https://link.springer.com/article/10.3758/BRM.42.2.381 
        """
        if not forward:
            tokens = tokens[::-1]
        
        unique_tokens = set()
        current_ttr = 1.0
        factors = 0.0
        token_count = 0

        for i, token in enumerate(tokens):
            token_count += 1
            unique_tokens.add(token)
            current_ttr = len(unique_tokens) / token_count

            if i == len(tokens) - 1 and current_ttr >= threshold:
                factors += (current_ttr - 1) / (threshold - 1)
            elif current_ttr < threshold:
                factors += 1
                # Reset
                unique_tokens = set()
                current_ttr = 1.0
                token_count = 0

        return len(tokens) / factors if factors != 0 else len(tokens)
            
    if 'tokens' not in data.columns:
        data = get_tokens(data, backbone=backbone)
    
    data = data.with_columns(
        pl.col("tokens").map_elements(lambda x: (
            sub_mtld(x, threshold=threshold) + \
                sub_mtld(x, forward=False, threshold=threshold)
            ) / 2.0, return_dtype=pl.Float32).alias("mtld")
    )

    return data


def get_hdd(data: pl.DataFrame,
            backbone: str = 'spacy',
            draws: int = 42,
            **kwargs: dict[str, str],
            ) -> pl.DataFrame:
    """
    Calculates the Hypergeometric Distribution Diversity (HD-D) of a text.

    The default number of draws is 42. We note, however, that this value
    should be smaller than the number of tokens in the text and thus will
    need to be adjusted for most short texts. A number of draws that is
    too large will result in NaN values.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
        draws: The number of draws for the HDD. The default value is 42.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the HD-D of the text data. 
            The HD-D is stored in a new column named 'hdd'.
    """
    def hdd(tokens: list[str],
            draws: int = 42,
            ) -> float:
        """
        Calculate the HDD of a text.
        """
        freqs = Counter(tokens)
        n_types = len(freqs)
        n_tokens = len(tokens)
        hdd = 0.0

        for freq in freqs.values():
            hdd += hypergeom.pmf(freq, n_tokens, n_types, draws)
        
        return hdd
    
    if 'tokens' not in data.columns:
        data = get_tokens(data, backbone=backbone)
    
    data = data.with_columns(
        pl.col("tokens").map_elements(lambda x: hdd(x, draws=draws),
                                      return_dtype=pl.Float32).alias("hdd")
    )

    return data

def get_mattr(data: pl.DataFrame,
              backbone: str = 'spacy',
              window_size: int = 5,
              **kwargs: dict[str, str],
              ) -> pl.DataFrame:
    """
    Calculates the Moving-Average Type-Token Ratio (MATTR) of a text.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
        window_size (int):
            The size of the window for the MATTR calculation.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the MATTR of the text data.
            The MATTR is stored in a new column named 'mattr'.
    """
    def mattr(tokens: list[str],
              window_size: int = 5,
              ) -> float:
        """
        Calculate the MATTR of a text.
        """
        n_types = []
        n_tokens = []
        for i in range(0, len(tokens)):
            window = tokens[i:i+window_size]
            n_types.append(len(set(window)))
            n_tokens.append(len(window))
        
        return np.mean(n_types) / np.mean(n_tokens)
    
    if 'tokens' not in data.columns:
        data = get_tokens(data, backbone=backbone)
    
    data = data.with_columns(
        pl.col("tokens").map_elements(
            lambda x: mattr(x,
                            window_size=window_size),
                            return_dtype=pl.Float32).alias("mattr")
    )

    return data

def get_msttr(data: pl.DataFrame,
              backbone: str = 'spacy',
              window_size: int = 5,
              discard: bool = False,
              **kwargs: dict[str, str],
              ) -> pl.DataFrame:
    """
    Calculates the Mean Segmental Type-Token Ratio (MSTTR) of a text.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str):
            The NLP library used to process the text data. Either 'spacy'
            or 'stanza'.
        window_size (int):
            The size of the window for the MSTTR calculation.
        discard (bool):
            Whether to discard the last window if it is not complete.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the MSTTR of the text data.
            The MSTTR is stored in a new column named 'msttr'.
    """
    def msttr(tokens: list[str],
              window_size: int = 5,
              discard: bool = False,
              ) -> float:
        """
        Calculate the MSTTR of a text.
        """
        scores = []

        for i in range(0, len(tokens), window_size):
            window = tokens[i:i+window_size]
            n_types = len(set(window))
            n_tokens = len(window)
            scores.append(n_types / n_tokens)
        
        # Discard the last window if it is not complete
        if discard and len(tokens) % window_size != 0:
            scores = scores[:-1]

        return np.mean(scores)
    if 'tokens' not in data.columns:
        data = get_tokens(data, backbone=backbone)
    
    data = data.with_columns(
        pl.col("tokens"). \
            map_elements(lambda x: msttr(x,
                                         window_size=window_size,
                                         discard=discard),
                                         return_dtype=pl.Float32). \
                                            alias("msttr")
    )

    return data

def get_yule_k(data: pl.DataFrame,
               backbone: str = 'spacy',
               **kwargs: dict[str, str],
               ) -> pl.DataFrame:
    """
    Calculates the Yule's K of a text.
    Yule's K is a characteristic of the vocabulary richness of a text.
    It is calculated as:

    K = 10^4 * (Σ(V(i,N) * (i/n)^2) - n) / n^2
    = 10^4 * ((Σ(V(i,N) * (i^2/n^4)) - (1/n))

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing Yule's K of the text data.
            Yule's K is stored in a new column named 'yule_k'.
    """
    def inner_sum(x: dict[str, int]) -> float:
        """
        Calculate the inner sum of the Yule's K formula, i.e.:
        (Σ(V(i,N) * (i^2/n^4))
        """
        counts = Counter(x.values())
        # gathering n from counts to streamline the calculation
        n = sum(counts.values())
        n_power_4 = n ** 4  # Precompute to avoid redundant calculations

        inner = sum(count * (i ** 2 / n_power_4) for i, count in \
                    counts.items())

        return inner
    
    # get the number of tokens
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    # calculate frequency of each token per text
    if 'token_freqs' not in data.columns:
        data = get_token_freqs(data, backbone=backbone)

    data = data.with_columns(
        (pl.lit(10**4) * \
        pl.col("token_freqs").map_elements(lambda x: inner_sum(x),
                                           return_dtype=pl.Float32) - \
        (1 / pl.col("n_tokens"))).alias("yule_k")
    )

    return data


def get_simpsons_d(data: pl.DataFrame,
                   backbone: str = 'spacy',
                   **kwargs: dict[str, str],
                   ) -> pl.DataFrame:
    """
    Calculates the Simpson's D of a text.
    
    D = Σ(V(i,N) * (i/n) * ((i-1)/(n-1)))

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing Simpson's D of the text data.
            Simpson's D is stored in a new column named 'simpsons_d'.
    """
    def simpsons_d(x: dict[str, int]) -> float:
        """
        Calculate the Simpson's D of a text.
        """
        counts = Counter(x.values())
        n = sum(counts.values())
        n_inv = 1 / n  # Precompute 1 / n
        n_minus_1_inv = 1 / (n - 1)  # Precompute 1 / (n - 1)

        d = sum(count * i * n_inv * (i - 1) * n_minus_1_inv for \
                i, count in counts.items())

        return d
    if 'token_freqs' not in data.columns:
        data = get_token_freqs(data, backbone=backbone)
    
    data = data.with_columns(
        pl.col("token_freqs").map_elements(lambda x: simpsons_d(x),
                                           return_dtype=pl.Float32). \
                                            alias("simpsons_d")
    )

    return data
    

def get_herdan_v(data: pl.DataFrame,
                 backbone: str = 'spacy',
                 **kwargs: dict[str, str],
                 ) -> pl.DataFrame:
    """
    Calculates the Herdan's Vm of a text:

    Vm^2 = K + (1/N) - (1/V(N))
    Vm = sqrt(K + (1/N) - (1/V(N)))

    where K is Yule's K, N is the number of tokens, and V(N) is the number
    of types:

    K = Σ(V(i,N) * (i/n)^2)

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
    
    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing Herdan's V of the text data. 
            Herdan's V is stored in a new column named 'herdan_v'.
    """
    if not 'n_tokens' in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if not 'n_types' in data.columns:
        data = get_num_types(data, backbone=backbone)
    if not 'yule_k' in data.columns:
        data = get_yule_k(data, backbone=backbone)

    data = data.with_columns(
        (pl.col("yule_k") + (1 / pl.col("n_tokens")) - \
         (1 / pl.col("n_types")).sqrt()
        ).alias("herdan_v")
    )

    return data

