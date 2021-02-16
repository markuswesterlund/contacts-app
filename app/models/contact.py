class Contact:
    def __init__(self, name: str, email: str, number: int):
        self.number = number
        self.name = name
        self.email = email

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "email": self.email,
            "number": self.number
        }

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<Contact name={self.name} email={self.email} number={self.number}>"

    def get_display_value(self) -> str:
        return f"{self.name} / {self.email} / {self.number}"

    def has_email(self) -> bool:
        return self.email is not None and len(self.email) > 0

