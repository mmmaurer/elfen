.. ELFEN documentation master file, created by
   sphinx-quickstart on Fri Dec 20 17:16:37 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ELFEN - Efficient Linguistic Feature Extraction for Natural Language Datasets
=============================================================================

ELFEN (Efficient Linguistic Feature Extraction for Natural Language Datasets) is a Python package that provides a set of tools for extracting linguistic features from text datasets. It provides an extensive set of features that can be used to analyze text data and NLP model outputs.
Since it is built on top of the modern dataframe package `polars`_, it is able to handle large datasets efficiently. Preprocessing backbones are built on top of the popular NLP libraries `spaCy`_ and `stanza`_, allowing for the use of both light-weight and state-of-the-art NLP models for feature extraction in various Languages.

.. note::
   The package is still under development. If you encounter any issues or have any suggestions, please feel free to open an issue or add a pull request on the `GitHub repository`_.

.. _GitHub repository: https://www.github.com/mmmaurer/elfen

.. _polars: https://www.pola.rs
.. _spaCy: https://spacy.io
.. _stanza: https://stanfordnlp.github.io/stanza/

.. toctree::
   :maxdepth: 4
   :caption: Getting Started
   
   installation
   quickstart

.. toctree::
   :caption: Guides

   tutorials
   custom_configuration
   feature_overview
   multilingual_support

.. toctree::
   :caption: API Reference

   elfen

