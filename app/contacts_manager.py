import json

from app.models import Contact
from app.models.json_encoder import ContactAwareJSONEncoder


class ContactsManager:
    def __init__(self, filename="data/contacts.json"):
        self.contacts = []
        self.filename = filename
        self.load_contacts()

    def __str__(self):
        return "Contacts Manager"

    def __len__(self):
        return self.get_contacts_count()

    def get_contacts_count(self):
        return len(self.contacts)

    def search_contacts(self):
        term = input("Name, email or number to search: ")

        matches = 0
        for contact in self.contacts:
            if term.lower() in contact.name.lower() \
                    or term.lower() in contact.email.lower() or term.lower() in contact.number.lower():
                print(f"{contact.name} / {contact.email} / {contact.number}")
                matches += 1

        if matches:
            print("Found {} contact(s)".format(matches))
        else:
            print("No results found")

    def load_contacts(self):
        with open(self.filename) as f:
            contacts = json.load(f)
            self.contacts = [Contact(**contact) for contact in contacts]

    def save_contacts(self):
        contacts = [{"name": contact.name, "email": contact.email, "number": contact.number} for contact in
                    self.contacts]
        data = json.dumps(contacts, indent=2, cls=ContactAwareJSONEncoder)
        with open(self.filename, "w") as f:
            f.write(data)

    def print_list(self):
        print("Your contacts:")
        for num, contact in enumerate(self.contacts, start=1):
            print(f"{num}: {contact.name} / {contact.email} / {contact.number}")

    def edit_contact(self):
        print("\n Edit a contact:")
        self.print_list()
        num_to_edit = int(input("Please enter a number to edit: "))

        for num, contact in enumerate(self.contacts, start=1):
            if num == num_to_edit:
                name = input(f"Enter new name ({contact.name}): ").strip()
                email = input(f"Enter email ({contact.email}): ").strip()
                number = input(f"Enter phone number ({contact.number}): ").strip()

                # updated_contact = {
                #     "first_name": first_name if first_name else contact['first_name'],
                #     "last_name": last_name if last_name else contact['last_name'],
                #     "full_name": full_name if full_name else contact['full_name'],
                #     "email": email if email else contact['email'],
                #     "number": number if number else contact['number'],
                # }
                # self.contacts[num - 1] = updated_contact
                contact.name = name if name else contact.name
                contact.email = email if email else contact.email
                contact.number = number if number else contact.number

                self.save_contacts()
                print("Contact was updated successfully.")

    def delete_contact(self):
        self.print_list()
        num_to_delete = int(input("Please enter the number of contact to delete: "))
        del self.contacts[num_to_delete - 1]

        self.save_contacts()
        print("Contacts was successfully removed.")

    def add_contact(self):
        print("\n Add new contact:")

        name = input("Enter name: ")
        email = input("Enter email: ")
        number = input("Enter phone number: ")

        self.contacts.append(Contact(name, email, number))
        self.save_contacts()
        print("Contact was added successfully.")
