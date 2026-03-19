import streamlit as st

# ---- GLOBAL HEADER (CENTER TOP) ----
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image("assets/logo.png", width=250)



#----SET UP PAGE----
about_page = st.Page(
    page ="views/about_me.py",
    title ="About Me",
    icon = "😊",
    default=True,
    )
project_1_page = st.Page(
    page = "views/sales_dashboard.py",
    title = "sales Dashboard",
    icon  = "💵",
)



#---- Navigation Setup----
pg = st.navigation(pages  = [about_page , project_1_page])

#----SHARED ON ALL PAGES---
st.sidebar.image("assets/logo.png", width=200)

pg.run()