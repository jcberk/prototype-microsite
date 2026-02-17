import streamlit as st
import os

st.set_page_config(page_title="Hunger in US Schools")

if 'access_code' not in st.session_state or \
    st.session_state.access_code != os.environ["access_code_secret"]:
    login_page = st.Page("login.py", title="Enter access code")
    pg = st.navigation([login_page])

else:
    map_page = st.Page("map.py", title="Map of schools")
    metro_page = st.Page("metro.py", title="Metro areas")
    pg = st.navigation([map_page, metro_page])

pg.run()
