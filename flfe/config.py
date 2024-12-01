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
            "lexical_density": {},
            "n_hapax_dislegomena": {},
            "n_hapax_dislegomena_token_ratio": {},
            "n_hapax_dislegomena_type_ratio": {},
            "sichel_s": {},
            "giroud_index": {},
            "mtld": {},
            "hdd": {},
            "mattr": {},
            "msttr": {},
            "yule_k": {},
            "simpsons_d": {},
            "herdan_v": {},
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
            "n_syllables": {},
            "n_monosyllables": {},
            "n_polysyllables": {},
            "flesch_reading_ease": {},
            "flesch_kincaid_grade": {},
            "gunning_fog": {},
            "ari": {},
            "smog": {},
            "cli": {},
            "lix": {},
            "rix": {},
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

GENDER = ["Com",
          "Fem",
          "Masc",
          "Neut"]

ANIMACITY = ["Anim",
             "Hum",
             "Inan",
             "Nhum"],

# TODO: finalize FULL UD universal features
MORPH_CONFIG = {
    # full UD universal features, 
    # check https://universaldependencies.org/u/feat/index.html
    # You may want to use a subset of these features
    # for your specific research question, dataset and language
    "VERB": {
        "VerbForm": ["Conf",
                     "Fin",
                     "Gdv",
                     "Ger",
                     "Inf",
                     "Part",
                     "Sup",
                     "Vnoun"],
        "Mood": ["Adm",
                 "Cnd",
                 "Des",
                 "Imp",
                 "Ind",
                 "Irr",
                 "Jus",
                 "Nec",
                 "Opt",
                 "Pot",
                 "Prp",
                 "Qot",
                 "Sub"],
        "Tense": ["Fut",
                  "Imp",
                  "Past",
                  "Pres",
                  "Pqp"],
        "Aspect": ["Hab",
                   "Imp",
                   "Iter",
                   "Perf",
                   "Prog",
                   "Prosp"],
        "Voice": ["Act",
                  "Antip",
                  "Bfoc",
                  "Cau",
                  "Dir",
                  "Inv",
                  "Lfoc",
                  "Mid",
                  "Pass",
                  "Rcp"],
        "Evident": ["Fh",
                    "Nfh"],
        "Polarity": ["Neg",
                     "Pos"],
        "Person": ["0",
                   "1",
                   "2",
                   "3",
                   "4"],
        "Polite": ["Elev",
                   "Form",
                   "Humb",
                   "Infm"],
        "Clusivity": ["Ex",
                      "In"],
    },
    "NOUN": {
        "Gender": GENDER,
        "Animacy": ANIMACITY,
        # "NounClass": [], # only applicable to Wolof and Bantu languages;
        # not included here (yet). If you work with these languages, you
        # may want to include this feature.
        "Number": ["Coll",
                   "Count",
                   "Dual",
                   "Grpa",
                   "Grpl",
                   "Inv",
                   "Pauc",
                   "Plur",
                   "Ptan",
                   "Sing",
                   "Tri"],
        "Case": [ # Core
                 "Abs",
                 "Acc",
                 "Erg",
                 "Nom",
                 #Non-core
                 "Abe",
                 "Ben",
                 "Cau",
                 "Cmp",
                 "Cns",
                 "Com",
                 "Dat",
                 "Dis",
                 "Equ",
                 "Gen",
                 "Ins",
                 "Par",
                 "Tem",
                 "Tra",
                 "Voc",
                 # Local
                 "Abl",
                 "Add",
                 "Ade",
                 "All",
                 "Del",
                 "Ela",
                 "Ill",
                 "Ine",
                 "Lat",
                 "Loc",
                 "Per",
                 "Sbe",
                 "Sub",
                 "Sup",
                 "Ter",],
        "Definite": ["Com",
                     "Cons",
                     "Def",
                     "Ind",
                     "Spec"],
        "Deixis": ["Abv",
                   "Bel",
                   "Even",
                   "Med",
                   "Nvis",
                   "Prox",
                   "Remt",],
        "DeixisRef": ["0",
                      "1"],
    },
    "PRON": {
        "PronType": ["Art",
                     "Dem",
                     "Emp",
                     "Exc",
                     "Ind",
                     "Int",
                     "Neg",
                     "Prs",
                     "Rcp",
                     "Rel",
                     "Tot"],
        "Poss": ["Yes"],
        "Reflex": ["Yes"],
        "Gender": GENDER,
        "Animacy": ANIMACITY,
    }
}