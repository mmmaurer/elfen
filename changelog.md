# Changelog

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