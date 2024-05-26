from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "PROJECT.md").read_text()

setup(
    name='streamlit-islands',
    version='0.0.5',
    author='Anas Bouzid',
    author_email='anasbouzid@gmail.com',
    description='Separate static content from dynamic content in Streamlit',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/bouzidanas/streamlit-islands",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
    ],
)