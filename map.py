# Imports

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import os

# Maintain state

for key in st.session_state:
    st.session_state[key] = st.session_state[key]

# Get data

@st.cache_data
def get_live_ish_schools():
    url = st.session_state.data_urls["live-hunger-2026-03-23"]
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn.read(spreadsheet=url)

live_ish_schools = get_live_ish_schools()

# Display page

st.header("Hunger in Your Communities: Live* Classroom Needs")

st.markdown("This live view shows classroom hunger-related projects across the US \
    to help local teams take immediate action.")

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader(f"{live_ish_schools['Project Count'].sum():,} Active Hunger Projects")
with col2:
    st.subheader(f"${live_ish_schools['Project Total Cost Breakdown Total Cost'].sum():,.2f} \
        Total Requested")
with col3:
    st.subheader(f"${live_ish_schools['Project Total Cost To Complete (Not Including Match)'].sum():,.2f} \
        Still Needed")

st.page_link(page="https://www.donorschoose.org/donors/search.html?subject8=-8", \
    label="[To Come] Click a school to fund now or export a list to share with your local team.")

mappable_live_ish_schools = live_ish_schools.dropna(subset=["Latitude","Longitude"]).copy()

def label_color(row):
    if row['School Percentage Free Lunch'] >= 50:
        return "#ff0000"
    if row['School Percentage Free Lunch'] < 50:
        return "#ffc000"
    return "#00ff00"
mappable_live_ish_schools.loc[:, "color"] = mappable_live_ish_schools.apply(label_color, axis=1)

st.map(data=mappable_live_ish_schools, latitude="Latitude", longitude="Longitude", color="color")
st.caption("Red = schools with live* hunger projects, 50+% free/reduced-price lunch")
st.caption("Yellow = schools with live* hunger projects, <50% free/reduced-price lunch")
