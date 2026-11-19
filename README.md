# GoIT Python Core - Homework 07

Homework assignment #7 from the GoIT Python Core course: advanced OOP. The address book from homework 06 gets birthdays, and the console bot from homework 05 now works with `AddressBook`.

## Step 1: Address Book with Birthdays

**File:** `address_book.py`

- `Birthday(Field)` - date in format `DD.MM.YYYY`, converted to a date object; invalid date -> `ValueError("Invalid date format. Use DD.MM.YYYY")`
- `Record.birthday` - optional field, only one per record (`None` by default)
- `Record.add_birthday(birthday)` - adds a birthday to the contact
- `AddressBook.get_upcoming_birthdays()` - adapted from homework 03 (task 4): contacts to congratulate during the next week; Saturday / Sunday birthdays move to Monday

**Validation:**

- phone - exactly 10 digits
- birthday - format `DD.MM.YYYY`

## Step 2: Bot Commands

**File:** `bot.py`

The bot uses `book = AddressBook()` instead of a `contacts` dict.

| Command | What it does |
|---|---|
| `add [name] [phone]` | adds a new contact, or a phone to an existing contact |
| `change [name] [old phone] [new phone]` | changes a phone of the contact |
| `phone [name]` | shows phones of the contact |
| `all` | shows all contacts |
| `add-birthday [name] [DD.MM.YYYY]` | adds a birthday to the contact |
| `show-birthday [name]` | shows the birthday of the contact |
| `birthdays` | shows birthdays to congratulate during the next week |
| `hello` | greeting |
| `close` / `exit` | closes the program |

Errors (wrong input, missing contact, invalid phone or date) are handled by the `@input_error` decorator and shown to the user as a clear message.

**Example:**

```
Welcome to the assistant bot!
Enter a command: add John 1234567890
Contact added.
Enter a command: add-birthday John 21.11.1990
Birthday added.
Enter a command: show-birthday John
John: 21.11.1990
Enter a command: exit
Good bye!
```

## Grading Criteria

1. All commands are implemented.
2. Output is clear and user-friendly.
3. All errors are handled with an informative message.
4. Birthday format is `DD.MM.YYYY`, phone has 10 digits.
5. The program closes correctly after `close` or `exit`.

## How to Run

```bash
python3 bot.py        # start the bot
python3 test_bot.py   # checks
```

No external dependencies, only the Python standard library (Python 3.10+).

## Project Structure

```
goit-pycore-hw-07/
├── address_book.py   # Address book classes with Birthday
├── bot.py            # Console assistant bot
├── test_bot.py       # Checks
├── .gitignore
└── README.md
```
