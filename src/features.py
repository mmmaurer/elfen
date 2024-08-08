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

def get_lemmas(data: pl.DataFrame,
               backbone: str = 'spacy',
               ) -> pl.DataFrame:
    if backbone == 'spacy':
        lemmas = pl.Series("lemmas", [[token.lemma_ for token in doc]
                                      for doc in data['nlp']])
    elif backbone == 'stanza':
        lemmas = pl.Series("lemmas", [[word.lemma for sent in doc.sentences
                                      for word in sent.words]
                                      for doc in data['nlp']])
    data = data.insert_column(len(data.columns), lemmas)
    
    return data

def get_tokens(data: pl.DataFrame,
               backbone: str = 'spacy',
               ) -> pl.DataFrame:
    if backbone == 'spacy':
        tokens = pl.Series("tokens", [[token.text for token in doc]
                                      for doc in data['nlp']])
    elif backbone == 'stanza':
        tokens = pl.Series("tokens", [[word.text for sent in doc.sentences
                                      for word in sent.words]
                                      for doc in data['nlp']])
    data = data.insert_column(len(data.columns), tokens)
    
    return data

