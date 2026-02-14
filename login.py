import streamlit as st

code_input = st.text_input("Please enter the access code:", max_chars=20, key="access_code", \
    type="password")

