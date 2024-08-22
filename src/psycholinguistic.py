"""
This module contains functions for calculating psycholinguistic features
from text data.

If you are using this module, please cite the respective sources for the
norms used in the functions.

The norms used in this module are:
- Concreteness norms: Brysbaert, M., Warriner, A. B., & Kuperman, V. (2014).
  Concreteness ratings for 40 thousand generally known English word lemmas.
  Behavior Research Methods, 46(3), 904-911.
  
- Age of acquisition norms: Kuperman, V., Stadthagen-Gonzalez, H., & Brysbaert, M. (2012).
  Age-of-acquisition ratings for 30,000 English words.
  Behavior Research Methods, 45(4), 1191-1207.
  
- Word prevalence norms: Brysbaert, M., Mandera, P., McCormick, S. F., & Keuleers, E. (2019).
  Word prevalence norms for 62,000 English lemmas.
  Behavior Research Methods, 51(2), 467-479.

- Prevalence norms: Brysbaert, M., Mandera, P., McCormick, S. F., & Keuleers, E. (2019).
  Word prevalence norms for 62,000 English lemmas.
  Behavior Research Methods, 51(2), 467-479.
"""
import polars as pl

from .features import (
    get_lemmas,
)
from .surface import (
    get_num_tokens,
)
from .util import (
    filter_lexicon,
)


# ---------------------------------------------------- #
#            Abstractness/Concreteness                 #
# ---------------------------------------------------- #

def load_concreteness_norms(path: str,
                            ) -> pl.DataFrame:
    """
    Loads the concreteness norms dataset.

    Args:
    - path: The path to the concreteness norms dataset.

    Returns:
    - concreteness_norms: A Polars DataFrame containing the concreteness
                          norms dataset.
    """
    concreteness_norms = pl.read_excel(path)

    return concreteness_norms

def filter_concreteness_norms(concreness_norms: pl.DataFrame,
                              words: list
                              ) -> pl.DataFrame:
    """
    Filters the concreteness norms dataset by a list of words.

    Args:
    - concreness_norms: A Polars DataFrame containing the concreteness norms.
    - words: A list of words to filter the concreteness norms dataset.

    Returns:
    - filtered_concreteness_norms: A Polars DataFrame containing the filtered
                                   concreteness norms dataset.
    """
    filtered_concreteness_norms = concreness_norms.filter(pl.col("Word"). \
                                                          is_in(words))
    return filtered_concreteness_norms

def get_avg_concreteness(data: pl.DataFrame,
                         concreteness_norms: pl.DataFrame,
                         backbone: str = 'spacy',
                         nan_value: float = 0.0
                         ) -> pl.DataFrame:
    """
    Calculates the average concreteness score of a text.

    Args:
    - data: A Polars DataFrame containing the text data.
    - concreteness_norms: A Polars DataFrame containing the concreteness norms.
    - backbone: The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
    - nan_value: The value to fill NaN and null values with.
                    Defaults to 0.0.

    Returns:
    - data: A Polars DataFrame containing the average concreteness score
            of the text data.
            The average concreteness score is stored in a new column named
            'avg_concreteness'.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
    data = data.with_columns(
        pl.col("lemmas").map_elements(
            lambda x: filter_lexicon(lexicon=concreteness_norms,
                                     words=x,
                                     word_column="Word"). \
                select(pl.col("Conc.M")).mean().item(),
                return_dtype=pl.Float64
                ).fill_nan(nan_value).fill_null(nan_value). \
                    alias("avg_concreteness")
    )

    return data

def get_n_low_concreteness(data: pl.DataFrame,
                           concreteness_norms: pl.DataFrame,
                           threshold: float = 1.66,
                           backbone: str = 'spacy'
                           ) -> pl.DataFrame:
    """
    Calculates the number of low concreteness words in a text.

    Args:
    - data: A Polars DataFrame containing the text data.
    - concreteness_norms: A Polars DataFrame containing the concreteness norms.
    - threshold: The threshold for the low concreteness words.
                    Defaults to 1.66.
    - backbone: The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
    - data: A Polars DataFrame containing the number of low concreteness words
            in the text data.
            The number of low concreteness words is stored in a new column
            named 'n_low_concreteness'.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
    data = data.with_columns(
        pl.col("lemmas").map_elements(
            lambda x: filter_lexicon(lexicon=concreteness_norms,
                                     words=x,
                                     word_column="Word"). \
                select(pl.col("Conc.M")).filter(pl.col("Conc.M") < threshold). \
                    count().item(),
                return_dtype=pl.Int64).alias("n_low_concreteness")
    )

    return data

