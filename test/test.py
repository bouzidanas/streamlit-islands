import streamlit as st
import streamlit_islands as sti
import os.path

def say_hello(name):
    st.write(name*10)

@st.experimental_fragment
def add(a, b, id=None):
    if st.button('Show the result', key=id):
        st.toast("The result is: " + str(a + b))

# Test the function
files = ["../streamlit_islands/test.md", "../README.md"]
for file in files:
    file_path = os.path.join(os.path.dirname(__file__), file)
    content1 = sti.load_content(file_path)
    st.markdown("---")