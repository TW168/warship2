import pandas as pd
import streamlit as st
import sqlite3
from streamlit_folium import st_folium
import folium
from folium.plugins import MarkerCluster


# page config
st.set_page_config(page_title='Daily Shipment List', layout='wide', initial_sidebar_state='expanded')
st.title ('Daily Avaiable to Ship List & Map')


def create_shipment_list(conn):
    # Create Streamlit components
    with st.container():
        with st.expander('Daily Available to Ship List', expanded=True):
            # Define the site group mapping
            sites_groups = {
                'AMJK': ['SW','BP', 'CT'],
                'TXAS': ['SW'],
                'AMIN': ['SW'],
                'AMAZ': ['SW'],
                'PFCH': ['SW'],
                'AMSC': ['BP'],
                'VAMT': ['BP']
            }

            def get_sites(group):
                if group in sites_groups:
                    return sites_groups[group]
                else:
                    return None
                
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                selected_date = st.date_input('Choose a date', format="YYYY-MM-DD")

            with col2:
                sorted_sites = sorted(sites_groups.keys())
                if 'AMJK' in sorted_sites:
                    sorted_sites.remove('AMJK')
                    sorted_sites.insert(0, 'AMJK')  # Move 'AMJK' to the first position
                selected_site = st.selectbox("Select a site:", sorted_sites)
                # selected_site = st.selectbox("Select a site:", sorted(sites_groups.keys()))
                
            with col3:
                corresponding_groups = get_sites(selected_site)
                if corresponding_groups:
                    selected_group = st.selectbox("Select a group:", corresponding_groups)
                    
                else:
                    st.write("No groups found for the selected site.")
            with col4:
                qry = f'select distinct rpt_run_time from shipments order by rpt_run_time asc'
                run_time = pd.read_sql_query(qry, conn)
                selected_time = st.selectbox('Select the Hour', run_time)
        
            st.divider()
            # Daily available to ship list with lat and lng
            qry = ("SELECT s.site, s.product_group, s.bl_number, s.ship_to_customer, s.truck_appointment_date, s.ship_to_city, s.state, "
            "SUM(s.pick_weight) AS net_pick_weight, SUM(s.number_of_pallet) AS total_number_of_pallet, "
            "c.lat, c.lng "
            "FROM shipments s "
            "LEFT JOIN coordinates c ON upper(s.ship_to_city) = upper(c.city_ascii) AND upper(s.state) = upper(c.state_id) "
            "WHERE s.site = ? AND s.product_group = ? AND DATE(s.rpt_run_date) = ? AND s.rpt_run_time = ? "
            "AND s.truck_appointment_date IS NULL AND s.product_code NOT LIKE 'INSERT%' AND s.bl_number NOT LIKE 'WZ%' "
            "GROUP BY s.bl_number "
            "ORDER BY s.state, s.ship_to_city ASC;")
            
            df = pd.read_sql_query(qry, conn, params=(selected_site, selected_group, selected_date.strftime("%Y-%m-%d"), selected_time))
            st.dataframe(df)
            # Calculate sum of net_pick_weight and total_number_of_pallet columns
            net_weight = df['net_pick_weight'].sum()
            nbr_pallet = df['total_number_of_pallet'].sum()

            # Write the combined information in one line 
            st.write(f"Total net weight: {net_weight:,}, Total number of pallets: {nbr_pallet}")
            return df



def create_map(df):
    with st.container():
        with st.expander('Daily Available to Ship Map', expanded=True):
            # Check if DataFrame is empty
            if df.empty:
                st.write("No data available to display.")
                return
            
            # Drop rows with NaN values in lat or lng columns
            df = df.dropna(subset=['lat', 'lng'])

            # Check if DataFrame is empty after dropping NaN values
            if df.empty:
                st.write("No valid latitude or longitude values available to display.")
                return
            
            # Create the map
            m = folium.Map(location=[df["lat"].mean(), df["lng"].mean()], zoom_start=4)

            # Add marker cluster to the map
            marker_cluster = MarkerCluster().add_to(m)

            # Function to add tooltip to markers
            def add_tooltip(row, marker):
                tooltip = "{}<br>{}<br>Weight: {}<br>Pallets: {}".format(
                    row["bl_number"], row["ship_to_customer"], row["net_pick_weight"], row["total_number_of_pallet"])
                folium.Marker(location=[row["lat"], row["lng"]], tooltip=tooltip).add_to(marker_cluster)

            # Add each point to the marker cluster with tooltip
            for index, row in df.iterrows():
                add_tooltip(row, marker_cluster)

            # Display the map in Streamlit
            st_data = st_folium(m, width=950)

# usage:

conn = sqlite3.connect(r'utils\ipg.sqlite')
df = create_shipment_list(conn)
create_map(df)
conn.close()
