import pandas as pd
from utils.current_datetime import get_current_datetime

def process_uploaded_file(dataframe):
    # Define the column mapping
    column_mapping = {
        'SITE': 'site',
        'B/L Number': 'bl_number',
        'Truck Appointment Date (YY/MM/DD)': 'truck_appointment_date',
        'B/L Weight (LB)': 'bl_weight',
        'Freight Amount ($)': 'freight_amount',
        'Truck Appt. Time': 'truck_appt_time',
        'PickUp Date (YY/MM/DD)': 'pickup_date',
        'State': 'state',
        'Ship to City': 'ship_to_city',
        'Ship to Customer': 'ship_to_customer',
        'Order Number': 'order_number',
        'Order Item': 'order_item',
        'CSR': 'csr',
        'Freight Term': 'freight_term',
        'Require Date (YY/MM/DD)': 'require_date',
        'Schedule Date (YY/MM/DD)': 'schedule_date',
        'Unshipped Weight (Lb)': 'unshipped_weight',
        'Product Code': 'product_code',
        'Pick Weight (Lb)': 'pick_weight',
        'Number of Pallet': 'number_of_pallet',
        'Pickup By': 'pickup_by',
        'Change Date (YY/MM/DD)': 'change_date',
        'Carrier ID': 'carrier_id',
        'Arrange By': 'arrange_by',
        'Unit Freight (cent/Lb)': 'unit_freight',
        'Waybill Number': 'waybill_number',
        'Sales Code': 'sales_code',
        'Transportation Code': 'transportation_code',
        'Transaction Type': 'transaction_type',
        'Product Group': 'product_group',
        # Dynamically rename the report run column
    }

    # Function to rename columns using the mapping
    def rename_columns(df, column_mapping):
        df.rename(columns=column_mapping, inplace=True)

    # Function to add 'rpt_run' column
    def add_rpt_run_column(df):
        last_column_name = df.columns[-1]
        df['file_name'] = last_column_name

    # Function to convert date columns
    def convert_date(date_str):
        try:
            return pd.to_datetime(date_str, format='%y/%m/%d').strftime('%Y-%m-%d')
        except ValueError:
            return pd.NaT
    
    # Function to extract report run date from file name
    def extract_report_run_date(file_name):
        return pd.to_datetime(file_name.str.extract(r'(\d{4}-\d{1,2}-\d{1,2})')[0])

    # Function to extract report run time from file name
    def extract_report_run_time(file_name):
        # Get current date time within time zone
        current_datetime = get_current_datetime()  # Provide the appropriate timezone
        print(current_datetime, "- Executed def extract_report_run_time(file_name)")
        return file_name.str.split('H').str[1].str.split('M').str[0].astype(int)
   
    # Add report run date and time columns
    if dataframe is not None:
        rename_columns(dataframe, column_mapping)
        add_rpt_run_column(dataframe)
        dataframe['rpt_run_date'] = extract_report_run_date(dataframe['file_name'])
        dataframe['rpt_run_time'] = extract_report_run_time(dataframe['file_name'])
        # Drop rows where 'Product Code' column has value 'SUBTOTAL'
        dataframe = dataframe.loc[dataframe['product_code'] != 'SUBTOTAL', :]
        # Convert date columns using .loc
        date_columns = ['pickup_date', 'require_date', 'schedule_date', 'truck_appointment_date', 'change_date']
        for col in date_columns:
            dataframe.loc[:, col] = dataframe[col].apply(convert_date)
        # # Convert date columns
        # date_columns = ['pickup_date', 'require_date', 'schedule_date', 'truck_appointment_date', 'change_date']
        # for col in date_columns:
        #     dataframe[col] = dataframe[col].apply(convert_date)
        # Drop the 4th column from the last inplace
        #dataframe.drop(dataframe.columns[-4], axis=1, inplace=True)
        if len(dataframe.columns) >= 4:
            dataframe = dataframe.loc[:, dataframe.columns[:-4].tolist() + dataframe.columns[-3:].tolist()]
        # Get current date time within time zone
        current_datetime = get_current_datetime()
        print(current_datetime, f"- Excecuted def process_uploaded_file(dataframe)")
        return dataframe
    else:
        return None

