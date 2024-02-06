import sqlite3
from datetime import datetime

import sqlite3

def initialize_database(db_file):
    try:
        # Connect to the database file
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        # Create table if not exists
        c.execute('''CREATE TABLE IF NOT EXISTS updates
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, update_date TEXT UNIQUE, update_datetime DATETIME, year INTEGER)''')
        print("Table 'updates' created successfully.")

        # Commit changes and close connection
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("Error creating table:", e)

if __name__ == "__main__":
    db_file = 'updates.db'
    initialize_database(db_file)



def insert_update_info(db_file, scheduled_date):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Check if the scheduled date already exists in the database
    c.execute("SELECT update_date FROM updates WHERE update_date = ?", (scheduled_date,))
    existing_date = c.fetchone()

    if existing_date:
        print("Entry already exists in the database.")
    else:
        # Insert data into the table
        try:
            scheduled_datetime = datetime.strptime(scheduled_date, '%A, %B %d')
            scheduled_year = datetime.now().year
            scheduled_datetime = scheduled_datetime.replace(year=scheduled_year, hour=0, minute=0, second=0)
            c.execute("INSERT INTO updates (update_date, update_datetime, year) VALUES (?, ?, ?)", (scheduled_date, scheduled_datetime, scheduled_year))
            conn.commit()
            print("Data inserted into the database successfully.")
        except ValueError:
            print("Error parsing scheduled date:", scheduled_date)

    # Close connection
    conn.close()

if __name__ == "__main__":
    db_file = 'updates.db'
    initialize_database(db_file)