def get_n_high_concreteness(data: pl.DataFrame,
                            concreteness_norms: pl.DataFrame,
                            backbone: str = 'spacy',
                            threshold: float = 3.33,
                            ) -> pl.DataFrame:
    """
    Calculates the number of high concreteness words in a text.

    Args:
    - data: A Polars DataFrame containing the text data.
    - concreteness_norms: A Polars DataFrame containing the concreteness norms.
    - threshold: The threshold for the high concreteness words.
                    Defaults to 3.33.
    - backbone: The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
    - data: A Polars DataFrame containing the number of high concreteness words
            in the text data.
            The number of high concreteness words is stored in a new column
            named 'n_high_concreteness'.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
    data = data.with_columns(
        pl.col("lemmas").map_elements(
            lambda x: filter_lexicon(lexicon=concreteness_norms,
                                     words=x,
                                     word_column="Word"). \
                select(pl.col("Conc.M")).filter(pl.col("Conc.M") > threshold). \
                    count().item(),
                return_dtype=pl.Int64).alias("n_high_concreteness")
    )

    return data

# ---------------------------------------------------- #
#            Age of Acquisition                        #
# ---------------------------------------------------- #

def load_aoa_norms(path: str,
                     ) -> pl.DataFrame:
    """
    Loads the age of acquisition norms dataset.

    Args:
    - path: The path to the age of acquisition norms dataset.

    Returns:
    - aoa_norms: A Polars DataFrame containing the age of acquisition norms
                 dataset.
    """
    aoa_norms = pl.read_excel(path)
    
    return aoa_norms

def get_avg_aoa(data: pl.DataFrame,
                aoa_norms: pl.DataFrame,
                backbone: str = 'spacy',
                nan_value: float = 0.0
                ) -> pl.DataFrame:
    """
    Calculates the average age of acquisition score of a text.

    Args:
    - data: A Polars DataFrame containing the text data.
    - aoa_norms: A Polars DataFrame containing the age of acquisition norms.
    - backbone: The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
    - data: A Polars DataFrame containing the average age of acquisition score
            of the text data.
            The average age of acquisition score is stored in a new column named
            'avg_aoa'.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
    data = data.with_columns(
        pl.col("lemmas").map_elements(
            lambda x: filter_lexicon(lexicon=aoa_norms,
                                     words=x,
                                     word_column="Word"). \
                select(pl.col("Rating.Mean")).mean().item(),
                return_dtype=pl.Float64
                ).fill_nan(nan_value).fill_null(nan_value). \
                    alias("avg_aoa")
    )

    return data

def get_n_low_aoa(data: pl.DataFrame,
                    aoa_norms: pl.DataFrame,
                    backbone: str = 'spacy',
                    threshold: float = 10.0,
                    ) -> pl.DataFrame:
        """
        Calculates the number of low age of acquisition words in a text.

        Args:
        - data: A Polars DataFrame containing the text data.
        - aoa_norms: A Polars DataFrame containing the age of acquisition norms.
        - backbone: The NLP library used to process the text data.
                    Either 'spacy' or 'stanza'. 
        - threshold: The threshold for the low age of acquisition words.
                    Defaults to 10.0.

        Returns:
        - data: A Polars DataFrame containing the number of low age of acquisition
                words in the text data.
                The number of low age of acquisition words is stored in a new column
                named 'n_low_aoa'.
        """
        if "lemmas" not in data.columns:
            data = get_lemmas(data, backbone=backbone)
        data = data.with_columns(
            pl.col("lemmas").map_elements(
                lambda x: filter_lexicon(lexicon=aoa_norms,
                                         words=x,
                                         word_column="Word"). \
                    select(pl.col("Rating.Mean")
                           ).filter(pl.col("Rating.Mean") < threshold). \
                        count().item(),
                    return_dtype=pl.Int64).alias("n_low_aoa")
        )
    
        return data

