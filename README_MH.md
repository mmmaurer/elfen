---
format:
  html:
    embed-resources: true
  gfm: default
---

# ELFEN - Efficient Linguistic Feature Extraction for Natural Language Datasets
<!--
General specifications:
- This specification of the Methods Hub friendly README often uses the word 'should' to indicate the usual case. If you feel you need to do it differently, add a comment to argue for your case when you submit your method.
- A Methods Hub friendly README should contain all sections below that are not marked as optional, and can contain more sections.
- A Methods Hub friendly README should contain as few technical terms as possible and explain (or link to an explanation of) all used technical terms.
- A Methods Hub friendly README should link to all code files that it mentions using the [text](URL relative to this file) format. The relative URL (i.e., no "https://github.com") is neccessary for proper versioning in Methods Hub.
- A Methods Hub friendly README should contain an explanation (in the text) and an alternative for each image it contains (e.g., data models, pipeline, schema structure). Format: ![alternative text that describes what is visible in the image](URL relative to this file).
- A Methods Hub friendly README should link to authoritative sources rather than containing a copy of the information (e.g., documentation).
- A Methods Hub friendly README should use a uniform citation style for all references, for example APA7 https://apastyle.apa.org/style-grammar-guidelines/references/examples

Title:
1. The title must be the README's only first-level heading (line starting with a single '#').
2. The title should make the method's purpose clear.
3. The title (line 1 of this file) must be changed by you, but all other headings should be kept as they are.
4. The title must be appropriate (not harmful, derogatory, etc.).

Section templates:
The README template comes with text templates for each section (after each comment) that can be used, customized or removed as desired.
-->

## Description
<!--
1. Provide a brief and exact description of the method clearly mentioning its purpose i.e., what the method does or aims to achieve in abstract terms (avoiding technical details).
2. The focus should be on explaining the method in a way that helps users with different levels of expertise understand what it does, without going into technical details. It should clearly describe what inputs are needed and what outputs can be expected.
3. Briefly explain the input and output of the method and its note worthy features.
4. Provide link(s) to related papers from the social science domain using the method or similar methods for solving social science research questions. 
5. In a separate paragraph, highlight the reproducibility aspect of the method providing details or references to the resources used by the method, the data used in building the pre-trained modules etc.
6. It should also discuss the decisions and parameters controlling the behavior of the method.
-->

A Python package to efficiently extract linguistic features at scale for text datasets.

## Keywords

<!-- EDITME -->

* Text as data
* Linguistic features
* Feature extraction
* nlp

