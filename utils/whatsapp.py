from urllib.parse import quote
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

cwd = os.path.abspath(os.getcwd())

WHATSAPP_WEB_URL = 'https://web.whatsapp.com'
DELAY = 30

def print_empty_lines(n):
    for _ in range(n):
        print('\n')

def generate_link(contact, message, web=False):
    """Generate WhatsApp URL with pre-filled message."""
    message = quote(message)  # URL encode the message
    if web:
        return f"https://web.whatsapp.com/send?phone={contact}&text={message}"
    else:
        return f"https://wa.me/{contact}&text={message}"

def get_names_from_file(file_path):
    """Reads names from the file and returns them as a list."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines()]

def get_messages_from_file(file_path):
    """Reads messages from the file and returns them as a list of lines."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines()]

def send_message(driver, contacts, message, same_message_for_all):
    print_empty_lines(2)
    print(f"Once your browser opens up, sign in to WhatsApp Web...")
    print("Wait for your chats to be visible so you don't have to sign in again.")
    print_empty_lines(1)

    driver.get(WHATSAPP_WEB_URL)

    input("Press any key to start...")

    contacts = [x for x in contacts if x]
    names = get_names_from_file(f"{cwd}/assets/Names.txt")  # Reading names from the file
    messages = get_messages_from_file(f"{cwd}/assets/message.txt")  # Reading messages from the file

    from utils.file import clean_file
    clean_file(f"{cwd}/assets/invalid_contacts.txt")

    # If the same message should be sent to all contacts, use the specified message
    if same_message_for_all:
        message_to_send = message if message else (messages[0] if messages else "No message specified.")
        for index, contact in enumerate(contacts):
            name = names[index] if index < len(names) else "there"  # Check if we have a name for this contact

            personalized_message = f"اهلا {name}, {message_to_send}"
            send_individual_message(driver, contact, personalized_message, index, len(contacts))
    else:
        # Send each line to its respective contact
        for index, contact in enumerate(contacts):
            name = names[index] if index < len(names) else "there"  # Check if we have a name for this contact

            # Make sure we don't run out of messages
            if index < len(messages):
                message_to_send = messages[index]
            else:
                message_to_send = "No message specified."

            personalized_message = f"اهلا {name}, {message_to_send}"
            send_individual_message(driver, contact, personalized_message, index, len(contacts))

def send_individual_message(driver, contact, personalized_message, sending_index, total_contacts):
    print(f"{sending_index + 1}/{total_contacts} => Sending message to {contact}.")

    try:
        whatsapp_url = generate_link(contact, personalized_message, web=True)
        print(f"Generated URL: {whatsapp_url}")  # Debugging statement to check URL
        driver.get(whatsapp_url)

        message_sent = False
        if not message_sent:
            try:
                # Try to find the send button
                send_button = WebDriverWait(driver, DELAY).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Send"]'))
                )
                sleep(1)
                send_button.click()
                message_sent = True
                sleep(3)

                print(f"Message sent to: {contact}")
                print_empty_lines(1)

            except Exception as e:
                print(f"Send button not found or failed: {str(e)}")

                # Try sending message by pressing the Enter key
                try:
                    input_box = WebDriverWait(driver, DELAY).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]'))
                    )
                    input_box.send_keys(Keys.ENTER)
                    message_sent = True
                    print(f"Message sent to {contact} by pressing Enter.")
                    print_empty_lines(1)

                except Exception as enter_exception:
                    print(f"Failed to send message to {contact} using Enter key: {str(enter_exception)}")
                    from utils.file import write_file
                    write_file(f"{cwd}/assets/invalid_contacts.txt", contact)

    except Exception as e:
        print(f"Failed to send message to {contact}: {str(e)}")
        from utils.file import write_file
        write_file(f"{cwd}/assets/invalid_contacts.txt", contact)
