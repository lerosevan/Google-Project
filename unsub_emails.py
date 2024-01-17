from googleapiclient.discovery import build
from quickstart import get_credentials  # Importing from quickstart.py
from bs4 import BeautifulSoup
import re
import base64
import email
from googleapiclient import errors

def search_emails(service, query, max_results=10):
    try:
        messages = []
        request = service.users().messages().list(userId='me', q=query, maxResults=500)
        response = request.execute()

        while request is not None and len(messages) < max_results:
            messages.extend(response.get('messages', []))
            request = service.users().messages().list_next(previous_request=request, previous_response=response)
            if request:
                response = request.execute()

        return messages[:max_results]
    except Exception as error:
        print(f"An error occurred: {error}")
        return []

def get_email_details(service, message_id):
    try:
        message = service.users().messages().get(userId='me', id=message_id, format='metadata').execute()
        headers = message.get('payload', {}).get('headers', [])

        details = {
            'From': next(header['value'] for header in headers if header['name'] == 'From'),
            'Subject': next(header['value'] for header in headers if header['name'] == 'Subject'),
            'Date': next(header['value'] for header in headers if header['name'] == 'Date')
        }
        return details
    except Exception as error:
        print(f"An error occurred: {error}")
        return None
        
def find_unsubscribe_link(email_body):
    soup = BeautifulSoup(email_body, 'html.parser')
    # Look for all links in the email
    for link in soup.find_all('a', href=True):
        if 'unsubscribe' in link.text.lower():
            return link['href']
    return None

def get_mime_message(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()
        msg_raw = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        mime_msg = email.message_from_bytes(msg_raw)
        return mime_msg
    except errors.HttpError as error:
        print(f'An error occurred: {error}')

def find_unsubscribe_link(mime_msg):
    if mime_msg.is_multipart():
        for part in mime_msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if "text/html" in content_type and "attachment" not in content_disposition:
                html = part.get_payload(decode=True).decode()
                soup = BeautifulSoup(html, 'html.parser')
                for link in soup.find_all('a', href=True):
                    if 'unsubscribe' in link.text.lower():
                        return link['href']
    else:
        if "text/html" in mime_msg.get_content_type():
            html = mime_msg.get_payload(decode=True).decode()
            soup = BeautifulSoup(html, 'html.parser')
            for link in soup.find_all('a', href=True):
                if 'unsubscribe' in link.text.lower():
                    return link['href']
    return None
    
def main(creds):
    service = build('gmail', 'v1', credentials=creds)

    query = 'unsubscribe'
    messages = search_emails(service, query)

    count = 0

    if not messages:
        print("No emails found.")
        return

    print("Emails containing 'unsubscribe':")
    for message in messages:
        details = get_email_details(service, message['id'])
        if details:
            print(details)
            count+= 1
            print("\033[92mCounter: \033[0m" + str(count))
            
    unsubscribe_links = []
    for message in messages:
        mime_msg = get_mime_message(service, 'me', message['id'])
        if mime_msg:
            link = find_unsubscribe_link(mime_msg)

    # Return or process the unsubscribe links
    return unsubscribe_links

if __name__ == "__main__":
    main()
