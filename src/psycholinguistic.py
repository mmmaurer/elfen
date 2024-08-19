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
    Load the concreteness norms dataset.
    """
    concreteness_norms = pl.read_excel(path)

    return concreteness_norms

def filter_concreteness_norms(concreness_norms: pl.DataFrame,
                              words: list
                              ) -> pl.DataFrame:
    """
    Filter the concreteness norms dataset by a list of words.
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
    Calculate the average concreteness score of a text.
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
    Calculate the number of low concreteness words in a text.
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
                            threshold: float = 3.33,
                            backbone: str = 'spacy'
                            ) -> pl.DataFrame:
    """
    Calculate the number of high concreteness words in a text.
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

def get_low_concreteness_ratio(data: pl.DataFrame,
                               concreteness_norms: pl.DataFrame,
                               threshold: float = 1.66,
                               backbone: str = 'spacy',
                               nan_value: float = 0.0
                               ) -> pl.DataFrame:
    """
    Calculate the ratio of low concreteness words in a text.
    """
    if "n_low_concreteness" not in data.columns:
        data = get_n_low_concreteness(data, concreteness_norms,
                                      threshold=threshold, backbone=backbone)
    if "n_tokens" not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    data = data.with_columns(
        (pl.col("n_low_concreteness") / pl.col("n_tokens")). \
            fill_nan(nan_value).alias("low_concreteness_ratio")
    )

    return data

def get_high_concreteness_ratio(data: pl.DataFrame,
                                concreteness_norms: pl.DataFrame,
                                threshold: float = 3.33,
                                backbone: str = 'spacy',
                                nan_value: float = 0.0
                                ) -> pl.DataFrame:
    """
    Calculate the ratio of high concreteness words in a text.
    """
    if "n_high_concreteness" not in data.columns:
        data = get_n_high_concreteness(data, concreteness_norms,
                                       threshold=threshold, backbone=backbone)
    if "n_tokens" not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    data = data.with_columns(
        (pl.col("n_high_concreteness") / pl.col("n_tokens")). \
            fill_nan(nan_value).alias("high_concreteness_ratio")
    )

    return data

# ---------------------------------------------------- #
#            Age of Acquisition                        #
# ---------------------------------------------------- #

def load_aoa_norms(path: str,
                     ) -> pl.DataFrame:
     """
     Load the age of acquisition norms dataset.
     """
     aoa_norms = pl.read_excel(path)
    
     return aoa_norms

def get_avg_aoa(data: pl.DataFrame,
                aoa_norms: pl.DataFrame,
                backbone: str = 'spacy',
                nan_value: float = 0.0
                ) -> pl.DataFrame:
    """
    Calculate the average age of acquisition score of a text.
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
                    threshold: float = 10.0,
                    backbone: str = 'spacy'
                    ) -> pl.DataFrame:
        """
        Calculate the number of low age of acquisition words in a text.
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
        Calculate the number of high age of acquisition words in a text.
        """
        if "lemmas" not in data.columns:
            data = get_lemmas(data, backbone=backbone)
        data = data.with_columns(
            pl.col("lemmas").map_elements(
                lambda x: filter_lexicon(lexicon=aoa_norms,
                                         words=x,
                                         word_column="Word"). \
                    select(pl.col("Rating.Mean")).filter(pl.col("Rating.Mean") > threshold). \
                        count().item(),
                    return_dtype=pl.Int64).alias("n_high_aoa")
        )
    
        return data

def get_low_aoa_ratio(data: pl.DataFrame,
                      aoa_norms: pl.DataFrame,
                      threshold: float = 10.0,
                      backbone: str = 'spacy',
                      nan_value: float = 0.0
                      ) -> pl.DataFrame:
    """
    Calculate the ratio of low age of acquisition words in a text.
    """
    if "n_low_aoa" not in data.columns:
        data = get_n_low_aoa(data, aoa_norms,
                             threshold=threshold, backbone=backbone)
    if "n_tokens" not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    data = data.with_columns(
        (pl.col("n_low_aoa") / pl.col("n_tokens")). \
            fill_nan(nan_value).alias("low_aoa_ratio")
    )

    return data

def get_high_aoa_ratio(data: pl.DataFrame,
                       aoa_norms: pl.DataFrame,
                       threshold: float = 10.0,
                       backbone: str = 'spacy',
                       nan_value: float = 0.0
                       ) -> pl.DataFrame:
    """
    Calculate the ratio of high age of acquisition words in a text.
    """
    if "n_high_aoa" not in data.columns:
        data = get_n_high_aoa(data, aoa_norms,
                              threshold=threshold, backbone=backbone)
    if "n_tokens" not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    data = data.with_columns(
        (pl.col("n_high_aoa") / pl.col("n_tokens")). \
            fill_nan(nan_value).alias("high_aoa_ratio")
    )

    return data

# ---------------------------------------------------- #
#                Word Prevalence                       #
# ---------------------------------------------------- #

def load_prevalence_norms(path: str,
                          ) -> pl.DataFrame:
    """
    Load the word prevalence norms dataset.
    """
    prevalence_norms = pl.read_excel(path)

    return prevalence_norms

def get_avg_prevalence(data: pl.DataFrame,
                       prevalence_norms: pl.DataFrame,
                       backbone: str = 'spacy',
                       nan_value: float = 0.0
                       ) -> pl.DataFrame:
    """
    Calculate the average prevalence score of a text.
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
                          threshold: float = 1.0,
                          backbone: str = 'spacy'
                          ) -> pl.DataFrame:
    """
    Calculate the number of high prevalence words in a text.
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

def get_low_prevalence_ratio(data: pl.DataFrame,
                             prevalence_norms: pl.DataFrame,
                             threshold: float = 1.0,
                             backbone: str = 'spacy',
                             nan_value: float = 0.0
                             ) -> pl.DataFrame:
    """
    Calculate the ratio of low prevalence words in a text.
    """
    if "n_low_prevalence" not in data.columns:
        data = get_n_low_prevalence(data, prevalence_norms,
                                   threshold=threshold, backbone=backbone)
    if "n_tokens" not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    data = data.with_columns(
        (pl.col("n_low_prevalence") / pl.col("n_tokens")). \
            fill_nan(nan_value).alias("low_prevalence_ratio")
    )

    return data

def get_high_prevalence_ratio(data: pl.DataFrame,
                              prevalence_norms: pl.DataFrame,
                              threshold: float = 1.0,
                              backbone: str = 'spacy',
                              nan_value: float = 0.0
                              ) -> pl.DataFrame:
    """
    Calculate the ratio of high prevalence words in a text.
    """
    if "n_high_prevalence" not in data.columns:
        data = get_n_high_prevalence(data, prevalence_norms,
                                    threshold=threshold, backbone=backbone)
    if "n_tokens" not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    data = data.with_columns(
        (pl.col("n_high_prevalence") / pl.col("n_tokens")). \
            fill_nan(nan_value).alias("high_prevalence_ratio")
    )

    return data

