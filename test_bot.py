"""
Checks for address_book.py and bot.py

Run: python3 test_bot.py
"""

from datetime import date

from address_book import AddressBook, Birthday, Record
from bot import add_birthday, add_contact, parse_input, show_birthday


def expect_error(error_type: type[Exception], func, *args) -> None:
    """Check that func(*args) raises error_type."""
    try:
        func(*args)
    except error_type:
        return
    raise AssertionError(f"{error_type.__name__} expected for {args!r}")


def make_book(birthdays: dict[str, str]) -> AddressBook:
    """Return a book with contacts {name: birthday}."""
    book = AddressBook()
    for name, birthday in birthdays.items():
        record = Record(name)
        record.add_birthday(birthday)
        book.add_record(record)
    return book


def test_birthday() -> None:
    """Only real dates in format DD.MM.YYYY are accepted."""
    for bad in ("1990-01-01", "32.01.1990", "29.02.2023", "01.13.1990",
                "abc", ""):
        expect_error(ValueError, Birthday, bad)
    Birthday("29.02.2024")


def test_add_birthday() -> None:
    """A record has one birthday, a new one replaces the old one."""
    record = Record("John")
    assert record.birthday is None
    record.add_birthday("01.01.1990")
    record.add_birthday("15.03.1995")
    assert "15.03.1995" in str(record)
    expect_error(ValueError, record.add_birthday, "1995-03-15")


def test_upcoming_birthdays() -> None:
    """Next 7 days only, weekend -> Monday. 19.11.2026 is Thursday."""
    book = make_book({
        "Today": "19.11.1990",      # Thursday, today
        "Friday": "20.11.1990",
        "Saturday": "21.11.1990",   # -> Monday 23.11
        "Sunday": "22.11.1990",     # -> Monday 23.11
        "Passed": "18.11.1990",     # yesterday
        "Later": "30.11.1990",      # in 11 days
    })
    book.add_record(Record("NoBirthday"))

    upcoming = book.get_upcoming_birthdays(today=date(2026, 11, 19))
    result = {item["name"]: item["congratulation_date"] for item in upcoming}
    assert result == {
        "Today": "19.11.2026",
        "Friday": "20.11.2026",
        "Saturday": "23.11.2026",
        "Sunday": "23.11.2026",
    }, result


def test_upcoming_birthdays_new_year() -> None:
    """A birthday in January is found at the end of December."""
    book = make_book({"Ann": "01.01.1990"})
    upcoming = book.get_upcoming_birthdays(today=date(2026, 12, 29))
    assert upcoming == [{"name": "Ann", "congratulation_date": "01.01.2027"}]


def test_parse_input() -> None:
    """Command is lowercased, arguments are kept."""
    assert parse_input("ADD-Birthday John 01.01.1990") == (
        "add-birthday", "John", "01.01.1990"
    )


def test_bot_errors() -> None:
    """Handlers return a message instead of crashing."""
    book = AddressBook()
    for result in (
        add_contact([], book),
        add_contact(["John", "123"], book),
        add_birthday(["Nobody", "01.01.1990"], book),
        show_birthday([], book),
    ):
        assert isinstance(result, str) and result, result

    assert add_contact(["John", "1234567890"], book) == "Contact updated."
    assert isinstance(add_birthday(["John", "1990-01-01"], book), str)
    add_birthday(["John", "01.01.1990"], book)
    assert "01.01.1990" in show_birthday(["John"], book)


if __name__ == "__main__":
    test_birthday()
    test_add_birthday()
    test_upcoming_birthdays()
    test_upcoming_birthdays_new_year()
    test_parse_input()
    test_bot_errors()
    print("All checks passed.")