def get_n_high_aoa(data: pl.DataFrame,
                    aoa_norms: pl.DataFrame,
                    threshold: float = 10.0,
                    backbone: str = 'spacy'
                    ) -> pl.DataFrame:
        """
        Calculates the number of high age of acquisition words in a text.

        Args:
        - data: A Polars DataFrame containing the text data.
        - aoa_norms: A Polars DataFrame containing the age of acquisition norms.
        - threshold: The threshold for the high age of acquisition words.
                    Defaults to 10.0.

        Returns:
        - data: A Polars DataFrame containing the number of high age of acquisition
                words in the text data.
                The number of high age of acquisition words is stored in a new column
                named 'n_high_aoa'.
        """
        if "lemmas" not in data.columns:
            data = get_lemmas(data, backbone=backbone)
        data = data.with_columns(
            pl.col("lemmas").map_elements(
                lambda x: filter_lexicon(lexicon=aoa_norms,
                                         words=x,
                                         word_column="Word"). \
                    select(pl.col("Rating.Mean")).filter(
                        pl.col("Rating.Mean") > threshold
                        ).count().item(),
                    return_dtype=pl.Int64).alias("n_high_aoa")
        )
    
        return data

# ---------------------------------------------------- #
#                Word Prevalence                       #
# ---------------------------------------------------- #

def load_prevalence_norms(path: str,
                          ) -> pl.DataFrame:
    """
    Loads the word prevalence norms dataset.

    Args:
    - path: The path to the word prevalence norms dataset.

    Returns:
    - prevalence_norms: A Polars DataFrame containing the word prevalence
                        norms dataset
    """
    prevalence_norms = pl.read_excel(path)

    return prevalence_norms

def get_avg_prevalence(data: pl.DataFrame,
                       prevalence_norms: pl.DataFrame,
                       backbone: str = 'spacy',
                       nan_value: float = 0.0
                       ) -> pl.DataFrame:
    """
    Calculates the average prevalence score of a text.

    Args:
    - data: A Polars DataFrame containing the text data.
    - prevalence_norms: A Polars DataFrame containing the word prevalence
                        norms.
    - backbone: The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
    - nan_value: The value to fill NaN and null values with.
                    Defaults to 0.0.

    Returns:
    - data: A Polars DataFrame containing the average prevalence score
            of the text data.
            The average prevalence score is stored in a new column named
            'avg_prevalence'.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
    data = data.with_columns(
        pl.col("lemmas").map_elements(
            lambda x: filter_lexicon(lexicon=prevalence_norms,
                                     words=x,
                                     word_column="Word"). \
                select(pl.col("Prevalence")).mean().item(),
                return_dtype=pl.Float64
                ).fill_nan(nan_value).fill_null(nan_value). \
                    alias("avg_prevalence")
    )

    return data

def get_n_low_prevalence(data: pl.DataFrame,
                         prevalence_norms: pl.DataFrame,
                         threshold: float = 1.0,
                         backbone: str = 'spacy'
                         ) -> pl.DataFrame:
    """
    Calculate the number of low prevalence words in a text.

    Args:
    - data: A Polars DataFrame containing the text data.
    - prevalence_norms: A Polars DataFrame containing the word prevalence
                        norms.

    Returns:
    - data: A Polars DataFrame containing the number of low prevalence words
            in the text data.
            The number of low prevalence words is stored in a new column named
            'n_low_prevalence'.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
    data = data.with_columns(
        pl.col("lemmas").map_elements(
            lambda x: filter_lexicon(lexicon=prevalence_norms,
                                     words=x,
                                     word_column="Word"). \
                select(pl.col("Prevalence")).filter(
                    pl.col("Prevalence") < threshold). \
                    count().item(),
                return_dtype=pl.Int64).alias("n_low_prevalence")
    )

    return data

def get_n_high_prevalence(data: pl.DataFrame,
                          prevalence_norms: pl.DataFrame,
                          backbone: str = 'spacy',
                          threshold: float = 1.0,
                          ) -> pl.DataFrame:
    """
    Calculate the number of high prevalence words in a text.

    Args:
    - data: A Polars DataFrame containing the text data.
    - prevalence_norms: A Polars DataFrame containing the word prevalence
                        norms.
    - backbone: The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
    - threshold: The threshold for the high prevalence words.
                    Defaults to 1.0.

    Returns:
    - data: A Polars DataFrame containing the number of high prevalence words
            in the text data.
            The number of high prevalence words is stored in a new column named
            'n_high_prevalence'.
    """
    if "lemmas" not in data.columns:
        data = get_lemmas(data, backbone=backbone)
    data = data.with_columns(
        pl.col("lemmas").map_elements(
            lambda x: filter_lexicon(lexicon=prevalence_norms,
                                     words=x,
                                     word_column="Word"). \
                select(pl.col("Prevalence")).filter(
                    pl.col("Prevalence") > threshold). \
                    count().item(),
                return_dtype=pl.Int64).alias("n_high_prevalence")
    )

    return data

