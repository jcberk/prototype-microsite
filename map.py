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

st.header("Hunger in Your Communities: Live* Classroom Needs")

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader(f"{january_schools['Project Count'].sum():,} Active Hunger Projects")
with col2:
    st.subheader(f"${january_schools['Project Total Cost Breakdown Total Cost'].sum():,.2f} \
        Total Requested")
with col3:
    st.subheader(f"${january_schools['Project Total Cost To Complete (Not Including Match)'].sum():,.2f} \
        Still Needed")

mappable_january_schools = january_schools.dropna(subset=["Latitude","Longitude"]).copy()

def label_color(row):
    if row['School Percentage Free Lunch'] >= 50:
        return "#ff0000"
    if row['School Percentage Free Lunch'] < 50:
        return "#ffc000"
    return "#00ff00"
mappable_january_schools.loc[:, "color"] = mappable_january_schools.apply(label_color, axis=1)

st.map(data=mappable_january_schools, latitude="Latitude", longitude="Longitude", color="color")
st.caption("Red = schools with live hunger projects, 50+% free/reduced-price lunch")
st.caption("Yellow = schools with live hunger projects, <50% free/reduced-price lunch")
