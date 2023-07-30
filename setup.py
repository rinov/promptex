# Copyright (c) 2023 rinov

from io import open
from setuptools import find_packages, setup

setup(
    name="promptex",
    version="0.1.0",
    author="rinov",
    author_email="rinov@rinov.jp",
    description="Efficiently manage prompts used as input for GPT",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords="gpt,prompt,promptex",
    license="MIT",
    url="https://github.com/rinov/promptex",
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    install_requires=["tiktoken>=0.3.3"],
    python_requires=">=3.8.0",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
