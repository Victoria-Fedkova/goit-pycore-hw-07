# Homework 7: Advanced Object-Oriented Programming in Python

## 📋 Description

This project extends the functionality of the address book from previous homework assignments, adding birthday support and new commands for working with them. A complete object-oriented architecture is implemented using inheritance, encapsulation, polymorphism, and abstraction.

## Project Structure

- `address_book.py` - Classes for working with address book (AddressBook, Record, Name, Phone, Birthday)
- `bot.py` - Console assistant bot with command processing
- `test_bot.py` - Test scripts for functionality verification

## Installation and Running

```bash
python3 bot.py
```

## Supported Commands

### Basic Commands

- `add [name] [phone]` - Add a new contact or phone to an existing contact
- `change [name] [old phone] [new phone]` - Change phone number for a contact
- `phone [name]` - Show phone numbers for the specified contact
- `all` - Show all contacts in the address book

### Birthday Commands

- `add-birthday [name] [date]` - Add birthday date for a contact (format: DD.MM.YYYY)
- `show-birthday [name]` - Show birthday date for a contact
- `birthdays` - Show birthdays that will occur within the next week

### Utility Commands

- `hello` - Get a greeting from the bot
- `close` or `exit` - Close the program

## 💡 Usage Examples

```bash
Enter a command: add John 1234567890
Contact added.

Enter a command: add John 5555555555
Contact updated.

Enter a command: add-birthday John 15.03.1990
Birthday added.

Enter a command: show-birthday John
John: 15.03.1990

Enter a command: phone John
John: 1234567890; 5555555555

Enter a command: all

--- All Contacts ---
John: 1234567890; 5555555555, birthday: 15.03.1990

Enter a command: birthdays
John: 15.03.2025

Enter a command: close
Good bye!
```

## Data Validation

### Phone Number
- Must consist of exactly 10 digits
- Can only contain digits

### Birthday Date
- Format: DD.MM.YYYY (e.g., 15.03.1990)
- Format and date correctness validation

## Error Handling

All errors are handled informatively:
- Incorrect input format
- Contact not found
- Invalid data format (phone, date)
- Missing arguments

## Testing

To run tests:

```bash
python3 test_bot.py
```

## 🏗️ Implementation Features

### Object-Oriented Design

1. **Abstraction** - The `Field` class (ABC) defines a common interface for fields
2. **Inheritance** - `Name`, `Phone`, `Birthday` inherit from `Field`
3. **Encapsulation** - Use of private (`__name`) and protected (`_phones`, `_birthday`) attributes
4. **Polymorphism** - Overriding methods `__str__()`, `_validate_value()` in subclasses
5. **Composition** - `Record` contains objects `Name`, `PhoneList` (UserList), `Birthday`
6. **Aggregation** - `AddressBook` (UserDict) stores references to `Record` objects

### Technical Features

- **Birthday Class** - Inherits from `Field`, has DD.MM.YYYY format validation
- **get_upcoming_birthdays Method** - Adapted from homework 3, week 4
- **Automatic Monday Move** - Birthdays falling on weekends (Saturday/Sunday) are moved to Monday
- **AddressBook Integration** - Bot uses `AddressBook` class (UserDict) instead of a simple dictionary
- **@input_error Decorator** - Handles all exceptions (KeyError, ValueError, IndexError, PhoneValidationError, BirthdayValidationError)
- **Data Validation** - Complete validation of phones (10 digits) and dates (DD.MM.YYYY)

### Python Tools Used

- `collections.UserDict`, `UserList`, `UserString` - For extending standard containers
- `dataclasses` - For simplifying class creation
- `abc.ABC`, `@abstractmethod` - For abstract base classes
- `enum.Enum` - For field types
- `datetime` - For date operations
