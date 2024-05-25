import streamlit as st
import streamlit.components.v1 as components
import os.path

def load_md(markdown_file_name, **kwargs):
    # if file name starts with the result of os.path.join("..", ""), then the path is relative to the parent directory
    parent_dir_prefix = os.path.join("..", "")
    current_dir_prefix = os.path.join(".", "")
    directory_symbol = os.path.join(" ", " ").strip()
    if markdown_file_name.startswith(parent_dir_prefix):
        markdown_file = os.path.join(os.path.split(os.path.dirname(__file__))[0], markdown_file_name.replace(parent_dir_prefix, ""))
    elif markdown_file_name.startswith(current_dir_prefix) or directory_symbol not in markdown_file_name:
        markdown_file = os.path.join(os.path.dirname(__file__), markdown_file_name.replace(current_dir_prefix, ""))
    else:
        markdown_file = markdown_file_name

    st.write(markdown_file)
    with open(markdown_file, "r") as f:
        md = f.read()
    return process_md(md, **kwargs)

def process_md(md, **kwargs):
    # Split the markdown into static and dynamic content
    # The dynamic content will be substituted in place of text
    # having the following format: \n[name]: # (list of arguments)\n
    # where 'name' is the name of a function that will generate the dynamic content
    # and the 'list of arguments' is a list of arguments that will be passed to this function
    static_content = []
    dynamic_content = []
    temp_content = []
    temp_call_name = ""
    temp_call_args = ""
    in_dynamic_content = False
    for line in md.split("\n"):
        if not in_dynamic_content and line.strip().startswith("[") and "]: # (" in line:
            temp_call_name = line.split("]: # (")[0][1:]
            temp_call_args = line.split("]: # (")[1][:-1]
            if line.strip().endswith(")"):
                in_dynamic_content = False
                dynamic_content.append([temp_call_name, temp_call_args])
            else:
                temp_call_args += line.split("]: # (")[1][-1]
                in_dynamic_content = True
            static_content.append("\n".join(temp_content))
        elif in_dynamic_content and line.strip().endswith(")"):
            temp_call_args += line[:-1].strip()
            dynamic_content.append([temp_call_name, temp_call_args])
            in_dynamic_content = False
        elif in_dynamic_content:
            temp_call_args += line.strip()
        else:
            temp_content.append(line)

    return static_content, dynamic_content
           

content1 = load_md("test.md")
content2 = load_md("../README.md")

st.markdown(content1[0][0])

st.write("---")

st.markdown(content2[0][0])

st.write("---")

st.write(content1[1])

st.write(content2[1])

