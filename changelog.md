# Changelog

## Version 1.3.5
### Bugfixes
- Fixed multilingual schemas (`VAD_SCHEMA_NRC_MULTILINGUAL`, `INTENSITY_SCHEMA_MULTILINGUAL`, `SENTIMENT_NRC_SCHEMA_MULTILINGUAL`) being `None` due to `dict.update()` misuse; switched to `|` merge operator so language keys are properly included.
- Corrected spaCy POS tag `"Aux"` to `"AUX"` in the morphological config so auxiliary-verb morphological features are no longer always zero.
- Replaced mutable default argument `CONFIG_ALL` in `Extractor.__init__` with `config=None` and a shallow copy, preventing module-level `CONFIG_ALL` mutation across instances.
- Added missing single-string branch to `token_normalize` so a single feature name in `str` format is normalized (previously silently ignored; only list and `"all"` were handled).
- Fixed `get_rix` to check `n_sentences == 0` (instead of `n_tokens == 0`) for the zero-division warning and to compute `n_sentences`/`n_long_words` if absent, preventing a `ColumnNotFoundError` crash when called standalone.
- Fixed column name mismatch in `get_num_tokens_per_sentence`: alias is now `n_tokens_per_sentence` (was `tokens_per_sentence`) to match `FUNCTION_MAP` and `CONFIG_ALL`.
- Added `backbone` parameter to `_explode_and_join` and forwarded it to `get_lemmas`; all seven callers (`get_avg`, `get_n_low`, `get_n_high`, `get_n_controversial`, `get_max`, `get_min`, `get_sd`) now pass their `backbone` through, fixing stanza crashes on lexicon-based features.
- Corrected Herdan's V formula: `.sqrt()` now wraps the entire expression `K + 1/N - 1/V` (previously only `1/n_types` was square-rooted and the outer root was missing, producing values ~20× too large).
- Renamed the `CONFIG_ALL` feature-area key `"morphology"` to `"morphological"` to match `FEATURE_AREA_MAP`, so `extract_feature_group("morphological")` works as documented.
- Added previously missing features to `CONFIG_ALL`: `ramification_factor` (dependency), 12 max/min/sd emotion features, and 6 sd psycholinguistic features, aligning `extract_features()` output with `extract_feature_group()`.
- Replaced `is_nan()` with `is_null()` in 14 `get_avg`/`get_avg_sd` functions across `emotion.py` and `psycholinguistic.py` so warnings now fire when no lexicon words match.
- Replaced `UnboundLocalError` in `filter_sentiment_lexicon` with a clear `ValueError` for unknown lexicon schemas (lexicons with neither a `label` nor `Afrikaans` column).
- Fixed stanza lemma extraction in `get_global_lemma_frequencies`, `get_n_global_lemma_hapax_legomena`, and `get_n_global_lemma_hapax_dislegomena` to iterate `sent.words` (which carry `.lemma`) instead of `sent.tokens` (which do not), preventing `AttributeError` on the stanza backbone.
- Resolved `avg_num_synsets` naming inconsistency: `FUNCTION_MAP`, `FEATURE_AREA_MAP`, and `CONFIG_ALL` now all use `avg_n_synsets`/`avg_n_synsets_per_pos`, consistent with the output column name.
- Removed silently-ignored `text_column=text_column` argument from the `get_num_characters` call in `get_avg_word_length` and replaced it with `backbone=backbone` for correct spaCy/stanza dispatch.
- Added a guard in `entropy()` to return `0.0` for empty strings, preventing `ZeroDivisionError`/`NaN`.
- Replaced `str.count()` substring matching with token-level matching in `get_num_hedges`, preventing overcounting due to substrings (e.g. "may" matching inside "maybe").
- Fixed stale docstring in `get_num_tokens_per_sentence` (documented column name now matches the actual `n_tokens_per_sentence` alias).
### Known issues (pushed to future)
- `__gather_resource_from_featurename` may raise `KeyError` when a feature maps to a resource not present in `RESOURCE_MAP`; currently not triggered because all mapped features have corresponding resource entries.

## Version 1.3.2
### Bugfixes
- Fixed faulty Flesch formulas addressing #20 
- Aligned the default value for empty texts with the output type for ``tree_depth`` in the ``dependency`` module.

## Version 1.3.1
### Bugfixes
- Lexicon filtering used in emotion and psycholinguistic features now takes into account all lemmas, not unique ones; addressing #17  

### Performance improvements
- Filtering lexicons rewritten to polars join operations instead of element mapping, benefiting from polars ' internal optimization. 

### Changes
- Added pointer to READMEs for users to fix potential `wn` incompatible database schema errors.

## Version 1.3.0
### New Features
- Maximum (max), Minimum (min), and Standard Deviation (std) of psycholinguistic and emotion features
### Extended Multilingual Support
- Added psycholinguistic norms for additional languages:
    - Concreteness:
        - Spanish (es)
        - Polish (pl)
    - Age of Acquisition (AoA):
        - Spanish (es)
        - Dutch (nl)
        - Polish (pl)
### Bug Fixes
- Included a tutorial on how to download the NRC lexicons in the documentation and READMEs to address licensing restrictions.
- Fixed the multilingual support table to correctly reflect the available psycholinguistic norms for each language.
- Added an indication for feature group extraction, if the respective group is not found, to improve debugging for users.
### Optimizations and Improvements
- Refactoring lexicon/norm based features to allow for easier maintenance and extension: Added generic feature implementations to reduce code duplication and apply improvements across multiple features automatically.
- Clearer custom extraction documentation.