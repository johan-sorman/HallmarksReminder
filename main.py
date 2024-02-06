from extract_update_info import extract_update_info
from database_operations import initialize_database, insert_update_info

if __name__ == "__main__":
    db_file = 'updates.db'
    
    # Initialize the database if it doesn't exist
    initialize_database(db_file)
    
    # Extract scheduled date
    url = "http://www.playonline.com/ff11us/index.shtml"
    scheduled_date = extract_update_info(url)
    
    if scheduled_date:
        # Insert update info into the database
        insert_update_info(db_file, scheduled_date)
    else:
        print("No entry found.")
