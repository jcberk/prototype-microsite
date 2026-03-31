import streamlit as st
from streamlit_gsheets import GSheetsConnection
import os

st.set_page_config(page_title="PROTOTYPE: Hunger in US Classrooms")

def credits():
    container = st.container()
    container.markdown("#### * Data Note")
    container.write("\"Live\" data in this prototype is from March 23, 2026.")
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

    pg.run()

else:

    @st.cache_data
    def get_data_urls():
        url = os.environ["data_secret"]
        conn = st.connection("gsheets", type=GSheetsConnection)
        return conn.read(spreadsheet=url)

    if 'data_urls' not in st.session_state:
        st.session_state.data_urls = dict(get_data_urls().values)

    map_page = st.Page("map.py", title="Live* classroom needs")
    metro_page = st.Page("metro.py", title="Hunger and nutrition by metro area")
    pg = st.navigation([map_page, metro_page])

    pg.run()

    credits()
