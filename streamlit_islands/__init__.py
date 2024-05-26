import streamlit as st
import streamlit.components.v1 as components
import inspect
from ast import literal_eval
# import os.path

def load_md(markdown_file_name):
    # # if file name starts with the result of os.path.join("..", ""), then the path is relative to the parent directory
    # parent_dir_prefix = os.path.join("..", "")
    # current_dir_prefix = os.path.join(".", "")
    # directory_symbol = os.path.join(" ", " ").strip()
    # if markdown_file_name.startswith(parent_dir_prefix):
    #     markdown_file = os.path.join(os.path.split(os.path.dirname(__file__))[0], markdown_file_name.replace(parent_dir_prefix, ""))
    # elif markdown_file_name.startswith(current_dir_prefix) or directory_symbol not in markdown_file_name:
    #     markdown_file = os.path.join(os.path.dirname(__file__), markdown_file_name.replace(current_dir_prefix, ""))
    # else:
    #     markdown_file = markdown_file_name

    # Until I can get the code above to work, I will use the following code
    markdown_file = markdown_file_name

    with open(markdown_file, "r") as f:
        md = f.read()
    return process_md(md)

def process_md(md):
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

            if len(static_content) > 0:
                for index in range(len(temp_content)):
                    if temp_content[index].strip() == "":
                        static_content.append("\n".join(temp_content[index:]))
                        break
            else:
                static_content.append("\n".join(temp_content))
            temp_content = []
        elif in_dynamic_content and line.strip().endswith(")"):
            temp_call_args += line[:-1].strip()
            dynamic_content.append([temp_call_name, temp_call_args])
            in_dynamic_content = False
        elif in_dynamic_content:
            temp_call_args += line.strip()
        else:
            temp_content.append(line)

    # Make sure to add the last bit of static content        
    if len(temp_content) > 0:
        for index in range(len(temp_content)):
            if temp_content[index].strip() == "":
                static_content.append("\n".join(temp_content[index:]))
                break

    return static_content, dynamic_content

def call_local_function(function_name, arguments, function):
    try:
        function(*literal_eval(arguments))
    except Exception as e:
        st.error("**ERROR!** An exception occurred while calling the function <" + function_name + "> with arguments: " + str(arguments) + " (see exception below)")
        st.exception(e)

def load_content(markdown_file_name, use_write=False, **kwargs):
    static_content, dynamic_content = load_md(markdown_file_name)

    for index in range(len(static_content)):
        if use_write:
            st.write(static_content[index], **kwargs)
        else:
            st.markdown(static_content[index], **kwargs)
        if len(dynamic_content) > index:
            caller_globals = dict(inspect.getmembers(inspect.stack()[1][0]))["f_locals"]
            function_name = dynamic_content[index][0]
            function_args = "[" + dynamic_content[index][1] + "]"
            if function_name in caller_globals and callable(caller_globals[function_name]):
                call_local_function(function_name, function_args, caller_globals[function_name])
            else:
                st.error('**ERROR!** `streamlit-islands` could not find a function called `<' + function_name + ">` in the streamlit script. Make sure the function is defined above the call to `load_content`.")

    return static_content, dynamic_content