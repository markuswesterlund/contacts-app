import sys
from .contacts_manager import ContactsManager

menu = """
What do you want to do?
1 - Print list of contacts
2 - Add new contact
3 - Delete contact
s - Search for a contact
e - Edit a contact
q - Exit from application
"""


def main():
    filename = "data/contacts.json"

    if len(sys.argv) > 1:
        filename = sys.argv[1]

    print("Using database:", filename)
    manager = ContactsManager(filename)

    while True:
        print(menu)
        print(f"Total contacts: {len(manager)}")
        op = input("Please select menu option: ")

        if op == "1":
            manager.print_list()
        elif op == "2":
            manager.add_contact()
        elif op == "3":
            manager.delete_contact()
        elif op == "s":
            manager.search_contacts()
        elif op == "e":
            manager.edit_contact()
        elif op == "q":
            print("Goodbye!")
            return 0
        else:
            print("Unknown operation")


if __name__ == '__main__':
    main()
