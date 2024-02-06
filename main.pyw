from extract_update_info import extract_update_info
from database_operations import initialize_database, insert_update_info
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    DB_PATH = os.getenv('DB_PATH')
    
    # Initialize the database if it doesn't exist
    initialize_database(DB_PATH)
    
    # Extract scheduled date
    url = "http://www.playonline.com/ff11us/index.shtml"
    scheduled_date = extract_update_info(url)
    
    if scheduled_date:
        # Insert update info into the database
        insert_update_info(DB_PATH, scheduled_date)
    else:
        print("No entry found.")
