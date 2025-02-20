"""
This module contains the Extractor class. The Extractor class is the main
class in the ELFEN package and is used to extract features from text data.
"""
import os
import re
from typing import Union

import polars as pl

from .configs.extractor_config import (
    CONFIG_ALL,
)
from .preprocess import (
    preprocess_data,
)
from .features import (
    FUNCTION_MAP,
    FEATURE_AREA_MAP,
    FEATURE_LEXICON_MAP,
)
from .emotion import (
    load_sentiment_nrc_lexicon,
    load_intensity_lexicon,
    load_vad_lexicon,
)
from .psycholinguistic import (
    load_concreteness_norms,
    load_aoa_norms,
    load_prevalence_norms,
    load_socialness_norms,
    load_sensorimotor_norms,
    load_iconicity_norms,
)
from .resources import (
    RESOURCE_MAP,
    get_resource,
)
from .ratios import (
    get_feature_token_ratio,
    get_feature_type_ratio,
    get_feature_sentence_ratio,
)
from .semantic import (
    load_hedges,
)

from .surface import (
    get_global_lemma_frequencies,
    get_global_token_frequencies,
)

from .util import (
    rescale_column,
    normalize_column,
)


class Extractor:
    """
    The Extractor class is the main class in the ELFEN package and is used
    to extract features from text data.

    The Extractor class takes a Polars DataFrame containing text data and
    a configuration dictionary as input. The configuration dictionary
    specifies the text column, the NLP library to use as backbone, the
    language of the text data, the model to use for processing the text
    data, and the features to extract.

    The Extractor class has methods to extract features from the text data,
    extract features in a feature group, extract a single feature, get the
    names of the extracted features, write the extracted features to a CSV
    file, and clean up the extracted features.

    To access the data with the extracted features, use the data attribute
    of the Extractor class: ``extractor.data``.
    """
    def __init__(self, 
                 data: pl.DataFrame,
                 config: dict[str, str] = CONFIG_ALL,
                 **kwargs,
                 ) -> None:
        self.data = data
        self.config = config
        self.basic_features = []
        self.ratio_features = {
            "type": [],
            "token": [],
            "sentence": [],
        }

        # Handle typical keyword arguments
        if "language" in kwargs:
            self.config["language"] = kwargs["language"]
        if "backbone" in kwargs:
            self.config["backbone"] = kwargs["backbone"]
        if "model" in kwargs:
            self.config["model"] = kwargs["model"]
        if "text_column" in kwargs:
            self.config["text_column"] = kwargs["text_column"]
        if "max_length" in kwargs:
            self.config["max_length"] = kwargs["max_length"]

        if "max_length" in self.config:
            max_length = self.config["max_length"]
        else:
            max_length = 1000000

        self.data = preprocess_data(data=self.data,
                                    text_column=self.config["text_column"],
                                    backbone=self.config["backbone"],
                                    lang=self.config["language"],
                                    model=self.config["model"],
                                    max_length=max_length)
        
        self.helper_cols = [
            "nlp",
            "lemmas",
            "tokens",
            "token_freqs",
            'synsets',
            'synsets_noun',
            'synsets_verb',
            'synsets_adj',
            'synsets_adv',
        ]
        self.initial_cols = self.data.columns
    
    def __apply_function(self,
                         feature,
                         function_map = FUNCTION_MAP,
                         **kwargs,
                         ) -> None:
        """
        Helper function to apply a feature extraction function to the
        data. Handles features that require additional parameters.

        NOTE: Currently works for all kwargs except pos_tags
        specification. This is a known issue that will be fixed in
        future versions.
        This is a minor problem though, as pos feature extraction
        is fast; removing the unwanted pos tag features is a bit
        of an inconvenience, but not a major issue.
        Major functionality like specifying lexicons, thresholds, etc. is
        supported.  

        Args:
            feature: The feature to extract.
            function_map: A dictionary of feature extraction functions.
            **kwargs: 
                Additional keyword arguments for the feature extraction.
                Any lexicons or thresholds required for the feature, or
                additional parameters the respective feature function
                takes.
        """
        backbone = self.config["backbone"]
        text_column = self.config["text_column"]
  
        self.data = function_map[feature](
            data=self.data,
            backbone=backbone,
            text_column=text_column,
            language=self.config["language"],
            **kwargs)

    def extract_feature_group(self,
                              feature_group: Union[str, list[str]],
                              feature_area_map: dict[str, str] = \
                                FEATURE_AREA_MAP
                             ) -> None:
        """
        Extract all features in a feature group with default settings.
        Available feature groups are dependency, emotion, entities,
        information, lexical_richness, morphological, pos,
        psycholinguistic, readability, semantic, and surface.

        NOTE: Multilingual support for features that require lexicons or
        norms is currently only implemented for emotion/sentiment features.
        For pscholinguistic features and hedges, only English resources
        are currently available.

        Args:
            feature_group (str): 
                The feature group to extract features from.
            feature_area_map (dict[str, str]):
                A dictionary mapping features to feature areas.

        Returns:
            data (pl.DataFrame):
                The data with the extracted features.
        """
        if type(feature_group) == str:
            feature_group = [feature_group]
        for group in feature_group:
            if group in feature_area_map:
                for feature in feature_area_map[group]:
                    if feature in FEATURE_LEXICON_MAP:
                        lexicon = self.__gather_resource_from_featurename(
                            language=self.config["language"],
                            feature=feature,
                            feature_lexicon_map=FEATURE_LEXICON_MAP)
                        if lexicon is not None:
                            print(f"Extracting {feature}...")
                            self.__apply_function(feature,
                                                  lexicon=lexicon)
                    elif feature in FUNCTION_MAP:
                        self.__apply_function(feature)
                    else:
                        print(f"Feature {feature} not found. Check "
                              "spelling.")
            else:
                print("Feature group not found. Check spelling.")
    
    def __load_lexicon_from_featurename(self,
                                        filepath: str,
                                        featurename: str,
                                        ) -> pl.DataFrame:
        """
        Helper function to load lexicons from the resources.

        Args:
            filepath (str): The path to the lexicon.
            featurename (str): The name of the feature.

        Returns:
            lexicon (pl.DataFrame):
                The lexicon to use for feature extraction.
        """
        if "aoa" in featurename:
            lexicon = load_aoa_norms(filepath)
        elif "concreteness" in featurename:
            lexicon = load_concreteness_norms(filepath)
        elif "prevalence" in featurename:
            lexicon = load_prevalence_norms(filepath)
        elif re.search(r"(valence|arousal|dominance)",
                       featurename):
            lexicon = load_vad_lexicon(filepath,
                                       language=self.config["language"])
        elif "sentiment" in featurename:
            lexicon = load_sentiment_nrc_lexicon(filepath,
                                                 language=self.config[
                                                     "language"])
        elif "intensity" in featurename:
            lexicon = load_intensity_lexicon(filepath,
                                             language=self.config[
                                                 "language"])
        elif "hedges" in featurename:
            lexicon = load_hedges(filepath)
        elif "socialness" in featurename:
            lexicon = load_socialness_norms(filepath)
        elif "sensorimotor" in featurename:
            lexicon = load_sensorimotor_norms(filepath)
        elif "iconicity" in featurename:
            lexicon = load_iconicity_norms(filepath)
        else:
            print(f"Feature {featurename} not found. Skipping...")
            lexicon = None
        return lexicon

    def ratio_normalize(self,
                        features: Union[list[str], str] = "all",
                        ratio: str = "type",
                        **kwargs,
                        ) -> None:
        """
        Normalize the extracted features with a specific ratio feature.
        Ratios available are type, token, and sentence ratios.

        Args:
            features (Union[list[str], str]):
                The features to normalize. Default is "all".
                Allows for a list of features or a single feature in str
                format, or 'all' to normalize all features.
            ratio (str):
                The ratio to normalize the features with.
                Default is "type".

        Returns:
            None
        """
        if ratio == "type":
            ratio_fct = get_feature_type_ratio
        elif ratio == "token":
            ratio_fct = get_feature_token_ratio
        elif ratio == "sentence":
            ratio_fct = get_feature_sentence_ratio
        else:
            print("Ratio not found. Check spelling.")
            return
        
        if type(features) == list:
            self.data = ratio_fct(data=self.data,
                                  features=features,
                                  backbone=self.config["backbone"])
        else:
            if features == "all":
                features = self.get_feature_names()
                self.data = ratio_fct(data=self.data,
                                      features=features,
                                      backbone=self.config["backbone"])
            else:  # single feature in str format
                self.data = ratio_fct(data=self.data,
                                      features=[features],
                                      backbone=self.config["backbone"])

    def normalize(self,
                  features: Union[list[str], str] = "all",
                  **kwargs,
                  ) -> None:
        """
        Normalize the extracted features to have a mean of 0 and a
        standard deviation of 1.

        Args:
            features (Union[list[str], str]):
                The features to normalize. Default is "all".
                Allows for a list of features or a single feature in str
                format, or 'all' to normalize all features.

        Returns:
            None
        """
        if type(features) == list:
            for feature in features:
                self.data = normalize_column(data=self.data,
                                             column=feature)
        else:
            if features == "all":
                features = self.get_feature_names()
                for feature in features:
                    self.data = normalize_column(data=self.data,
                                                 column=feature)
            else:
                self.data = normalize_column(data=self.data,
                                             column=features)
        
    def rescale(self,
                features: Union[list[str], str] = "all",
                minimum: float = 0,
                maximum: float = 1,
                **kwargs,
                ) -> None:
        """
        Rescale the extracted features to a specific range.

        Args:
            features (Union[list[str], str]):
                The features to rescale. Default is "all".
                Allows for a list of features or a single feature in str
                format, or 'all' to rescale all features.
            minimum (float):
                The minimum value to rescale the features to.
                Default is 0.
            maximum (float):
                The maximum value to rescale the features to.
                Default is 1.

        Returns:
            None
        """
        if type(features) == list:
            for feature in features:
                self.data = rescale_column(data=self.data,
                                           column=feature,
                                           minimum=minimum,
                                           maximum=maximum)
        else:
            if features == "all":
                features = self.get_feature_names()
                for feature in features:
                    self.data = rescale_column(data=self.data,
                                               column=feature,
                                               minimum=minimum,
                                               maximum=maximum)
            else:
                self.data = rescale_column(data=self.data,
                                           column=features,
                                           minimum=minimum,
                                           maximum=maximum)

    def __gather_resource_from_featurename(self,
                                           language: str,
                                           feature: str,
                                           feature_lexicon_map: 
                                           dict[str, str] = \
                                               FEATURE_LEXICON_MAP
                                           ) -> pl.DataFrame:
        """
        Helper function to gather resources for feature extraction.

        Args:
            feature (str): The feature to extract.
            feature_lexicon_map (dict[str, str]):
                A dictionary mapping features to lexicons.
        
        Returns:
            lexicon (pl.DataFrame):
                The lexicon to use for feature extraction.
        """
        if feature in feature_lexicon_map:
            if feature_lexicon_map[feature] in RESOURCE_MAP:
                if language == "en":
                    filepath = RESOURCE_MAP[
                        feature_lexicon_map[feature]]["filepath"]
                else:
                    filepath = RESOURCE_MAP[
                        feature_lexicon_map[feature]][
                            "multilingual_filepath"]
                if not os.path.exists(filepath):
                    get_resource(feature_lexicon_map[feature])
                lexicon = self.__load_lexicon_from_featurename(
                    filepath, feature)
                return lexicon
            else:
                print(f"Resource {feature_lexicon_map[feature]} not "
                      "found. Skipping...")
                return None
        else:
            print(f"Feature {feature} not found. Skipping...")
            return None

    def extract_features(self) -> None:
        """
        Extracts all features specified in the config.

        Returns:
            None
        """
        features = self.config["features"]
        for feature_area in features:
            for feature in features[feature_area]:
                print(f"Extracting {feature}...")
                if feature in FUNCTION_MAP:
                    if feature in FEATURE_LEXICON_MAP:
                        lexicon = self.__gather_resource_from_featurename(
                            language=self.config["language"],
                            feature=feature,
                            feature_lexicon_map=FEATURE_LEXICON_MAP
                        )
                        self.__apply_function(feature,
                                              lexicon=lexicon)
                    else:
                        self.__apply_function(feature)
                else:
                    print(f"Feature {feature} not found. Check spelling. "
                          "Skipping...")

        # Remove constant columns if specified and if there is more than 
        # one row
        if self.config["remove_constant_cols"] and len(self.data) > 1:
            self.__remove_constant_cols()
    
    def extract(self,
                feature_name: str,
                **kwargs,
                ):
        """
        Extract a single feature from the data.

        Args:
            feature_name (str): The feature to extract.
            **kwargs:
                Additional keyword arguments for the feature extraction.
                Any lexicons or thresholds required for the feature, or
                additional parameters the respective feature function
                takes.

        Returns:
            None
        """
        if feature_name in FUNCTION_MAP:
            # handle lexicon separately from other kwargs to ensure
            # that the lexicon is loaded correctly if specified by 
            # the user
            if "lexicon" in kwargs:
                lexicon = kwargs["lexicon"]
                self.__apply_function(feature_name,
                                      **kwargs)
            elif feature_name in FEATURE_LEXICON_MAP and \
                 "lexicon" not in kwargs:
                lexicon = self.__gather_resource_from_featurename(
                    language=self.config["language"],
                    feature=feature_name,
                    feature_lexicon_map=FEATURE_LEXICON_MAP)
                self.__apply_function(feature_name,
                                      lexicon=lexicon,
                                      **kwargs)
            else:
                self.__apply_function(feature_name)
        else:
            print(f"Feature {feature_name} not found. Check spelling.")
    
    def __cleanup_cols(self):
        """
        Helper function to remove helper columns from the data.
        """
        if self.config["remove_constant_cols"] and len(self.data) > 1:
            self.__remove_constant_cols()
        self.data = self.data.drop(
            set(self.data.columns).intersection(set(self.helper_cols)))

    def __remove_constant_cols(self):
        """
        Helper function to remove constant columns from the data.
        Constant columns are columns with only one unique value.
        """
        # Remove constant feature columns
        cols_to_drop = [col for col in self.get_feature_names() if
                        self.data[col].n_unique() == 1]
        
        self.data = self.data.drop(cols_to_drop)

    def get_feature_names(self) -> list[str]:
        """
        Get the names of the extracted features.

        Returns:
            feature_names (list[str]):
                A list of the names of the extracted features.
        """
        return list(
            set(self.data.columns) - set(self.initial_cols + \
                                            self.helper_cols))
    
    def write_csv(self,
                  filepath: str,
                  **kwargs,
                  ) -> None:
        """
        Save the extracted features to a CSV file.
        Cleans up the data by removing helper columns before saving and
        then writes the data to a CSV using Polars DataFrame to_csv.
        To specify additional keyword arguments for the to_csv method,
        pass them as keyword arguments to this function.

        Args:
            filepath (str): The path to save the CSV file.
            **kwargs:
                Additional keyword arguments for the Polars DataFrame
                to_csv method.
        """
        self.__cleanup_cols()
        self.data.write_csv(filepath, **kwargs)

    def get_data(self) -> pl.DataFrame:
        """
        Get the data with the extracted features.

        Returns:
            data (pl.DataFrame):
                The data with the extracted features.
        """
        return self.data
    
    def get_corpus_frequencies(self,
                               kind: str = "token",
                               ) -> dict[str, int]:
        """
        Get the global frequencies of tokens or lemmas in the data.

        Args:
            kind (str): 
                The kind of frequency to get. Default is "token".
                Options are "token" or "lemma".
        
        Returns:
            frequencies (dict[str, int]):
                A dictionary of the global frequencies of tokens or lemmas
                in the data.
        """
        if kind == "token":
            frequencies = get_global_token_frequencies(
                data=self.data,
                backbone=self.config["backbone"])
        elif kind == "lemma":
            frequencies = get_global_lemma_frequencies(
                data=self.data,
                backbone=self.config["backbone"])
            
        return frequencies

