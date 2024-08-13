import polars as pl

from .surface import (
    get_num_tokens,
)

def load_hedges(hedges_file: str) -> list[str]:
    """
    Loads the hedges from the given file.
    """
    with open(hedges_file, 'r') as f:
        raw = f.readlines()
        hedges = []
        for line in raw:
            if not line.startswith("%") and line.strip() != "\n" and \
                line.strip() != "":
                hedges.append(line.strip())
    
    return hedges

def get_num_hedges(data: pl.DataFrame,
                   hedges: list[str],
                   text_column: str = 'text'
                   ) -> pl.DataFrame:
    """
    Calculates the number of hedges in a text.
    """
    def n_matches(string: str, patterns: list[str]) -> int:
        """
        Helper function.
        Returns the number of matches of the patterns in the string.
        """
        total_matches = 0
        for pattern in patterns:
            total_matches += string.count(pattern)
        return total_matches
    
    data = data.with_columns(
        pl.col(text_column).map_elements(lambda x: 
                                         n_matches(x, hedges),
            return_dtype=pl.UInt16
            ).alias("n_hedges"),
    )
    
    return data

def get_hedges_ratio(data: pl.DataFrame,
                     hedges: list[str],
                     text_column: str = 'text'
                     ) -> pl.DataFrame:
    """
    Calculates the ratio of hedges in a text.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data)
    
    if 'n_hedges' not in data.columns:
        data = get_num_hedges(data, hedges)
    
    data = data.with_columns(
        (pl.col("n_hedges") / pl.col("n_tokens")
         ).alias("hedges_ratio"),
    )
    
    return data