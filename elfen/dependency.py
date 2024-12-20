"""
This module contains functions to extract dependency features from the input text.
"""
import numpy as np
import polars as pl

from .configs.dependency_config import (
    CLEARNLP_DEPENDENCIES_CONFIG,
    UNIVERSAL_DEPENDENCIES_CONFIG,
)

# ---------------------- Dependency Tree Features ---------------------- #

def get_tree_width(data: pl.DataFrame,
                   backbone: str = 'spacy',
                   **kwargs: dict[str, str],
                   ) -> pl.DataFrame:
    """
    Extracts the dependency tree width of the input text.
    Tree width is the maximum number of nodes in the dependency
    tree of a token.

    Parameters
    ----------
    data : pl.DataFrame
        Input data.
    backbone : str
        The backbone used to extract the dependency tree.
    kwargs : dict
        Additional parameters to pass to the backbone.

    Returns
    -------
    pl.DataFrame
        The input data with the dependency tree width.
    """
    def get_width(nlp):
        return max([len(list(token.children)) for token in nlp])
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col('nlp').map_elements(
                lambda x: get_width(x)
            ).alias('tree_width')
        )
    elif backbone == 'stanza':
        print('Dependency tree width extraction is not yet implemented for Stanza.')

    return data

def get_tree_depth(data: pl.DataFrame,
                   backbone: str = 'spacy',
                   **kwargs: dict[str, str],
                   ) -> pl.DataFrame:
    """
    Extracts the dependency tree depth of the input text.
    Tree depth is the maximum distance of a token from the root
    of the dependency tree.
    If the input text contains multiple sentences, the average
    tree depth is calculated.

    Parameters
    ----------
    data : pl.DataFrame
        Input data.
    backbone : str
        The backbone used to extract the dependency tree.
    kwargs : dict
        Additional parameters to pass to the backbone.

    Returns
    -------
    pl.DataFrame
        The input data with the dependency tree depth.
    """
    def walk_tree(token, depth):
        if len(list(token.children)) == 0:
            return depth
        return max([walk_tree(child, depth + 1) for child in token.children])
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col('nlp').map_elements(
                lambda x: np.mean([walk_tree(sent.root, 0) for sent in x.sents])
            ).alias('tree_depth')
        )
    elif backbone == 'stanza':
        print('Dependency tree depth extraction is not yet implemented for Stanza.')

    return data

def get_tree_branching(data: pl.DataFrame,
                       backbone: str = 'spacy',
                       **kwargs: dict[str, str],
                       ) -> pl.DataFrame:
     """
     Extracts the dependency tree branching factor of the input text.
     The branching factor is the average number of children of a token.
    
     Parameters
     ----------
     data : pl.DataFrame
          Input data.
     backbone : str
          The backbone used to extract the dependency tree.
     kwargs : dict
          Additional parameters to pass to the backbone.
    
     Returns
     -------
     pl.DataFrame
          The input data with the dependency tree branching factor.
     """
     def get_branching(nlp):
          return sum([len(list(token.children)) for token in nlp]) / len(nlp)
     if backbone == 'spacy':
          data = data.with_columns(
                pl.col('nlp').map_elements(
                 lambda x: get_branching(x)
                ).alias('tree_branching')
          )
     elif backbone == 'stanza':
          print('Dependency tree branching factor extraction is not yet implemented for Stanza.')
    
     return data

def get_ramification_factor(data: pl.DataFrame,
                            backbone: str = 'spacy',
                            **kwargs: dict[str, str],
                            ) -> pl.DataFrame:
    """
    Extracts the dependency tree ramification factor of the input text.
    The ramification factor is the mean number of children per level.

    Parameters
    ----------
    data : pl.DataFrame
        Input data.
    backbone : str
        The backbone used to extract the dependency tree.
    kwargs : dict
        Additional parameters to pass to the backbone.

    Returns
    -------
    pl.DataFrame
        The input data with the dependency tree ramification factor.
    """
    def get_ramification(nlp):
        levels = {}
        for token in nlp:
            if token.dep not in levels:
                levels[token.dep] = 0
            levels[token.dep] += len(list(token.children))
        return sum(levels.values()) / len(levels)
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col('nlp').map_elements(
                lambda x: get_ramification(x)
            ).alias('ramification_factor')
        )
    elif backbone == 'stanza':
        print('Dependency tree ramification factor extraction is not yet implemented for Stanza.')

    return data

def get_n_noun_chunks(data: pl.DataFrame,
                      backbone: str = 'spacy',
                      **kwargs: dict[str, str],
                      ) -> pl.DataFrame:
    """
    Extracts the number of noun chunks in the input text.

    Parameters
    ----------
    data : pl.DataFrame
        Input data.
    backbone : str
        The backbone used to extract the dependency tree.
    kwargs : dict
        Additional parameters to pass to the backbone.

    Returns
    -------
    pl.DataFrame
        The input data with the number of noun chunks.
    """
    def get_n_chunks(nlp):
        return len(list(nlp.noun_chunks))
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col('nlp').map_elements(
                lambda x: get_n_chunks(x)
            ).alias('n_noun_chunks')
        )
    elif backbone == 'stanza':
        print('Number of noun chunks extraction is not yet implemented for Stanza.')

    return data

# ---------------------- Dependency Relation/Type Features ---------------------- #

def get_n_per_dependency_type(data: pl.DataFrame,
                              backbone: str = 'spacy',
                              language: str = 'en',
                              **kwargs: dict[str, str],
                              ) -> pl.DataFrame:
    """
    Extracts the frequency per dependency type in the input text.
    """
    if backbone == 'spacy':
        if language in ['en', 'de']:
            dependencies = CLEARNLP_DEPENDENCIES_CONFIG
        else:
            dependencies = UNIVERSAL_DEPENDENCIES_CONFIG

        for dep in dependencies:
            data = data.with_columns(
                pl.col('nlp').map_elements(
                    lambda x: len([token for token in x if token.dep_ == dep]),
                return_dtype=pl.UInt16
                ).alias(f'n_dependency_{dep}')
            )
    elif backbone == 'stanza':
        dependencies = UNIVERSAL_DEPENDENCIES_CONFIG
        for dep in dependencies:
            data = data.with_columns(
                pl.col('nlp').map_elements(
                    lambda x: len([token for sent in x.sentences for \
                                   token in sent.words if \
                                    token.deprel == dep]),
                return_dtype=pl.UInt16
                ).alias(f'n_dependency_{dep}')
            )
    
    return data

