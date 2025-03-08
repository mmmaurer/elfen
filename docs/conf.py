# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
from pathlib import Path
import sys

setup_py_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
elfen_dir = os.path.join(setup_py_dir, 'elfen')

# Add "../" to the system path
sys.path.insert(0, setup_py_dir)

# Add the package directory to the system path
sys.path.insert(0, os.path.abspath(elfen_dir))

project = 'ELFEN'
copyright = '2025, Maximilian Maurer'
author = 'Maximilian Maurer'
release = '1.1.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.mathjax',
    'sphinx_copybutton',
    'sphinx.ext.autodoc.preserve_defaults',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# autodoc_default_options = {
#     'show-inheritance': True,
#     'ignore-module-all': True,
#     'no-value': True  # Exclude default values for parameters
# }

autodoc_docstring_signature = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

autodoc_default_flags = ['members', 'undoc-members', 'private-members', 'special-members']

