# report/services/utils.py

import pandas as pd

# Utility function to execute a query and return a DataFrame
def execute_query(conn, query, params=None):
    try:
        return pd.read_sql_query(query, conn, params=params)
    except Exception as e:
        # Handle the exception appropriately, maybe log the error
        return pd.DataFrame()

# SQL Queries
def get_combined_in_query():
    return """
        SELECT  
            COALESCE(day.Date, night.Date) AS Date,
            day.DayShiftIn,
            night.NightShiftIn,
            COALESCE(day.max_scraped_date, night.max_scraped_date) AS max_scraped_date
        FROM (
            SELECT  
                MIN(id) AS id,  
                Date,
                MIN(DayShiftIn) AS DayShiftIn,
                MAX(DATE(scraped_dt)) AS max_scraped_date
            FROM  
                eric.scraped_day_shift_in
            WHERE YEAR(Date) = %s AND MONTH(Date) = %s
            GROUP BY  
                Date
        ) AS day
        LEFT JOIN (
            SELECT  
                MIN(id) AS id, 
                Date,
                MIN(NightShiftIn) AS NightShiftIn,
                MAX(DATE(scraped_dt)) AS max_scraped_date
            FROM  
                eric.scraped_night_shift_in
            WHERE YEAR(Date) = %s AND MONTH(Date) = %s
            GROUP BY
                Date
        ) AS night
        ON day.Date = night.Date
        ORDER BY  
            Date DESC;
    """

def get_combined_out_query():
    return """
        SELECT 
            COALESCE(s1.Date, s2.Date, s3.Date) AS Date,
            s1.1stShiftOut,
            s2.2ndShiftOut,
            s3.3rdShiftOut,
            GREATEST(
                COALESCE(s1.max_scraped_date, '1900-01-01'),
                COALESCE(s2.max_scraped_date, '1900-01-01'),
                COALESCE(s3.max_scraped_date, '1900-01-01')
            ) AS max_scraped_date
        FROM (
            SELECT 
                MIN(id) AS id,
                Date,
                MIN(1stShiftOut) AS 1stShiftOut,
                MAX(DATE(scraped_dt)) AS max_scraped_date
            FROM 
                eric.scraped_shift_1_out
            WHERE YEAR(Date) = %s AND MONTH(Date) = %s
            GROUP BY 
                Date
        ) AS s1
        LEFT JOIN (
            SELECT 
                MIN(id) AS id,
                Date,
                MIN(2ndShiftOut) AS 2ndShiftOut,
                MAX(DATE(scraped_dt)) AS max_scraped_date
            FROM 
                eric.scraped_shift_2_out
            WHERE YEAR(Date) = %s AND MONTH(Date) = %s
            GROUP BY 
                Date
        ) AS s2
        ON s1.Date = s2.Date
        LEFT JOIN (
            SELECT 
                MIN(id) AS id,
                Date,
                MIN(3rdShiftOut) AS 3rdShiftOut,
                MAX(DATE(scraped_dt)) AS max_scraped_date
            FROM 
                eric.scraped_shift_3_out
            WHERE YEAR(Date) = %s AND MONTH(Date) = %s
            GROUP BY 
                Date
        ) AS s3
        ON COALESCE(s1.Date, s2.Date) = s3.Date
        ORDER BY 
            Date DESC;
    """

def get_cell_summary_query():
    return """
        SELECT 
            scraped_dt,
            Status, 
            Cell_counts 
        FROM 
            eric.scraped_cell_summary 
        WHERE 
            YEAR(scraped_dt) = %s AND 
            MONTH(scraped_dt) = %s;
    """

def get_ship_today_query():
    return """
        SELECT DISTINCT BL_Number, Truck_Appointment_Date, BL_weight
          FROM ipg_ez
         WHERE Truck_Appointment_Date = %s
           AND Product_Group='SW'
           AND Site='AMJK'; 
    """
