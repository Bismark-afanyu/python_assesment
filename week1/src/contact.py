import re
import os

# File to store the contacts
CONTACT_FILE = '/Users/caasidev/development/python_assesment_1/week1/docs/contacts.csv'


# Load contacts from file when program starts
def load_contacts():
    contacts = {}
    if os.path.exists(CONTACT_FILE):
        with open(CONTACT_FILE, 'r') as file:
            for line in file:
                name, phone, email = line.strip().split(',')
                contacts[name] = {'phone': phone, 'email': email}
    return contacts

# Save contacts to the file
def save_contacts(contacts):
    with open(CONTACT_FILE, 'w') as file:
        for name, info in contacts.items():
            file.write(f"{name},{info['phone']},{info['email']}\n")

# Add a new contact
def add_contact(contacts):
    name = input("Enter contact name: ").strip()
    if name in contacts:
        print("Contact already exists.")
        return
    
    phone = input("Enter phone number: ").strip()
    while not phone.isdigit():
            print("Invalid phone number! Must contain only digits.")
            phone = input("Enter phone number: ").strip()

    email = input("Enter email address: ").strip()
    while not is_valid_email(email):
        print("Invalid email address format.")
        email = input("Enter email address: ").strip()

    contacts[name] = {'phone': phone, 'email': email}
    save_contacts(contacts)
    print(f"Contact {name} added successfully.")

# Update an existing contact
def update_contact(contacts):
    name = input("Enter the name of the contact to update: ").strip()
    if name not in contacts:
        print(f"Contact {name} does not exist.")
        return

    phone = input(f"Enter new phone number for {name} (Leave empty to skip): ").strip()
    email = input(f"Enter new email for {name} (Leave empty to skip): ").strip()

    if phone:
        if not phone.isdigit():
            print("Invalid phone number! Must contain only digits.")
            return
        contacts[name]['phone'] = phone

    if email:
        if not is_valid_email(email):
            print("Invalid email address format.")
            return
        contacts[name]['email'] = email

    save_contacts(contacts)
    print(f"Contact {name} updated successfully.")

# View all contacts
def view_contacts(contacts):
    if not contacts:
        print("No contacts found.")
        return

    for name, info in contacts.items():
        print(f"Name: {name}, Phone: {info['phone']}, Email: {info['email']}")

# Delete a contact
def delete_contact(contacts):
    name = input("Enter the name of the contact to delete: ").strip()
    if name not in contacts:
        print(f"Contact {name} does not exist.")
        return

    del contacts[name]
    save_contacts(contacts)
    print(f"Contact {name} deleted successfully.")

# Validate email address format
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)

# Main menu
def run():
    contacts = load_contacts()
    while True:
        print("\n--- Contact Book Menu ---")
        print("1. Add Contact")
        print("2. Update Contact")
        print("3. View Contacts")
        print("4. Delete Contact")
        print("5. Exit")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            add_contact(contacts)
        elif choice == '2':
            update_contact(contacts)
        elif choice == '3':
            view_contacts(contacts)
        elif choice == '4':
            delete_contact(contacts)
        elif choice == '5':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

