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