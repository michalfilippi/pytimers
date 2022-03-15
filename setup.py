import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytimers",
    version_config=True,
    author="Michal Filippi",
    author_email="michal.filippi@gmail.com",
    description="Measuring time to run functions, methods or blocks of code made easy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/michalfilippi/pytimers",
    packages=setuptools.find_packages(),
    setup_requires=["setuptools-git-versioning"],
    install_requires=[
        "decorator>=4.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
