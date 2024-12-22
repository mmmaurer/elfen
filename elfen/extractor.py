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
                             ):
        """
        Extract all features in a feature group.
        Available feature groups are dependency, emotion, entities,
        information, lexical_richness, morphological, pos,
        psycholinguistic, readability, semantic, and surface.

        Args:
            feature_group (str): 
                The feature group to extract features from.
            feature_area_map (dict[str, str]):
                A dictionary mapping features to feature areas.
        """
        # TODO: Implement for feature groups to use instead of the
        # full feature extraction via config
        pass

    def gather_resource(self,
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
            if "aoa" in feature:
                lexicon = load_aoa_norms(filepath)
            elif "concreteness" in feature:
                lexicon = load_concreteness_norms(filepath)
            elif "prevalence" in feature:
                lexicon = load_prevalence_norms(filepath)
            elif re.search(r"(valence|arousal|dominance)",
                           feature):
                lexicon = load_vad_lexicon(filepath)
            elif "sentiment" in feature:
                lexicon = load_sentiment_nrc_lexicon(filepath)
            elif "intensity" in feature:
                lexicon = load_intensity_lexicon(filepath)
            elif "hedges" in feature:
                lexicon = load_hedges(filepath)
            elif "socialness" in feature:
                lexicon = load_socialness_norms(filepath)
            elif "sensorimotor" in feature:
                lexicon = load_sensorimotor_norms(filepath)
            elif "iconicity" in feature:
                lexicon = load_iconicity_norms(filepath)
            return lexicon
        else:
            print(f"Resource {features[feature_area][feature]['lexicon']}"
                  " not found. Skipping...")
            return None

    def extract_features(self):
        """
        Extracts all features specified in the config.
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
                        lexicon = self.gather_resource(features,
                                                       feature_area,
                                                       feature)
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
            self.data = get_feature_sentence_ratio(self.data, ratio_feature)
        for ratio_feature in ratio_features["type"]:
            self.data = get_feature_type_ratio(self.data, ratio_feature)

        # Remove constant columns if specified and if there is more than one row
        if self.config["remove_constant_cols"] and len(self.data) > 1:
            self.__remove_constant_cols()

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

