import requests
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from unsub_emails import main as unsub_emails_main
from quickstart import get_credentials
from unsub_emails import main as unsub_emails_main
from selenium import webdriver
import time
from quickstart import get_credentials

def open_links_safari(links):
    driver = webdriver.Safari()
    for link in links:
        driver.get(link)
        # Add any additional logic needed to interact with the page
        time.sleep(5)  # Adjust as necessary
    driver.quit()

if __name__ == "__main__":
    creds = get_credentials()
    unsubscribe_links = unsub_emails_main(creds)
    open_links_safari(unsubscribe_links)

# Get credentials
creds = get_credentials()

# Call read_emails function with creds
unsub_emails_main(creds)

# Check for token.json for successful login
if 'token.json':
    print("\033[92mLogin Successful\033[0m")
else:
    print("Authentication Failed")
