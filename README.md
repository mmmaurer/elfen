# ELFEN - Efficient Linguistic Feature Extraction for Natural Language Datasets

This Python package provides efficient linguistic feature extraction for text datasets (i.e. datasets with N text instances, in a tabular structure). 

For a full overview of the features available, check the [overview table](features.md), for further details and tutorials check the
[documentation](https://elfen.readthedocs.io). Some example use cases are illustrated in Jupyter notebooks in [this repository](https://github.com/mmmaurer/elfen-examples)

The multilingual support is documented in the [multilingual support table](multilingual_support.md).

Check out our [roadmap](roadmap.md) for planned features and improvements. Check out the [changelog](changelog.md) for recent changes.

## Installation
Install this package using the current PyPI version
```bash
python -m pip install elfen
```

Install this package from source 
```bash
python -m pip install git+https://github.com/mmmaurer/elfen.git
```

If you want to use the spacy backbone, you will need to download the respective model, e.g. "en_core_web_sm":
 ```bash
 python -m spacy download en_core_web_sm
 ```

To use wordnet features, download open multilingual wordnet using:
```bash
python -m wn download omw:1.4
```

Note that for some languages, you will need to install another wordnet collection. For example, for German, you can use the following command:

```bash
python -m wn download odenet:1.4
```

For more information on the available wordnet collections, consult the [wn package documentation](https://wn.readthedocs.io/en/latest/guides/lexicons.html).

> [!CAUTION]
> Some of the external resources used for feature extraction (e.g., NRC lexicons) have to be downloaded manually due to licensing restrictions. For this, please see [this guide](download_nrc.md). Note that without these resources, only a subset of features will be available.

## Multiprocessing and limiting the numbers of cores used
The underlying dataframe library, polars, uses all available cores by default.
If you are working on a shared server, you may want to consider limiting the resources available to polars.
To do that, you will have to set the ``POLARS_MAX_THREADS`` variable in your shell, e.g.:

```bash
export POLARS_MAX_THREADS=8
```

## Usage of third-party resources usable in this package
The extraction of psycholinguistic, emotion/lexicon and semantic features relies on third-party resources such as lexicons.
Please refer to the original author's licenses and conditions for usage, and cite them if you use the resources through this package in your analyses.

For an overview which features use which resource, and how to export all third-party resource references in a `bibtex` string, consult the [documentation](https://elfen.readthedocs.io).

## Acknowledgements

While all feature extraction functions in this package are written from scratch, the choice of features in the readability and lexical richness feature areas (partially) follows the [`readability`](https://github.com/andreasvc/readability) and [`lexicalrichness`](https://github.com/LSYS/LexicalRichness) Python packages.

We use the [`wn`](https://github.com/goodmami/wn) Python package to extract Open  Multilingual Wordnet synsets.

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
