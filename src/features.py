from collections import Counter

import polars as pl
import spacy
from spacy_syllables import SpacySyllables
import stanza

def preprocess_data(data: pl.DataFrame,
                    text_column: str = 'text',
                    backbone: str = 'spacy',
                    model: str = 'en_core_web_sm',
                    ) -> pl.DataFrame:
    
    if backbone == 'spacy':
        nlp = spacy.load(model)
        nlp.add_pipe("syllables", after="tagger")
    elif backbone == 'stanza':
        nlp = stanza.Pipeline(model=model)
    
    # Process the text data to retrieve nlp objects
    processed = pl.Series("nlp", [nlp(text) for text in data[text_column]])

    # Insert the processed data into the DataFrame as the last column
    data = data.insert_column(len(data.columns), processed)
    
    return data

