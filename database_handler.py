import sqlite3

def insert_into_database(update_date, update_datetime):
    conn = sqlite3.connect('version_updates.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS VersionUpdates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            update_date TEXT,
            update_datetime DATETIME
        )
    ''')

    # Check if an entry with the same update_date already exists
    cursor.execute("SELECT COUNT(*) FROM VersionUpdates WHERE update_date = ?", (update_date,))
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("INSERT INTO VersionUpdates (update_date, update_datetime) VALUES (?, ?)",
                       (update_date, update_datetime))
        conn.commit()
        print("Inserted into the database.")

    conn.close()


def is_entry_exist_for_current_month(update_date):
    conn = sqlite3.connect('version_updates.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS VersionUpdates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            update_date TEXT,
            update_datetime DATETIME
        )
    ''')

    # Check if an entry with the same month and year already exists
    cursor.execute("SELECT COUNT(*) FROM VersionUpdates WHERE strftime('%Y-%m', update_datetime) = ?", (update_date,))
    count = cursor.fetchone()[0]

    conn.close()

    return count > 0
