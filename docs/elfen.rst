Module documentation
====================

elfen.configs module
--------------------

.. automodule:: elfen.configs
   :members:
   :undoc-members:
   :show-inheritance:

Submodules
~~~~~~~~~~

.. automodule:: elfen.configs.dependency_config
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: elfen.configs.extractor_config
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: elfen.configs.morphological_config
   :members:
   :undoc-members:
   :show-inheritance:

elfen.custom module
-------------------

.. automodule:: elfen.custom
   :members:
   :undoc-members:
   :show-inheritance:

elfen.dependency module
-----------------------

.. automodule:: elfen.dependency
   :members:
   :undoc-members:
   :show-inheritance:

elfen.emotion module
--------------------

.. automodule:: elfen.emotion
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: load_intensity_lexicon, load_sentiment_nrc_lexicon, load_vad_lexicon

   .. autofunction:: load_intensity_lexicon(path: str = INTENSITY_LEXICON_PATH, schema: dict = INTENSITY_LEXICON_SCHEMA) -> DataFrame

   .. autofunction:: load_sentiment_nrc_lexicon(path: str = SENTIMENT_NRC_LEXICON_PATH, schema: dict = SENTIMENT_NRC_LEXICON_SCHEMA) -> DataFrame

   .. autofunction:: load_vad_lexicon(path: str = VAD_LEXICON_PATH, schema: dict = VAD_LEXICON_SCHEMA) -> DataFrame

elfen.entities module
---------------------

.. automodule:: elfen.entities
   :members:
   :undoc-members:
   :show-inheritance:

.. _elfen.extractor:

elfen.extractor module
----------------------

.. automodule:: elfen.extractor
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: Extractor

   .. autoclass:: Extractor(data: pl.DataFrame, config: dict[str, str] = CONFIG)
      :members:
      :undoc-members:
      :show-inheritance:
      :exclude-members: extract_feature_group

      .. automethod:: extract_feature_group(feature_group: str | list[str] = 'all', feature_area_map: dict[str, list[str]] = FEATURE_AREA_MAP)

elfen.features module
---------------------

.. automodule:: elfen.features
   :members:
   :undoc-members:
   :show-inheritance:

elfen.information module
------------------------

.. automodule:: elfen.information
   :members:
   :undoc-members:
   :show-inheritance:

elfen.lexical\_richness module
------------------------------

.. automodule:: elfen.lexical_richness
   :members:
   :undoc-members:
   :show-inheritance:

elfen.morphological module
--------------------------

.. automodule:: elfen.morphological
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: get_morph_feats
   
   .. autofunction:: get_morph_feats(data: pl.DataFrame, backbone: str = 'spacy', morph_config: dict[str, str] = MORPH_CONFIG) -> pl.DataFrame

elfen.pos module
----------------

.. automodule:: elfen.pos
   :members:
   :undoc-members:
   :show-inheritance:

elfen.preprocess module
-----------------------

.. automodule:: elfen.preprocess
   :members:
   :undoc-members:
   :show-inheritance:

elfen.psycholinguistic module
-----------------------------

.. automodule:: elfen.psycholinguistic
   :members:
   :undoc-members:
   :show-inheritance:

elfen.ratios module
-------------------

.. automodule:: elfen.ratios
   :members:
   :undoc-members:
   :show-inheritance:

elfen.readability module
------------------------

.. automodule:: elfen.readability
   :members:
   :undoc-members:
   :show-inheritance:

elfen.resources module
----------------------

.. automodule:: elfen.resources
   :members:
   :undoc-members:
   :show-inheritance:

elfen.schemas module
--------------------

.. automodule:: elfen.schemas
   :members:
   :undoc-members:
   :show-inheritance:

elfen.semantic module
---------------------

.. automodule:: elfen.semantic
   :members:
   :undoc-members:
   :show-inheritance:

elfen.surface module
--------------------

.. automodule:: elfen.surface
   :members:
   :undoc-members:
   :show-inheritance:

elfen.util module
-----------------

.. automodule:: elfen.util
   :members:
   :undoc-members:
   :show-inheritance:

