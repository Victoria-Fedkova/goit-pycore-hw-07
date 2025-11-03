"""
Task: Console Assistant Bot with Address Book

Extended console assistant bot that works with AddressBook class.
Supports commands: add, change, phone, all, add-birthday, show-birthday, birthdays, hello, close/exit.
"""

from typing import Callable
from address_book import AddressBook, Record, PhoneValidationError, BirthdayValidationError


def input_error(func: Callable) -> Callable:
    """
    Decorator for handling input errors.
    
    Handles KeyError, ValueError, IndexError exceptions and returns
    appropriate error messages to user.
    
    Args:
        func: Handler function to wrap
        
    Returns:
        Wrapped function with error handling
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError as e:
            # Check if it's a validation error with message
            if "Invalid" in str(e) or "must" in str(e):
                return str(e)
            return "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command"
        except PhoneValidationError as e:
            return str(e)
        except BirthdayValidationError as e:
            return str(e)
        except Exception as e:
            return f"Error: {e}"
    
    return inner


def parse_input(user_input: str) -> tuple[str, list[str]]:
    """
    Parses user input string into command and arguments.
    
    Handles commands with hyphens (e.g., "add-birthday") by splitting on spaces
    and joining multi-word commands.
    
    Args:
        user_input: User input string
        
    Returns:
        Tuple of (command, arguments list)
    """
    parts = user_input.strip().split()
    if not parts:
        return "", []
    
    # Handle commands with hyphens (e.g., "add-birthday", "show-birthday")
    cmd = parts[0].lower()
    args = parts[1:] if len(parts) > 1 else []
    
    return cmd, args


@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    """
    Adds new contact or phone to existing contact.
    
    Args:
        args: List of arguments [name, phone]
        book: AddressBook instance
        
    Returns:
        Success message
        
    Raises:
        ValueError: If arguments count is incorrect
    """
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")
    
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
    """
    Changes phone number for existing contact.
    
    Args:
        args: List of arguments [name, old_phone, new_phone]
        book: AddressBook instance
        
    Returns:
        Success message
        
    Raises:
        ValueError: If arguments count is incorrect
        KeyError: If contact not found
    """
    if len(args) < 3:
        raise ValueError("Give me name, old phone and new phone please.")
    
    name, old_phone, new_phone = args[0], args[1], args[2]
    
    record = book.find(name)
    if record is None:
        raise KeyError
    
    success = record.edit_phone(old_phone, new_phone)
    if not success:
        return f"Phone '{old_phone}' not found for contact '{name}'."
    
    return "Contact updated."


@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    """
    Shows phone numbers for specified contact.
    
    Args:
        args: List of arguments [name]
        book: AddressBook instance
        
    Returns:
        Contact's phone numbers
        
    Raises:
        IndexError: If name not provided
        KeyError: If contact not found
    """
    if len(args) < 1:
        raise IndexError
    
    name = args[0]
    
    record = book.find(name)
    if record is None:
        raise KeyError
    
    if not record.phones:
        return f"Contact '{name}' has no phone numbers."
    
    phones_str = '; '.join(str(phone.value) for phone in record.phones)
    return f"{name}: {phones_str}"


@input_error
def show_all(args: list[str], book: AddressBook) -> str:
    """
    Shows all saved contacts.
    
    Args:
        args: List of arguments (not used)
        book: AddressBook instance
        
    Returns:
        Formatted string with all contacts
    """
    if not book.data:
        return "No contacts saved."
    
    result = []
    for name, record in book.data.items():
        phones_str = str(record.phones) if record.phones else "no phones"
        birthday_str = f", birthday: {record.birthday}" if record.birthday else ""
        result.append(f"{name}: {phones_str}{birthday_str}")
    
    return "\n".join(result)


@input_error
def add_birthday(args: list[str], book: AddressBook) -> str:
    """
    Adds birthday to contact.
    
    Args:
        args: List of arguments [name, birthday]
        book: AddressBook instance
        
    Returns:
        Success message
        
    Raises:
        ValueError: If arguments count is incorrect
        KeyError: If contact not found
        BirthdayValidationError: If date format is invalid
    """
    if len(args) < 2:
        raise ValueError("Give me name and birthday please.")
    
    name, birthday = args[0], args[1]
    
    record = book.find(name)
    if record is None:
        raise KeyError
    
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args: list[str], book: AddressBook) -> str:
    """
    Shows birthday for specified contact.
    
    Args:
        args: List of arguments [name]
        book: AddressBook instance
        
    Returns:
        Contact's birthday
        
    Raises:
        IndexError: If name not provided
        KeyError: If contact not found
    """
    if len(args) < 1:
        raise IndexError
    
    name = args[0]
    
    record = book.find(name)
    if record is None:
        raise KeyError
    
    if record.birthday is None:
        return f"Contact '{name}' has no birthday set."
    
    return f"{name}: {record.birthday}"


@input_error
def birthdays(args: list[str], book: AddressBook) -> str:
    """
    Shows upcoming birthdays in the next week.
    
    Args:
        args: List of arguments (not used)
        book: AddressBook instance
        
    Returns:
        Formatted string with upcoming birthdays
    """
    upcoming = book.get_upcoming_birthdays()
    
    if not upcoming:
        return "No upcoming birthdays in the next week."
    
    result = []
    for item in upcoming:
        result.append(f"{item['name']}: {item['congratulation_date']}")
    
    return "\n".join(result)


def main() -> None:
    """
    Main function to manage command processing loop.
    """
    book = AddressBook()
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        
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
        
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
