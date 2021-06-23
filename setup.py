import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytimers",
    version="2.3",
    author="Michal Filippi",
    author_email="michal.filippi@gmail.com",
    description="Timing of functions, methods or blocks of code made easy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/michalfilippi/pytimers",
    packages=setuptools.find_packages(),
    install_requires=[
        "decorator",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
