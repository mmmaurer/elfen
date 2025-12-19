
THE NRC VALENCE, AROUSAL, AND DOMINANCE LEXICON (aka THE NRC VAD LEXICON)
-------------------------------------------------------------------------

Version: 	1
Released: 	July 2018
Copyright: 	2018 National Research Council Canada (NRC)
Created By: Dr. Saif M. Mohammad (Senior Research Scientist, National Research Council Canada)

README Last Updated: August 2022
Automatic translations from English to 108 languages was last updated: August 2022

Home Page:  http://saifmohammad.com/WebPages/nrc-vad.html

Contact:  	Dr. Saif M. Mohammad
          	saif.mohammad@nrc-cnrc.gc.ca
          	uvgotsaif@gmail.com

TABLE OF CONTENTS

  		  	I. 	  General Description
  		  	II.   Papers And Citation
  		  	III.  Python Code To Analyze Emotions In Text
  		  	IV.   NRC VAD Lexicon In Various Languages
  		  	V.    Using Polar Terms Only, Rescaling, Lemmatization, And Other Techniques That May Be Beneficial  
		    VI.   Forms Of The Lexicon, Files, And Format
		    VII.  Version Information And Change Log
			VIII. Other Emotion Lexicons
  		  	IX.   Terms Of Use
  		  	X.    Ethical Considerations
 

I. GENERAL DESCRIPTION
----------------------

Words play a central role in language and thought. Several influential factor analysis studies have shown that
the primary dimensions of word meaning are valence, arousal, and dominance (VAD). 
- valence is the positive--negative or pleasure--displeasure dimension; 
- arousal is the excited--calm or active--passive dimension; and 
- dominance is the powerful--weak or 'have control'--'have no control' dimension.

The NRC Valence, Arousal, and Dominance (VAD) Lexicon includes a list of more than 20,000 English words and
their valence, arousal, and dominance scores.  For a given word and a dimension (V/A/D), the scores range from
0 (lowest V/A/D) to 1 (highest V/A/D).  The lexicon with its fine-grained real-valued scores was created by
manual annotation using best--worst scaling.  The lexicon is markedly larger than any of the existing VAD
lexicons. We also show that the ratings obtained are substantially more reliable than those in existing
lexicons. (See associated paper for details.)

Applications: The NRC VAD Lexicon has a broad range of applications in Computational Linguistics, Psychology,
Digital Humanities, Computational Social Sciences, and beyond. Notably it can be used to:
- study how people use words to convey emotions.
- study how emotions are conveyed through literature, stories, and characters.
- obtain features for machine learning systems in sentiment, emotion, and other affect-related tasks and 
  to create emotion-aware word embeddings and emotion-aware sentence representations.
- evaluate automatic methods of determining V, A, and D (using NRC VAD entries as gold/reference scores).
- study psychological models of emotions.
- study the role of high VAD words in high emotion intensity sentences, tweets, snippets from literature.

An Interactive Visualization of the NRC VAD Lexicon is available here: 
http://saifmohammad.com/WebPages/nrc-vad.html#Viz

Companion lexicons -- the NRC Emotion Lexicon and the NRC Emotion Intensity Lexicon are available here:
http://saifmohammad.com/WebPages/lexicons.html

This study was approved by the NRC Research Ethics Board (NRC-REB) under protocol number 2017-98. REB review
seeks to ensure that research projects involving humans as participants meet Canadian standards of ethics.


II. PAPERS AND CITATION
-----------------------

Details of the NRC VAD Lexicon are available in this paper:

- Obtaining Reliable Human Ratings of Valence, Arousal, and Dominance for 20,000 English Words.  Saif M.
Mohammad. In Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics,
Melbourne, Australia, July 2018.

A copy of the paper is included in this package (VAD-ACL2018.pdf).

If you use the lexicon in your work, then:

- Cite the paper:
		@inproceedings{vad-acl2018,
  			title={Obtaining Reliable Human Ratings of Valence, Arousal, and Dominance for 20,000 English Words},
 			author={Mohammad, Saif M.},
    		booktitle={Proceedings of The Annual Conference of the Association for Computational Linguistics (ACL)},
    		year={2018},
    		address={Melbourne, Australia}
		}	

- Point to the lexicon homepage: 
		http://saifmohammad.com/WebPages/nrc-vad.html

Other relevant papers:

- Practical and Ethical Considerations in the Effective use of Emotion and Sentiment Lexicons.
  Saif M. Mohammad. arXiv preprint arXiv:2011.03492. November 2020.

