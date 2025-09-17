import os

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

RESOURCE_MAP = {
    # Hedges, https://github.com/words/hedges
    "hedges": {
        "link": "https://raw.githubusercontent.com/words/hedges/main/data.txt",
        "area": "Semantics",
        "subarea": "Hedges",
        "filename": "hedges.txt",
        "filepath": os.path.join(PROJECT_PATH, "elfen_resources", "Semantics",
                                 "Hedges", "hedges.txt"),
        "bibtex": rb"""@misc{hedges, author = {Titus Wormer}, title = {Hedges}, year = {2022}, publisher = {GitHub}, journal = {GitHub repository}, howpublished = {\url{github.com/words/hedges}}, }"""
    },
    # Warriner, A. B., Kuperman, V., & Brysbaert, M. (2013).
    # Norms of valence, arousal, and dominance for 13,915 English lemmas.
    # Behavior Research Methods, 45(4), 1191-1207.
    "vad_warriner": {
        "link": "https://static-content.springer.com/esm/"
                "art%3A10.3758%2Fs13428-012-0314-x/MediaObjects/"
                "13428_2012_314_MOESM1_ESM.zip",
        "area": "Emotion",
        "subarea": "VAD",
        "filename": "BRM-emot-submit.csv",
        "filepath": os.path.join(PROJECT_PATH, "elfen_resources", "Emotion",
                                 "VAD", "BRM-emot-submit.csv"),
        "bibtex": rb"""
        @article{vad_warriner,
        title={Norms of valence, arousal, and dominance for 13,915 English lemmas},
        author={Warriner, Amy Beth and Kuperman, Victor and Brysbaert, Marc},
        journal={Behavior research methods},
        volume={45},
        pages={1191--1207},
        year={2013},
        publisher={Springer}
        }
        """
    },
    # Mohammad, S. M. (2018).
    # Obtaining reliable human ratings of valence, arousal, and dominance for 
    # 20,000 English words.
    # In Proceedings of the 56th Annual Meeting of the Association for
    # Computational Linguistics (Volume 1: Long Papers) (pp. 174-184).
    "vad_nrc": {
        "link": "https://saifmohammad.com/WebDocs/Lexicons/"
                "NRC-VAD-Lexicon.zip",
        "area": "Emotion",
        "subarea": "VAD",
        "filename": "NRC-VAD-Lexicon/NRC-VAD-Lexicon.txt",
        "filepath": os.path.join(PROJECT_PATH, "elfen_resources", "Emotion",
                                 "VAD", "NRC-VAD-Lexicon", 
                                 "NRC-VAD-Lexicon.txt"),
        "multilingual_filepath": os.path.join(PROJECT_PATH, "elfen_resources", 
                                              "Emotion", "VAD",
                                              "NRC-VAD-Lexicon",
                                              "NRC-VAD-Lexicon-"
                                              "ForVariousLanguages.txt"),
        "bibtex": rb"""
        @inproceedings{vad_nrc,
        title = "Obtaining Reliable Human Ratings of Valence, Arousal, and Dominance for 20,000 {E}nglish Words",
        author = "Mohammad, Saif",
        editor = "Gurevych, Iryna  and
        Miyao, Yusuke",
        booktitle = "Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
        month = jul,
        year = "2018",
        address = "Melbourne, Australia",
        publisher = "Association for Computational Linguistics",
        url = "https://aclanthology.org/P18-1017",
        doi = "10.18653/v1/P18-1017",
        pages = "174--184",
        }
        """
    },
    # Mohammad, S. M. (2018)
    # Word affect intensity.
    # In Proceedings of the 56th Annual Meeting of the Association for
    # Computational Linguistics (Volume 1: Long Papers) (pp. 1609-1619).
    "intensity_nrc": {
        "link": "https://saifmohammad.com/WebDocs/Lexicons/"
                "NRC-Emotion-Intensity-Lexicon.zip",
        "area": "Emotion",
        "subarea": "Intensity",
        "filename": "NRC-Emotion-Intensity-Lexicon/"
                    "NRC-Emotion-Intensity-Lexicon-v1.txt",
        "filepath": os.path.join(PROJECT_PATH, "elfen_resources", "Emotion",
                                 "Intensity", "NRC-Emotion-Intensity-Lexicon",
                                 "NRC-Emotion-Intensity-Lexicon-v1.txt"),
        "multilingual_filepath": os.path.join(PROJECT_PATH, "elfen_resources",
                                              "Emotion", "Intensity",
                                              "NRC-Emotion-Intensity-Lexicon/",
                                              "NRC-Emotion-Intensity-Lexicon"
                                              "-v1-ForVariousLanguages.txt"),
                                              
        "bibtex": rb"""
        @inproceedings{vad_nrc,
            title = "Word Affect Intensities",
            author = "Mohammad, Saif",
            editor = "Calzolari, Nicoletta  and
            Choukri, Khalid  and
            Cieri, Christopher  and
            Declerck, Thierry  and
            Goggi, Sara  and
            Hasida, Koiti  and
            Isahara, Hitoshi  and
            Maegaard, Bente  and
            Mariani, Joseph  and
            Mazo, H{\'e}l{\`e}ne  and
            Moreno, Asuncion  and
            Odijk, Jan  and
            Piperidis, Stelios  and
            Tokunaga, Takenobu",
            booktitle = "Proceedings of the Eleventh International Conference on Language Resources and Evaluation ({LREC} 2018)",
            month = may,
            year = "2018",
            address = "Miyazaki, Japan",
            publisher = "European Language Resources Association (ELRA)",
            url = "https://aclanthology.org/L18-1027",
        }
        """
    },
    # Brysbaert, M., Warriner, A. B., & Kuperman, V. (2014).
    # Concreteness ratings for 40 thousand generally known English word lemmas.
    # Behavior Research Methods, 46(3), 904-911.
    "concreteness_brysbaert": {
        "link": "https://static-content.springer.com/esm/"
                "art%3A10.3758%2Fs13428-013-0403-5/MediaObjects/"
                "13428_2013_403_MOESM1_ESM.xlsx",
        "area": "Psycholinguistics",
        "subarea": "Concreteness",
        "filename": "13428_2013_403_MOESM1_ESM.xlsx",
        "filepath": os.path.join(PROJECT_PATH, "elfen_resources", "Psycholinguistics",
                                 "Concreteness", "13428_2013_403_MOESM1_ESM.xlsx"),
        "bibtex": rb"""
        @article{concreteness_brysbaert,
        title={Concreteness ratings for 40 thousand generally known English word lemmas},
        author={Brysbaert, Marc and Warriner, Amy Beth and Kuperman, Victor},
        journal={Behavior research methods},
        volume={46},
        pages={904--911},
        year={2014},
        publisher={Springer}
        }
        """
    },
    # Brysbaert, M., Mandera, P., McCormick, S. F., & Keuleers, E. (2019).
    # Word prevalence norms for 62,000 English lemmas.
    # Behavior Research Methods, 51(2), 467-479.
    "prevalence_brysbaert": {
        "link": "https://static-content.springer.com/"
                "esm/art%3A10.3758%2Fs13428-018-1077-9/"
                "MediaObjects/13428_2018_1077_MOESM2_ESM.xlsx",
        "area": "Psycholinguistics",
        "subarea": "Prevalence",
        "filename": "13428_2018_1077_MOESM2_ESM.xlsx",
        "filepath": os.path.join(PROJECT_PATH, "elfen_resources", "Psycholinguistics",
                                 "Prevalence", "13428_2018_1077_MOESM2_ESM.xlsx"),
        "bibtex": rb"""
        @article{prevalence_brysbaert,
        title={Word prevalence norms for 62,000 English lemmas},
        author={Brysbaert, Marc and Mandera, Pawe{\l} and McCormick, Samantha F and Keuleers, Emmanuel},
        journal={Behavior research methods},
        volume={51},
        pages={467--479},
        year={2019},
        publisher={Springer}
        }
        """
    },
    # Kuperman, V., Stadthagen-Gonzalez, H., & Brysbaert, M. (2013).
    # Age-of-acquisition ratings for 30,000 English words.
    # Behavior Research Methods, 45(4), 1191-1207.
    "aoa_kuperman": {
        "link": "https://static-content.springer.com/esm/"
                "art%3A10.3758%2Fs13428-013-0348-8/"
                "MediaObjects/13428_2013_348_MOESM1_ESM.xlsx",
        "area": "Psycholinguistics",
        "subarea": "AgeOfAcquisition",
        "filename": "13428_2013_348_MOESM1_ESM.xlsx",
        "filepath": os.path.join(PROJECT_PATH, "elfen_resources", "Psycholinguistics",
                                 "AgeOfAcquisition", "13428_2013_348_MOESM1_ESM.xlsx"),
        "bibtex": rb"""
        @article{aoa_kuperman,
        title={Age-of-acquisition ratings for 30,000 English words},
        author={Kuperman, Victor and Stadthagen-Gonzalez, Hans and Brysbaert, Marc},
        journal={Behavior research methods},
        volume={44},
        pages={978--990},
        year={2012},
        publisher={Springer}
        }
        """
    },
    # Baccianella, S., Esuli, A., & Sebastiani, F. (2010).
    # SentiWordNet 3.0: An enhanced lexical resource for sentiment
    # analysis and opinion mining.
    # In LREC (Vol. 10, pp. 2200-2204).
    "sentiwordnet": { # Currently not supported
        "link": "https://raw.githubusercontent.com/aesuli/SentiWordNet/"
                "master/data/SentiWordNet_3.0.0.txt",
        "area": "Emotion",
        "subarea": "Sentiment",
        "filename": "SentiWordNet_3.0.0.txt",
        "filepath": os.path.join(PROJECT_PATH, "elfen_resources", "Emotion",
                                 "Sentiment", "SentiWordNet_3.0.0.txt"),
        "bibtex": rb""  # TODO
    },
        # Mohammad, S. M., & Turney, P. D. (2013).
    # Emotions evoked by common words and phrases:
    # Using Mechanical Turk to create an emotion lexicon.
    # In Proceedings of the NAACL HLT 2013 Workshop on
    # Computational Approaches to Analysis and Generation
    # of Emotion in Text (pp. 26-34).
    "sentiment_nrc": {
        "link": "https://saifmohammad.com/WebDocs/Lexicons/NRC-Emotion-Lexicon.zip",
        "area": "Emotion",
        "subarea": "Sentiment",
        "filename": "NRC-Emotion-Lexicon/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt",
        "filepath": os.path.join(PROJECT_PATH, "elfen_resources", "Emotion",
                                 "Sentiment", "NRC-Emotion-Lexicon",
                                 "NRC-Emotion-Lexicon-Wordlevel-v0.92.txt"),
        "multilingual_filepath": os.path.join(PROJECT_PATH, "elfen_resources",
                                              "Emotion", "Sentiment",
                                              "NRC-Emotion-Lexicon",
                                              "NRC-Emotion-Lexicon-"
                                              "ForVariousLanguages.txt"),
        "bibtex": rb"""
        @article{sentiment_nrc,
        Author = {Mohammad, Saif M. and Turney, Peter D.},
        Journal = {Computational Intelligence},
        Number = {3},
        Pages = {436--465},
        Title = {Crowdsourcing a Word-Emotion Association Lexicon},
        Volume = {29},
        Year = {2013}
        }
        """
    },
    # Coso, B., Guasch, M., Buganovic, I., Ferre, P., & Hinojosa, J. A. (2022).
    # CROWD-5e: A croatian psycholinguistic database for affective norms for
    # five discrete emotions.
    # Behavior Research Methods, 55(1), 4018-4034.
    # TODO: Handle processing the data
    "affect_crowd5e": {
        "link": "https://figshare.com/ndownloader/files/36434421",
        "area": "Emotion",
        "subarea": "Affect",
        "filename": "CROWD-5e.xlsx",
        "filepath": os.path.join(PROJECT_PATH, "elfen_resources", "Emotion",
                                 "Affect", "CROWD-5e.xlsx"),
        "bibtex": rb""  # TODO
    },
    # Diveica, V, Pexman, P. M., & Binney, R. J. (2023).
    # Quantifying Social Semantics: An Inclusive Definition
    # of Socialness and Ratings for 8,388 English Words.
    # Behavior Research Methods, 55, 461-473.
    "socialness": {
        "link": "https://osf.io/download/29eyh/",
        "area": "Psycholinguistics",
        "subarea": "Socialness",
        "filename": "Socialness.csv",
        "filepath": os.path.join(PROJECT_PATH, "elfen_resources", "Psycholinguistics",
                                 "Socialness", "Socialness.csv"),
        "bibtex": rb"""
        @article{socialness,
        title={Quantifying social semantics: An inclusive definition of socialness and ratings for 8388 English words},
        author={Diveica, Veronica and Pexman, Penny M and Binney, Richard J},
        journal={Behavior Research Methods},
        volume={55},
        number={2},
        pages={461--473},
        year={2023},
        publisher={Springer}
        }
        """
    },
     # Lynott, D., Connell, L., Brysbaert, M., Brand, J., & Carney, J. (2020).
    # The Lancaster Sensorimotor Norms: Multidimensional measures of
    # perceptual and action strength for 40,000 English words.
    # Behavior Research Methods, 52, 1271-1291.
    "sensorimotor_lancaster": {
        "link": "https://osf.io/download/pu85v/",
        "area": "Psycholinguistics",
        "subarea": "Sensorimotor",
        "filename": "LancasterSensorimotorNorms.xlsx",
        "filepath": os.path.join(PROJECT_PATH, "elfen_resources", "Psycholinguistics",
                                 "Sensorimotor", "LancasterSensorimotorNorms.xlsx"),
        "bibtex": rb"""
        @article{sensorimotor_lancaster,
        title={The Lancaster Sensorimotor Norms: multidimensional measures of perceptual and action strength for 40,000 English words},
        author={Lynott, Dermot and Connell, Louise and Brysbaert, Marc and Brand, James and Carney, James},
        journal={Behavior research methods},
        volume={52},
        pages={1271--1291},
        year={2020},
        publisher={Springer}
        }
        """
    },
    # Winter, B., Lupyan, G., Perry, L. K., Dingemanse, M., & Perlman, M. (2021).
    # Iconicity ratings for 14,000 English words.
    # Behavior Research Methods, 56, 1640-1655.
    "iconicity_winter": {
        "link": "https://osf.io/download/ex37k/",
        "area": "Psycholinguistics",
        "subarea": "Iconicity",
        "filename": "WinterIconicityNorms.csv",
        "filepath": os.path.join(PROJECT_PATH, "elfen_resources",
                                 "Psycholinguistics",
                                 "Iconicity", "WinterIconicityNorms.csv"),
        "bibtex": rb"""
        @article{iconicity_winter,
        title={Iconicity ratings for 14,000+ English words},
        author={Winter, Bodo and Lupyan, Gary and Perry, Lynn K and Dingemanse, Mark and Perlman, Marcus},
        journal={Behavior research methods},
        volume={56},
        number={3},
        pages={1640--1655},
        year={2024},
        publisher={Springer}
        }
        """
    },
    # Bonin, P., M\'eot, A., & Burgiska, A. (2018).
    # Concreteness ratings for 1,659 French words.
    # Behavior Research Methods, 50(6), 2366-2387.
    # has concreteness, aoa, and other ratings
    "concreteness_bonin": {
        "link": "https://static-content.springer.com/esm/"
                "art%3A10.3758%2Fs13428-018-1014-y/MediaObjects/"
                "13428_2018_1014_MOESM3_ESM.xlsx",
        "area": "Psycholinguistics",
        "subarea": "Concreteness",
        "filename": "BoninConcretenessNorms.xlsx",
        "filepath": os.path.join(PROJECT_PATH, "elfen_resources",
                                 "Psycholinguistics",
                                 "Concreteness",
                                 "BoninConcretenessNorms.xlsx"),
        "bibtex": rb"""
        @article{concreteness_bonin,
        title={Concreteness ratings for 1,659 French words: Relationships with other psycholinguistic variables and word recognition times},
        author={Bonin, Patrick and M\'eot, Aur\'elie and Burgiska, Aur\'elia},
        journal={Behavior Research Methods},
        volume={50},
        pages={2366--2387},
        year={2018},
        publisher={Springer}
        }
        """
    },
    # AoA German
    "aoa_schroeder": {
        "link": "https://static-content.springer.com/"
                "esm/art%3A10.3758%2Fs13428-011-0164-y/"
                "MediaObjects/13428_2011_164_MOESM1_ESM.xls",
        "area": "Psycholinguistics",
        "subarea": "AgeofAcquisition",
        "filename": "SchroederAoANorms.xls",
        "filepath": os.path.join(PROJECT_PATH, "elfen_resources",
                                 "Psycholinguistics",
                                 "AgeofAcquisition", "SchroederAoANorms.xls"),
        "bibtex": rb"""
        @article{aoa_schroeder,
        title={German norms for semantic typicality, age of acquisition, and concept familiarity},
        author={Schroeder, Sabine and Gemballa, Teresa and Ruppin, Steffie and Wartenburger, Isabelle},
        journal={Behavior Research Methods},
        volume={44},
        pages={380--394},
        year={2011},
        publisher={Springer}
        }
        """
    },
    # concreteness German
    "leipzig_affective_norms": {
        "link": "https://static-content.springer.com/"
                "esm/art%3A10.3758%2FBRM.42.4.987/"
                "MediaObjects/Kanske-BRM-2010.zip",
        "area": "Psycholinguistics",
        "subarea": "Concreteness",
        "filename": "Kanske-BRM-2010/LANG_database.txt",
        "filepath": os.path.join(PROJECT_PATH, "elfen_resources",
                                 "Psycholinguistics",
                                 "Concreteness", 
                                 "Kanske-BRM-2010",
                                 "LANG_database.txt"),
        "bibtex": rb"""
        @article{leipzig_affective_norms,
        title={The Leipzig Affective Norms for German: A reliability study},
        author={Kanske, Philipp and Kotz, Sonja A.},
        journal={Behavior Research Methods},
        volume={42},
        number={4},
        pages={987--991},
        year={2010},
        publisher={Springer}
        }
        """
    },
    # sensorimotor norms for italian
    "sensorimotor_vergallito": {
        "link": "https://osf.io/download/qhywk/",
        "area": "Psycholinguistics",
        "subarea": "Sensorimotor",
        "filename": "vergallito_sensorimotor.txt",
        "filepath": os.path.join(PROJECT_PATH, "elfen_resources",
                                 "Psycholinguistics", "Sensorimotor",
                                 "vergallito_sensorimotor.txt"),
        "bibtex": rb"""
        @article{sensorimotor_vergallito,
        title={Perceptual modality norms for 1,121 Itlaian words: A comparison with concreteness and imageability scores and an analysis of their impact on word processing tasks},
        author={Vergallito, Alessandra and Petilli, Marco Alessandro and Marelli, Marco},
        journal={Behavior Research Methods},
        volume={52},
        pages={1599--1614},
        year={2020},
        publisher={Springer}
        }
        """
    },
    # concreteness norms for italian
    "affective_norms_montefinese": {
        "link": "https://osf.io/download/cdu3b/",
        "area": "Psycholinguistics",
        "subarea": "Concreteness",
        "filename": "2014-Montefinese_Database.xlsx",
        "filepath": os.path.join(PROJECT_PATH, "elfen_resources",
                                 "Psycholinguistics", "Concreteness",
                                 "2014-Montefinese_Database‰.xlsx"),
        "bibtex": rb"""
        @article{affective_norms_montefinese,
        title={The adaptation of the Affective Norms for English Words (ANEW) in Italian},
        author={Montefinese, Maria and Ambrosini, Elena and Fairfield, Beth and Mammarella, Nicola},
        journal={Behavior Research Methods},
        volume={46},
        pages={887--903},
        year={2014},
        publisher={Springer}
        """
    },
    # age of acquisition norms for italian
    "aoa_montefinese": {
        "link": "https://osf.io/download/3nvh6/",
        "area": "Psycholinguistics",
        "subarea": "AgeofAcquisition",
        "filename": "ItAoA.xlsx",
        "filepath": os.path.join(PROJECT_PATH, "elfen_resources",
                                 "Psycholinguistics", "Age of Acquisition",
                                 "ItAoA.xlsx"),
        "bibtex": rb"""
        @article{aoa_montefinese,
        AUTHOR={Montefinese, Maria  and Vinson, David  and Vigliocco, Gabriella  and Ambrosini, Ettore }, 
        TITLE={Italian Age of Acquisition Norms for a Large Set of Words (ItAoA)},
        JOURNAL={Frontiers in Psychology},
        VOLUME={Volume 10 - 2019},
        YEAR={2019},
        DOI={10.3389/fpsyg.2019.00278}
        }
        """
    },
    # "perceptual_chedid": {
    # # TODO: Has two sheets, one for visual and one for auditory
    # # TBD how to handle this
    #     # https://lingualab.ca/en/project/norms-familiarity-perceptual-strength/
    #     "link": "",
    #     "area": "Psycholinguistics",
    #     "subarea": "Sensorimotor",
    #     "filename": "ChedidPerceptualNorms.xlsx",
    #     "filepath": os.path.join(PROJECT_PATH, "elfen_resources",
    #                              "Psycholinguistics", "Sensorimotor",
    #                              "ChedidPerceptualNorms.xlsx"),
    #     "bibtex": rb"""
    #     @article{perceptual_chedid,
    #     title={Visual and auditory perceptual strength norms for 3,596 French nouns and their relationship with other psycholinguistic variables},
    #     author={Chedid, Georges and Brambati, Simona Maria and Bedetti, Christophe and Rey, Amandine E. and Wilson, Maximiliano A. and Vallet, Guillaume T.},
    #     journal={Behavior Research Methods},
    #     volume={51},
    #     pages={2094--2105},
    #     year={2019},
    #     publisher={Springer}
    #     }
    #     """
    # }
}

