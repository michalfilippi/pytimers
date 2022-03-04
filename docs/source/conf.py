import os
import sys

sys.path.insert(0, os.path.abspath("../.."))


# -- Project information -----------------------------------------------------

project = "pytimers"
copyright = "2022, Michal Filippi"
author = "Michal Filippi"

# The full version, including alpha/beta/rc tags
release = "3.0"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"
html_theme_options = {
    "description": "Measuring time to run functions, methods or blocks of code made easy.",
    "logo": "stopwatch_400.png",
    "github_user": "michalfilippi",
    "github_repo": "pytimers",
    "github_button": "true",
    "github_count": "none",
    "show_related": "true",
    # "extra_nav_links": "true",
}
html_title = f"Pytimers Documentation (3.0)"
html_sidebars = {
    # "index": [],
    "**": [
        "about.html",
        "navigation.html",
        # "localtoc.html",
        # "globaltoc.html",
        "relations.html",
        "searchbox.html",
    ],
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
