from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="everything2text4prompt",
    version="0.0.10",
    description="Convert many medium into text, and the text format is specialized for prompt input",
    # package_dir={'': 'everything2text4prompt'},
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/michaelthwan/everything2text4prompt",
    author="michaethwan",
    author_email="michaelthwan@gmail.com",
    license="MIT",
    python_requires=">=3.8",
    install_requires=[
        "openai>=0.27.6",
        "youtube-transcript-api>=0.6.0",
        "bs4",
        "pypdf",
    ]
)
