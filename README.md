streamlit-islands  [![Version](https://img.shields.io/pypi/v/streamlit-islands)](https://pypi.org/project/streamlit-islands/#history) 
[![PyPi - Downloads](https://img.shields.io/pypi/dm/streamlit-islands)](https://pypi.org/project/streamlit-islands/#files)[![Component Demo](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://islands-demo.streamlit.app/)
============

Separate static content from dynamic content in Streamlit

## Installation
Install [streamlit-islands](https://pypi.org/project/streamlit-islands/) with pip:
```bash
pip install streamlit-islands
```

## Overview
For content heavy Streamlit applications, it can be useful to separate static content from dynamic/interactive content. This package provides a way to do that by allowing you to define static content in markdown files which then leaves you to focus on the logic heavy parts of your application in your Streamlit script. 

To use this package, you define your static content in markdown files and insert special placeholders within the markdown in the locations where you want to insert dynamic content. The package then reads the markdown file and splits it at the placeholders. The static content is passed to `st.markdown` or `st.write` and the placeholders are replaced with calls to functions you define in your Streamlit script that contain the dynamic or interactive parts of the app.

### Why 'islands'?
The general idea here can be achieved in other ways but this package is designed to make it easy and to encourage a separation of concerns. Inspiration for the name comes from [Astro Islands](https://docs.astro.build/en/concepts/islands/).

While the concept of 'islands' architecture is not the same as what this package does, the idea of separating static and dynamic regions of the app is similar.

It might be useful to think of the dynamic parts of the app as 'islands' in a sea of static content. These islands are where the user interacts with the app and where the logic of the app is executed. Islands in the same app share the same global scope and thus can share data (variables, functions. etc) and state (`session_state`, etc).

>[!NOTE]
>*You can achieve something even closer to 'component islands' if you decorate the functions (that add dynamic parts of the script) with the `@st.experimental_fragment` decorator. This turns those dynamic parts of the script into fragments which can rerun independently of the full script!*

## Usage
To use this package, you need to have a markdown file that contains the static content of your Streamlit app and a Streamlit script that contains the dynamic content.

### Markdown file
The markdown file should contain the static content of your Streamlit app. Use placeholders to indicate where functions that add dynamic content should be called.

#### Placeholder format
The placeholders in the markdown file must be formatted as follows:

```
(empty line)
[function_name]: # (args)
This text here will NOT be added to the Streamlit app but will still be seen by markdown parsers.
(empty line)
```
The `function_name` should be the name of the function you define in your Streamlit script that contains the dynamic content. The args should be the arguments you want to pass to the function (seperated by commas). The arguments should what the function expects. For example, if the function expects a list of strings, the args should be in the format `['arg1', 'arg2']`. 

This special format is specifically designed to be ignored by markdown parsers so that the markdown file can still be rendered as expected. 

>[!NOTE]
>*The `args` inside the parentheses can span multiple lines.*

There is one additional requirement for the placeholders. There must be an empty line ***before AND after*** the placeholder. Anything that comes directly after (not separated by an empty line) will be removed before the markdown is added to the Streamlit app. This is to allow you to add backup content, comments, or other content to the markdown file that you don't want to be rendered in the app but you ***DO*** want to be rendered by markdown parsers.

#### Example: `my-markdown-file.md`
```markdown
# My header

This is a test of the markdown content for the `streamlit-islands` package.
This is a paragraph. It contains a few sentences. 

[add]: # (1, 2)

We start another paragraph here. This is a test of the markdown content for the `streamlit-islands` package.
This is a paragraph. It contains a few sentences.

[say_hello]: # ("Bob")

## A subheader
A new section of the document.
```

### Streamlit script
To load the static content and add the dynamic content, you can use the `load_content` function from the `streamlit_islands` package. 

```python
import streamlit as st
import streamlit_islands as sti
import os.path

def say_hello(name):
    st.write("Hello, " + name)

def add(a, b):
    if st.button('Show the result'):
        st.toast("The result is: " + str(a + b)) 

# Load the content of the markdown file
file_path = os.path.join(os.path.dirname(__file__), "my-markdown-file.md")
content = sti.load_content(file_path)
```

The dynamic/interactive sections of the app are added by the functions you define in your Streamlit script. The functions that you want to be seen by `load_content` must be placed above where `load_content` is called. The function names must also match the names in the placeholders in the markdown file. The arguments passed to the functions should match the arguments in those placeholders as well. 

>[!NOTE]
> *For organization purposes, you might want to have functions that are defined above `load_content` that you want to be ignored. You can do this using the `exclude` function from the `streamlit_islands` package.*

```python
import streamlit as st
import streamlit_islands as sti
import os.path

def say_hello(name):
    st.write("Hello, " + name)

def add(a, b):
    if st.button('Show the result'):
        st.toast("The result is: " + str(a + b)) 

# Exclude the function from being used by load_content
sti.exclude("say_hello")

# Load the content of the markdown file
file_path = os.path.join(os.path.dirname(__file__), "my-markdown-file.md")
content = sti.load_content(file_path)
```

## License
This project is licensed under the [MIT License](LICENSE.txt)