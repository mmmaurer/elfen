CONFIG_ALL = {
    "backbone": "spacy",
    "language": "en",
    "model": "en_core_web_sm",
    "text_column": "text",
    "lexicons": {
        "vad_nrc": {
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
        "aoa_kuperman": {
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
        },
        "emotion": {
            "avg_valence": {
                "lexicon": "vad_nrc"
            },
            "n_low_valence": {
                "lexicon": "vad_nrc",
                "threshold": 0.33
            },
            "n_high_valence": {
                "lexicon": "vad_nrc",
                "threshold": 0.66
            },
            "avg_arousal": {
                "lexicon": "vad_nrc"
            },
            "n_low_arousal": {
                "lexicon": "vad_nrc",
                "threshold": 0.33
            },
            "n_high_arousal": {
                "lexicon": "vad_nrc",
                "threshold": 0.66
            },
            "avg_dominance": {
                "lexicon": "vad_nrc"
            },
            "n_low_dominance": {
                "lexicon": "vad_nrc",
                "threshold": 0.33
            },
            "n_high_dominance": {
                "lexicon": "vad_nrc",
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
            "n_low_intensity": {
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
            "n_high_intensity": {
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
        },
        "information": {
            "compressibility": {},
            "entropy": {}
        },
        "lexical_richness": {
            "lemma_token_ratio": {},
            "ttr": {},
            "rttr": {},
            "cttr": {},
            "herdan_c": {},
            "summer_index": {},
            "dougast_u": {},
            "maas_index": {},
            "n_hapax_legomena": {},
            "n_hapax_legomena_token_ratio": {},
            "n_hapax_legomena_type_ratio": {},
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
            "avg_aoa": {
                "lexicon": "aoa_kuperman"
            },
            "n_low_aoa": {
                "lexicon": "aoa_kuperman",
                "threshold": 10.0
            },
            "n_high_aoa": {
                "lexicon": "aoa_kuperman",
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
        },
        "readability": {
            "flesch_reading_ease": {},
            "flesch_kincaid_grade": {},
            "gunning_fog": {},
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
        },
        "entities": {
            "n_entities": {},
            "n_entities_token_ratio": {},
            "n_entities_sentence_ratio": {},
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
        }
    }
}