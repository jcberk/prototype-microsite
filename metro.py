# Imports

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import os

# Maintain state

for key in st.session_state:
    st.session_state[key] = st.session_state[key]

# Set up metro areas with abbreviations for secret names
metros = {"Cleveland": "cleveland",\
    "Washington, DC": "dc"}

# Get data function

@st.cache_data
def get_metro_schools(metro):
    url = os.environ[metros[metro] + "_schools_secret"]
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn.read(spreadsheet=url)

# Display page

st.selectbox(label="Select metro area", options=metros.keys(), key="metro")

if 'metro' in st.session_state:

    metro_schools = get_metro_schools(st.session_state.metro)

    st.header(f"School Hunger Projects, January 2024 through December 2025, {st.session_state.metro} Area")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader(f"{metro_schools['Project Count'].sum():,}")
        st.write("Hunger projects")
    with col2:
        st.subheader(f"${metro_schools['Project Total Cost Breakdown Total Cost'].sum():,.2f}")
        st.write("Requested")
    with col3:
        st.subheader(f"${metro_schools['Project Total Cost To Complete (Not Including Match)'].sum():,.2f}")
        st.write("Remaining to Fund")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader(f"{metro_schools.shape[0]:,}")
        st.write("Local schools")
    with col2:
        st.subheader(f"{metro_schools[metro_schools['School (MDR demographics) Is 2025 Equity Focus School (Yes / No)']=='Yes'].shape[0]:,}")
        st.write("DonorsChoose Equity Focus Schools")

mappable_metro_schools = metro_schools.dropna(subset=["Latitude","Longitude"])

#mappable_metro_schools["color"] = "#ff0000"
mappable_metro_schools.loc[:,"color"] = ["#ff0000" if d >= 50 else "#ffc000" \
    for d in mappable_metro_schools["School Percentage Free Lunch"]]

st.map(data=mappable_metro_schools, latitude="Latitude", longitude="Longitude", color="color")
st.caption("&#x1F534; 50+% Free / Reduced Price Lunch, &#x1F7E1; < 50%")
