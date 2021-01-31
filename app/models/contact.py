class Contact:
    def __init__(self, name, email, number):
        self.number = number
        self.name = name
        self.email = email

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "number": self.number
        }

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Contact name={self.name} email={self.email}>"

    def get_display_value(self):
        return f"{self.name} / {self.email} / {self.number}"

    def has_email(self):
        return self.email is not None and len(self.email) > 0

