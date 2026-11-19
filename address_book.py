"""
Address book with birthdays (advanced OOP)

Classes from homework 06 (Field, Name, Phone, Record, AddressBook)
are extended with birthday support.

New in this homework:
- Birthday(Field): date in format DD.MM.YYYY, converted to a date object;
  invalid date -> ValueError("Invalid date format. Use DD.MM.YYYY")
- Record.birthday: optional field, only one per record (None by default)
- Record.add_birthday(birthday): adds / replaces the birthday
- AddressBook.get_upcoming_birthdays(): adapted from homework 03 (task 4) -
  contacts to congratulate during the next 7 days;
  Saturday / Sunday birthdays move to Monday
"""

from collections import UserDict
from datetime import date


class Field:
    """Base class for record fields."""

    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """Contact name. Required, cannot be empty."""

    def __init__(self, value: str) -> None:
        # value is always a str (it comes from user input), so only
        # the content is checked, not the type
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        super().__init__(value.strip())


class Phone(Field):
    """Phone number that contains exactly 10 digits."""

    def __init__(self, value: str) -> None:
        # value is always a str (it comes from user input), so only
        # the content is checked, not the type.
        # Validation lives only in __init__: a Phone is never changed,
        # edit_phone replaces it with a new one, so every Phone is valid.
        # isascii() rejects other digit systems like '١٢٣' that pass isdigit()
        if len(value) != 10 or not (value.isascii() and value.isdigit()):
            raise ValueError(f"Phone '{value}' must have exactly 10 digits.")
        super().__init__(value)


class Birthday(Field):
    """Birthday date in format DD.MM.YYYY."""

    def __init__(self, value: str) -> None:
        try:
            # TODO: check the data and convert the string to a date object
            pass
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    """Contact: a Name, a list of Phone objects and an optional Birthday."""

    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None

    def add_phone(self, phone: str) -> None:
        """Add a phone. Raise ValueError if it is invalid or already added."""
        new_phone = Phone(phone)  # validates the number
        if self.find_phone(phone):
            raise ValueError(f"Phone {phone} is already in the record.")
        self.phones.append(new_phone)

    def remove_phone(self, phone: str) -> None:
        """Remove a phone. Raise ValueError if there is no such phone."""
        found = self.find_phone(phone)
        if found is None:
            raise ValueError(f"Phone {phone} not found.")
        self.phones.remove(found)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Replace old_phone with new_phone.

        Raise ValueError if old_phone is missing, new_phone is invalid
        or new_phone is already in the record. The record is not changed
        when an error happens.
        """
        found = self.find_phone(old_phone)
        if found is None:
            raise ValueError(f"Phone {old_phone} not found.")
        if old_phone != new_phone and self.find_phone(new_phone):
            raise ValueError(f"Phone {new_phone} is already in the record.")
        # Phone() raises before the assignment if new_phone is invalid,
        # so the old phone stays in place
        self.phones[self.phones.index(found)] = Phone(new_phone)

    def find_phone(self, phone: str) -> Phone | None:
        """Return the Phone object with this number or None."""
        for item in self.phones:
            if item.value == phone:
                return item
        return None

    def add_birthday(self, birthday: str) -> None:
        """Add or replace the birthday. Raise ValueError if it is invalid."""
        pass  # TODO: your solution

    def __str__(self) -> str:
        # TODO: show the birthday too, if it is set
        return (
            f"Contact name: {self.name.value}, "
            f"phones: {'; '.join(p.value for p in self.phones)}"
        )


class AddressBook(UserDict):
    """Address book: {name: Record}."""

    def add_record(self, record: Record) -> None:
        """Add a record. Raise ValueError if the name already exists."""
        # record is always a Record (we create it in our own code),
        # so its type is not checked
        if record.name.value in self.data:
            raise ValueError(f"Contact '{record.name.value}' already exists.")
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        """Return the record with this name or None."""
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """Delete the record with this name. Raise KeyError if missing."""
        if name not in self.data:
            raise KeyError(f"Contact '{name}' not found.")
        del self.data[name]

    def get_upcoming_birthdays(self, today: date | None = None) -> list[dict]:
        """Return contacts to congratulate during the next 7 days.

        Each item: {"name": "John", "congratulation_date": "DD.MM.YYYY"}.
        Saturday / Sunday birthdays move to Monday.
        today is used in tests; by default it is date.today().
        """
        pass  # TODO: your solution

    def __str__(self) -> str:
        if not self.data:
            return "Address book is empty."
        return "\n".join(str(record) for record in self.data.values())


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    # Виведення: Contact name: John, phones: 1112223333; 5555555555
    print(john)

    # Пошук конкретного телефону в записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
