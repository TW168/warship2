import sqlite3

# Connect to SQLite database (create it if it doesn't exist)
conn = sqlite3.connect('ipg.sqlite')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Define the SQLite table creation query
create_table_query = '''
CREATE TABLE IF NOT EXISTS lat_lng (
    city TEXT,
    city_ascii TEXT,
    state_id TEXT,
    state_name TEXT,
    county_fips TEXT,
    county_name TEXT,
    lat REAL,
    lng REAL,
    population INTEGER,
    density REAL,
    source TEXT,
    military TEXT,
    incorporated TEXT,
    timezone TEXT,
    ranking INTEGER,
    zips TEXT,
    id INTEGER PRIMARY KEY
);
'''

# Execute the table creation query
cursor.execute(create_table_query)

# Commit changes and close connection
conn.commit()
conn.close()

print("Table 'city_data' created successfully.")
