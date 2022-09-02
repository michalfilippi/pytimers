import os

import setuptools


VERSION_FILE = os.path.join(os.path.dirname(__file__), "VERSION.txt")

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytimers",
    author="Michal Filippi",
    author_email="michal.filippi@gmail.com",
    description="Measuring time to run functions, methods or blocks of code made easy.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/michalfilippi/pytimers",
    packages=setuptools.find_packages(),
    setup_requires=["setuptools-git-versioning"],
    setuptools_git_versioning={
        "enabled": True,
        "version_file": VERSION_FILE,
        "count_commits_from_version_file": True,
        "dev_template": "{tag}.dev{timestamp:%Y%m%d%H%M%S}",
        "dirty_template": "{tag}.dev{timestamp:%Y%m%d%H%M%S}",
    },
    install_requires=[
        "decorator>=4.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    package_data={"pytimers": ["py.typed"]},
)
