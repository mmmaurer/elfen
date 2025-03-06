# ELFEN - Efficient Linguistic Feature Extraction for Natural Language Datasets

This python package provides efficient linguistic feature extraction for text datasets (i.e. datasets with N text instances, in a tabular structure). 

For a full overview of the features available, check the [overview table](features.md), for further details and tutorials check the
[documentation](https://elfen.readthedocs.io).

The multilingual support is documented in the [multilingual support table](multilingual_support.md).


## Installation
Install this package using the current pypi version
```bash
python -m pip install elfen
```

Install this package from source 
```bash
python -m pip install git+https://github.com/mmmaurer/elfen.git
```

To use wordnet features, download open multilingual wordnet using:
```bash
python -m wn download omw:1.4
```

## Usage of third-party resources usable in this package
The extraction of psycholinguistic, emotion/lexicon and semantic features relies on third-party resources such as lexicons.
Please refer to the original author's licenses and conditions for usage, and cite them if you use the resources through this package in your analyses.

For an overview which features use which resource, and how to export all third-party resource references in a `bibtex` string, consult the [documentation](https://elfen.readthedocs.io).

## Acknowledgements

While all feature extraction functions in this package are written from scratch, the choice of features in the readability and lexical richness feature areas (partially) follows the [`readability`](https://github.com/andreasvc/readability) and [`lexicalrichness`](https://github.com/LSYS/LexicalRichness) python packages.

We use the [`wn`](https://github.com/goodmami/wn) python package to extract Open  Multilingual Wordnet synsets.

## Citation
If you use this package in your work, for now, please cite
```bibtex
@misc{maurer-2025-elfen,
  author = {Maurer, Maximilian},
  title = {ELFEN - Efficient Linguistic Feature Extraction for Natural Language Datasets},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/mmmaurer/elfen}},
}
```