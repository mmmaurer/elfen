|Feature|Feature Area|Name in extracted dataframe|Function|Description|Notes|References|
|-|-|-|-|-|-|-|
|Raw sequence length/total number of characters|surface|raw_sequence_length|get_raw_sequence_length|Number of characters in the text (including whitespaces)| | |
|Number of tokens|surface|n_tokens|get_num_tokens|Number of tokens in the text| | |
|Number of sentences|surface|n_sentences|get_num_sentences|Number of sentences in the text| | |
|Number of token per sentence|surface|tokens_per_sentence|get_num_tokens_per_sentence|Average number of tokens per sentence: n_tokens / n_sentences| | |
|Number of characters|surface|n_characters|get_num_characters|Number of characters in the text (excluding whitespaces)| | |
|Characters per sentence|surface|characters_per_sentence|get_chars_per_sentence|Average number of characters per sentence: n_characters / n_sentences| | |
|Raw sequence length per sentence|surface|raw_length_per_sentence|get_raw_length_per_sentence|Average number of characters per sentence: raw_sequence_length / n_sentences| | |
|Average word length|surface|avg_word_length|get_avg_word_length|Average word length (in characters): n_characters / n_tokens| | |
|Number of types|surface|n_types|get_num_types|Number of types (unique tokens) in the text| | |
|Number of long words|surface|n_long_words|get_num_long_words|Number of long words (i.t.o. characters)|Threshold of what is considered a long word defaults to >6 characters; can be adapted in the config| |
|Number of lemmas|surface|n_lemmas|get_num_lemmas|Number of lemmas in the text| | |
|Token frequencies|surface|token_freqs|get_token_freqs|Token frequencies of the types in the text|As this produces a list in a column, writing to file has to be handled| |
|Number of lexical tokens|pos|n_lexical_tokens|get_num_lexical_tokens|Number of lexical tokens (tokens w/ upos tag NOUN, ADVERB, ADJ, ADV)| | |
|POS variability|pos|pos_variability|get_pos_variability|POS variability of the text: (unique upos text in the text) / n_tokens| | |
|Number of tokens with upos tag {pos}|pos|n_{pos}|get_num_per_pos|Number of tokens with a given upos tag in the text. Takes a list of upos tag to extract this feature for|pos_list defaults to all  upos tags; if you only need a subset, this can be adapted in the config| |
|Lemma token ratio|lexical richness|lemma_token_ratio|get_lemma_token_ratio|Lemma token ratio of the text: n_lemmas / n_tokens| | |
|Type token ratio|lexical richness|ttr|get_ttr|Type token ratio of the text: n_types / n_tokens| | |
|Root type token ratio|lexical richness|rttr|get_rttr|Root type token ratio of the text: sqrt(n_types / n_tokens)| | |
|Corrected type token ratio|lexical richness|cttr|get_cttr|Corrected type token ratio of the text: n_types / sqrt(2 * n_tokens)| | |
|Herdan's C|lexical richness|herdan_c|get_herdan_c|Herdan's C of a text: log(n_types) / log(n_tokens)| | |
|Summer's type token ratio/ index|lexical richness|summer_index|get_summer_index|Summer's text token ratio of the text: log(log(n_types)) / log(log(n_tokens))| | |
|Dougast's Uber index|lexical richness|dougast_u|get_dougast_u|Dougast's Uber index of the text: log(n_types)^2 / (log(n_tokens) - log( n_types))| | |
|Maas' text token ratio/index|lexical richness|maas_index|get_maas_index|Maas' text token ratio of the text: (n_tokens - n_types) / log(n_types)^2| | |
|Number of hapax legomena|lexical richness|n_hapax_legomena|get_n_hapax_legomena|Number of hapax legomena (tokens that occur only once) in the text| | |
|Number of hapax dislegomena|lexical richness|n_hapax_dislegomena|get_n_hapax_dislegomena|Number of hapax dislegomena (tokens that occur once or twice) in the text| | |
|Sichel's S|lexical richness|sichel_s|get_sichel_s|Sichel's S of the text: n_hapax_dislegomena / n_types| | |
|Lexical density|lexical richness|lexical_density|get_lexical_density|Lexical density of the text: n_lexical_tokens / n_tokens| | |
|Giroud's index|lexical richness|giroud_index|get_giroud_index|Giroud's index of a text: n_types / sqrt(n_tokens)| | |
|Measure of Textual Lexical Density (MTLD)|lexical richness|mtld|get_mtld|For definition, check https://link.springer.com/article/10.3758/BRM.42.2.381| | |
|Hypergeometric Distribution Diversity (HD-D|lexical richness|hdd|get_hdd|For definition, check https://link.springer.com/article/10.3758/BRM.42.2.381| | |
|Moving-average type token ratio (MATTR)|lexical richness|mattr|get_mattr|Calculates the TTR for a sliding window of n tokens, then takes the average| | |
|Mean segmental type token ratio (MSTTR)|lexical richness|msttr|get_msttr|Divides the text into n segments, calculates the TTR for all of them, then takes the average| | |
|Yule's K|lexical richness|yule_k|get_yule_k|Yule's characteristic constant of vocabulary richness, for definition, check https://quantling.org/~hbaayen/publications/TweedieBaayen1998.pdf| | |
|Simpson's D|lexical richness|simpsons_d|get_simpsons_d|For definition, check https://quantling.org/~hbaayen/publications/TweedieBaayen1998.pdf| | |
|Herdan's Vm|lexical richness|herdan_v|get_herdan_v|For definition, check https://quantling.org/~hbaayen/publications/TweedieBaayen1998.pdf| | |
|Number of syllables|readability|n_syllables|get_num_syllables|Number of syllables in the text|Only implemented for spacy backbone| |
|Number of monosyllables|readability|n_monosyllables|get_num_monosyllables|Number of monosyllables (words with only one syllable) in the text| | |
|Number of polysyllables|readability|n_polysyllables|get_num_polysyllables|Number of polysyllables (words with three or more syllables) in the text| | |
|Flesch reading ease|readability|flesch_reading_ease|get_flesch_reading_ease|Flesch reading ease score of the text; for reference: https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests#Flesch_Reading_Ease| | |
|Flesch-Kincaid Grade Level|readability|flesch_kincaid_grade|get_flesch_kincaid_grade|Flesch-Kincaid grade level of the text; for reference:https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests#Flesch.E2.80.93Kincaid_Grade_Level| | |
|Automated Readability Index (ARI)|readability|ari|get_ari|For reference: https://en.wikipedia.org/wiki/Automated_readability_index| | |
|Simple Measure of Gobbledygook (SMOG)|readability|smog|get_smog|For reference: https://en.wikipedia.org/wiki/SMOG| | |
|Coleman-Liau Index (CLI)|readability|cli|get_cli|For reference: https://en.wikipedia.org/wiki/Coleman%E2%80%93Liau_index| | |
|Gunning-fog Index|readability|gunning_fog|get_gunning_fog|For reference: https://en.wikipedia.org/wiki/Gunning_fog_index| | |
|LIX|readability|lix|get_lix|For reference: https://en.wikipedia.org/wiki/Lix_(readability_test)| | |
|RIX|readability|rix|get_rix|For reference: https://www.jstor.org/stable/40031755| | |
|Compressibility|information|compressibility|get_compressibility|Compressibility is the ratio of the length of the compressed text to the length of the original text. This is a proxy for the Kolmogorov complexity of the text| | |
|Entropy|information|entropy|get_entropy|Shannon entropy of the text| | |
|Number of named entities|entities|n_entitites|get_num_entities|Number of named entities in the text| | |
|Number of named entities of type {ent}|entities|n_{ent}|get_num_per_entity_type|Number of named entities in the text with type {ent}. Takes a list of entity types to extract this feature for|ent_types defaults to all possible entity types; if you only need a subset, this can be adapted in the config| |
|Number of hedge words|semantic|n_hedges|get_num_hedges|Number of hedge words in the text (words expressing uncertainty of the speaker). |requires a hedge lexicon; currently only supported in English| |
|Hedges token ratio|semantic|hedges_ratio|get_hedges_ratio|Ratio of hedges in the text: n_hedges / n_tokens| | |
|Average number of synsets|semantic|avg_n_synsets|get_avg_num_synsets|Average number of wordnet synsets of lexical tokens; proxy for ambiguity/polysemy| | |
|Number of words with a low number of synsets per pos|semantic|n_low_synsets_{pos}|get_low_synsets_{pos}|Number of lexical tokens with a low number of synsets per pos tag|Threshold defaults to <=2| |
|Number of words with a high number of synsets per pos|semantic|n_high_synsets_{pos}|get_high_synsets_{pos}|Number of lexical tokens with a high number of synsets per pos tag|Threshold defaults to >=5| |
|Number of words with a low number of synsets|semantic|n_low_synsets|get_num_low_synsets|Number of lexical tokens with a low number of synsets|Threshold defaults to <=2| |
|Number of words with a high number of synsets|semantic|n_high_synsets|get_num_high_synsets|Number of lexical tokens with a high number of synsets|Threshold defaults to >=5| |
|Average valence|emotion|avg_valence|get_avg_valence| | | |
|Number of low valence tokens|emotion|n_low_valence|get_n_low_valence| |Threshold defaults to 0.33| |
|Number of high valence tokens|emotion|n_high_valence|get_n_high_valence| |Threshold defaults to 0.66| |
|Average arousal|emotion|avg_arousal|get_avg_arousal| | | |
|Number of low arousal tokens|emotion|n_low_arousal|get_n_low_arousal| |Threshold defaults to 0.33| |
|Number of high arousal tokens|emotion|n_high_arousal|get_n_high_arousal| |Threshold defaults to 0.66| |
|Average dominance|emotion|avg_dominance|get_avg_dominance| | | |
|Number of low dominance tokens|emotion|n_low_dominance|get_n_low_dominance| |Threshold defaults to 0.33| |
|Number of high dominance tokens|emotion|n_high_dominance|get_n_high_dominance| |Threshold defaults to 0.66| |
|Average emotion intensity for {emotion}|emotion|avg_intensity|get_avg_intensity|Average intensity of an emotion; takes a list of emotions| | |
|Number of high intensity tokens for {emotion}|emotion|n_high_intensity|get_n_high_intensity| |Threshold defaults to 0.33| |
|Number of low intensity tokens for {emotion}|emotion|n_low_intensity|get_n_low_intensity| |Threshold defaults to 0.66| |
|Sentiment score|emotion|sentiment_score|get_sentiment_score|Difference between the number of positive and negative sentiment words in the text: (n_positive_sentiment - n_negative_sentiment) / n_tokens|Values in range (-1,1) where 0 is neutral, -1 is completely negative sentiment, and 1 is completely positive sentiment| |
|Number of negative sentiment tokens|emotion|n_negative_sentiment|get_n_negative_sentiment| | | |
|Number of positive sentiment tokens|emotion|n_positive_sentiment|get_n_positive_sentiment| | | |
|Average concreteness|psycholinguistic|avg_concreteness|get_avg_concreteness|Average human concreteness ratings of the tokens in the text| | |
|Average standard deviation of concreteness|psycholinguistic|avg_sd_concreteness|get_avg_sd_concreteness|Average standard deviation in the human concreteness ratings of the tokens in the text| | |
|Number of low concreteness tokens|psycholinguistic|n_low_concreteness|get_n_low_concreteness|Number of tokens with a low concreteness rating| | |
|Number of high concreteness tokens|psycholinguistic|n_high_concreteness|get_n_high_concreteness|Number of tokens with a high concreteness rating| | |
|Number of tokens with controversial concreteness|psycholinguistic|n_controversial_concreteness|get_n_controversial_concreteness|Number of tokens with a high standard deviation in the human concreteness rating| | |
|Average age of acquisition|psycholinguistic|avg_aoa|get_avg_aoa|Average age of acquisition rating| | |
|Average standard deviation of age of acquisition|psycholinguistic|avg_sd_aoa|get_avg_sd_aoa|Average standard deviation in the age of acquisition rating| | |
|Number of low age of acquisition tokens|psycholinguistic|n_low_aoa|get_n_low_aoa| | | |
|Number of high age of acquisition tokens|psycholinguistic|n_high_aoa|get_n_high_aoa| | | |
|Number of tokens with controversial age of acquisition|psycholinguistic|n_controversial_aoa|get_n_controversial_aoa| | | |
|Average prevalence|psycholinguistic|avg_prevalence|get_avg_prevalence| | | |
|Number of low prevalence tokens|psycholinguistic|n_low_prevalence|get_n_low_prevalence| | | |
|Number of high prevalence tokens|psycholinguistic|n_high_prevalence|get_n_high_prevalence| | | |
|Average socialness|psycholinguistic|avg_socialness|get_avg_socialness| | | |
|Average standard deviation of socialness|psycholinguistic|avg_sd_socialness|get_avg_sd_socialness| | | |
|Number of high socialness tokens|psycholinguistic|n_high_socialness|get_n_high_socialness| | | |
|Number of low socialness tokens|psycholinguistic|n_low_socialness|get_n_low_socialness| | | |
|Number of tokens with controversial socialness|psycholinguistic|n_controversial_socialness|get_n_controversial_socialness| | | |
|Average iconicity|psycholinguistic|avg_iconicity|get_avg_iconicity| | | |
|Average standard deviation of iconicity|psycholinguistic|avg_sd_iconicity|get_avg_sd_iconicity| | | |
|Number of high iconicity tokens|psycholinguistic|n_high_iconicity|get_n_high_iconicity| | | |
|Number of low iconicity tokens|psycholinguistic|n_low_iconicity|get_n_low_iconicity| | | |
|Number of tokens with controversial iconicity|psycholinguistic|n_controversial_iconicity|get_n_controversial_iconicity| | | |
|Average sensorimotor score for {sensorimotor}|psycholinguistic|avg_sensorimotor|get_avg_sensorimotor| | | |
|Average standard deviation of sensorimotor score |psycholinguistic|avg_sd_sensorimotor|get_avg_sd_sensorimotor| | | |
|Number of tokens with low sensorimotor rating|psycholinguistic|n_low_sensorimotor|get_n_low_sensorimotor| | | |
|Number of tokens with high sensorimotor rating|psycholinguistic|n_high_sensorimotor|get_n_high_sensorimotor| | | |
|Number of tokens with controversial sensorimotor rating|psycholinguistic|n_controversial_sensorimotor|get_n_controversial_sensorimotor| | | |
|Morphological feature counts|morphological|n_{pos}_{feature}_{val}|get_morph_feats|Number of tokens with {pos} {feature} {val} (e.g. VERB VerbForm Inf), takes a dictionary of pos and associated features and values for them|Default dictionary is the full set of UD options; adapt if you do not need all of them (may be language-specific)| |
|Dependency tree width|dependency|tree_width|get_tree_width|Maximum number of siblings of a node at any level| | |
|Dependency tree depth|dependency|tree_depth|get_tree_depth|Maximum distance of a token to the root of the dependency tree| | |
|Tree branching factor|dependency|tree_branching|get_tree_branching|Average number of children of a token in the dependency tree| | |
|Tree ramification factor|dependency|ramification_factor|get_ramification_factor|Average number of children per level| | |
|Number of noun chunks|dependency|n_noun_chunks|get_n_noun_chunks|Number of noun chunks in the dependency tree| | |
|Number of dependencies of type {type}|dependency|n_dependency_{type}|get_n_per_dependency_type| | | |
|{Feature} token ratio|ratios/normalization|{feature}_token_ratio|get_feature_token_ratio| | | |
|{Feature} type ratio|ratios/normalization|{feature}_type_ratio|get_feature_type_ratio| | | |
|{Feature} sentence ratio|ratios/normalization|{feature}_sentence ratio|get_feature_sentence_ratio| | | |