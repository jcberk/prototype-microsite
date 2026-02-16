# Imports

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import os

# Maintain state

for key in st.session_state:
    st.session_state[key] = st.session_state[key]

# Get data

@st.cache_data
def get_january_schools():
    url = os.environ["january_schools_secret"]
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn.read(spreadsheet=url)

january_schools = get_january_schools()

# Display page

st.header("Schools with Hunger Projects, January 2026")

mappable_january_schools = january_schools.dropna(subset=["Latitude","Longitude"])
st.map(data=mappable_january_schools, latitude="Latitude", longitude="Longitude")
