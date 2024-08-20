"""
This module contains functions to extract named entity-related features
from text data.
"""
import polars as pl

from .surface import (
    get_num_tokens,
    get_num_sentences
)

ENT_TYPES = [
    'ORG', 'CARDINAL', 'DATE', 'GPE', 'PERSON', 'MONEY', 'PRODUCT', 'TIME',
    'PERCENT', 'WORK_OF_ART', 'QUANTITY', 'NORP', 'LOC', 'EVENT', 'ORDINAL',
    'FAC', 'LAW', 'LANGUAGE'
]

def get_num_entities(data: pl.DataFrame,
                     backbone: str = 'spacy'
                     ) -> pl.DataFrame:
    """
    Calculates the number of entities in the text data.

    Args:
    - data: A Polars DataFrame containing the text data.
    - backbone: The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
    - data: A Polars DataFrame containing the number of entities in the
            text data.
    """
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: len(x.ents),
                                       return_dtype=pl.UInt16
                                       ).alias("n_entities"),
        )
    elif backbone == 'stanza':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: len(x.entities),
                                       return_dtype=pl.UInt16
                                       ).alias("n_entities"),
        )
    
    return data

def get_entity_ratio(data: pl.DataFrame,
                     backbone: str = 'spacy'
                     ) -> pl.DataFrame:
        """
        Calculates the ratio of entities to tokens in the text data.

        Args:
        - data: A Polars DataFrame containing the text data.
        - backbone: The NLP library used to process the text data.
                    Either 'spacy' or 'stanza'.
        
        Returns:
        - data: A Polars DataFrame containing the entity ratio in the
                text data.
        """
        if "n_tokens" not in data.columns:
            data = get_num_tokens(data, backbone)
        
        if "n_entities" not in data.columns:
            data = get_num_entities(data, backbone)
        
        data = data.with_columns(
            (
                 pl.col("n_entities") / pl.col("n_tokens")
            ).alias("entity_ratio")
        )
        return data

def get_entities_per_sentence(data: pl.DataFrame,
                              backbone: str = 'spacy'
                              ) -> pl.DataFrame:
    """
    Calculates the average number of entities per sentence in the text data.

    Args:
    - data: A Polars DataFrame containing the text data.
    - backbone: The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
    - data: A Polars DataFrame containing the average number of entities
            per sentence in the text data.
    """
    if "n_sentences" not in data.columns:
        data = get_num_sentences(data, backbone)
    if "n_entities" not in data.columns:
        data = get_num_entities(data, backbone)
    
    data = data.with_columns(
        (
             pl.col("n_entities") / pl.col("n_sentences")
        ).alias("entities_per_sentence")
    )
    return data

def get_num_per_entity_type(data: pl.DataFrame,
                            backbone: str = 'spacy',
                            ent_types: list = ENT_TYPES
                            ) -> pl.DataFrame:
    """
    Calculates the number of entities per entity type in the text data.

    Args:
    - data: A Polars DataFrame containing the text data.
    - backbone: The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
    - ent_types: A list of entity types to calculate the number of entities for.
                 Default is the list of entity types in the spaCy/stanza
                 libraries.
    
    Returns:
    - data: A Polars DataFrame containing the number of entities per entity type
            in the text data.
    """
    if backbone == 'spacy':
        for ent_type in ent_types:
            data = data.with_columns(
                pl.col("nlp").map_elements(lambda x: len(
                    [ent for ent in x.ents if ent.label_ == ent_type]),
                    return_dtype=pl.UInt16
                    ).alias(f"n_{ent_type.lower()}"),
            )
    elif backbone == 'stanza':
        for ent_type in ent_types:
            data = data.with_columns(
                pl.col("nlp").map_elements(lambda x: len(
                    [ent for ent in x.entities if ent.type == ent_type]),
                    return_dtype=pl.UInt16
                    ).alias(f"n_{ent_type.lower()}"),
            )
    
    return data

def get_entity_type_ratio(data: pl.DataFrame,
                          backbone: str = 'spacy',
                          ent_types: list = ENT_TYPES
                          ) -> pl.DataFrame:
    """
    Calculates the ratio of entities per entity type to tokens in the
    text data.

    Args:
    = data: A Polars DataFrame containing the text data.
    - backbone: The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
    - data: A Polars DataFrame containing the entity type ratio in the
            text data.
    """
    if "n_tokens" not in data.columns:
         data = get_num_tokens(data, backbone)
    
    for ent_type in ent_types:
         if f"n_{ent_type.lower()}" not in data.columns:
               data = get_num_per_entity_type(data, backbone, ent_types)
         data = data.with_columns(
               (
                    pl.col(f"n_{ent_type.lower()}") / pl.col("n_tokens")
               ).alias(f"{ent_type.lower()}_ratio")
         )
    return data

def get_entity_type_per_sentence(data: pl.DataFrame,
                                 backbone: str = 'spacy',
                                 ent_types: list = ENT_TYPES
                                 ) -> pl.DataFrame:
        """
        Calculates the average number of entities per entity type per sentence
        in the text data.

        Args:
        - data: A Polars DataFrame containing the text data.
        - backbone: The NLP library used to process the text data.
                    Either 'spacy' or 'stanza'.
        - ent_types: A list of entity types to calculate the number of entities
                     for.
                     Default is the list of entity types in the spaCy/stanza
                     libraries.

        Returns:
        - data: A Polars DataFrame containing the average number of entities
                per entity type per sentence in the text data.
        """
        if "n_sentences" not in data.columns:
            data = get_num_sentences(data, backbone)
        if "n_entities" not in data.columns:
            data = get_num_entities(data, backbone)
        
        for ent_type in ent_types:
            if f"n_{ent_type.lower()}" not in data.columns:
                data = get_num_per_entity_type(data, backbone, ent_types)
            data = data.with_columns(
                (
                     pl.col(f"n_{ent_type.lower()}") / pl.col("n_sentences")
                ).alias(f"{ent_type.lower()}_per_sentence")
            )
        return data

