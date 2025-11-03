"""
Test script for bot functionality
"""

from address_book import AddressBook, Record, PhoneValidationError, BirthdayValidationError
from bot import parse_input, add_contact, change_contact, show_phone, show_all, add_birthday, show_birthday, birthdays


def test_parse_input():
    """Test parse_input function"""
    assert parse_input("add John 1234567890") == ("add", ["John", "1234567890"])
    assert parse_input("add-birthday John 01.01.1990") == ("add-birthday", ["John", "01.01.1990"])
    assert parse_input("show-birthday John") == ("show-birthday", ["John"])
    assert parse_input("birthdays") == ("birthdays", [])
    print("✓ parse_input tests passed")


def test_address_book():
    """Test AddressBook functionality"""
    book = AddressBook()
    
    # Test add contact
    result = add_contact(["John", "1234567890"], book)
    assert "Contact added" in result or "updated" in result
    
    # Test find
    record = book.find("John")
    assert record is not None
    assert record.name.value == "John"
    
    # Test add phone to existing contact
    result = add_contact(["John", "5555555555"], book)
    assert "updated" in result or "added" in result
    
    # Test add birthday
    result = add_birthday(["John", "01.01.1990"], book)
    assert "Birthday added" in result
    
    # Test show birthday
    result = show_birthday(["John"], book)
    assert "1990" in result
    
    # Test phone validation
    try:
        record.add_phone("123")  # Invalid - too short
        assert False, "Should have raised PhoneValidationError"
    except PhoneValidationError:
        pass
    
    # Test birthday validation
    try:
        record.add_birthday("1990-01-01")  # Invalid format
        assert False, "Should have raised BirthdayValidationError"
    except BirthdayValidationError:
        pass
    
    # Test valid birthday format
    record.add_birthday("15.03.1995")
    assert record.birthday.value == "15.03.1995"
    
    print("✓ AddressBook tests passed")


def test_get_upcoming_birthdays():
    """Test get_upcoming_birthdays functionality"""
    from datetime import datetime, timedelta
    
    book = AddressBook()
    
    # Add contacts with birthdays
    today = datetime.today().date()
    
    # Add contact with birthday in 3 days
    record1 = Record("Alice")
    record1.add_phone("1111111111")
    future_date = (today + timedelta(days=3)).strftime("%d.%m.%Y")
    record1.add_birthday(future_date)
    book.add_record(record1)
    
    # Add contact with birthday in 10 days (should not appear)
    record2 = Record("Bob")
    record2.add_phone("2222222222")
    future_date2 = (today + timedelta(days=10)).strftime("%d.%m.%Y")
    record2.add_birthday(future_date2)
    book.add_record(record2)
    
    # Get upcoming birthdays
    upcoming = book.get_upcoming_birthdays()
    
    # Should find Alice but not Bob
    names = [item["name"] for item in upcoming]
    assert "Alice" in names
    assert "Bob" not in names
    
    print("✓ get_upcoming_birthdays tests passed")


def run_all_tests():
    """Run all tests"""
    print("Running tests...\n")
    test_parse_input()
    test_address_book()
    test_get_upcoming_birthdays()
    print("\n✅ All tests passed!")


if __name__ == "__main__":
    run_all_tests()
