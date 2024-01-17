import bisect

# List Node
class EmailInfo:
    def __init__(self, name, count, is_clicked):
        self.name = name
        self.count = count
        self.is_clicked = is_clicked

    # for alphabetical order purposes
    def __lt__(self, other):
        return self.name < other.name

# Create a list to hold the email information
emails = []

# Insert function. Checks if email is in list, count++ if it is.
# Adds new email if not in list
def insert(emails, _name, _count, _is_checked):
  # add relevant info to an email node
  # NOTE: count should default to 0 as we do not know if the name already exists or not
  # NOTE: _is_checked should also be defaulted to false, same reasons.
  email_info = EmailInfo(_name, _count, _is_checked)

  # If list is empty, add email to list 
  if not list:
    emails.append(email_info)
    return
  
  #iterate through emails list, add new email if not found.
  # Position contains location of email if it exists, -1 if it does not
  position = find_email_position(emails, email_info)
  if position == -1: # If email is not found, add it to the list
    bisect.insort(emails, email_info)
  else: # If found, increment count
    emails[position].count += 1
    

# Function to find a position in the emails list 
# bisect_left uses a binary search with O(logn) complexity, if i did it right
def find_email_position(emails, email_info):
  # Assign position of email to i
  i = bisect.bisect_left(emails, email_info)
  if i != len(emails) and emails[i].name == email_info.name:
    return i
  else:
    return -1


# Function to print list of all emails in email list
def print_emails(emails):
    for email in emails:
      print(email.name, email.count, email.is_clicked)

# Function to form a list of all true "is_clicked" nodes and return them
def print_clicked(emails):
  check_list = []
  for email in emails:
    if email.is_clicked:
      check_list.append(email)
  return check_list