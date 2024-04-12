import sqlite3
from utils.current_datetime import get_current_datetime



def insert_non_duplicate_records(df, db_path):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Iterate over unique file names in the DataFrame
        for file_name in df['file_name'].unique():
            # Check if the file name already exists in the shipment table
            query = f"SELECT COUNT(*) FROM shipments WHERE file_name = '{file_name}'"
            cursor.execute(query)
            num_existing_records = cursor.fetchone()[0]

            # If the file name doesn't exist, insert non-duplicate records
            if num_existing_records == 0:
                # Filter DataFrame rows by file_name and insert into the shipment table
                df_subset = df[df['file_name'] == file_name]
                df_subset.to_sql('shipments', conn, if_exists='append', index=False)
                # Get current date time within time zone
                current_datetime = get_current_datetime()
                print(current_datetime, f"- Inserted {len(df_subset)} non-duplicate records for file_name '{file_name}'.")

        # Commit the transaction
        conn.commit()

        # Close the cursor and the connection
        cursor.close()
        conn.close()

    except sqlite3.Error as error:
        # Get current date time within time zone
        current_datetime = get_current_datetime()
        print(current_datetime, f"- Error inserting non-duplicate records: {error}")


