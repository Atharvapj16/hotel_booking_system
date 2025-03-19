import sqlite3
import pandas as pd

def initialize_db(db_path, df):
    conn = sqlite3.connect(db_path)
    df.to_sql('bookings', conn, if_exists='replace', index=False)
    conn.close()

def update_database(new_record):
    conn = sqlite3.connect('hotel_bookings.db')
    pd.DataFrame([new_record]).to_sql('bookings', conn, if_exists='append', index=False)
    conn.close()