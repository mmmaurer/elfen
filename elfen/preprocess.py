"""
This module contains functions to preprocess text data.

This preprocessing enables the fast extraction of features from the text
data.

The preprocessing steps implemented in this module are:

- Tokenization:
    The text data is tokenized into individual words.
- Lemmatization:
    The words in the text data are converted to their base form.
- Syllabification:
    The words in the text data are split into syllables.
- POS Tagging:
    The words in the text data are tagged with their part-of-speech.
- Dependency Parsing:
    The words in the text data are parsed for dependencies.
- Named Entity Recognition:
    The named entities in the text data are identified.
"""
import polars as pl
import spacy
# Custom function to download spacy models if they are not available
from spacy_download import load_spacy
from spacy_syllables import SpacySyllables
import stanza

def preprocess_data(data: pl.DataFrame,
                    text_column: str = 'text',
                    backbone: str = 'spacy',
                    model: str = 'en_core_web_sm',
                    max_length: int = 1000000,
                    **kwargs: dict[str, str],
                    ) -> pl.DataFrame:
    """
    Preprocesses the text data using the specified NLP library.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        text_column: The name of the column containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.
        model (str): The name of the model used by the NLP library.
        max_length (int): The maximum number of characters to process.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the processed text data.
            The processed data is stored in a new column named 'nlp'.
    """
    if backbone == 'spacy':
        nlp = load_spacy(model)
        nlp.max_length = max_length
        if not nlp.has_pipe("tagger"):
            nlp.add_pipe("syllables")
        else:
            nlp.add_pipe("syllables", after="tagger")
    elif backbone == 'stanza':
        nlp = stanza.Pipeline(model=model,
                              processors='tokenize,pos,lemma,depparse')
    
    # Process the text data to retrieve nlp objects
    processed = pl.Series("nlp", [nlp(text) for text in data[text_column]])

    # Insert the processed data into the DataFrame as the last column
    data = data.insert_column(len(data.columns), processed)
    
    return data

def get_lemmas(data: pl.DataFrame,
               backbone: str = 'spacy',
               **kwargs: dict[str, str],
               ) -> pl.DataFrame:
    """
    Gets the lemmas of the text data.

    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame):
            A Polars DataFrame containing the lemmas of the text data.
            The lemmas are stored in a new column named 'lemmas'.
    """
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
               **kwargs: dict[str, str],
               ) -> pl.DataFrame:
    """
    Gets the tokens of the text data.
    
    Args:
        data (pl.DataFrame): A Polars DataFrame containing the text data.
        backbone (str): The NLP library used to process the text data.
                Either 'spacy' or 'stanza'.

    Returns:
        data (pl.DataFrame): 
            A Polars DataFrame containing the tokens of the text data.
            The tokens are stored in a new column named 'tokens'.
    """
    if backbone == 'spacy':
        tokens = pl.Series("tokens", [[token.text for token in doc]
                                      for doc in data['nlp']])
    elif backbone == 'stanza':
        tokens = pl.Series("tokens", [[word.text for sent in doc.sentences
                                      for word in sent.words]
                                      for doc in data['nlp']])
    data = data.insert_column(len(data.columns), tokens)
    
    return data

