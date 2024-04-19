import pandas as pd
import sqlite3
from utils.current_datetime import get_current_datetime


def ftl(dt, site, group, dtt):
    conn = sqlite3.connect(r"utils\ipg.sqlite")
    qry = """SELECT bl_number, carrier_id, truck_appointment_date, 
                    SUM(pick_weight), SUM(number_of_pallet), ship_to_customer 
             FROM shipments 
             WHERE date(rpt_run_date) = ?
             AND rpt_run_time = 16 
             AND site = ?
             AND product_group = ?
             AND truck_appointment_date = date(?, '+1 day') 
             AND carrier_id NOT IN ('SAIA-IP', 'CWF-IP') 
             AND product_code NOT LIKE 'INSERT%' 
             AND ship_to_customer NOT IN ('AMTOPP WAREHOUSE - HOUSTON', 
                                           'INTEPLAST GROUP CORP.(AMTOPP ( CFP)', 
                                           'PINNACLE FILMS') 
             GROUP BY bl_number, carrier_id, truck_appointment_date 
             ORDER BY truck_appointment_date ASC"""

    df = pd.read_sql_query(qry, conn, params=(dt, site, group, dt))
    conn.close()
    current_dt = get_current_datetime()
    print(current_dt, f"Excecuted def ftl(dt, site, group, dt):")
    return df


def ltl(dt, site, group, dtt):
    conn = sqlite3.connect(r"utils\ipg.sqlite")
    qry = """SELECT bl_number, carrier_id, truck_appointment_date, 
                    SUM(pick_weight), SUM(number_of_pallet), ship_to_customer 
             FROM shipments 
             WHERE date(rpt_run_date) = ?
             AND rpt_run_time = 16 
             AND site = ?
             AND product_group = ?
             AND truck_appointment_date = date(?, '+1 day') 
             AND carrier_id IN ('SAIA-IP', 'CWF-IP') 
             AND product_code NOT LIKE 'INSERT%' 
             AND ship_to_customer NOT IN ('AMTOPP WAREHOUSE - HOUSTON', 
                                           'INTEPLAST GROUP CORP.(AMTOPP ( CFP)', 
                                           'PINNACLE FILMS') 
             GROUP BY bl_number, carrier_id, truck_appointment_date 
             ORDER BY truck_appointment_date ASC"""

    df = pd.read_sql_query(qry, conn, params=(dt, site, group, dt))


def ltl(dt, site, group, dtt):
    conn = sqlite3.connect(r"utils\ipg.sqlite")
    qry = """SELECT bl_number, carrier_id, truck_appointment_date, 
                    SUM(pick_weight), SUM(number_of_pallet), ship_to_customer 
             FROM shipments 
             WHERE date(rpt_run_date) = ?
             AND rpt_run_time = 16 
             AND site = ?
             AND product_group = ?
             AND truck_appointment_date = date(?, '+1 day') 
             AND carrier_id IN ('SAIA-IP', 'CWF-IP') 
             AND product_code NOT LIKE 'INSERT%' 
             AND ship_to_customer NOT IN ('AMTOPP WAREHOUSE - HOUSTON', 
                                           'INTEPLAST GROUP CORP.(AMTOPP ( CFP)', 
                                           'PINNACLE FILMS') 
             GROUP BY bl_number, carrier_id, truck_appointment_date 
             ORDER BY truck_appointment_date ASC"""

    df = pd.read_sql_query(qry, conn, params=(dt, site, group, dt))
    conn.close()
    current_dt = get_current_datetime()
    print(current_dt, f"Excecuted def ltl(dt, site, group, dt):")
    return df


def inteplast_shipments(dt, site, group, dtt):
    conn = sqlite3.connect(r"utils\ipg.sqlite")
    qry = """SELECT bl_number, carrier_id, truck_appointment_date, 
                    SUM(pick_weight), SUM(number_of_pallet), ship_to_customer 
             FROM shipments 
             WHERE date(rpt_run_date) = ?
             AND rpt_run_time = 16 
             AND site = ?
             AND product_group = ?
             AND truck_appointment_date = date(?, '+1 day') 
             AND carrier_id NOT IN ('SAIA-IP', 'CWF-IP') 
             AND product_code NOT LIKE 'INSERT%' 
             AND ship_to_customer IN ('AMTOPP WAREHOUSE - HOUSTON', 
                                           'INTEPLAST GROUP CORP.(AMTOPP ( CFP)', 
                                           'PINNACLE FILMS') 
             GROUP BY bl_number, carrier_id, truck_appointment_date 
             ORDER BY truck_appointment_date ASC"""

    df = pd.read_sql_query(qry, conn, params=(dt, site, group, dt))
    conn.close()
    current_dt = get_current_datetime()
    print(current_dt, f"Excecuted def inteplast_shipment(dt, site, group, dt):")
    return df


# Example usage:
# site = "AMJK"
# group = "SW"
# dt = "2024-04-18"  # example date

# ftl_df = ftl(dt=dt, site=site, group=group, dtt=dt)
# print("Result DataFrame:")
# print(ftl_df)
