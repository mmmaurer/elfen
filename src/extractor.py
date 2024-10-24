import re
import os

from .config import (
    CONFIG_ALL,
)
from .preprocess import (
    get_lemmas,
    get_tokens,
    preprocess_data,
)
from .emotion import (
    # sentiment
    load_sentiment_nrc_lexicon,
    get_sentiment_score,
    get_n_negative_sentiment,
    get_n_positive_sentiment,
    # emotion intensity
    load_intensity_lexicon,
    get_avg_emotion_intensity,
    get_n_low_intensity,
    get_n_high_intensity,
    # VAD
    load_vad_lexicon,
    get_avg_valence,
    get_avg_arousal,
    get_avg_dominance,
    get_n_low_valence,
    get_n_high_valence,
    get_n_low_arousal,
    get_n_high_arousal,
    get_n_low_dominance,
    get_n_high_dominance,
)
from .entities import (
    get_num_entities,
    get_num_per_entity_type,
)
from .information import (
    get_compressibility,
    get_entropy,
)
from .lexical_richness import (
    get_lemma_token_ratio,
    get_ttr,
    get_cttr,
    get_rttr,
    get_herdan_c,
    get_summer_index,
    get_dougast_u,
    get_maas_index,
    get_n_hapax_legomena,
    get_lexical_density,
)
from .pos import (
    get_num_lexical_tokens,
    get_num_per_pos,
    get_pos_variability,
    get_num_per_pos,
)
from .psycholinguistic import (
    load_concreteness_norms,
    get_avg_concreteness,
    get_n_high_concreteness,
    get_n_low_concreteness,
    load_aoa_norms,
    get_avg_aoa,
    get_n_high_aoa,
    get_n_low_aoa,
    load_prevalence_norms,
    get_avg_prevalence,
    get_n_high_prevalence,
    get_n_low_prevalence,
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
from .readability import (
    get_flesch_reading_ease,
    get_flesch_kincaid_grade,
    get_smog,
    get_ari,
    get_cli,
    get_gunning_fog,
    get_lix,
    get_rix,
    get_num_monosyllables,
    get_num_polysyllables,
    get_num_syllables,
)
from .semantic import (
    load_hedges,
    get_num_hedges,
    get_avg_num_synsets,
    get_avg_num_synsets_per_pos,
    get_num_high_synsets,
    get_num_low_synsets,
)
from .surface import (
    get_avg_word_length,
    get_num_lemmas,
    get_num_long_words,
    get_num_sentences,
    get_num_tokens,
    get_num_tokens_per_sentence,
    get_num_types,
    get_raw_sequence_length,
    get_num_characters
)

FUNCTION_MAP = {
    # SURFACE FEATURES
    "tokens": get_tokens,
    "lemmas": get_lemmas,
    "raw_sequence_length": get_raw_sequence_length,
    "n_tokens": get_num_tokens,
    "n_lemmas": get_num_lemmas,
    "n_sentences": get_num_sentences,
    "n_types": get_num_types,
    "avg_word_length": get_avg_word_length,
    "n_long_words": get_num_long_words,
    "n_tokens_per_sentence": get_num_tokens_per_sentence,
    "n_characters": get_num_characters,
    # EMOTION FEATURES
    # Sentiment features
    "sentiment_score": get_sentiment_score,
    "n_positive_sentiment": get_n_positive_sentiment,
    "n_negative_sentiment": get_n_negative_sentiment,
    # VAD features
    "avg_valence": get_avg_valence,
    "avg_arousal": get_avg_arousal,
    "avg_dominance": get_avg_dominance,
    "n_low_valence": get_n_low_valence,
    "n_high_valence": get_n_high_valence,
    "n_low_arousal": get_n_low_arousal,
    "n_high_arousal": get_n_high_arousal,
    "n_low_dominance": get_n_low_dominance,
    "n_high_dominance": get_n_high_dominance,
    # Emotion intensity features
    "avg_emotion_intensity": get_avg_emotion_intensity,
    "n_low_intensity": get_n_low_intensity,
    "n_high_intensity": get_n_high_intensity,
    # ENTITY FEATURES
    "n_entities": get_num_entities,
    "n_per_entity_type": get_num_per_entity_type,
    # INFORMATION THEORETIC FEATURES
    "compressibility": get_compressibility,
    "entropy": get_entropy,
    # LEXICAL RICHNESS FEATURES
    "lemma_token_ratio": get_lemma_token_ratio,
    "ttr": get_ttr,
    "cttr": get_cttr,
    "rttr": get_rttr,
    "herdan_c": get_herdan_c,
    "summer_index": get_summer_index,
    "dougast_u": get_dougast_u,
    "maas_index": get_maas_index,
    "n_hapax_legomena": get_n_hapax_legomena,
    "lexical_density": get_lexical_density,
    # POS FEATURES
    "n_lexical_tokens": get_num_per_pos,
    "pos_variability": get_pos_variability,
    "n_per_pos": get_num_per_pos,
    # PSYCHOLINGUISTIC FEATURES
    # Concreteness
    "avg_concreteness": get_avg_concreteness,
    "n_high_concreteness": get_n_high_concreteness,
    "n_low_concreteness": get_n_low_concreteness,
    # AoA
    "avg_aoa": get_avg_aoa,
    "n_high_aoa": get_n_high_aoa,
    "n_low_aoa": get_n_low_aoa,
    # Prevalence
    "avg_prevalence": get_avg_prevalence,
    "n_high_prevalence": get_n_high_prevalence,
    "n_low_prevalence": get_n_low_prevalence,
    # READABILITY FEATURES
    "flesch_reading_ease": get_flesch_reading_ease,
    "flesch_kincaid_grade": get_flesch_kincaid_grade,
    "smog": get_smog,
    "ari": get_ari,
    "cli": get_cli,
    "gunning_fog": get_gunning_fog,
    "lix": get_lix,
    "rix": get_rix,
    "n_monosyllables": get_num_monosyllables,
    "n_polysyllables": get_num_polysyllables,
    "n_syllables": get_num_syllables,
    # SEMANTIC FEATURES
    "n_hedges": get_num_hedges,
    "avg_num_synsets": get_avg_num_synsets,
    "avg_num_synsets_per_pos": get_avg_num_synsets_per_pos,
    "n_high_synsets": get_num_high_synsets,
    "n_low_synsets": get_num_low_synsets,
}

class Extractor:
    def __init__(self, data, config=CONFIG_ALL):
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

        self.data = preprocess_data(data=self.data,
                                    text_column=self.config["text_column"],
                                    backbone=self.config["backbone"],
                                    lang=self.config["lang"],
                                    model=self.config["model"],)

    def parse_config(self):
        return self.config
    
    def __apply_function(self,
                         feature,
                         lexicon = None,
                         threshold = None,
                         function_map = FUNCTION_MAP):
        """
        Helper function to apply a feature extraction function to the data.
        Handles features that require lexicons and thresholds.

        Args:
        - feature: str
            The feature to extract.
        - lexicon: str
            The lexicon to use for the feature extraction.
        - threshold: float
            The threshold to use for the feature extraction.
        - function_map: dict
            A dictionary of feature extraction functions.
        
        Returns:
        - pd.DataFrame
            The input data with the extracted features.
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
            self.data = function_map[feature](data=self.data,
                                            lexicon=lexicon,
                                            backbone=backbone,
                                            text_column=text_column)
        elif threshold is not None:
            self.data = function_map[feature](data=self.data,
                                              threshold=threshold,
                                              backbone=backbone,
                                              text_column=text_column)
        else:
            self.data = function_map[feature](data=self.data,
                                              backbone=backbone,
                                              text_column=text_column)
            
    def extract_feature_group(self, feature_group):
        """
        Extract all features in a feature group.
        Available feature groups are:
        - surface
        - emotion
        - entity
        - information
        - lexical_richness
        - pos
        - psycholinguistic
        - readability
        - semantic

        Args:
        - feature_group: str
            The feature group to extract features from.

        Returns:
        - pd.DataFrame
            The input data with the extracted features.
        """
        pass

    def gather_resource(self,
                        features,
                        feature_area,
                        feature,
                        language="en"):
        """
        Hekper function to gather resources for feature extraction.

        Args:
        - features: dict
            The features to extract.
        - feature_area: str
            The feature area to extract features from.
        - feature: str
            The feature to extract.
        - language: str
            The language to use for the lexicon.

        Returns:
        - lexicon: pd.DataFrame
            The lexicon to use for feature extraction.
        """
        if features[feature_area][feature]["lexicon"] in \
                              RESOURCE_MAP:
            if language != "en" and "multilingual_filepath" in \
                                  RESOURCE_MAP[
                                      features[feature_area][feature]["lexicon"]
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
            return lexicon
        else:
            print(f"Resource {features[feature_area][feature]['lexicon']}"
                  " not found. Skipping...")
            return None

    def extract_features(self):
        features = self.config["features"]
        ratio_features = {
                "type": [],
                "token": [],
                "sentence": [],
            }
        for feature_area in features:
            for feature in features[feature_area]:
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
                    print(feature)
                    if feature.endswith("_token_ratio"):
                        ratio_features["token"].append(feature.replace("_token_ratio", ""))
                    elif feature.endswith("_sentence_ratio"):
                        ratio_features["sentence"].append(feature.replace("_sentence_ratio", ""))
                    elif feature.endswith("_type_ratio"):
                        ratio_features["type"].append(feature.replace("_type_ratio", ""))
                    else:
                        print(f"Feature {feature} not found. Check spelling. Skipping...")

        print(ratio_features)
        for ratio_feature in ratio_features["token"]:
            print(ratio_feature)
            self.data = get_feature_token_ratio(self.data, ratio_feature)
        for ratio_feature in ratio_features["sentence"]:
            self.data = get_feature_sentence_ratio(self.data, ratio_feature)
            print(ratio_feature)
        for ratio_feature in ratio_features["type"]:
            self.data = get_feature_type_ratio(self.data, ratio_feature)
            print(ratio_feature)

        return self.data

