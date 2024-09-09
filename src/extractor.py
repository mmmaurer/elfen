from .features import (
    get_lemmas,
    get_tokens,
    preprocess_data,
)
from .emotion import (
    # sentiment
    load_sentiment_nrc_lexicon,
    filter_sentiment_nrc_lexicon,
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
    filter_lexicon,
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
    filter_concreteness_norms,
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
    get_synsets,
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
    def __init__(self, data, config):
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

        self.data = preprocess_data(self.data)
    
    def parse_config(self):
        return self.config
    
    def extract_features(self):
        features = self.config["features"]
        backbone = self.config["backbone"]

        for feature in features:
            if feature not in FUNCTION_MAP:
                if feature.endswith("_token_ratio"):
                    self.ratio_features["token"].append(feature)
                elif feature.endswith("_type_ratio"):
                    self.ratio_features["type"].append(feature)
                elif feature.endswith("_sentence_ratio"):
                    self.ratio_features["sentence"].append(feature)
                else:
                    raise ValueError(f"Feature {feature} is not supported.")
            else:
                self.data = FUNCTION_MAP[feature](self.data, backbone=backbone)
        
        # Calculate ratio features; if feature list is empty,
        # the function will return the data as is
        self.data = get_feature_token_ratio(self.data,
                                            self.ratio_features["token"])
        self.data = get_feature_type_ratio(self.data,
                                           self.ratio_features["type"])
        self.data = get_feature_sentence_ratio(self.data,
                                               self.ratio_features["sentence"])

        return self.data