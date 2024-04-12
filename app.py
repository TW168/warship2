import streamlit as st
import pandas as pd
from utils.process_uploaded_ipg_file import process_uploaded_file
from utils.insert_non_duplicate import insert_non_duplicate_records
import sqlite3



# page config
st.set_page_config(page_title='Summary', layout='wide', initial_sidebar_state='expanded')

db_path = r'utils\ipg.sqlite'


# uploaded_file = st.file_uploader('choose ipg report')
# if uploaded_file is not None:
#     df = pd.read_excel(uploaded_file)  # Specify the appropriate encoding
#     processed_df = process_uploaded_file(df)
#     insert_non_duplicate_records(processed_df, db_path)
    
# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create Streamlit components
with st.container():
    with st.expander('Site and Product Group', expanded=True):
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

    

        qry = f"select * from Shipments where site=? and product_group=? and rpt_run_date=? and rpt_run_time=? and truck_appointment_date is null and bl_number not like 'WZ%'"
        df = pd.read_sql_query(qry, conn, params=(selected_site, selected_pg, selected_date.strftime("%Y-%m-%d 00:00:00"), selected_time ))
        st.write(df)
        conn.close()
    
    