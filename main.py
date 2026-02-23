import streamlit as st
import os

st.set_page_config(page_title="PROTOTYPE: Hunger in US Classrooms")

def credits():
    container = st.container()
    container.markdown("#### * Data Note")
    container.write("\"Live\" data in this prototype is from January 26, 2026.")
    container.write("This site uses data from DonorsChoose projects and data about schools \
        from the National Center for Education Statistics, via our partners at MDR Education.")
    container.write("This dashboard is a directional tool to inform strategy, not a \
        comprehensive measure of all school hunger. \
        Not all hunger needs appear on the DonorsChoose platform: many teachers \
        don't realize they can request support for these needs, and some school districts and \
        states have policies that suppress certain types of requests.")

if 'access_code' not in st.session_state or \
    st.session_state.access_code != os.environ["access_code_secret"]:
    login_page = st.Page("login.py", title="Enter access code")
    pg = st.navigation([login_page])

else:
    map_page = st.Page("map.py", title="Map of schools")
    metro_page = st.Page("metro.py", title="Metro areas")
    pg = st.navigation([map_page, metro_page])

pg.run()

if 'access_code' in st.session_state and \
    st.session_state.access_code == os.environ["access_code_secret"]:
    credits()
