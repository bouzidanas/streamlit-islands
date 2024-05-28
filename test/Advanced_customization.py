import json
import streamlit as st
from code_editor import code_editor
from streamlit_islands import load_content
import os

# Opening JSON files
# You can also just use a dictionary but with files (JSON or text for example),
# its easier to transfer or use in multiple projects
def load_resources():
    with open('./test/resources/example_custom_buttons_bar_adj.json') as json_button_file:
        custom_buttons_alt = json.load(json_button_file)

    with open('./test/resources/example_custom_buttons_set.json') as json_button_file:
        custom_buttons = json.load(json_button_file)

    # Load Info bar CSS from JSON file
    with open('./test/resources/example_info_bar.json') as json_info_file:
        info_bar = json.load(json_info_file)

    # Load Code Editor CSS from file
    with open('./test/resources/code_editor.scss') as css_file:
        css_text = css_file.read()

    return custom_buttons, custom_buttons_alt, info_bar, css_text

def add_style():
    html_style_string = '''<style>
@media (min-width: 576px)
section div.block-container {
  padding-left: 20rem;
}
section div.block-container {
  padding-left: 4rem;
  padding-right: 4rem;
  max-width: 80rem;
}  
.floating-side-bar {
    display: flex;
    flex-direction: column;
    position: fixed;
    margin-top: 2rem;
    margin-left: 2.75rem;
    margin-right: 2.75rem;
}
.flt-bar-hd {
    color: #5e6572;
    margin: 1rem 0.1rem 0 0;
}
.floating-side-bar a {
    color: #b3b8c2;

}
.floating-side-bar a:hover {

}
.floating-side-bar a.l2 {

}
</style>'''

    st.markdown(html_style_string, unsafe_allow_html=True)

def setting_style_code_editor():
    code_setting_style = """# style dict for Ace Editor
ace_style = {"borderRadius": "0px 0px 8px 8px"}

# style dict for Code Editor
code_style = {"width": "100%"}

# set style of info bar dict from previous example
info_bar["style"] = {**info_bar["style"], "order": "1", "height": "2.0rem", "padding": "0rem 0.6rem", "padding-bottom": "0.2rem"}
response_dict = code_editor(your_code_string, height=20, info=info_bar, props={"style": ace_style}, component_props={"style": code_style})
"""
    info_bar["style"] = {**info_bar["style"], "order": "1", "height": "2.0rem", "padding": "0rem 0.6rem", "padding-bottom": "0.2rem"}
    code_editor(code_setting_style, height=20, info=info_bar, props={"style": {"borderRadius": "0px 0px 8px 8px"}});

def setting_css_code_editor():
    code_setting_css = """# CSS string for Code Editor
css_string = '''
font-weight: 600;
&.streamlit_code-editor .ace-streamlit-dark.ace_editor {
  background-color: #111827;
  color: rgb(255, 255, 255);
}
&.streamlit_code-editor .ace-streamlit-light.ace_editor {
        background-color: #eeeeee;
        color: rgb(0, 0, 0);
}'''

# same as previous example but with CSS string
response_dict = code_editor(your_code_string, height=20, info=info_bar, props={"style": ace_style}, component_props={"style": code_style, "css": css_string})"""
    css_string = '''
font-weight: 600;
&.streamlit_code-editor .ace-streamlit-dark.ace_editor {
  background-color: #111827;
  color: rgb(255, 255, 255);
}
&.streamlit_code-editor .ace-streamlit-light.ace_editor {
        background-color: #eeeeee;
        color: rgb(0, 0, 0);
}'''
    code_editor(code_setting_css, height=20, info=info_bar, props={"style": {"borderRadius": "0px 0px 8px 8px"}}, component_props={"css": css_string});

def css_result_code():
    css_result = """
.jBzdJR {
    font-weight: 500;
}
.jBzdJR.streamlit_code-editor .ace-streamlit-dark.ace_editor {
  background-color: #111827;
  color: rgb(255, 255, 255);
}
.jBzdJR.streamlit_code-editor .ace-streamlit-light.ace_editor {
        background-color: #eeeeee;
        color: rgb(0, 0, 0);
}"""
    st.code(css_result, language="css")

def demo_code_editor():
    code_styles_comp_demo = """# Load custom buttons from file
with open('example_custom_buttons_bar_adj.json') as json_button_file:
    custom_buttons = json.load(json_button_file)
# Load Info Bar from file
with open('example_info_bar.json') as json_info_file:
    info_bar = json.load(json_info_file)
# Load Code Editor CSS from file
with open('code_editor.scss') as css_file:
    css_text = css_file.read()
# construct component props dictionary (->Code Editor)
comp_props = {"css": css_text, "globalCSS": ":root {--streamlit-dark-background-color: #111827;}"}
# construct props dictionary (->Ace Editor)
ace_props = {"style": {"borderRadius": "0px 0px 8px 8px"}}
# add code editor component
response_dict = code_editor(your_code_string,  height = [19, 22], theme="contrast", buttons=custom_buttons, info=info_bar, component_props=comp_props, props=ace_props) 
# handle response to the Run button being clicked (command: submit)
if response_dict['type'] == "submit" and len(response_dict['text']) != 0:
    st.write("Response type: ", response_dict['type'])
    st.code(response_dict['text'], language=response_dict['lang'])"""
    # construct component props dictionary (->Code Editor)
    comp_props = {"css": css_text, "globalCSS": ":root {--streamlit-dark-background-color: #111827;}"}

    # construct props dictionary (->Ace Editor)
    ace_props = {"style": {"borderRadius": "0px 0px 8px 8px"}}
    response_dict = code_editor(code_styles_comp_demo,  height = [19, 22], theme="contrast", buttons=custom_buttons_alt, info=info_bar, component_props=comp_props, props=ace_props)

    if response_dict['type'] == "submit" and len(response_dict['text']) != 0:
        st.write("Response type: ", response_dict['type'])
        st.code(response_dict['text'], language=response_dict['lang'])

def floating_sidebar():
    floating_side_bar = '''
<div class="floating-side-bar">
    <span class="flt-bar-hd"> CONTENTS </span>
    <a href="#advanced-customization">Advanced customization</a>
    <a class="l2" href="#code-editor-component-layout">Code Editor component layout</a>
    <a class="l2" href="#customizing-the-ace-editor">Customizing the Ace Editor</a>
    <a class="l2" href="#style-and-css">Style and CSS</a>
    <a class="l3" href="#adding-classes">Adding classes</a>
    <a class="l3" href="#global-styles">Global styles</a>
    <a class="l3" href="#demo">Demo</a>
    <span class="flt-bar-hd"> LINKS </span>
    <a href="https://github.com/securingsincity/react-ace/blob/master/docs/Ace.md">general properties</a>
    <a href="https://github.com/securingsincity/react-ace/blob/master/src/types.ts">editor properties</a>
    <a href="https://github.com/ajaxorg/ace/wiki/Configuring-Ace#editor-options">editor options</a>
</div>
'''
    st.markdown(floating_side_bar, unsafe_allow_html=True)

def st_status(status, type="info"):
    if type == "info":
        st.info(status)
    elif type == "warning":
        st.warning(status)
    elif type == "success":
        st.success(status)

def st_image(image_path):
    st.image(image_path)

# The app ------------------------------------------------
custom_buttons, custom_buttons_alt, info_bar, css_text = load_resources()
col1, col2 = st.columns([6,2])
add_style()
with col1:
    file = "./markdown/advanced_customization.md"
    file_path = os.path.join(os.path.dirname(__file__), file)
    content1 = load_content(file_path)

with col2:
    floating_sidebar()
