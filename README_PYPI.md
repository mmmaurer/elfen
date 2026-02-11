# ELFEN - Efficient Linguistic Feature Extraction for Natural Language Datasets

This Python package provides efficient linguistic feature extraction for text datasets (i.e. datasets with N text instances, in a tabular structure).

For further information, check the [GitHub repository](https://github.com/mmmaurer/elfen) and the [documentation](https://elfen.readthedocs.io)

## Using spacy models

If you want to use the spacy backbone, you will need to download the respective model, e.g. "en_core_web_sm":
 ```bash
 python -m spacy download en_core_web_sm
 ```

## Usage of third-party resources usable in this package
For the full functionality, some external resources are necessary. While most of them are downloaded and located automatically, some have to be loaded manually.

### WordNet features
To use wordnet features, download open multilingual wordnet using:
```bash
python -m wn download omw:1.4
```

Note that for some languages, you will need to install another wordnet collection. For example, for German, you can use the following command:

```bash
python -m wn download odenet:1.4
```

For more information on the available wordnet collections, consult the [wn package documentation](https://wn.readthedocs.io/en/latest/guides/lexicons.html).

### Emotion lexicons
The emotion lexicons used in this package have to be downloaded manually due to licensing restrictions.
After downloading, the extracted folders have to be placed in the respective directories.

To do so, download the intensity lexicons from the [NRC Emotion Intensity Lexicon page](https://saifmohammad.com/WebPages/AffectIntensity.htm), the association lexicons from the [NRC Emotion Association Lexicon page](https://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm) and the vad lexicons from the [NRC VAD Lexicon page](https://saifmohammad.com/WebPages/nrc-vad.html).

To use them in elfen, find the `elfen_resources` directory in your local elfen installation (for example with pip):

```
python -m pip show elfen
```

Then, the `elfen_resources` directory should be located in the same directory as the `elfen` package directory.

Create the following subdirectories if they do not exist yet:
- `elfen_resources/Emotion/Sentiment`
- `elfen_resources/Emotion/VAD`
- `elfen_resources/Emotion/Intensity`

Then, place the downloaded extracted zip folders in the respective directories:
- Place the extracted zip folder of the NRC Emotion Intensity Lexicon in `elfen_resources/Emotion/Intensity/`
- Place the extracted zip folder of the NRC Emotion Association Lexicon in `elfen_resources/Emotion/Sentiment/`
- Place the extracted zip folder of the NRC VAD Lexicon in `elfen_resources/Emotion/VAD/`

### Licences of lexicons
The extraction of psycholinguistic, emotion/lexicon and semantic features relies on third-party resources such as lexicons.
Please refer to the original author's licenses and conditions for usage, and cite them if you use the resources through this package in your analyses.

For an overview which features use which resource, and how to export all third-party resource references in a `bibtex` string, consult the [documentation](https://elfen.readthedocs.io).

## Multiprocessing and limiting the numbers of cores used
The underlying dataframe library, polars, uses all available cores by default.
If you are working on a shared server, you may want to consider limiting the resources available to polars.
To do that, you will have to set the ``POLARS_MAX_THREADS`` variable in your shell, e.g.:

```bash
export POLARS_MAX_THREADS=8
```

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