- Ethics Sheet for Automatic Emotion Recognition and Sentiment Analysis.
  Saif M. Mohammad. Computational Linguistics. 48 (2): 239–278. June 2022.



III. PYTHON CODE TO ANALYZE EMOTIONS IN TEXT
--------------------------------------------

There are many third party software packages that can be used in conjunction with the NRC
VAD Lexicon to analyze emotion word use in text. We recommend Emotion Dynamics:

	https://github.com/Priya22/EmotionDynamics

It is the primary package that we use to analyze text using the NRC Emotion Lexicon and
the NRC VAD Lexicon.  It can be used to generate a csv file with a number of emotion
features pertaining to the text of interest, including metrics of utterance emotion
dynamics.

See this paper for an example of the use of the lexicon to analyze emotions in text:

	Tweet Emotion Dynamics: Emotion Word Usage in Tweets from US and Canada. Krishnapriya
	Vishnubhotla and Saif M. Mohammad. In Proceedings of the 13th Language Resources and
	Evaluation Conference (LREC-2022), May 2022, Marseille, France.

	https://arxiv.org/pdf/2204.04862.pdf


IV. NRC VAD LEXICON IN VARIOUS LANGUAGES
-----------------------------------------

The NRC VAD Lexicon has annotations for English words. Despite some cultural
differences, it has been shown that a majority of affective norms are stable across
languages. Thus, we provide versions of the lexicon in over 100 languages by translating
the English terms using Google Translate (August 2022).

The lexicon is thus available for English and these languages:

Afrikaans, Albanian, Amharic, Arabic, Armenian, Azerbaijani, Basque, Belarusian, Bengali,
Bosnian, Bulgarian, Burmese, Catalan, Cebuano, Chichewa, Corsican, Croatian, Czech,
Danish, Dutch, Esperanto, Estonian, Filipino, Finnish, French, Frisian, Gaelic, Galician,
Georgian, German, Greek, Gujarati, HaitianCreole, Hausa, Hawaiian, Hebrew, Hindi, Hmong,
Hungarian, Icelandic, Igbo, Indonesian, Irish, Italian, Japanese, Javanese, Kannada,
Kazakh, Khmer, Kinyarwanda, Korean, Kurmanji, Kyrgyz, Lao, Latin, Latvian, Lithuanian,
Luxembourgish, Macedonian, Malagasy, Malay, Malayalam, Maltese, Maori, Marathi, Mongolian,
Nepali, Norwegian, Odia, Pashto, Persian, Polish, Portuguese, Punjabi, Romanian, Russian,
Samoan, Sanskrit, Serbian, Sesotho, Shona, Simplified, Sindhi, Sinhala, Slovak, Slovenian,
Somali, Spanish, Sundanese, Swahili, Swedish, Tajik, Tamil, Tatar, Telugu, Thai,
Traditional, Turkish, Turkmen, Ukranian, Urdu, Uyghur, Uzbek, Vietnamese, Welsh, Xhosa,
Yiddish, Yoruba, Zulu

Note that an earlier version included translations obtained in 2018. The current 2022
translations are markedly better. That said, some of the translations are still incorrect
or they may simply be transliterations of the original English terms.


V. USING POLAR TERMS ONLY, RESCALING, LEMMATIZATION, AND OTHER TECHNIQUES THAT MAY BE BENEFICIAL
------------------------------------------------------------------------------------------------

The lexicon file can be used as is, but occasionally certain additional techniques can be
applied to make the most of it for one's specific application context.

1. POLAR SUBSET: For some applications it is more suitable to ignore neutralish words
(terms with V/A/D scores close to the middle of the scale) and only consider the more
polar words (terms with V/A/D scores close to the two ends of the scale).  There is no one
universally ``correct'' threshold; different thresholds simply make the polar and neutral
classes more or less restrictive. We provide one version of such a polar lexicon
(described below), but one can easily create their own version from the full lexicon by
excluding terms based on their own pre-chosen thresholds.  (One can also determine
threshold suitable for their application by tuning on a development set.)

The OneFilePerDimension/PolarSubset directory, provides a version of the valence lexicon
with only those entries that have scores less than or equal to 0.3333 (negative words) and
scores greater than or equal to 0.6667 (positive words).  Similarly, the directory has
arousal and dominance lexicons with only those entries that have scores less than or equal
to 0.3333 (low arousal/dominance words) and greater than or equal to 0.6667 (high
arousal/dominance words). The entries with scores between 0.3333 and 0.6667 for a given
dimension are considered neutral for that dimension.

