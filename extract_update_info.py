import requests
from bs4 import BeautifulSoup
import re

# Function to extract the scheduled date from the entry text
def extract_scheduled_date(entry_text):
    match = re.search(r"The next version update is scheduled for (.+?)\.", entry_text)
    if match:
        return match.group(1)
    else:
        return None

def extract_update_info(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the first <p> element with class="tx_topics"
    entry = soup.find("p", class_="tx_topics")

    # Check if entry was found
    if entry:
        # Extract the text content of the entry
        entry_text = entry.text.strip()

        # Extract scheduled date
        scheduled_date = extract_scheduled_date(entry_text)
        return scheduled_date
    else:
        return None

if __name__ == "__main__":
    url = "http://www.playonline.com/ff11us/index.shtml"
    scheduled_date = extract_update_info(url)
    if scheduled_date:
        print("Scheduled Date:", scheduled_date)
    else:
        print("No entry found.")
