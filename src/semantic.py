import numpy as np
import polars as pl
import wn

from .features import (
    get_tokens,
)
from .surface import (
    get_num_tokens,
)
from .util import (
    upos_to_wn,
)

# --------------------------------------------------------------------------- #
#                                    Hedges                                   #
# --------------------------------------------------------------------------- #

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
                     text_column: str = 'text',
                     backbone: str = 'spacy'
                     ) -> pl.DataFrame:
    """
    Calculates the ratio of hedges in a text.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    
    if 'n_hedges' not in data.columns:
        data = get_num_hedges(data, hedges, text_column)
    
    data = data.with_columns(
        (pl.col("n_hedges") / pl.col("n_tokens")
         ).alias("hedges_ratio"),
    )
    
    return data

# --------------------------------------------------------------------------- #
#                       Ambiguity, Polysemy                                   #
# --------------------------------------------------------------------------- #

def get_synsets(data: pl.DataFrame,
                backbone: str = 'spacy',
                language: str = 'en',
                pos_tags: list[str] = [
                    'NOUN', 'VERB', 'ADJ', 'ADV'
                    ]
                ) -> pl.DataFrame:
    """
    Calculates the number of synsets in a text per token.
    """
    if backbone == 'spacy':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x:
                                        [len(wn.synsets(token.text,
                                                        lang=language,
                                                        pos=upos_to_wn(token.pos_)
                                                        ))
                                         for token in x
                                         if token.pos_ in pos_tags],
                return_dtype=pl.List(pl.Int64)).alias("synsets")
        )
        for pos in pos_tags:
            data = data.with_columns(
                pl.col("nlp").map_elements(lambda x:
                                            [len(wn.synsets(token.text,
                                                            lang=language,
                                                            pos=upos_to_wn(token.pos_)
                                                            ))
                                             for token in x
                                             if token.pos_ == pos],
                    return_dtype=pl.List(pl.Int64)).alias(f"synsets_{pos.lower()}")
            )
    elif backbone == 'stanza':
        data = data.with_columns(
            pl.col("nlp").map_elements(lambda x:
                                        [len(wn.synsets(word.text,
                                                        lang=language,
                                                        pos=upos_to_wn(word.upos)
                                                        ))
                                         for sent in x.sentences
                                         for word in sent.words
                                         if word.upos in pos_tags],
                return_dtype=pl.List(pl.Int64)).alias("synsets")
        )
        for pos in pos_tags:
            data = data.with_columns(
                pl.col("nlp").map_elements(lambda x:
                                            [len(wn.synsets(word.text,
                                                            lang=language,
                                                            pos=upos_to_wn(word.upos)
                                                            ))
                                             for sent in x.sentences
                                             for word in sent.words
                                             if word.upos == pos],
                    return_dtype=pl.List(pl.Int64)).alias(f"synsets_{pos.lower()}")
            )

    return data

def get_avg_num_synsets(data: pl.DataFrame,
                        backbone: str = 'spacy',
                        language: str = 'en',
                        pos_tags: list[str] = [
                            'NOUN', 'VERB', 'ADJ', 'ADV'
                            ]
                        ) -> pl.DataFrame:
    """
    Calculates the average number of synsets in a text.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'synsets' not in data.columns:
        data = get_synsets(data, backbone=backbone,
                           language=language,
                           pos_tags=pos_tags)
    
    data = data.with_columns(
        pl.col("synsets").list.mean().alias("avg_num_synsets")
    )
    
    
    return data

def get_avg_num_synsets_per_pos(data: pl.DataFrame,
                                backbone: str = 'spacy',
                                language: str = 'en',
                                pos_tags: list[str] = [
                                    'NOUN', 'VERB', 'ADJ', 'ADV'
                                    ],
                                nan_value: float = 0
                                ) -> pl.DataFrame:
    """
    Calculates the average number of synsets per POS in a text.
    """
    # if backbone == 'spacy':
    #     for pos in pos_tags:
    #         data = data.with_columns(
    #             (pl.col("nlp").map_elements(lambda x:
    #                                             [
    #                                                 len(wn.synsets(
    #                                                     token.text,
    #                                                     lang=language,
    #                                                     pos=upos_to_wn(pos)
    #                                                 ))
    #                                                 for token in x
    #                                                 if token.pos_ == pos
    #                                             ],
    #             return_dtype=pl.List(pl.Int64)).list.mean()
    #             ).fill_null(0).alias(f"avg_num_synsets_{pos.lower()}")
    #         )
    # elif backbone == 'stanza':
    #     for pos in pos_tags:
    #         data = data.with_columns(
    #             (pl.col("nlp").map_elements(lambda x:
    #                                        [
    #                                             len(wn.synsets(
    #                                                 word.text,
    #                                                 lang=language,
    #                                                 pos=upos_to_wn(pos)
    #                                             ))
    #                                             for sent in x.sentences
    #                                             for word in sent.words
    #                                             if word.upos == pos
    #                                         ],
    #             return_dtype=pl.List(pl.Int64)).list.mean()
    #             ).fill_null(0).alias(f"avg_num_synsets_{pos.lower()}")
    #         )
    if "synsets" not in data.columns:  # ensures all synsets are calculated
        data = get_synsets(data, backbone=backbone,
                           language=language,
                           pos_tags=pos_tags)
    for pos_tag in pos_tags:
        if backbone == 'spacy':
            data = data.with_columns(
                pl.col("synsets_" + pos_tag.lower()).list.mean(). \
                fill_nan(nan_value).fill_null(nan_value). \
                    alias(f"avg_num_synsets_{pos_tag.lower()}")
            )
        elif backbone == 'stanza':
            data = data.with_columns(
                pl.col("synsets_" + pos_tag.lower()).list.mean(). \
                fill_nan(nan_value).fill_null(nan_value). \
                    alias(f"avg_num_synsets_{pos_tag.lower()}")
            )

    return data

