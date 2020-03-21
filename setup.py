import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytimers",
    version="1.1",
    author="Michal Filippi",
    author_email="michal.filippi@gmail.com",
    description="Python library for simple and easy to use code timing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/michalfilippi/pytimers",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)