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
    metro_schools = metro_schools.rename(columns={\
        'Project Total Cost Breakdown Total Cost': 'Total Requested', \
        'Project Total Cost To Complete (Not Including Match)': 'Total To Complete', \
        'School (MDR demographics) Is 2025 Equity Focus School (Yes / No)': 'EFS'})

    st.header(f"School Hunger Projects, January 2024 through December 2025, {st.session_state.metro} Area")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"{metro_schools['Project Count'].sum():,}")
        st.write("Total projects")
    with col2:
        st.subheader(f"${metro_schools['Total Requested'].sum():,.2f}")
        st.write("Total requested")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"{metro_schools['Hunger Project Count'].sum():,}")
        st.write("Hunger projects")
    with col2:
        st.subheader(f"${metro_schools['Hunger Total Requested'].sum():,.2f}")
        st.write("Hunger total requested")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"{metro_schools.shape[0]:,}")
        st.write("Local schools")
    with col2:
        st.subheader(f"{metro_schools[metro_schools['EFS']=='Yes'].shape[0]:,}")
        st.write("DonorsChoose Equity Focus Schools")

    st.subheader("Schools with Most Hunger Requests")
    st.dataframe(metro_schools\
        [['School Name','EFS','Hunger Project Count','Hunger Total Requested']]\
        .sort_values(by='Hunger Project Count', ascending=False).head(10)\
        .style.format({'Hunger Total Requested': '${:,.2f}'}), hide_index=True)

    st.subheader("All area schools")

    mappable_metro_schools = metro_schools.dropna(subset=["Latitude","Longitude"])\
        .sort_values(by="Hunger Project Count").copy()  # Red and yellow dots drawn last so on top

    def label_color(row):
        if row['School Percentage Free Lunch'] >= 50 and row['Hunger Total Requested'] > 0:
            return "#ff0000"
        if row['School Percentage Free Lunch'] < 50 and row['Hunger Total Requested'] > 0:
            return "#ffc000"
        if row['School Percentage Free Lunch'] >= 50 and row['Hunger Total Requested'] == 0:
            return "#666666"
        if row['School Percentage Free Lunch'] < 50 and row['Hunger Total Requested'] == 0:
            return "#cccccc"
        return "#00ff00"
    mappable_metro_schools["color"] = mappable_metro_schools.apply(label_color, axis=1)

    st.map(data=mappable_metro_schools, latitude="Latitude", longitude="Longitude", color="color")
    st.caption("Red = schools with hunger projects, 50+% free/reduced-price lunch")
    st.caption("Yellow = schools with hunger projects, <50% free/reduced-price lunch")
    st.caption("Dark gray = schools with no hunger projects, 50+% free/reduced-price lunch")
    st.caption("Light gray = schools with no hunger projects, <50% free/reduced-price lunch")
