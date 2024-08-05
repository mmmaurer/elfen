import polars as pl

from .surface import (
    get_sequence_length,
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
    """
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x: len(x.ents),
                                       return_dtype=pl.UInt16
                                       ).alias("n_entities"),
        )
    elif backbone == 'stanza':
        raise NotImplementedError(
            "Not implemented for Stanza backbone yet."
        )
    
    return data

def get_entity_ratio(data: pl.DataFrame,
                        backbone: str = 'spacy'
                        ) -> pl.DataFrame:
        """
        Calculates the ratio of entities to tokens in the text data.
        """
        if "n_tokens" not in data.columns:
            data = get_sequence_length(data, backbone)
        
        if "n_entities" not in data.columns:
            data = get_num_entities(data, backbone)
        
        data = data.with_columns(
            pl.col("n_entities") / pl.col("n_tokens")
            ).alias("entity_ratio")
        
        return data

def get_entities_per_sentence(data: pl.DataFrame,
                              backbone: str = 'spacy'
                              ) -> pl.DataFrame:
    """
    Calculates the average number of entities per sentence in the text data.
    """
    if "n_sentences" not in data.columns:
        data = get_num_sentences(data, backbone)
    if "n_entities" not in data.columns:
        data = get_num_entities(data, backbone)
    
    data = data.with_columns(
        pl.col("n_entities") / pl.col("n_sentences")
        ).alias("entities_per_sentence")
    
    return data

def get_num_per_ent_type(data: pl.DataFrame,
                         backbone: str = 'spacy',
                         ent_types: list = ENT_TYPES
                         ) -> pl.DataFrame:
    """
    Calculates the number of entities per entity type in the text data.
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
        raise NotImplementedError(
            "Not implemented for Stanza backbone yet."
        )
    
    return data

def get_ent_type_ratio(data: pl.DataFrame,
                          backbone: str = 'spacy',
                          ent_types: list = ENT_TYPES
                          ) -> pl.DataFrame:
     """
     Calculates the ratio of entities per entity type to tokens in the text data.
     """
     if "n_tokens" not in data.columns:
          data = get_sequence_length(data, backbone)
     
     for ent_type in ent_types:
          if f"n_{ent_type.lower()}" not in data.columns:
                data = get_num_per_ent_type(data, backbone, ent_types)
          data = data.with_columns(
                pl.col(f"n_{ent_type.lower()}") / pl.col("n_tokens")
                ).alias(f"{ent_type.lower()}_ratio")
     
     return data

def get_ent_type_per_sentence(data: pl.DataFrame,
                                backbone: str = 'spacy',
                                ent_types: list = ENT_TYPES
                                ) -> pl.DataFrame:
        """
        Calculates the average number of entities per entity type per sentence in the text data.
        """
        if "n_sentences" not in data.columns:
            data = get_num_sentences(data, backbone)
        if "n_entities" not in data.columns:
            data = get_num_entities(data, backbone)
        if "n_tokens" not in data.columns:
            data = get_sequence_length(data, backbone)
        
        for ent_type in ent_types:
            if f"n_{ent_type.lower()}" not in data.columns:
                data = get_num_per_ent_type(data, backbone, ent_types)
            data = data.with_columns(
                pl.col(f"n_{ent_type.lower()}") / pl.col("n_sentences")
                ).alias(f"{ent_type.lower()}_per_sentence")
        
        return data

