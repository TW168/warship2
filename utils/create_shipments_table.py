import sqlite3

# Connect to the SQLite database (create a new database if it doesn't exist)
conn = sqlite3.connect('ipg.sqlite')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Define the SQL statement to create a table with correct data types
create_table_query = '''
CREATE TABLE IF NOT EXISTS shipments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site TEXT,
    bl_number TEXT,
    truck_appointment_date DATE,  -- Changed data type to DATE
    bl_weight REAL,
    freight_amount REAL,
    truck_appt_time TEXT,
    pickup_date DATE,             -- Changed data type to DATE
    state TEXT,
    ship_to_city TEXT,
    ship_to_customer TEXT,
    order_number TEXT,
    order_item REAL,
    csr TEXT,
    freight_term TEXT,
    require_date DATE,            -- Changed data type to DATE
    schedule_date DATE,           -- Changed data type to DATE
    unshipped_weight REAL,
    product_code TEXT,
    pick_weight REAL,
    number_of_pallet INTEGER,
    pickup_by TEXT,
    change_date DATE,           -- Changed data type to DATE
    carrier_id TEXT,
    arrange_by TEXT,
    unit_freight REAL,
    waybill_number TEXT,
    sales_code TEXT,
    transportation_code TEXT,
    transaction_type TEXT,
    product_group TEXT,
    file_name TEXT,
    rpt_run_date DATE,            -- Changed data type to DATE
    rpt_run_time INTEGER
)
'''

# Execute the SQL statement to create the table
cursor.execute(create_table_query)

# Commit the transaction
conn.commit()

# Close the cursor and the connection
cursor.close()
conn.close()
