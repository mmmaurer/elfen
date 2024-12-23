"""
This module contains the Extractor class. The Extractor class is the main
class in the ELFEN package and is used to extract features from text data.
"""
import re
import os

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
class Extractor:
    def __init__(self, 
                 data: pl.DataFrame,
                 config: dict[str, str] = CONFIG_ALL,
                 ) -> None:
        self.data = data
        self.config = config
        self.basic_features = []
        self.ratio_features = {
            "type": [],
            "token": [],
            "sentence": [],
        }
        
        self.resources = {
            "sentiment": None,
            "vad": None,
            "concreteness": None,
            "aoa": None,
            "prevalence": None,
            "hedges": None,
        }

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
    
    def __apply_function(self,
                         feature,
                         lexicon = None,
                         threshold = None,
                         function_map = FUNCTION_MAP):
        """
        Helper function to apply a feature extraction function to the data.
        Handles features that require lexicons and thresholds.

        Args:
            feature: The feature to extract.
            lexicon: The lexicon to use for the feature extraction.
            threshold: The threshold to use for the feature extraction.
            function_map: A dictionary of feature extraction functions.
        """
        backbone = self.config["backbone"]
        text_column = self.config["text_column"]
        if lexicon is not None:
            if threshold is not None:
                self.data = function_map[feature](data=self.data,
                                             lexicon=lexicon,
                                             threshold=threshold,
                                             backbone=backbone,
                                             text_column=text_column)
            else:
                self.data = function_map[feature](data=self.data,
                                                lexicon=lexicon,
                                                backbone=backbone,
                                                text_column=text_column)
        elif threshold is not None and lexicon is None:
            self.data = function_map[feature](data=self.data,
                                              threshold=threshold,
                                              backbone=backbone,
                                              text_column=text_column)
        else:
            self.data = function_map[feature](data=self.data,
                                              backbone=backbone,
                                              text_column=text_column)

    def extract_feature_group(self,
                              feature_group: str,
                              feature_area_map: dict[str, str] = \
                                FEATURE_AREA_MAP
                             ) -> pl.DataFrame:
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
        if feature_group in feature_area_map:
            for feature in feature_area_map[feature_group]:
                if feature in FEATURE_LEXICON_MAP:
                    lexicon = self.__gather_resource_from_featurename(
                        feature, feature_lexicon_map=FEATURE_LEXICON_MAP)
                    if lexicon is not None:
                        print(f"Extracting {feature}...")
                        self.__apply_function(feature, lexicon=lexicon)
                elif feature in FUNCTION_MAP:
                    self.__apply_function(feature)
                else:
                    print(f"Feature {feature} not found. Check spelling.")
        else:
            print("Feature group not found. Check spelling.")

        return self.data
    
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
            lexicon = load_vad_lexicon(filepath)
        elif "sentiment" in featurename:
            lexicon = load_sentiment_nrc_lexicon(filepath)
        elif "intensity" in featurename:
            lexicon = load_intensity_lexicon(filepath)
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


    def __gather_resource_from_featurename(self,
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
                filepath = RESOURCE_MAP[
                    feature_lexicon_map[feature]]["filepath"]
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
    
    def __gather_resource_for_config(self,
                                     features: dict[str, str],
                                     feature_area: str,
                                     feature: str,
                                     language: str = "en"
                                     ) -> pl.DataFrame:
        """
        Helper function to gather resources for feature extraction.

        Args:
            features (dict[str, str]): The features to extract.
            feature_area (str): The feature area of the feature.
            feature (str): The feature to extract.
            language (str): The language of the text data.

        Returns:
            lexicon (pl.DataFrame):
                The lexicon to use for feature extraction.
        """
        if features[feature_area][feature]["lexicon"] in \
                              RESOURCE_MAP:
            if language != "en" and "multilingual_filepath" in \
                                  RESOURCE_MAP[
                                      features[
                                          feature_area
                                          ][feature]["lexicon"]
                                  ]:
                filepath = RESOURCE_MAP[
                    features[feature_area][feature]["lexicon"]
                    ]["multilingual_filepath"]
            else:
                filepath = RESOURCE_MAP[
                    features[feature_area][feature]["lexicon"]
                    ]["filepath"]

            # First check if the resource exists
            if not os.path.exists(filepath):
                get_resource(
                    features[feature_area][feature]["lexicon"])
                
            # Then load it
            lexicon = self.__load_lexicon_from_featurename(
                filepath, feature)
            return lexicon
        else:
            print(f"Resource {features[feature_area][feature]['lexicon']}"
                  " not found. Skipping...")
            return None

    def extract_features(self):
        """
        Extracts all features specified in the config.

        Returns:
            data (pl.DataFrame):
                The data with the extracted features.
        """
        features = self.config["features"]
        ratio_features = {
                "type": [],
                "token": [],
                "sentence": [],
            }
        for feature_area in features:
            for feature in features[feature_area]:
                print(f"Extracting {feature}...")
                if feature in FUNCTION_MAP:
                    # Handle features that require lexicons
                    if "lexicon" in features[feature_area][feature]:
                        lexicon = self.__gather_resource_for_config(
                            features, feature_area, feature)
                        self.__apply_function(feature, lexicon=lexicon)
                    else:
                        self.__apply_function(feature)
                else:
                    if feature.endswith("_token_ratio"):
                        ratio_features["token"].append(
                            feature.replace("_token_ratio", ""))
                    elif feature.endswith("_sentence_ratio"):
                        ratio_features["sentence"].append(
                            feature.replace("_sentence_ratio", ""))
                    elif feature.endswith("_type_ratio"):
                        ratio_features["type"].append(
                            feature.replace("_type_ratio", ""))
                    else:
                        print(f"Feature {feature} not found. "
                              "Check spelling. Skipping...")

        for ratio_feature in ratio_features["token"]:
            self.data = get_feature_token_ratio(self.data, ratio_feature)
        for ratio_feature in ratio_features["sentence"]:
            self.data = get_feature_sentence_ratio(self.data,
                                                   ratio_feature)
        for ratio_feature in ratio_features["type"]:
            self.data = get_feature_type_ratio(self.data, ratio_feature)

        # Remove constant columns if specified and if there is more than 
        # one row
        if self.config["remove_constant_cols"] and len(self.data) > 1:
            self.__remove_constant_cols()

        return self.data
    
    def extract(self,
                feature_name: str,
                ) -> pl.DataFrame:
        """
        Extract a single feature from the data.

        Args:
            feature_name (str): The feature to extract.

        Returns:
            data (pl.DataFrame):
                The data with the extracted feature.
        """
        if feature_name in FUNCTION_MAP:
            if feature_name in FEATURE_LEXICON_MAP:
                lexicon = self.__gather_resource_from_featurename(
                    feature_name, feature_lexicon_map=FEATURE_LEXICON_MAP)
                self.__apply_function(feature_name, lexicon=lexicon)
            else:
                self.__apply_function(feature_name)
        else:
            print(f"Feature {feature_name} not found. Check spelling.")
        
        return self.data
    
    def __remove_constant_cols(self):
        """
        Helper function to remove constant columns from the data.
        Constant columns are columns with only one unique value.
        Only removes columns for dataframes with more than one row.
        """
        # Remove constant feature columns
        feature_cols = [col for col in self.data.select(
            pl.selectors.by_dtype(pl.Int32,
                                  pl.Int64,
                                  pl.Float32,
                                  pl.Float64,
                                  pl.UInt16,
                                  pl.UInt32,
                                  pl.UInt64)
                                ).columns]
        cols_to_drop = [col for col in feature_cols if
                        self.data[col].n_unique() == 1]
        
        self.data = self.data.drop(cols_to_drop)