def get_num_low_synsets(data: pl.DataFrame,
                        backbone: str = 'spacy',
                        language: str = 'en',
                        pos_tags: list[str] = [
                            'NOUN', 'VERB', 'ADJ', 'ADV'
                            ],
                        threshold: int = 2
                        ) -> pl.DataFrame:
    """
    Calculates the number of words with a low number of synsets in a text.
    """
    # if  backbone == 'spacy':
    #     data = data.with_columns(
    #         pl.col("nlp").map_elements(lambda x:
    #                                     [
    #                                         1 for token in x
    #                                         if len(wn.synsets(
    #                                             token.text,
    #                                             lang=language,
    #                                             pos=upos_to_wn(token.pos_)
    #                                         )) <= threshold
    #                                         and token.pos_ in pos_tags
    #                                         ],
    #         return_dtype=pl.List(pl.Int64)
    #         ).list.len().alias("n_low_synsets"))
    # elif backbone == 'stanza':
    #     data = data.with_columns(
    #         pl.col("nlp").map_elements(lambda x:
    #                                     [
    #                                         1 for sent in x.sentences
    #                                         for word in sent.words
    #                                         if len(wn.synsets(
    #                                             word.text,
    #                                             lang=language,
    #                                             pos=upos_to_wn(word.upos)
    #                                         )) <= threshold
    #                                         and word.upos in pos_tags
    #                                     ],
    #         return_dtype=pl.List(pl.Int64)
    #         ).list.len().alias("n_low_synsets")
    #     )
    if "synsets" not in data.columns:
        data = get_synsets(data, backbone=backbone,
                           language=language,
                           pos_tags=pos_tags)
    
    data = data.with_columns(
        pl.col("synsets").map_elements(lambda x:
                                       [
                                           1 for synset in x
                                           if synset <= threshold
                                       ],
        return_dtype=pl.List(pl.Int64)).list.len().alias("n_low_synsets")
    )


    return data

def get_low_synsets_ratio(data: pl.DataFrame,
                          backbone: str = 'spacy',
                          language: str = 'en',
                          pos_tags: list[str] = [
                              'NOUN', 'VERB', 'ADJ', 'ADV'
                              ],
                          threshold: int = 2
                          ) -> pl.DataFrame:
    """
    Calculates the ratio of words with a low number of synsets in a text.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_low_synsets' not in data.columns:
        data = get_num_low_synsets(data, backbone=backbone,
                                   language=language,
                                   threshold=threshold,
                                   pos_tags=pos_tags)
    
    data = data.with_columns(
        (pl.col("n_low_synsets") / pl.col("n_tokens")
         ).alias("low_synsets_ratio"),
    )

    return data

def get_num_high_synsets(data: pl.DataFrame,
                         backbone: str = 'spacy',
                         language: str = 'en',
                         pos_tags: list[str] = [
                             'NOUN', 'VERB', 'ADJ', 'ADV'
                             ],
                        threshold: int = 5
                        ) -> pl.DataFrame:
    """
    Calculates the number of words with a high number of synsets in a text.
    """
    # if  backbone == 'spacy':
    #     data = data.with_columns(
    #         pl.col("nlp").map_elements(lambda x:
    #                                    [
    #                                         1 for token in x
    #                                         if len(wn.synsets(
    #                                             token.text,
    #                                             lang=language,
    #                                             pos=upos_to_wn(token.pos_)
    #                                         )) >= threshold
    #                                         and token.pos_ in pos_tags
    #                                     ],
    #         return_dtype=pl.List(pl.Int64)).list.len().alias("n_high_synsets")
    #     )
    # elif backbone == 'stanza':
    #     data = data.with_columns(
    #         pl.col("nlp").map_elements(lambda x:
    #                                    [
    #                                         1 for sent in x.sentences
    #                                         for word in sent.words
    #                                         if len(wn.synsets(
    #                                             word.text,
    #                                             lang=language,
    #                                             pos=upos_to_wn(word.upos)
    #                                         )) >= threshold
    #                                         and word.upos in pos_tags
    #                                     ],
    #         return_dtype=pl.List(pl.Int64)).list.len().alias("n_high_synsets"))
    
    # return data
    if "synsets" not in data.columns:
        data = get_synsets(data, backbone=backbone,
                           language=language,
                           pos_tags=pos_tags)
    
    data = data.with_columns(
        pl.col("synsets").map_elements(lambda x:
                                       [
                                           1 for synset in x
                                           if synset >= threshold
                                       ],
        return_dtype=pl.List(pl.Int64)).list.len().alias("n_high_synsets")
    )

    return data

def get_high_synsets_ratio(data: pl.DataFrame,
                           backbone: str = 'spacy',
                           language: str = 'en',
                            pos_tags: list[str] = [
                                 'NOUN', 'VERB', 'ADJ', 'ADV'
                                 ],
                            threshold: int = 5
                            ) -> pl.DataFrame:
    """
    Calculates the ratio of words with a high number of synsets in a text.
    """
    if 'n_tokens' not in data.columns:
        data = get_num_tokens(data, backbone=backbone)
    if 'n_high_synsets' not in data.columns:
        data = get_num_high_synsets(data, backbone=backbone,
                                   language=language,
                                   threshold=threshold,
                                   pos_tags=pos_tags)
        
    data = data.with_columns(
        (pl.col("n_high_synsets") / pl.col("n_tokens")
         ).alias("high_synsets_ratio"),
    )

    return data


