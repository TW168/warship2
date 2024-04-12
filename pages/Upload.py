import streamlit as st
import pandas as pd
from utils.process_uploaded_ipg_file import process_uploaded_file
from utils.insert_non_duplicate import insert_non_duplicate_records

db_path = r'utils\ipg.sqlite'

uploaded_file = st.file_uploader('choose ipg report')
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)  # Specify the appropriate encoding
    processed_df = process_uploaded_file(df)
    insert_non_duplicate_records(processed_df, db_path)
    