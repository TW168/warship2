import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('ipg.sqlite')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Define the SQL query to create the table
create_table_query = '''
CREATE TABLE site_group (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site TEXT NOT NULL,
    product_group TEXT NOT NULL
);
'''

# Execute the create table query
cursor.execute(create_table_query)

# Define the data to be inserted
data = [
    ("AMJK", "SW"),
    ("TXAS", "SW"),
    ("AMIN", "SW"),
    ("AMAZ", "SW"),
    ("AMJK", "BP"),
    ("AMJK", "CT"),
    ("AMSC", "BP"),
    ("VAMT", "BP"),
    ("PFCH", "SW")
]

# Define the SQL query to insert data into the table
insert_query = 'INSERT INTO site_group (site, product_group) VALUES (?, ?)'

# Execute the insert query for each row of data
cursor.executemany(insert_query, data)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
