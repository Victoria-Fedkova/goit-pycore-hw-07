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

from typing import Callable

from address_book import AddressBook, Record


def input_error(func: Callable) -> Callable:
    """Catch input errors in a handler and return a message instead."""
    pass  # TODO: your solution


def parse_input(user_input: str) -> tuple[str, ...]:
    """Split user input into a lowercase command and arguments."""
    pass  # TODO: your solution


@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    """Add a new contact or a phone to an existing contact."""
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args: list[str], book: AddressBook) -> str:
    """Change a phone: change [name] [old phone] [new phone]."""
    pass  # TODO: your solution


@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    """Show phones of the contact: phone [name]."""
    pass  # TODO: your solution


@input_error
def show_all(args: list[str], book: AddressBook) -> str:
    """Show all contacts."""
    pass  # TODO: your solution


@input_error
def add_birthday(args: list[str], book: AddressBook) -> str:
    """Add a birthday: add-birthday [name] [DD.MM.YYYY]."""
    pass  # TODO: your solution


@input_error
def show_birthday(args: list[str], book: AddressBook) -> str:
    """Show the birthday of the contact: show-birthday [name]."""
    pass  # TODO: your solution


@input_error
def birthdays(args: list[str], book: AddressBook) -> str:
    """Show birthdays to congratulate during the next week."""
    pass  # TODO: your solution


def main() -> None:
    """Run the command loop."""
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        # TODO: change, phone, all, add-birthday, show-birthday, birthdays

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
