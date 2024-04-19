import streamlit as st
from utils.internal_shipments_ym import shipments_to_customer

def display_customer_data(customer):
    try:
        df = shipments_to_customer(customer, site='AMJK', product_group='SW')
        st.write(customer)
        st.dataframe(df)
        st.divider()
    except Exception as e:
        st.write(f"Failed to get data for {customer}. Error: {str(e)}")

customers = ['AMTOPP WAREHOUSE - HOUSTON', 'INTEPLAST GROUP CORP. (AMTOPP)', 'INTEPLAST GROUP CORP.(AMTOPP ( CFP)','PINNACLE FILMS']

for customer in customers:
    display_customer_data(customer)
