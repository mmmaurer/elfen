# ELFEN - Efficient Linguistic Feature Extraction for Natural Language Datasets

## Description
A python package to efficiently extract linguistic features at scale for text datasets.

## Keywords
*text as data*, *linguistic features*, *feature extraction*, *nlp*

## Science Usecase(s)
Though none of the following example use our package, the features can be used, for example, for:
- Assessment of stylistic differences of social media texts for different sociodemographic groups [(e.g. Flekova et al., 2016)](https://aclanthology.org/P16-2051/)
- Finding patterns in LLM-produced text [(e.g. Miaschi et al., 2024)](https://aclanthology.org/2024.emnlp-main.166/)

## Repo Structure
The repo follows the usual structure of a python package.

It contains two main directories: ``elfen/docs`` and ``elfen/elfen``.

The top-level directory ``elfen`` contains files to define the package (`pyproject.toml`), the license file, READMEs along with some documentation files.

``elfen/docs`` contains the reStructuredText files and configuration code for creating and rendering the documentation for the package.

``elfen/elfen`` contains the package's code structured in python files per feature area, the main extractor class, and utilities. 
```
elfen
├── docs
└── elfen
```


## Environment Setup
This method requires 3.10<=Python<=3.12.9, 
dependencies are defined in `pyproject.toml`.

To install the package along with the necessary dependencies, run

```bash
python -m pip install elfen
```

If you want to use the spacy backbone, you will need to download the respective model, e.g. "en_core_web_sm":
 ```bash
 python -m spacy download en_core_web_sm
 ```

For the full functionality, some external resources are necessary. While most of them are downloaded and located automatically, some have to be loaded manually.

To use wordnet features, download open multilingual wordnet using:
```bash
python -m wn download omw:1.4
```

Note that for some languages, you will need to install another wordnet collection. For example, for German, you can use the following command:

```bash
python -m wn download odenet:1.4
```

For more information on the available wordnet collections, consult the [wn package documentation](https://wn.readthedocs.io/en/latest/guides/lexicons.html).

## Input Data
The input data is any textual data a user may want to extract linguistic features for.

The expected format is a [polars](https://pola.rs/) dataframe with a column containing text instances.

## Sample Input and Output Data

The input is a polars dataframe with a column containing text instances:

```
> print(df)

shape: (2, 3)
┌────────────────────────────────┬─────────┬───────────┐
│ text                           ┆ subject ┆ condition │
│ ---                            ┆ ---     ┆ ---       │
│ str                            ┆ str     ┆ str       │
╞════════════════════════════════╪═════════╪═══════════╡
│ This is a test sentence.       ┆ A       ┆ C         │
│ This is another test sentence. ┆ B       ┆ D         │
└────────────────────────────────┴─────────┴───────────┘
```

Running the extraction of a single feature, for example ``n_tokens`` using the ``Extractor`` will yield the original dataframe with a column containing the extracted feature:

```
> print(extractor.data)

shape: (2, 4)
┌────────────────────────────────┬─────────┬───────────┬──────────┐
│ text                           ┆ subject ┆ condition ┆ n_tokens │
│ ---                            ┆ ---     ┆ ---       ┆ ---      │
│ str                            ┆ str     ┆ str       ┆ i64      │
╞════════════════════════════════╪═════════╪═══════════╪══════════╡
│ This is a test sentence.       ┆ A       ┆ C         ┆ 6        │
│ This is another sentence.      ┆ B       ┆ D         ┆ 5        │
└────────────────────────────────┴─────────┴───────────┴──────────┘
```

In practice, ``extractor.data`` will contain the additional helper columns ``nlp``, and ``tokens`` and/or ``types`` (depending on which features are extracted).

To write the original dataframe including the extracted features but not the helper columns, a user can run the following command for saving the dataframe to a CSV file.

```
extractor.write_csv("path/to/csv/")
```


## Acknowledgements

While all feature extraction functions in this package are written from scratch, the choice of features in the readability and lexical richness feature areas (partially) follows the [`readability`](https://github.com/andreasvc/readability) and [`lexicalrichness`](https://github.com/LSYS/LexicalRichness) python packages.

We use the [`wn`](https://github.com/goodmami/wn) python package to extract Open  Multilingual Wordnet synsets.

## Disclaimer
### Multiprocessing and limiting the numbers of cores used
The underlying dataframe library, polars, uses all available cores by default.
If you are working on a shared server, you may want to consider limiting the resources available to polars.
To do that, you will have to set the ``POLARS_MAX_THREADS`` variable in your shell, e.g.:

```bash
export POLARS_MAX_THREADS=8
```

### Usage of some of the features
The extraction of psycholinguistic, emotion/lexicon and semantic features available through this package relies on third-party resources such as lexicons.
Please refer to the original author's licenses and conditions for usage, and cite them if you use the resources through this package in your analyses.

For an overview which features use which resource, and how to export all third-party resource references in a `bibtex` string, consult the [documentation](https://elfen.readthedocs.io).