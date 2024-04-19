import streamlit as st
import pandas as pd
from utils.tomorrow_shipments import ftl, ltl, inteplast_shipments


st.write("Tomorrow")


with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_date = st.date_input("Date:")
    with col2:
        selected_site = st.selectbox("Site:", ("AMJK", "TXAS", "AMIN", "AMAZ"))
    with col3:
        selected_group = st.selectbox("Group:", ("SW",))
st.divider()

ftl_df = ftl(selected_date, selected_site, selected_group, selected_date)
tomorrow_ftl_wt = "{:,.0f}".format(ftl_df["SUM(pick_weight)"].sum())
tomorrow_ftl_plt = "{:,.0f}".format(ftl_df["SUM(number_of_pallet)"].sum())

ltl_df = ltl(selected_date, selected_site, selected_group, selected_date)
tomorrow_ltl_wt = "{:,.0f}".format(ltl_df["SUM(pick_weight)"].sum())
tomorrow_ltl_plt = "{:,.0f}".format(ltl_df["SUM(number_of_pallet)"].sum())

inteplast_shipment_df = inteplast_shipments(
    selected_date, selected_site, selected_group, selected_date
)
inteplast_shipment_df = inteplast_shipment_df.rename(
    columns={
        "bl_number": "BL Number",
        "carrier_id": "Carrier",
        "truck_appointment_date": "Appointment Date",
        "SUM(pick_weight)": "LBS",
        "SUM(number_of_pallet)": "PLT",
        "ship_to_customer": "Plant",
    }
)
inteplast_shipment_df["LBS"] = inteplast_shipment_df["LBS"].apply(
    lambda x: "{:,.0f}".format(x)
)

st.write(selected_site + " Tomorrow's Shipment Summary:")
summary_data = {
    "Shipment Type": ["FTL", "LTL"],
    "Total Weight": [tomorrow_ftl_wt, tomorrow_ltl_wt],
    "Total Pallets": [tomorrow_ftl_plt, tomorrow_ltl_plt],
}
summary_table = pd.DataFrame(summary_data)
st.table(summary_table)
st.table(inteplast_shipment_df)
