import streamlit as st
from __init__ import *

def say_hello(name):
    st.write(name*10)

def add(a, b):
    if st.button('Show the result'):
        st.toast("The result is: " + str(a + b)) 

# Test the function
files = ["test.md", "../README.md"]
for file in files:
    content1 = load_content(file)
    st.markdown("---")