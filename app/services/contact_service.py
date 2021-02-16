import json
import typing

from app.json_encoder import ContactAwareJSONEncoder
from app.models import Contact


class ContactService:
    def __init__(self, filename: str):
        self.contacts: typing.List[Contact] = []
        self.filename = filename

        self.load_contacts()

    def get_count(self) -> int:
        return len(self.contacts)

    def get_contacts(self) -> typing.List[Contact]:
        return self.contacts

    def get_contact(self, id_: int):
        return self.contacts[id_ - 1]

    def find(self, term: str) -> typing.List[Contact]:
        results = []
        for contact in self.contacts:
            if term.lower() in contact.name.lower() or term.lower() in contact.email.lower() \
                    or term in contact.number:
                results.append(contact)

        return results

    def create(self, name: str, email: str, number: int) -> Contact:
        contact = Contact(name, email, number)

        self.contacts.append(contact)
        self.save_contacts()

        return contact

    def update(self, id_, name, email, number) -> None:
        for num, contact in enumerate(self.contacts, start=1):
            if num == id_:
                contact.name = name if name else contact.name
                contact.email = email if email else contact.email
                contact.number = number if number else contact.number

                self.save_contacts()

    def remove(self, contact: typing.Union[int, "Contact"]):
        if isinstance(contact, Contact):
            self.contacts.remove(contact)
        else:
            del self.contacts[contact - 1]
        self.save_contacts()

    def load_contacts(self):
        with open(self.filename) as f:
            contacts = json.load(f)

            # self.contacts = [Contact(contact["name"], contact["email"]) for contact in contacts]
            # Contact(name="...", email="...")
            self.contacts = [Contact(**contact) for contact in contacts]

    def save_contacts(self):
        data = json.dumps(self.contacts, indent=2, cls=ContactAwareJSONEncoder)
        with open(self.filename, "w") as f:
            f.write(data)