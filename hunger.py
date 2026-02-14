import streamlit as st

st.set_page_config(page_title="Hunger in US Schools")

# TODO move the code to secrets
if 'access_code' not in st.session_state or st.session_state.access_code != "test":
    login_page = st.Page("login.py", title="Enter access code")
    pg = st.navigation([login_page])

else:
    map_page = st.Page("map.py", title="Map of schools")
    pg = st.navigation([map_page])

pg.run()
