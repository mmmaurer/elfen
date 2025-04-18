from elfen.util import (
    rescale_column,
    normalize_column,
    filter_lexicon,
    upos_to_wn
)
import polars as pl
import pytest

@pytest.fixture
def sample_data():
    """
    Fixture to provide sample data for testing.
    """
    data = {
        'feature': [
            1.0, 2.0, 3.0, 4.0, 5.0,
            6.0, 7.0, 8.0, 9.0, 10.0
        ]
    }
    df = pl.DataFrame(data)
    return df

def test_rescale_column(sample_data):
    """
    Test the rescale_column function.
    """
    data = rescale_column(sample_data, 'feature', 0.0, 1.0)
    assert 'feature' in data.columns
    assert data['feature'].min() == 0.0
    assert data['feature'].max() == 1.0

def test_rescale_column_custom_range(sample_data):
    """
    Test the rescale_column function with a custom range.
    """
    data = rescale_column(sample_data, 'feature', 1.0, 5.0)
    assert 'feature' in data.columns
    assert data['feature'].min() == 1.0
    assert data['feature'].max() == 5.0

def test_rescale_column_no_change(sample_data):
    """
    Test the rescale_column function with no change.
    """
    data = rescale_column(sample_data, 'feature', 1.0, 10.0)
    assert 'feature' in data.columns
    assert data['feature'].min() == 1.0
    assert data['feature'].max() == 10.0
    for i in range(len(data)):
        assert data['feature'][i] == pytest.approx(sample_data['feature'][i])

def test_rescale_column_to_constant(sample_data):
    """
    Test the rescale_column function to a constant value.
    """
    data = rescale_column(sample_data, 'feature', 0.0, 0.0)
    assert 'feature' in data.columns
    assert data['feature'].min() == 0.0
    assert data['feature'].max() == 0.0
    for i in range(len(data)):
        assert data['feature'][i] == 0.0

