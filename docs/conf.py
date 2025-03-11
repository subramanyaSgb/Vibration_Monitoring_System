# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Vibration Monitoring System'
copyright = '2025, Deevia Software India Pvt Ltd'
author = 'Subramanya Gopal Bellary'

version = '1.0'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'recommonmark',  # Markdown support
    'sphinx.ext.autodoc',  # Automatic documentation from docstrings
    'sphinx.ext.viewcode',  # Add links to highlighted source code
    'sphinx.ext.napoleon',  # Support for Google-style docstrings
    'sphinx.ext.githubpages',  # GitHub pages integration
    'sphinx.ext.mathjax',  # Math support
    'sphinx_rtd_theme',  # ReadTheDocs theme
]

# Add support for both .rst and .md files
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# Markdown configuration
import recommonmark
from recommonmark.transform import AutoStructify

# AutoStructify configuration for better Markdown parsing
def setup(app):
    app.add_config_value('recommonmark_config', {
        'auto_toc_tree_section': 'Contents',
        'enable_auto_doc_ref': True,
        'enable_math': True,
        'enable_inline_math': True,
        'enable_eval_rst': True,
    }, True)
    app.add_transform(AutoStructify)

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for language output ----------------------------------------------
language = 'en'
locale_dirs = ['locale/']
gettext_compact = False

# -- Options for autodoc -----------------------------------------------------
# Automatically extract typehints when specified and place them in
# descriptions of the relevant function/method.
autodoc_typehints = 'description'
autodoc_member_order = 'bysource'
# Default role for `name` in the documentation
default_role = 'py:obj'


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
