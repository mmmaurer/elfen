.. _tutorials:

Tutorials
=========

Extracting a single feature
---------------------------

To extract a single feature, you will first need to import the ``Extractor`` class from the ``elfen.extractor`` module and initialize it with your data. The ``Extractor`` class will automatically preprocess your data upon initialization.

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

To extract a single feature, you will need to use the ``extract`` method and pass the ``feature`` parameter with the desired feature.

.. code-block:: python

    # Extract a single feature
    # In this case, we are extracting the "average_word_length" feature
    extractor.extract(feature = "avg_word_length")

    print(extractor.data.head())

Extracting a single feature with additional parameters
------------------------------------------------------

For some features, you may want to pass additional parameters or resources. For example, you may have a custom sentiment lexicon that you want to use for the emotional valence features. Additionally, your lexicon may have ratings collected on a different scale, and you may thus want to adapt what constitutes a high-valence word.
You can pass these additional parameters such as custom lexicons and thresholds to the ``extract`` method.

.. code-block:: python
    
    import polars as pl

    from elfen.extractor import Extractor

    # Load your dataset as a polars DataFrame
    # example from csv
    df = pl.read_csv("path/to/your/dataset.csv")

    # Initialize the Extractor with your DataFrame
    extractor = Extractor(data = df)

    # Custom lexicon
    custom_lexicon = pl.read_csv("path/to/your/custom_lexicon.csv")

    # Extract a single feature with additional parameters
    # We are passing a custom lexicon and a threshold
    # Assuming the words in the lexicon are in the "word" column
    # and the valence ratings are in the "valence" column
    extractor.extract(feature = "n_low_valence", lexicon = custom_lexicon, threshold = 0.5)

    print(extractor.data.head())

Extracting multiple specific features
-------------------------------------

You can extract multiple specific features at once by passing a list of features to the ``extract`` method.

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

    # Extract multiple specific features
    # In this case, we are extracting the "avg_word_length" and "n_low_valence" features
    extractor.extract(features = ["avg_word_length", "n_low_valence"])

    print(extractor.data.head())

Unfortunately, at the moment you cannot pass additional parameters to the features when extracting multiple features at once.

Extracting feature areas
------------------------

Instead of extracting features one by one, or all at once, it is possible to extract features in groups, or areas. This is useful when you want to extract features that are related to each other, or when you only want to analyze certain types of features.

Similar to the feature extraction showcased in :ref:`quickstart`, you can extract features using the ``Extractor`` class.
To do this, you will first need to import the ``Extractor`` class from the ``elfen.extractor`` module and Initialize it to preprocess your data.

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

Given that you have initialized the ``Extractor`` class, you can now extract features in groups. To do this, you will need to use the ``extract_feature_group`` method and pass the ``feature_group`` parameter with the desired feature area.

.. code-block:: python

    # Extract features in groups
    # This will extract all implemented features for the specified feature area
    # In this case, we are extracting features from the "lexical_richness" area
    extractor.extract_feature_group(feature_group = "lexical_richness")

    print(extractor.data.head())

Alternatively, you can also extract features from multiple feature areas at once. To do this, you will need to pass a list of feature areas to the ``feature_group`` parameter.

.. code-block:: python

    # Extract features in groups
    # This will extract all implemented features for the specified feature areas
    # In this case, we are extracting features from the "lexical_richness" and "readability" areas
    extractor.extract_feature_group(feature_group = ["lexical_richness", "readability"])

    print(extractor.data.head())

For more information on the available feature areas, check the :ref:`feature_overview` section.

Specifying the model, language, text column, and maximum length
===============================================================
By default, the Extractor class uses the spaCy backbone and the `en_core_web_sm` model, the column `text`, and a maximum length of 100,000 tokens for feature extraction. However, you can specify the model, language, text column, and maximum length of the text to process by passing the respective parameters to the Extractor class.

.. code-block:: python

    import polars as pl
    from elfen.extractor import Extractor

    # Load your dataset as a polars DataFrame
    # example from csv
    df = pl.read_csv("path/to/your/dataset.csv")

    # Initialize the Extractor with your DataFrame
    # This will automatically load the specified model
    # and preprocess the text column
    # Assumes the text column is named "comment"
    extractor = Extractor(data = df,
                          language = "de",
                          model = "de_dep_news_trf",
                          text_column = "comment",
                          max_length = 10000)

    # Extract features
    extractor.extract_features()

    print(extractor.data.head())

Extracting features using a custom configuration
------------------------------------------------

