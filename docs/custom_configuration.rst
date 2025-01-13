.. _custom_configuration:

Custom configuration
--------------------

The full specification of the custom configuration is as follows:

.. code-block:: python

    custom_config = {
        "backbone": str,  # Backbone to use for feature extraction. Either "spacy" or "stanza"
        "language": str,  # Language to use for feature extraction. E.g. "en" for English, "de" for German
        # NOTE: The language must be supported by the specified backbone
        "model": str,  # Model to use for feature extraction. E.g. "en_core_web_sm" for English, "de_dep_news_trf" for German
        "max_length": int,  # Maximum length (chars) of the text to process. Default is 100000
        "remove_constant_cols": bool,  # Remove feature columns with constant values, i.e. where all texts produce the same feature value. Default is True
        "text_column": str,  # Name of the text column in the DataFrame. Default is "text"
        "features": {  # Features to extract, grouped by feature area
            "dependency": List[str],
            "emotion": List[str],
            "entities": List[str],
            "information": List[str],
            "lexical_richness": List[str],
            "morphological": List[str],
            "pos": List[str],
            "readability": List[str],
            "semantic": List[str],
            "surface": List[str]
        }
    }