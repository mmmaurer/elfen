CONFIG_ALL = {
    "backbone": "spacy",
    "language": "en",
    "model": "en_core_web_sm",
    "text_column": "text",
    "max_length": 1000000,
    "remove_constant_cols": True,
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
        },
        "socialness": {
            "area": "Psycholinguistics",
            "subarea": "Socialness"
        },
        "sensorimotor_lancaster": {
            "area": "Psycholinguistics",
            "subarea": "Sensorimotor"
        },
        "iconicity_winter": {
            "area": "Psycholinguistics",
            "subarea": "Iconicity"
        },
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
        "morphology": {
            "n_per_morph_feature": {}
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
            "avg_sd_concreteness": {
                "lexicon": "concreteness_brysbaert"
            },
            "n_controversial_concreteness": {
                "lexicon": "concreteness_brysbaert",
                "threshold": 2.0
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
            "avg_sd_aoa": {
                "lexicon": "aoa_kuperman"
            },
            "n_controversial_aoa": {
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
            "avg_socialness": {
                "lexicon": "socialness"
            },
            "n_low_socialness": {
                "lexicon": "socialness",
                "threshold": 2.33
            },
            "n_high_socialness": {
                "lexicon": "socialness",
                "threshold": 3.66
            },
            "avg_sd_socialness": {
                "lexicon": "socialness"
            },
            "n_controversial_socialness": {
                "lexicon": "socialness",
                "threshold": 2.0
            },
            "avg_sensorimotor": {
                "lexicon": "sensorimotor_lancaster"
            },
            "n_low_sensorimotor": {
                "lexicon": "sensorimotor_lancaster",
                "threshold": 2.33
            },
            "n_high_sensorimotor": {
                "lexicon": "sensorimotor_lancaster",
                "threshold": 3.66
            },
            "avg_sd_sensorimotor": {
                "lexicon": "sensorimotor_lancaster"
            },
            "n_controversial_sensorimotor": {
                "lexicon": "sensorimotor_lancaster",
                "threshold": 2.0
            },
            "avg_iconicity": {
                "lexicon": "iconicity_winter"
            },
            "n_low_iconicity": {
                "lexicon": "iconicity_winter",
                "threshold": 2.33
            },
            "n_high_iconicity": {
                "lexicon": "iconicity_winter",
                "threshold": 3.66
            },
            "avg_sd_iconicity": {
                "lexicon": "iconicity_winter"
            },
            "n_controversial_iconicity": {
                "lexicon": "iconicity_winter",
                "threshold": 2.5
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
            "n_high_synsets_per_pos": {
                "pos": [
                    "NOUN",
                    "VERB",
                    "ADJ",
                    "ADV"
                ],
                "threshold": 5.0
            },
            "n_low_synsets_per_pos": {
                "pos": [
                    "NOUN",
                    "VERB",
                    "ADJ",
                    "ADV"
                ],
                "threshold": 2.0
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

TENSE = ["Fut",
         "Imp",
         "Past",
         "Pres",
         "Pqp"],

ASPECT = ["Hab",
                   "Imp",
                   "Iter",
                   "Perf",
                   "Prog",
                   "Prosp"]

VOICE = ["Act",
                  "Antip",
                  "Bfoc",
                  "Cau",
                  "Dir",
                  "Inv",
                  "Lfoc",
                  "Mid",
                  "Pass",
                  "Rcp"]

POLARITY = ["Neg", "Pos"]

CLUSIVITY = ["Ex", "In"]

NUMBER = ["Coll",
                   "Count",
                   "Dual",
                   "Grpa",
                   "Grpl",
                   "Inv",
                   "Pauc",
                   "Plur",
                   "Ptan",
                   "Sing",
                   "Tri"]

CASE = [ # Core
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
                 "Ter",]

DEGREE = ["Abs",
          "Aug",
          "Cmp",
          "Dim",
          "Equ",
          "Pos",
          "Sup"]

PRON_TYPE = ["Art",
                     "Dem",
                     "Emp",
                     "Exc",
                     "Ind",
                     "Int",
                     "Neg",
                     "Prs",
                     "Rcp",
                     "Rel",
                     "Tot"]

DEIXIS_REF = ["0", "1"]

DEIXIS = ["Abv",
                   "Bel",
                   "Even",
                   "Med",
                   "Nvis",
                   "Prox",
                   "Remt",]

ABBR = ["Yes"]

FOREIGN = ["Yes"]

DEFINITIVE = ["Com",
                     "Cons",
                     "Def",
                     "Ind",
                     "Spec"]

PERSON = ["0",
                   "1",
                   "2",
                   "3",
                   "4"]

MOOD = ["Adm",
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
                 "Sub"]

POLITE = ["Elev",
                   "Form",
                   "Humb",
                   "Infm"]

EVIDENT = ["Fh", "Nfh"]

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
        "Mood": MOOD,
        "Tense": TENSE,
        "Aspect": ASPECT,
        "Voice": VOICE,
        "Evident": EVIDENT,
        "Polarity": POLARITY,
        "Person": PERSON,
        "Polite": POLITE, 
        "Clusivity": CLUSIVITY,
        "Gender": GENDER,
        "Animacy": ANIMACITY,
        "Number": NUMBER,
        "Case": CASE,
        "Abbr": ABBR,
        "Foreign": FOREIGN,
    },
    "NOUN": {
        "Gender": GENDER,
        "Animacy": ANIMACITY,
        # "NounClass": [], # only applicable to Wolof and Bantu languages;
        # not included here (yet). If you work with these languages, you
        # may want to include this feature.
        "Number": NUMBER,
        "Case": CASE,
        "Definite": DEFINITIVE,
        "Abbr": ABBR,
        "Degree": DEGREE,
        "Tense": TENSE,
        "Aspect": ASPECT,
        "Voice": VOICE,
        "Polarity": POLARITY,
        "Foreign": FOREIGN,
    },
    "PRON": {
        "PronType": PRON_TYPE,
        "Poss": ["Yes"],
        "Reflex": ["Yes"],
        "Gender": GENDER,
        "Animacy": ANIMACITY,
        "Aspect": ASPECT,
        "Tense": TENSE,
        "Voice": VOICE,
        "Polarity": POLARITY,
        "Number": NUMBER,
        "Case": CASE,
        "Deixis": DEIXIS,
        "DeixisRef": DEIXIS_REF,
        "Person": PERSON,
        "Clusivity": CLUSIVITY,
        "Abbr": ABBR,
        "Foreign": FOREIGN,
    },
    "ADJ": {
        "Gender": GENDER,
        "Animacy": ANIMACITY,
        "Number": NUMBER,
        "Case": CASE,
        "Definite": DEFINITIVE,
        "Degree": DEGREE,
        "Ten": TENSE,
        "Aspect": ASPECT,
        "Voice": VOICE,
        "Polarity": POLARITY,
        "Abbr": ABBR,
        "Foreign": FOREIGN,
    },
    "DET": {
        "Gender": GENDER,
        "Animacy": ANIMACITY,
        "Number": NUMBER,
        "Case": CASE,
        "Definite": DEFINITIVE,
        "Deixis": DEIXIS,
        "DeixisRef": DEIXIS_REF,
        "Person": PERSON,
        "Abbr": ABBR,
        "Foreign": FOREIGN,
    },
    "NUM": {
        "NumType": ["Card",
                    "Dist",
                    "Frac",
                    "Mult",
                    "Ord",
                    "Range",
                    "Sets",],
        "NumForm": ["Digit",
                    "Combi",
                    "Word",
                    "Roman"],
        "Gender": GENDER,
        "Animacy": ANIMACITY,
        "Number": NUMBER,
        "Case": CASE,
        "Abbr": ABBR,
        "Foreign": FOREIGN,
    },
    "ADV": {
        "Polarity": POLARITY,
        "Degree": DEGREE,
        "Abbr": ABBR,
        "Foreign": FOREIGN,
        "Deixis": DEIXIS,
        "DeixisRef": DEIXIS_REF,
        "Tense": TENSE,
        "Aspect": ASPECT,
        "Voice": VOICE,
    },
    "PROPN": {
        "Gender": GENDER,
        "Animacy": ANIMACITY,
        "Number": NUMBER,
        "Case": CASE,
        "Definite": DEFINITIVE,
        "Degree": DEGREE,
        "Tense": TENSE,
        "Aspect": ASPECT,
        "Voice": VOICE,
        "Polarity": POLARITY,
        "Abbr": ABBR,
        "Foreign": FOREIGN,
    },
    "Aux": {
        "VerbForm": ["Fin",
                     "Inf",
                     "Part"],
        "Tense": TENSE,
        "Aspect": ASPECT,
        "Voice": VOICE,
        "Evident": EVIDENT,
        "Polarity": POLARITY,
        "Person": PERSON,
        "Clusivity": CLUSIVITY,
        "Mood": MOOD,
        "Polite": POLITE,
        "Gender": GENDER,
        "Animacy": ANIMACITY,
        "Number": NUMBER,
        "Case": CASE,
        "Abbr": ABBR,
        "Foreign": FOREIGN,
    },
    "PUNCT": {
        "PunctType": ["Brck",
                      "Comm",
                      "Dash",
                      "Excl",
                      "Peri",
                      "Qest",
                      "Quot",
                      "Semi",
                      "Symb",],
        "PunctSide": ["Fin",
                      "Ini"],
    },
    "CONJ": {
        "ConjType": ["Cmp",
                     "Oper"],
    },
    "CCONJ": {
        "ConjType": ["Cmp",
                     "Oper"],
    },
    "SCONJ": {
        "ConjType": ["Cmp",
                     "Oper"],
    },
    "ADP": {
        "AdpType": ["Prep",
                    "Post",
                    "Circ",
                    "Voc"],
    }
}