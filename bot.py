"""
Console assistant bot with an address book

The bot works with AddressBook instead of a contacts dict:
book = AddressBook()

Commands:
- add [name] [phone]: add a new contact or a phone to an existing contact
- change [name] [old phone] [new phone]: change a phone of the contact
- phone [name]: show phones of the contact
- all: show all contacts
- add-birthday [name] [date]: add a birthday (DD.MM.YYYY) to the contact
- show-birthday [name]: show the birthday of the contact
- birthdays: show birthdays to congratulate during the next week
- hello: greeting
- close / exit: close the program

All errors (wrong input, missing contact, invalid phone / date)
are handled by @input_error and shown as a clear message.
"""

from functools import wraps
from typing import Callable

from address_book import AddressBook, Record

NOT_FOUND = "Contact not found."
NEED_ARGUMENT = "Enter the argument for the command."


def input_error(func: Callable) -> Callable:
    """Turn KeyError, ValueError, IndexError into messages for the user."""

    @wraps(func)  # keeps the name and docstring of the wrapped handler
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return NOT_FOUND
        except ValueError as error:
            # Validation errors from address_book carry a clear text
            return str(error)
        except IndexError:
            return NEED_ARGUMENT

    return inner


def parse_input(user_input: str) -> tuple[str, ...]:
    """Split user input into a lowercase command and arguments."""
    if not user_input.strip():
        return ("",)
    cmd, *args = user_input.split()
    return cmd.lower(), *args


def find_record(name: str, book: AddressBook) -> Record:
    """Return the record with this name. Raise KeyError if it is missing."""
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    return record


@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    """Add a new contact or a phone to an existing contact."""
    if len(args) < 2:
        raise ValueError("Give me name and phone please: add [name] [phone]")
    name, phone, *_ = args
    record = book.find(name)
    if record is None:
        # The phone is checked before the contact gets into the book,
        # so an invalid phone does not leave an empty contact behind
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."
    record.add_phone(phone)
    return "Contact updated."


@input_error
def change_contact(args: list[str], book: AddressBook) -> str:
    """Change a phone: change [name] [old phone] [new phone]."""
    if len(args) < 3:
        raise ValueError(
            "Give me name, old and new phone please: "
            "change [name] [old phone] [new phone]"
        )
    name, old_phone, new_phone, *_ = args
    find_record(name, book).edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    """Show phones of the contact: phone [name]."""
    record = find_record(args[0], book)  # IndexError if no name
    if not record.phones:
        return f"{record.name} has no phones."
    return f"{record.name}: {'; '.join(p.value for p in record.phones)}"


@input_error
def show_all(args: list[str], book: AddressBook) -> str:
    """Show all contacts."""
    return str(book)


@input_error
def add_birthday(args: list[str], book: AddressBook) -> str:
    """Add a birthday: add-birthday [name] [DD.MM.YYYY]."""
    if len(args) < 2:
        raise ValueError(
            "Give me name and birthday please: "
            "add-birthday [name] [DD.MM.YYYY]"
        )
    name, birthday, *_ = args
    find_record(name, book).add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args: list[str], book: AddressBook) -> str:
    """Show the birthday of the contact: show-birthday [name]."""
    record = find_record(args[0], book)  # IndexError if no name
    if record.birthday is None:
        return f"{record.name} has no birthday."
    return f"{record.name}: {record.birthday}"


@input_error
def birthdays(args: list[str], book: AddressBook) -> str:
    """Show birthdays to congratulate during the next week."""
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays during the next week."
    return "\n".join(
        f"{item['name']}: {item['congratulation_date']}" for item in upcoming
    )


def main() -> None:
    """Run the command loop."""
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        try:
            user_input = input("Enter a command: ")
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C / Ctrl+D close the bot politely, without a traceback
            print("\nGood bye!")
            break

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        elif command == "":
            print("Enter a command.")

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
