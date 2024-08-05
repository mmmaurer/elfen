import polars as pl

from .surface import (
    get_sequence_length,
    get_num_types
)

def get_ttr(data: pl.DataFrame,
            backbone: str = 'spacy'
            ) -> pl.DataFrame:
    if 'n_tokens' not in data.columns:
        data = get_sequence_length(data, backbone=backbone)
    if 'n_types' not in data.columns:
        data = get_num_types(data)
    
    data = data.with_columns(
        (pl.col("n_types") / pl.col("n_tokens")).alias("ttr"),
    )

    return data

def get_rttr(data: pl.DataFrame,
                backbone: str = 'spacy'
                ) -> pl.DataFrame:
        if 'n_tokens' not in data.columns:
            data = get_sequence_length(data, backbone=backbone)
        if 'n_types' not in data.columns:
            data = get_num_types(data)
        
        data = data.with_columns(
            (pl.col("n_types") / pl.col("n_tokens"). \
             map_elements(lambda x: x**0.5)
             ).alias("rttr"),
        )
    
        return data

def get_cttr(data: pl.DataFrame,
                backbone: str = 'spacy'
                ) -> pl.DataFrame:
        if 'n_tokens' not in data.columns:
            data = get_sequence_length(data, backbone=backbone)
        if 'n_types' not in data.columns:
            data = get_num_types(data)
        
        data = data.with_columns(
            (pl.col("n_types") / pl.col("n_tokens"). \
             map_elements(lambda x: (2*x)**0.5, return_dtype=pl.Float64)
             ).alias("cttr"),
        )
    
        return data

def get_herdan_c(data: pl.DataFrame,
                backbone: str = 'spacy'
                ) -> pl.DataFrame:
        if 'n_tokens' not in data.columns:
            data = get_sequence_length(data, backbone=backbone)
        if 'n_types' not in data.columns:
            data = get_num_types(data)
        
        data = data.with_columns(
            (pl.col("n_types").log() / pl.col("n_tokens").log()
             ).alias("herdan_c"),
        )
    
        return data

def get_summer_ttr(data: pl.DataFrame,
                    backbone: str = 'spacy'
                    ) -> pl.DataFrame:
    if 'n_tokens' not in data.columns:
        data = get_sequence_length(data, backbone=backbone)
    if 'n_types' not in data.columns:
        data = get_num_types(data)
    
    data = data.with_columns(
        (pl.col("n_types").log().log() / pl.col("n_tokens").log().log()
         ).alias("summer_ttr"),
    )

    return data

def get_dougast_ttr(data: pl.DataFrame,
                    backbone: str = 'spacy'
                    ) -> pl.DataFrame:
    if 'n_tokens' not in data.columns:
        data = get_sequence_length(data, backbone=backbone)
    if 'n_types' not in data.columns:
        data = get_num_types(data)
    
    data = data.with_columns(
        (pl.col("n_types").log()**2 / (pl.col("n_tokens") - pl.col("n_types"))
         ).alias("dougast_ttr"),
    )

    return data

def get_maas_ttr(data: pl.DataFrame,
                    backbone: str = 'spacy'
                    ) -> pl.DataFrame:
    if 'n_tokens' not in data.columns:
        data = get_sequence_length(data, backbone=backbone)
    if 'n_types' not in data.columns:
        data = get_num_types(data)
    
    data = data.with_columns(
        ((pl.col("n_tokens") - pl.col("n_types")) / pl.col("n_types").log()**2 
         ).alias("dougast_ttr"),
    )

    return data 