Disregarding the large number of neutralish words has an additional benefit of sharpening
the contrast when comparing average emotion scores across two sets of texts. For example,
when comparing the average valence across different genres of novels, including a large
number of neutralish terms in the lexicons leads to average scores close to the mid-point
score (0.5) for all genres, whereas only including polar terms will show greater
disparities in their average scores.


2. RESCALING AND BIPOLAR -1 to 1 SCALE: The default form of the lexicon has entries with
real-valued scores between 0 and 1. However, the scores themselves have no inherent
meaning other than being an indication of relative score. (For example, a term with a
higher valence score than another term, is expected to be more positive than the other
term.) Thus, for one's specific application, if needed, the scores can be rescaled to
other ranges such as 0 to 100 or -1 to 1.  

The -1 to 1 scale version of the lexicon may be of particular interest because:

a. Valence, arousal, and dominance are generally considered bipolar scales.  When rescaled
to the -1 to 1 range, the highly polar terms have scores close to -1 and 1, and a large
number of neutralish terms have scores around 0. 

b. Highly polar words are often more informative for machine learning tasks than neutral
words.  Thus when features are derived from lexicons, it is often more useful for feature
values of polar terms to have higher scores than feature values of neutral words.  Thus,
using a -1 to 1 scale and taking the absolute values of the scores will often lead to
better features than deriving features using a 0 to 1 scale.

The bipolar -1 to 1 scale lexicon is available in the BipolarScale directory.


3. ANALYZING HIGH AND LOW V/A/D SEPARATELY: Analyzing high and low V/A/D  word usage
separately will provide more detailed insights than analyzing average V/A/D alone.  For
example, it helps distinguish cases with mostly neutral words from cases with many high-
and many low-valence words. It also helps determine whether greater use of high-V/A/D
words goes hand-in-hand with less frequent use of low-V/A/D word usage.


4. LEMMATIZATION: The lexicon largely includes the base forms or lemmas of words. For
example, it may include an entry for 'attack', but not for 'attacks' or 'attacking'. In
many cases, such morphological variants are expected to have similar emotion scores. So
one can first apply a third-party lemmatizer on the target text to determine the base forms
before applying the lexicon. Note that lemmatization must be applied with care; for
example, while it it good to go from 'helplessness' to 'helpless' (they are expected to
have similar emotional connotations), 'helplessness' should not be lemmatized to 'help'
(they are expected to have markedly different emotional connotations). Further, various
factors such as tense and 'differing predominant senses for different morphological forms'
can impact emotionality. So benefits of lemmatization are limited, especially when
analyzing large pieces of text.


5. OTHER: Other techniques such discarding highly ambiguous terms (terms with many
meanings), or identifying most common terms in one's text and inspecting emotion entries
in the lexicon for those terms (and correcting entries where appropriate), etc. are also
good practice.


VI. FORMS OF THE LEXICON, FILES, AND FORMAT
-------------------------------------------

1. NRC-VAD-Lexicon.txt: This is the main lexicon file with entries for ~20,000 English
words. It has four columns (separated by tabs):

- Word: The English word for which V, A, and D scores are provided. The words are listed in alphabetic order.
- Valence: valence score of the word
- Arousal: arousal score of the word
- Dominance: dominance score of the word

2. The directory 'OneFilePerDimension' has the same information as in NRC-VAD-Lexicon.txt,
but in multiple files -- one for each dimension: 

- valence-NRC-VAD-Lexicon.txt: Includes valence scores. The words are sorted in decreasing order of valence.
- arousal-NRC-VAD-Lexicon.txt: Includes arousal scores. The words are sorted in decreasing order of arousal.
- dominance-NRC-VAD-Lexicon.txt: Includes dominance scores. The words are sorted in decreasing order of dominance.


3. NRC-VAD-Lexicon-ForVariousLanguages.txt: This files has the same first four columns as
the NRC-VAD-Lexicon.txt.  Additionally, it has columns pertaining to over 100 languages.
Each of these columns lists the translations of the English words into the corresponding
language. For example, the column Japanese contains the Japanese translations of the
English words.  The translations were obtained using Google Translate in August 2022. 