In cases where you want to extract features using a specific model (either from spacy or stanza), in a specific language, or you have a specific set of features you want to extract, you can use a custom configuration.

To extract features using a custom configuration, you will need to pass a dictionary with the desired configuration to the ``extract`` method.

For example, you can extract features using the spacy backbone, in German, using the model ``de_dep_news_trf``, with a maximum length of 10,000 and only extract the average word length from the surface features and the number of low-valence words and high-valence words from the emotion features.

.. code-block:: python

    import polars as pl
    from elfen.extractor import Extractor

    # Load your dataset as a polars DataFrame
    # example from csv
    df = pl.read_csv("path/to/your/dataset.csv")

    # Custom configuration
    custom_config = {
        "backbone": "stanza", 
        "language": "de",
        "model": "de_dep_news_trf",
        "max_length": 10000,
        "features": {
            "surface": ["avg_word_length"],
            "emotion": ["n_low_valence", "n_high_valence"]
        }
    }

    # Initialize the Extractor with your DataFrame and configuration
    extractor = Extractor(data = df, config = custom_config)

    # Extract features using a custom configuration
    extractor.extract_features()

    print(extractor.data.head())

For a full overview over available parameters in the custom configuration, check the :ref:`custom_configuration` section. 

Normalizing extracted features
-------------------------------

We provide the possibility to normalize extracted features in three different ways:

- ``normalize``: Normalizes the extracted features such that they have a mean of 0 and a standard deviation of 1
- ``ratio_normalize``: Normalizes the extracted features using a specific ratio (e.g. given features divided by the number of tokens)
- ``rescale``: Rescales the extracted features using the min-max scaling method

Normalize
~~~~~~~~~

.. code-block:: python

    import polars as pl
    from elfen.extractor import Extractor

    # Load your dataset as a polars DataFrame
    # example from csv
    df = pl.read_csv("path/to/your/dataset.csv")

    # Initialize the Extractor with your DataFrame
    extractor = Extractor(data = df)

    # Extract features
    extractor.extract_feature_group(feature_group = "lexical_richness")
    extractor.extract("avg_word_length")
    extractor.extract("n_low_valence")

    # Normalize extracted features
    extractor.normalize("all") # Normalizes all extracted features
    extractor.normalize("avg_word_length") # Normalizes specific feature
    extractor.normalize(["avg_word_length", "n_low_valence"]) # Normalizes multiple specific features

    print(extractor.data.head())

Ratio Normalize
~~~~~~~~~~~~~~~

.. code-block:: python

    import polars as pl
    from elfen.extractor import Extractor

    # Load your dataset as a polars DataFrame
    # example from csv
    df = pl.read_csv("path/to/your/dataset.csv")

    # Initialize the Extractor with your DataFrame
    extractor = Extractor(data = df)

    # Extract features
    extractor.extract_feature_group(feature_group = "lexical_richness")
    extractor.extract("avg_word_length")
    extractor.extract("n_low_valence")

    # Ratio normalize extracted features
    extractor.ratio_normalize("all", "tokens") # Ratio normalizes all extracted features
    extractor.ratio_normalize("avg_word_length", "tokens") # Ratio normalizes specific feature
    extractor.ratio_normalize(["avg_word_length", "n_low_valence"], "tokens") # Ratio normalizes multiple specific features

    print(extractor.data.head())

Rescale
~~~~~~~

.. code-block:: python

    import polars as pl
    from elfen.extractor import Extractor

    # Load your dataset as a polars DataFrame
    # example from csv
    df = pl.read_csv("path/to/your/dataset.csv")

    # Initialize the Extractor with your DataFrame
    extractor = Extractor(data = df)

    # Extract features
    extractor.extract_feature_group(feature_group = "lexical_richness")
    extractor.extract("avg_word_length")
    extractor.extract("n_low_valence")

    # Rescale extracted features to a range of 0 to 1
    extractor.rescale("all") # Rescales all extracted features
    extractor.rescale("avg_word_length") # Rescales specific feature
    extractor.rescale(["avg_word_length", "n_low_valence"]) # Rescales multiple specific features

    # Rescale extracted features to a custom range
    extractor.rescale("all", minimum = 0, maximum = 10) # Rescales all extracted features

Extracting custom lexicon-based features
----------------------------------------

In cases where you want to extract features based on a custom lexicon that do not fit into the predefined feature areas or way of processing the specific feature, we provide the possibility to extract custom lexicon-based features using some custom template functions for five potential templated features of interest: 

