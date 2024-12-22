"""
This module contains functions to extract named entity-related features
from text data.
"""
import polars as pl


ENT_TYPES = [
    'ORG', 'CARDINAL', 'DATE', 'GPE', 'PERSON', 'MONEY', 'PRODUCT', 'TIME',
    'PERCENT', 'WORK_OF_ART', 'QUANTITY', 'NORP', 'LOC', 'EVENT', 'ORDINAL',
    'FAC', 'LAW', 'LANGUAGE'
]

def get_num_entities(data: pl.DataFrame,
                     backbone: str = 'spacy',
                     **kwargs: dict[str, str],
                     ) -> pl.DataFrame:
    """
    Calculates the number of entities in the text data.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the number of entities in the
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

def get_num_per_entity_type(data: pl.DataFrame,
                            backbone: str = 'spacy',
                            ent_types: list = ENT_TYPES,
                            **kwargs: dict[str, str],
                            ) -> pl.DataFrame:
    """
    Calculates the number of entities per entity type in the text data.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
        ent_types: A list of entity types to calculate the number of
                entities for. Default is the list of entity types in the
                spaCy/stanza libraries.
    
    Returns:
        data (pl.DataFrame): 
            A Polars DataFrame containing the number of entities per 
            entity type in the text data.
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

