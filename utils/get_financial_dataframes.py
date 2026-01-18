import json
import pandas as pd


def get_financial_dataframes(financials):

    # 2. Extract records into a flat list
    records = []
    for entry in financials:
        date = entry.get('EndDate')
        report_type = entry.get('Type')

        # Check if 'stockFinancialMap' exists and iterate through its categories (CAS, BAL, INC)
        if entry.get('stockFinancialMap'):
            for stmt_type, items in entry['stockFinancialMap'].items():
                if items:
                    for item in items:
                        records.append({
                            'Date': date,
                            'Type': report_type,
                            'Key': item.get('key'),
                            'Value': item.get('value')
                        })

    # 3. Create a DataFrame and convert data types
    df = pd.DataFrame(records)
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

    # 4. Pivot the table
    # This turns unique financial Keys (rows) into Columns
    # Index becomes [Date, Type]
    df_pivot = df.pivot_table(
        index=['Date', 'Type'],
        columns='Key',
        values='Value',
        aggfunc='first'
    ).reset_index()

    # Convert Date to datetime objects for sorting
    df_pivot['Date'] = pd.to_datetime(df_pivot['Date'])

    # 5. Separate into Annual and Interim DataFrames
    # Filter by Type, sort by Date, and set Date as the index
    df_annual = df_pivot[df_pivot['Type'] == 'Annual'].sort_values('Date').set_index('Date')
    df_interim = df_pivot[df_pivot['Type'] == 'Interim'].sort_values('Date').set_index('Date')

    return df_annual, df_interim

