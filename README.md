# ELFEN - Efficient Linguistic Feature Extraction for Natural Language Datasets

This python package provides efficient linguistic feature extraction for text datasets (i.e. datasets with N text instances, in a tabular structure). 

For a full overview of the features available, check the [overview table](features.md), for further details and tutorials check the
[Documentation (TODO)]()


## Installation

(Currently, final version should be pip install [final name])

Step 1: Download this repo
```bash
git clone git@github.com:mmmaurer/flfe.git
```

Step 2: Move to the dir and install using pip
```bash
cd flfe && pip install -e .
```

Step 3: If you want to use the spacy backbone, download the respective model, e.g. "en_core_web_sm":
```bash
python -m spacy download en_core_web_sm
```

Step 4: To use wordnet features, download open multilingual wordnet using:
```bash
python -m wn download omw:1.4
```

## Usage of third-party resources usable in this package
Please refer to the original author's licenses and conditions for usage, and cite them if you use the resources through this package in your analyses.


## Citation
If you use this package in your work, for now, please cite
```bibtex
@misc{maurer-2024-elfen,
  author = {Maurer, Maximilian},
  title = {ELFEN - Efficient Linguistic Feature Extraction for Natural Language Datasets},
  year = {2024},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/mmmaurer/elfen}},
}
```