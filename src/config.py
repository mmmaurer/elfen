CONFIG_ALL = {
    "backbone": "spacy",
    "language": "en",
    "text_column": "text",
    "lexicons": {
        "vad_warriner": {
            "area": "Emotion",
            "subarea": "VAD"
        },
        "intensity_nrc": {
            "area": "Emotion",
            "subarea": "Intensity"
        },
        "sentiment_nrc": {
            "area": "Emotion",
            "subarea": "Sentiment"
        },
        "concreteness_brysbaert": {
            "area": "Psycholinguistics",
            "subarea": "Concreteness"
        },
        "aoa_brysbaert": {
            "area": "Psycholinguistics",
            "subarea": "Age of Acquisition"
        },
        "prevalence": {
            "area": "Psycholinguistics",
            "subarea": "Prevalence"
        },
        "hedges": {
            "area": "Semantics",
            "subarea": "Hedges"
        }
    },
    "features": {
        "surface": {
            "raw_sequence_length": {},
            "n_tokens": {},
            "n_sentences": {},
            "n_tokens_per_sentence": {},
            "n_characters": {},
            "avg_word_length": {},
            "n_types": {},
            "n_long_words": {},
            "n_lemmas": {}
        },
        "sentiment": {
            "sentiment_score": {
                "lexicon": "sentiment_nrc"
            },
            "n_negative_sentiment": {
                "lexicon": "sentiment_nrc"
            },
            "n_positive_sentiment": {
                "lexicon": "sentiment_nrc"
            },
            "n_negative_sentiment_token_ratio": {
                "lexicon": "sentiment_nrc"
            },
            "n_positive_sentiment_token_ratio": {
                "lexicon": "sentiment_nrc"
            }
        },
        "emotion": {
            "avg_valence": {
                "lexicon": "vad_warriner"
            },
            "n_low_valence": {
                "lexicon": "vad_warriner",
                "threshold": 0.33
            },
            "n_high_valence": {
                "lexicon": "vad_warriner",
                "threshold": 0.66
            },
            "n_low_valence_token_ratio": {
                "lexicon": "vad_warriner",
                "threshold": 0.33
            },
            "n_high_valence_token_ratio": {
                "lexicon": "vad_warriner",
                "threshold": 0.66
            },
            "avg_arousal": {
                "lexicon": "vad_warriner"
            },
            "n_low_arousal": {
                "lexicon": "vad_warriner",
                "threshold": 0.33
            },
            "n_high_arousal": {
                "lexicon": "vad_warriner",
                "threshold": 0.66
            },
            "n_low_arousal_token_ratio": {
                "lexicon": "vad_warriner",
                "threshold": 0.33
            },
            "n_high_arousal_token_ratio": {
                "lexicon": "vad_warriner",
                "threshold": 0.66
            },
            "avg_dominance": {
                "lexicon": "vad_warriner"
            },
            "n_low_dominance": {
                "lexicon": "vad_warriner",
                "threshold": 0.33
            },
            "n_high_dominance": {
                "lexicon": "vad_warriner",
                "threshold": 0.66
            },
            "n_low_dominance_token_ratio": {
                "lexicon": "vad_warriner",
                "threshold": 0.33
            },
            "n_high_dominance_token_ratio": {
                "lexicon": "vad_warriner",
                "threshold": 0.66
            },
            "avg_emotion_intensity": {
                "lexicon": "intensity_nrc",
                "emotions": [
                    "anger",
                    "anticipation",
                    "disgust",
                    "fear",
                    "joy",
                    "sadness",
                    "surprise",
                    "trust"
                ],
                "threshold": 0.5
            },
            "n_low_emotion_intensity": {
                "lexicon": "intensity_nrc",
                "emotions": [
                    "anger",
                    "anticipation",
                    "disgust",
                    "fear",
                    "joy",
                    "sadness",
                    "surprise",
                    "trust"
                ],
                "threshold": 0.33
            },
            "n_high_emotion_intensity": {
                "lexicon": "intensity_nrc",
                "emotions": [
                    "anger",
                    "anticipation",
                    "disgust",
                    "fear",
                    "joy",
                    "sadness",
                    "surprise",
                    "trust"
                ],
                "threshold": 0.66
            },
            "n_low_emotion_intensity_token_ratio": {
                "lexicon": "intensity_nrc",
                "emotions": [
                    "anger",
                    "anticipation",
                    "disgust",
                    "fear",
                    "joy",
                    "sadness",
                    "surprise",
                    "trust"
                ],
                "threshold": 0.33
            },
            "n_high_emotion_intensity_token_ratio": {
                "lexicon": "intensity_nrc",
                "emotions": [
                    "anger",
                    "anticipation",
                    "disgust",
                    "fear",
                    "joy",
                    "sadness",
                    "surprise",
                    "trust"
                ],
                "threshold": 0.66
            }
        },
        "information": {
            "compressibility": {},
            "entropy": {}
        },
        "lexical_richness": {
            "lemma_token_token_ratio": {},
            "ttr": {},
            "rttr": {},
            "cttr": {},
            "herdan_c": {},
            "summer_index": {},
            "dugast_u": {},
            "maas_index": {},
            "n_hapax_legomena": {},
            "hapax_legomena_token_ratio": {},
            "n_hapax_legomena_type_token_ratio": {},
            "lexical_density": {}
        },
        "pos": {
            "n_lexical_tokens": {},
            "pos_variability": {},
            "n_per_pos": {
                "pos": [
                    "ADJ",
                    "ADP",
                    "ADV",
                    "AUX",
                    "CCONJ",
                    "DET",
                    "INTJ",
                    "NOUN",
                    "NUM",
                    "PART",
                    "PRON",
                    "PROPN",
                    "PUNCT",
                    "SCONJ",
                    "SYM",
                    "VERB",
                    "X"
                ]
            },
            "n_pos_token_ratio": {
                "pos": [
                    "ADJ",
                    "ADP",
                    "ADV",
                    "AUX",
                    "CCONJ",
                    "DET",
                    "INTJ",
                    "NOUN",
                    "NUM",
                    "PART",
                    "PRON",
                    "PROPN",
                    "PUNCT",
                    "SCONJ",
                    "SYM",
                    "VERB",
                    "X"
                ]
            },
            "n_pos_sentence_ratio": {
                "pos": [
                    "ADJ",
                    "ADP",
                    "ADV",
                    "AUX",
                    "CCONJ",
                    "DET",
                    "INTJ",
                    "NOUN",
                    "NUM",
                    "PART",
                    "PRON",
                    "PROPN",
                    "PUNCT",
                    "SCONJ",
                    "SYM",
                    "VERB",
                    "X"
                ]
            }
        },
        "psycholinguistic": {
            "avg_concreteness": {
               "lexicon": "concreteness_brysbaert"
            },
            "n_low_concreteness": {
                "lexicon": "concreteness_brysbaert",
                "threshold": 1.66
            },
            "n_high_concreteness": {
                "lexicon": "concreteness_brysbaert",
                "threshold": 3.33
            },
            "n_low_concreteness_token_ratio": {
                "lexicon": "concreteness_brysbaert",
                "threshold": 1.66
            },
            "n_high_concreteness_token_ratio": {
                "lexicon": "concreteness_brysbaert",
                "threshold": 3.33
            },
            "avg_age_of_acquisition": {
                "lexicon": "aoa_brysbaert"
            },
            "n_low_aoe": {
                "lexicon": "aoa_brysbaert",
                "threshold": 10.0
            },
            "n_high_aoe": {
                "lexicon": "aoa_brysbaert",
                "threshold": 10.0
            },
            "low_aoe_token_ratio": {
                "lexicon": "aoa_brysbaert",
                "threshold": 10.0
            },
            "high_aoe_token_ratio": {
                "lexicon": "aoa_brysbaert",
                "threshold": 10.0
            },
            "avg_prevalence": {
                "lexicon": "prevalence_brysbaert"
            },
            "n_low_prevalence": {
                "lexicon": "prevalence_brysbaert",
                "threshold": 1.0
            },
            "n_high_prevalence": {
                "lexicon": "prevalence_brysbaert",
                "threshold": 1.0
            },
            "low_prevalence_token_ratio": {
                "lexicon": "prevalence_brysbaert",
                "threshold": 1.0
            },
            "high_prevalence_token_ratio": {
                "lexicon": "prevalence_brysbaert",
                "threshold": 1.0
            }
        },
        "readability": {
            "flesch_reading_ease": {},
            "flesch_kincaid_grade_level": {},
            "gunning_fog_index": {},
            "ari": {},
            "smog": {},
            "cli": {},
            "lix": {},
            "rix": {}
        },
        "semantic": {
            "n_lemmas": {},
            "n_hedges": {
                "lexicon": "hedges"
            },
            "n_hedge_token_ratio": {
                "lexicon": "hedges"
            },
            "n_hedges_sentence_ratio": {
                "lexicon": "hedges"
            },
            "avg_num_synsets": {},
            "avg_num_synsets_per_pos": {
                "pos": [
                    "NOUN",
                    "VERB",
                    "ADJ",
                    "ADV"
                ]
            },
            "n_low_synsets": {
                "threshold": 2.0
            },
            "n_high_synsets": {
                "threshold": 5.0
            },
            "n_low_synset_token_ratio": {
                "threshold": 2.0
            },
            "n_high_synset_token_ratio": {
                "threshold": 5.0
            },
            "n_synsets_sentence_ratio": {},
        },
        "entities": {
            "n_entities": {},
            "entity_token_ratio": {},
            "entities_sentence_ratio": {},
            "n_per_entity_type": {
                "entity_types": [
                    "ORG",
                    "CARDINAL",
                    "DATE",
                    "GPE",
                    "PERSON",
                    "MONEY",
                    "PRODUCT",
                    "TIME",
                    "PERCENT",
                    "WORK_OF_ART",
                    "QUANTITY",
                    "NORP",
                    "LOC",
                    "EVENT",
                    "ORDINAL",
                    "FAC",
                    "LAW",
                    "LANGUAGE"
                ]
            },
            "n_per_entity_type_token_ratio": {
                "entity_types": [
                    "PERSON",
                    "NORP",
                    "FAC",
                    "ORG",
                    "GPE",
                    "LOC",
                    "ORG",
                    "CARDINAL",
                    "DATE",
                    "GPE",
                    "PERSON",
                    "MONEY",
                    "PRODUCT",
                    "TIME",
                    "PERCENT",
                    "WORK_OF_ART",
                    "QUANTITY",
                    "NORP",
                    "LOC",
                    "EVENT",
                    "ORDINAL",
                    "FAC",
                    "LAW",
                    "LANGUAGE"
                ]
            },
            "n_per_entity_type_sentence": {
                "entity_types": [
                    "ORG",
                    "CARDINAL",
                    "DATE",
                    "GPE",
                    "PERSON",
                    "MONEY",
                    "PRODUCT",
                    "TIME",
                    "PERCENT",
                    "WORK_OF_ART",
                    "QUANTITY",
                    "NORP",
                    "LOC",
                    "EVENT",
                    "ORDINAL",
                    "FAC",
                    "LAW",
                    "LANGUAGE"
                ]
            }
        }
    }
}