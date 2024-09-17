from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from utils.file import read_file
from utils.whatsapp import send_message
import os

cwd = os.path.abspath(os.getcwd())

# Ask whether to send the same message to all contacts
same_message = input("Do you want to send the same message to all contacts? (yes/no): ").lower()
same_message_for_all = same_message == 'yes'

# Get messages with proper UTF-8 encoding
messages = read_file(f"{cwd}/assets/message.txt", array=True, encoding='utf-8')

# Handle cases when there are no messages in the file
if not messages:
    print("No messages found in the file.")
    exit()

# Determine the message to use
if same_message_for_all:
    message = messages[0]  # Get the first message
    # Ensure UTF-8 encoding for the message
    message_to_send = message.encode('utf-8').decode('utf-8')
else:
    # Ensure there are enough messages for the contacts
    contacts_count = len(read_file(f"{cwd}/assets/contacts.txt", array=True, encoding='utf-8'))
    if len(messages) < contacts_count:
        print("Not enough messages for each contact.")
        exit()
    message_to_send = None  # Messages will be determined in the send_message function

# Get all contacts
contacts = read_file(f"{cwd}/assets/contacts.txt", array=True, encoding='utf-8')

# Initialize Chrome Driver
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

# Send WhatsApp Message
send_message(driver=driver, contacts=contacts, message=message_to_send, same_message_for_all=same_message_for_all)