## Use Cases
<!--
1. The use cases section should contain a list of use cases relevant to the social sciences.
2. Each use case should start with a description of a task and then detail how one can use the method to assist in the task.
3. Each use case may list publications in which the use case occurs (e.g., in APA7 style, https://apastyle.apa.org/style-grammar-guidelines/references/examples).
-->

elfen has been used in a variety of use cases, for example:
- Analyzing differences between human-written and LLM-generated counterarguments (see [Dönmez, Maurer et al., 2025](https://aclanthology.org/2025.emnlp-main.1755/)).
- Perceived gendered text style differences (see [Chen et al., 2025](https://aclanthology.org/2025.emnlp-main.1602/)).
- Disagreement patterns of humans and LLMs for moral foundations and human values (see [Falk & Lapesa, 2025](https://aclanthology.org/2025.acl-long.1116/)).
- Analyzing LLM multi-agent communication (see [Parfenova et al., 2025](https://aclanthology.org/2025.blackboxnlp-1.12/)).

## Input Data
<!--
1. The input data section should illustrate the input data format by showing a (possibly abbreviated) example item and explaining (or linking to an explanation of) the data fields.
2. The input data section should specify which parts of the input data are optional and what effect it has to not provide these.
3. The input data section should link to a small example input file in the same repository that can be used to test the method (this test should be described in the section "How to Use").
-->

The input data is any textual data a user may want to extract linguistic features for.
The expected format is a [polars](https://pola.rs/) dataframe with a column containing text instances.

## Sample Input and Output Data
<!--
1. The output data section should illustrate the output data format by showing a (possibly abbreviated) example item and explaining (or linking to an explanation of) the data fields.
2. The output data section should link to a small example output file in the same repository that can be re-created (as far as the method is non-random) from the input data (as described in the section "How to Use").
-->

The input is a polars dataframe with a column containing text instances in the column "text", with two additional columns "subject" and "condition" for metadata:

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

## Hardware Requirements
<!--
1. The hardware requirements section should list all requirements (storage, memory, compute, GPUs, cluster software, ...) that exceed the capabilities of a cheap virtual machine provided by cloud computing company (2 x86 CPU core, 4 GB RAM, 40GB HDD).
2. If the method requires a GPU, the hardware requirements section must list the minimal GPU requirements (especially VRAM).
-->

Elfen is compatible with Python versions ≥ 3.10 and ≤ 3.12.11, on any supported hardware.

## Environment Setup
<!--
1. The environment setup section should list all requirements and provide all further steps to prepare an environment for running the method (installing requirements, downloading files, creating directoriees, etc.).
2. The environment setup section should recommend to use a virtual environment or similar if the programming language supports one.
-->

Dependencies are defined in `pyproject.toml`.

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

If you are running this in a Jupyter notebook on a binder instance, you can use `%%bash` magic commands to run the commands in a cell:
```bash
%%bash
python -m wn download omw:1.4
```

For more information on the available wordnet collections, consult the [wn package documentation](https://wn.readthedocs.io/en/latest/guides/lexicons.html).

For the full functionality of the emotion features, you will need to download the NRC emotion lexicon following [this guide](https://github.com/mmmaurer/elfen/blob/main/download_nrc.md).

## Repository structure

The repo follows the usual structure of a Python package.

It contains two main directories: ``elfen/docs`` and ``elfen/elfen``.

The top-level directory ``elfen`` contains files to define the package (`pyproject.toml`), the license file, READMEs along with some documentation files.

``elfen/docs`` contains the reStructuredText files and configuration code for creating and rendering the documentation for the package.

``elfen/elfen`` contains the package's code structured in Python files per feature area, the main extractor class, and utilities. 
```
elfen
├── docs
└── elfen
```

## How to Use
<!--
1. The how to use section should provide the list of steps that are necessary to produce the example output file (see section Output Data) after having set up the environment (see section Environment Setup).
2. The how to use section should explain how to customize the steps to one's own needs, usually through configuration files or command line parameters, or refer to the appropriate open documentation.
-->

For a comprehensive tutorial of all the features visit the [official documentation page](https://elfen.readthedocs.io/en/latest/tutorials.html#).

## Technical Details
<!--
1. The technical details section should proview a process overview, linking to key source code files at every step of the process.
2. In case a publication provides the details mentioned below, the technical details section should link to this publication using a sentence like "See the [publication](url-of-publication-best-using-doi) for ...". In this case, the mentioned technical details can be omitted from the section.
3. The technical details section should list all information needed to reproduce the method, including employed other methods and selected parameters.
4. The input data section should link to external data it uses, preferably using a DOI to a dataset page or to API documentation.
5. The technical details section should mention how other methods and their parameters were selected and which alternatives were tried.
6. The technical details section should for employed machine learning models mention on what kind of data they were trained.
-->

See the official [documentation](https://elfen.readthedocs.io/en/latest/index.html) for further information about technical details.

<!--## References -->
<!--
1. The references section is optional, especially if they are cited in a publication that explains the technical details (see section Technical Details).
2. The references section should provide references of publications related to this method (e.g., in APA7 style, https://apastyle.apa.org/style-grammar-guidelines/references/examples).
-->

## Acknowledgements
<!--
1. The acknowledgments section is optional.
2. The acknowledgments section should list expressions of gratitude to people or organizations who contributed, supported or guided.
-->

While all feature extraction functions in this package are written from scratch, the choice of features in the readability and lexical richness feature areas (partially) follows the [`readability`](https://github.com/andreasvc/readability) and [`lexicalrichness`](https://github.com/LSYS/LexicalRichness) Python packages.

We use the [`wn`](https://github.com/goodmami/wn) Python package to extract Open  Multilingual Wordnet synsets.

## Disclaimer
<!--
1. The disclaimer section is optional.
2. The disclaimer section should list disclaimers, legal notices, or usage restrictions for the method.
-->

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

## Contact Details
<!-- 
1. The contact details section should specify whom to contact for questions or contributions and how (can be separate entitites; for example email addresses or links to the GitHub issue board).
-->

Maintainer: Maximilian Maurer <maximilian.maurer@gesis.org>

Issue Tracker: [https://github.com/mmmaurer/elfen/issues](https://github.com/mmmaurer/elfen/issues)
