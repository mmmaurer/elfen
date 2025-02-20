.. _quickstart:

Quickstart
==========

The easiest way to get started with ELFEN is to use the Extractor class in with the standard configutation. This will use spaCy as a default backbone, and extract all implemented features for an English dataset using the `en_core_web_sm` model.

.. code-block:: python

    import polars as pl
    from elfen.extractor import Extractor

    # Load your dataset as a polars DataFrame
    # example from csv
    df = pl.read_csv("path/to/your/dataset.csv")

    # Initialize the Extractor with your DataFrame
    # This will automatically load the spaCy model
    # and preprocess the text column
    # Assumes the text column is named "text"
    extractor = Extractor(data = df)

    # Extract features
    features = extractor.extract_features()

    print(extractor.data.head())


To load a specific model in a different language, you can specify the `language` and `model` parameters in the Extractor class.

.. code-block:: python

    extractor = Extractor(data = df, language = "de", model = "de_dep_news_trf")

    # Extract features
    features = extractor.extract_features()

    print(extractor.data.head())

For more advanced usage, check our :ref:`tutorials` section.