- ``get_n_custom``: Number of words in a text that are in a custom lexicon
- ``get_occurs_custom``: Whether or not a text contains a word from a custom lexicon
- ``get_n_custom_high``: The number of words in a text that are in a custom lexicon and have a rating above a certain threshold (given in another column of the lexicon)
- ``get_n_custom_low``: The number of words in a text that are in a custom lexicon and have a rating below a certain threshold.
- ``get_avg_custom``: The average rating of words in a text that are in a custom lexicon

To extract these custom lexicon-based features, you will need to load the respective custom lexicon as a polars DataFrame and extract the features as shown below.

.. code-block:: python

    import polars as pl

    from elfen.extractor import Extractor
    from elfen.custom import (
        get_n_custom,
        get_occurs_custom,
        get_n_custom_low,
        get_n_custom_high,
        get_avg_custom
    )

    # Load your custom lexicon as a polars DataFrame
    custom_lexicon = pl.read_csv("path/to/your/custom_lexicon.csv")

    # Load your dataset as a polars DataFrame
    # example from csv
    df = pl.read_csv("path/to/your/dataset.csv")

    # Initialize the Extractor with your DataFrame; 
    # preprocessing will be done automatically
    extractor = Extractor(data = df)

    # Load your custom lexicon as a polars DataFrame
    df = extractor.data

    # Load your custom lexicon as a polars DataFrame
    custom_lexicon = pl.read_csv("path/to/your/custom_lexicon.csv")

    # Number of words in a text that are in a custom lexicon
    df = get_n_custom(data=df,  # DataFrame with text data
                      lexicon=custom_lexicon,  # DataFrame with custom lexicon
                      feature_name="n_custom",  # Name of the feature-column after extraction
                      word_column="word",  # Name of the column in the lexicon with the words
                      measurement_level="tokens")  # Measurement level of the feature; either "tokens" or "lemmas"
    
    # Whether or not a text contains a word from a custom lexicon
    df = get_occurs_custom(data=df,  # DataFrame with text data
                           lexicon=custom_lexicon,  # DataFrame with custom lexicon
                           feature_name="occurs_custom",  # Name of the feature-column after extraction
                           word_column="word",  # Name of the column in the lexicon with the words
                           measurement_level="tokens")  # Measurement level of the feature; either "tokens" or "lemmas"

    # Number of words in a text that are in a custom lexicon and have a rating above a certain threshold
    df = get_n_custom_high(data=df,  # DataFrame with text data
                           lexicon=custom_lexicon,  # DataFrame with custom lexicon
                           threshold=0.5,  # Threshold for the rating
                           feature_name="n_custom_high",  # Name of the feature-column after extraction
                           word_column="word",  # Name of the column in the lexicon with the words
                           feature_column="rating",  # Name of the column in the lexicon with the ratings
                           measurement_level="tokens")  # Measurement level of the feature; either "tokens" or "lemmas"

    # Number of words in a text that are in a custom lexicon and have a rating below a certain threshold
    df = get_n_custom_low(data=df,  # DataFrame with text data
                          lexicon=custom_lexicon,  # DataFrame with custom lexicon
                          threshold=0.5,  # Threshold for the rating
                          feature_name="n_custom_low",  # Name of the feature-column after extraction
                          word_column="word",  # Name of the column in the lexicon with the words
                          feature_column="rating",  # Name of the column in the lexicon with the ratings
                          measurement_level="tokens")  # Measurement level of the feature; either "tokens" or "lemmas"

    # Average rating of words in a text that are in a custom lexicon
    df = get_avg_custom(data=df,  # DataFrame with text data
                        lexicon=custom_lexicon,  # DataFrame with custom lexicon
                        feature_name="avg_custom",  # Name of the feature-column after extraction
                        word_column="word",  # Name of the column in the lexicon with the words
                        feature_column="rating",  # Name of the column in the lexicon with the ratings
                        measurement_level="tokens")  # Measurement level of the feature; either "tokens" or "lemmas"

    print(df.head())

Limiting the numbers of cores used
----------------------------------
The underlying dataframe library, polars, uses all available cores by default.
If you are working on a shared server, you may want to consider limiting the resources available to polars.
To do that, you will have to set the ``POLARS_MAX_THREADS`` variable in your shell, e.g.:

.. code-block:: shell

    # Limit the number of threads to 8
    export POLARS_MAX_THREADS=8

.. note::
    If you do not find a suitable template function or different feature extraction function, and you implement your own, please consider contributing to the package by opening a pull request on the `GitHub repository`_.

.. _GitHub repository: https://www.github.com/mmmaurer/elfen

