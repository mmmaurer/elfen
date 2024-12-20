# Spacy uses the Universal Dependencies (UD) tagset for dependency parsing
# except for EN and DE languages. For these languages, Spacy uses the
# ClearNLP dependency labels.
CLEARNLP_DEPENDENCIES_CONFIG = [
   "acl", "acomp", "advcl", "advmod", "agent", "amod", "appos", "attr", "aux",
    "auxpass", "case", "cc", "ccomp", "compound", "conj", "csubj", "csubjpass",
    "dative", "dep", "det", "dobj", "expl", "intj", "mark", "meta", "neg",
    "nounmod", "npmod", "nsubj", "nsubjpass", "nummod", "oprd", "parataxis",
    "pcomp", "pobj", "poss", "preconj", "predet", "prep", "prt", "punct",
    "quantmod", "relcl", "root", "xcomp"
]

UNIVERSAL_DEPENDENCIES_CONFIG = [
   "nsubj", "obj", "iobj", "csubj", "ccomp", "xcomp", "obl", "vocative",
   "expl", "dislocated", "advcl", "advmod", "discourse", "aux", "cop", "mark",
    "nmod", "appos", "nummod", "acl", "amod", "det", "clf", "case", "conj",
    "cc", "fixed", "flat", "list", "parataxis", "compound", "orphan", "goeswith",
    "reparandum", "punct", "root", "dep"
]