4. The directory 'OneFilePerLanguage' has the same information as in
NRC-VAD-Lexicon-ForVariousLanguages.txt, but in multiple files -- one for each language.
Each of these files has five columns. The first four columns are the same as in
NRC-VAD-Lexicon.txt. The fifth column is the translation of the English words to a
different language -- the language corresponding to the file name. So if one is interested
only in the Japanese version of the NRC VAD Lexicon, then they can simply use
Japanese-NRC-VAD-Lexicon.txt.

5. The directory 'OneFilePerDimension/PolarSubset' has a version of the lexicon that only
includes polar terms (terms with scores <= 0.3333 or >= 0.6667).

6. The directory 'BipolarScale' has a version of the lexicon where the scores are
re-scaled to lie between -1 and 1. It has subdirectories 'OneFilePerDimension' and
'OneFilePerDimension/PolarSubset' with versions as described in 2 and 5, but in bipolar
scale.

7. ListOfLanguages-For-Which-Lexicon-Availabale.txt: Lists the languages for which the
lexicon is available.

8. Paper-VAD-ACL2018.pdf: Research paper describing the NRC VAD Lexicon.

9. Paper-Practical-Ethical-Considerations-Lexicons.pdf: Research paper describing
practical and ethical considerations in the effective use of emotion and sentiment
lexicons.

10. Paper-Ethics-Sheet-Emotion-Recognition.pdf: Research paper discussing ethical
considerations involved in automatic emotion recognition 'Ethics Sheet for Automatic
Emotion Recognition and Sentiment Analysis'.


ENCODING: The lexicon files were created using UTF-8 encoding. You can view the lexicon files using
most text editors, Microsoft Excel, etc. You might have to make sure that the viewer
supports characters from various languages, i.e., set the encoding option in the viewer to
UTF-8, etc.  For example, to view in excel, follow these steps:

- open excel
- click on File -> Import
- select file type as 'Text file'
- select the lexicon file to import in the dialog box that opens up
- select 'File Origin' type as 'Unicode (UTF-8)'
- click 'Finish'


VII. VERSION INFORMATION AND CHANGE LOG
---------------------------------------

- Version 1 is the latest version (Released July 2018).  
- The automatic translations generated using Google Translate are updated every few years.  
  They were last obtained in August 2022. 
- Versions of the lexicon in bipolar scale and that only include polar terms were included 
  in the package in August 2022.
- The README was last updated in August 2022.


VIII. OTHER EMOTION LEXICONS
----------------------------

- The NRC Emotion Lexicon includes a list of more than 14,000 English words and their
associations with eight emotions (anger, fear, anticipation, trust, surprise, sadness,
joy, and disgust) and two sentiments (negative and positive). 
	
	Crowdsourcing a Word-Emotion Association Lexicon, Saif Mohammad and Peter Turney, Computational
    Intelligence, 29 (3), 436-465, 2013.

	http://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm

- The NRC Emotion Intensity Lexicon is a list of English words (taken from the NRC Emotion
Lexicon and other sources) with real-valued scores of intensity for eight discrete emotions
(anger, anticipation, disgust, fear, joy, sadness, surprise, and trust).

	Word Affect Intensities. Saif M. Mohammad. In Proceedings of the 11th Edition of the Language 
	Resources and Evaluation Conference (LREC-2018), May 2018, Miyazaki, Japan.

    http://saifmohammad.com/WebPages/AffectIntensity.htm

Various other emotion lexicons can be found here:
http://saifmohammad.com/WebPages/lexicons.html

You may also be interested in some of the other resources and work we have done on the
analysis of emotions in text:

http://saifmohammad.com/WebPages/ResearchAreas.html
http://saifmohammad.com/WebPages/ResearchInterests.html#EmotionAnalysis


IX. TERMS OF USE
----------------

1. Research Use: The lexicon mentioned in this page can be used freely for non-commercial
research and educational purposes.

2. Citation: Cite the papers associated with the lexicon in your research papers and
articles that make use of them.

3. Media Mentions: In news articles and online posts on work using the lexicon, cite the
lexicon. For example: "We make use of the <resource name>, created by <author(s)> at the
National Research Council Canada." We would appreciate a hyperlink to the lexicon home
page and an email to the contact author (saif.mohammad@nrc-cnrc.gc.ca).  (Authors and
homepage information provided at the top of the README.)

4. Credit: If you use the lexicon in a product or application, then acknowledge this in
the 'About' page and other relevant documentation of the application by stating the name
of the resource, the authors, and NRC. For example: "This application/product/tool makes
use of the <resource name>, created by <author(s)> at the National Research Council
Canada." We would appreciate a hyperlink to the lexicon home page and an email to the
contact author (saif.mohammad@nrc-cnrc.gc.ca).

