import streamlit as st
import pandas as pd
from utils.process_uploaded_ipg_file import process_uploaded_file
from utils.insert_non_duplicate import insert_non_duplicate_records
import sqlite3


# page config
st.set_page_config(page_title='Summary', layout='wide', initial_sidebar_state='expanded')


# Connect to the SQLite database
db_path = r'utils\ipg.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create Streamlit components
with st.container():
    with st.expander('Daily Available to Ship List', expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            selected_date = st.date_input('Choose a date', format="YYYY-MM-DD")

        with col2:
            qry = f'select distinct site from shipments'
            site = pd.read_sql_query(qry, conn)
            selected_site = st.selectbox('Select a Site', site)
        with col3:
            qry = f'select distinct product_group from shipments'
            pg = pd.read_sql_query(qry, conn)
            selected_pg = st.selectbox('Select a Product Group', pg)
        with col4:
            qry = f'select distinct rpt_run_time from shipments'
            run_time = pd.read_sql_query(qry, conn)
            selected_time = st.selectbox('Select the Hour', run_time)
    
        st.divider()
        # Daily available to ship list with lat and lng
        qry = ("SELECT s.site, s.product_group, s.bl_number, s.ship_to_customer, s.ship_to_city, s.state, "
        "SUM(s.pick_weight) AS net_pick_weight, SUM(s.number_of_pallet) AS total_number_of_pallet, "
        "c.lat, c.lng "
        "FROM shipments s "
        "LEFT JOIN coordinates c ON s.ship_to_city = upper(c.city_ascii) AND s.state = upper(c.state_id) "
        "WHERE s.site = ? AND s.product_group = ? AND DATE(s.rpt_run_date) = ? AND s.rpt_run_time = ? "
        "AND s.truck_appointment_date IS NULL AND s.product_code NOT LIKE 'INSERT%' AND s.bl_number NOT LIKE 'WZ%' "
        "GROUP BY s.bl_number "
        "ORDER BY s.state, s.ship_to_city ASC;")
        
        df= pd.read_sql_query(qry, conn, params=(selected_site, selected_pg, selected_date.strftime("%Y-%m-%d"), selected_time))
        st.dataframe(df)
        st.write(f'Total {len(df)} records')
        conn.close()

        st.divider()
        # make the map
    