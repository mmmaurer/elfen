import pytest
import polars as pl
from elfen import Extractor

@pytest.fixture
def sample_data():
    """
    Fixture to provide sample data for testing.
    """
    data = {
        'text': [
            "This is a test sentence.",
            "Another test sentence.",
            "Yet another test sentence."
        ]
    }
    df = pl.DataFrame(data)
    return df

def test_initialization(sample_data):
    """
    Test the initialization of the Extractor class.
    """
    extractor = Extractor(data=sample_data,
                          backbone='spacy',
                          text_column='text',
                          language='en',
                          model='en_core_web_sm')
    assert extractor.data is not None
    assert 'nlp' in extractor.data.columns

def test_extraction_single_feature(sample_data):
    """
    Test the extraction of features from the text data.
    """
    extractor = Extractor(data=sample_data,
                          backbone='spacy',
                          text_column='text',
                          language='en',
                          model='en_core_web_sm')
    extractor.extract("n_tokens")
    assert 'n_tokens' in extractor.data.columns
    assert len(extractor.data['n_tokens']) == len(sample_data)
    assert extractor.data.shape == (3, 3)  # 3 rows, 3 columns (text, nlp, n_tokens)

def test_extraction_multiple_features(sample_data):
    """
    Test the extraction of multiple features from the text data.
    """
    extractor = Extractor(data=sample_data,
                          backbone='spacy',
                          text_column='text',
                          language='en',
                          model='en_core_web_sm')
    extractor.extract(["n_tokens", "n_sentences"])
    assert 'n_tokens' in extractor.data.columns
    assert 'n_sentences' in extractor.data.columns
    assert len(extractor.data['n_tokens']) == len(sample_data)
    assert len(extractor.data['n_sentences']) == len(sample_data)
    assert extractor.data.shape == (3, 4)  # 3 rows, 4 columns (text, nlp, n_tokens, n_sentences)

def test_extraction_invalid_feature(sample_data):
    """
    Test the extraction of an invalid feature from the text data.
    """
    extractor = Extractor(data=sample_data,
                          backbone='spacy',
                          text_column='text',
                          language='en',
                          model='en_core_web_sm')
    extractor.extract("invalid_feature")
    assert 'invalid_feature' not in extractor.data.columns
    assert len(extractor.data['invalid_feature']) == len(sample_data)

def test_initialization_invalid_backbone(sample_data):
    """
    Test the extraction with an invalid backbone.
    """
    with pytest.raises(ValueError):
        extractor = Extractor(data=sample_data,
                            backbone='invalid_backbone',
                            text_column='text',
                            language='en',
                            model='en_core_web_sm')

    