5. No Redistribution: Do not redistribute the data. Direct interested parties to the
lexicon home page.  You may not rent or license the use of the lexicon nor otherwise
permit third parties to use it.

6. Proprietary Notice: You will ensure that any copyright notices, trademarks or other
proprietary right notices placed by NRC on the lexicon remains in evidence.

7. Title: All intellectual property rights in and to the lexicon shall remain the property
of NRC. All proprietary interests, rights, unencumbered titles, copyrights, or other
Intellectual Property Rights in the lexicon and all copies thereof remain at all times
with NRC.

8. Commercial License: If interested in commercial use of the lexicon, contact the author:
saif.mohammad@nrc-cnrc.gc.ca

9. Disclaimer: National Research Council Canada (NRC) disclaims any responsibility for the
use of the lexicon and does not provide technical support. NRC makes no representation and
gives no warranty of any kind with respect to the accuracy, usefulness, novelty,
validity, scope, or completeness of the lexicon and expressly disclaims any implied
warranty of merchantability or fitness for a particular purpose of the lexicon.  That
said, the contact listed above welcomes queries and clarifications.

10 Limitation of Liability: You will not make claims of any kind whatsoever upon or
against NRC or the creators of the lexicon, either on your own account or on behalf of any
third party, arising directly or indirectly out of your use of the lexicon. In no event
will NRC or the creators be liable on any theory of liability, whether in an action of
contract or strict liability (including negligence or otherwise), for any losses or
damages incurred by you, whether direct, indirect, incidental, special, exemplary or
consequential, including lost or anticipated profits, savings, interruption to business,
loss of business opportunities, loss of business information, the cost of recovering such
lost information, the cost of substitute intellectual property or any other pecuniary loss
arising from the use of, or the inability to use, the lexicon regardless of whether you
have advised NRC or NRC has advised you of the possibility of such damages.


We will be happy to hear from you. For example,:
- telling us what you are using the lexicon for
- providing feedback regarding the lexicon;
- if you are interested in having us analyze your data for sentiment, emotion, and other affectual information;
- if you are interested in a collaborative research project. We regularly collaborate with graduate students,
post-docs, faculty, and research professional from Computer Science, Psychology, Digital Humanities,
Linguistics, Social Science, etc.

Email: Dr. Saif M. Mohammad (saif.mohammad@nrc-cnrc.gc.ca, uvgotsaif@gmail.com)


X. ETHICAL CONSIDERATIONS
-------------------------

Please see the papers below (included with the download) for ethical
considerations involved in automatic emotion detection and the use of emotion
lexicons. (These also act as the Ethics and Data Statements for the lexicon.)

- Ethics Sheet for Automatic Emotion Recognition and Sentiment Analysis.
Saif M. Mohammad. Computational Linguistics. 48 (2): 239–278. June 2022.

- Practical and Ethical Considerations in the Effective use of Emotion and Sentiment Lexicons.
Saif M. Mohammad. arXiv preprint arXiv:2011.03492. December 2020.

Note that the labels for words are *associations* (and not denotations). As noted in the
paper above, they are limited by when the dataset was annotated, by the people that
annotated them, historical perceptions, and biases. (See bullets c through h in the
paper). It is especially worth noting that identity terms, such as those referring to
groups of people may be particularly prone to inappropriate biases. Further, marginalized
groups have historically faced more negative perceptions. Thus some terms that are
associated with marginalized groups may be marked as having associations with negative
emotions by the annotators. For example, group X marked as being associated with negative
emotions could imply that they have historically faced negative emotions or that some
people have negative associations with group X, or there is some other reason for the
negative association. The exact relationship is not listed in the lexicon. In order to
avoid misinterpretation and misuse, and as recommended generally in the ethical
considerations paper, we have removed entries for a small number of terms (about 25) that
are associated with identity groups. For the vast majority of sentiment and emotion
analysis requirements this removal will likely have no impact or will be beneficial.

The list of identity terms used is taken from this list developed in 2019 on an offensive
language project (abusive language is often directed at some identity groups):

https://github.com/hadarishav/Ruddit/blob/main/Dataset/identityterms_group.txt

Only some of these terms occurred in our lexicon. This is not an exhaustive list; users
may choose to filter out additional terms for their particular task. We also welcome
requests for removal of additional terms from the list. Simply email us with the term or
terms and reason for removal.

