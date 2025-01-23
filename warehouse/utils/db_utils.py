from django.db import connection
import pandas as pd

def fetch_from_db(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        return pd.DataFrame(data, columns=columns)
