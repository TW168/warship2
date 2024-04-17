# utils\customer_shipments_ym.py

import pandas as pd
import sqlite3


def shipments_to_customer(ship_to_customer, site='AMJK', product_group='SW'):
     
    qry = f"""
        SELECT strftime('%Y', truck_appointment_date) AS appointment_year,
            strftime('%m', truck_appointment_date) AS appointment_month,
            SUM(pick_weight) AS total_pick_weight,
            SUM(number_of_pallet) AS total_number_of_pallet
        FROM shipments 
        WHERE site='{site}' 
            AND product_group='{product_group}' 
            AND ship_to_customer='{ship_to_customer}' 
            AND truck_appointment_date IS NOT NULL
            AND bl_number is not null 
            AND rpt_run_time=16
        GROUP BY strftime('%Y', truck_appointment_date), strftime('%m', truck_appointment_date);"""
    
    conn = sqlite3.connect(r'utils\ipg.sqlite')
    df = pd.read_sql_query(qry, conn)
    
    conn.close()
    return(df)
    
    


# def ship_to_customer(ship_to_customer, site='AMJK', product_group='SW', rpt_run_time=16):
#     """
#     Retrieve shipment data based on specified parameters.
#     """
#     qry = f"""
#         SELECT strftime('%Y', truck_appointment_date) AS appointment_year,
#             strftime('%m', truck_appointment_date) AS appointment_month,
#             SUM(pick_weight) AS total_pick_weight,
#             SUM(number_of_pallet) AS total_number_of_pallet
#         FROM shipments 
#         WHERE site='{site}' 
#             AND product_group='{product_group}' 
#             AND ship_to_customer='{ship_to_customer}' 
#             AND truck_appointment_date IS NOT NULL 
#             AND rpt_run_time={rpt_run_time}
#         GROUP BY strftime('%Y', truck_appointment_date), strftime('%m', truck_appointment_date);"""
    
#     def query_shipments(sql_query, database='ipg.sqlite'):
#         """
#         Execute a SQL query and return the results as a DataFrame.
#         """
#         with sqlite3.connect(database) as conn:
#             df = pd.read_sql_query(sql_query, conn)
#         return df
    
#     return query_shipments(qry)

# # Example usage:
# shipment_data = ship_to_customer(ship_to_customer='AMTOPP WAREHOUSE - HOUSTON', site='AMJK', product_group='SW', rpt_run_time=16)
# print(shipment_data)
