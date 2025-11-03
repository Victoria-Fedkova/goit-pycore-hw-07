"""
Task: Address Book Management System with OOP

Object-Oriented Programming implementation of an address book management system.
Demonstrates: Abstraction, Encapsulation, Inheritance, Polymorphism, Composition, Aggregation.
Uses: UserDict, UserList, UserString, dataclasses, Enum, ABC, custom exceptions.
Extended with Birthday functionality.
"""

from collections import UserDict, UserList, UserString
from dataclasses import dataclass, field, InitVar
from enum import Enum
from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime, timedelta


# ==================== Custom Exceptions ====================
class ValidationError(Exception):
    """Base class for validation errors"""
    pass


class PhoneValidationError(ValidationError):
    """Phone number validation error"""
    pass


class BirthdayValidationError(ValidationError):
    """Birthday validation error"""
    pass


class RecordNotFoundError(Exception):
    """Error when record is not found"""
    pass


class PhoneNotFoundError(Exception):
    """Error when phone is not found"""
    pass


# ==================== Enum ====================
class FieldType(Enum):
    """Field types for contact records"""
    NAME = "name"
    PHONE = "phone"
    BIRTHDAY = "birthday"


# ==================== UserString, UserList ====================
class FieldValue(UserString):
    """Wrapper for field values using UserString"""
    pass


class PhoneList(UserList):
    """Class for storing phone list using UserList"""
    
    def __init__(self, initlist: Optional[List] = None):
        super().__init__(initlist if initlist else [])
    
    def __str__(self) -> str:
        """Override for better display"""
        return '; '.join(str(phone.value) for phone in self.data)


# ==================== Abstraction and Inheritance ====================
class Field(ABC):
    """
    Abstract base class for record fields.
    
    Uses abstraction to define common interface for fields.
    Subclasses must implement _validate_value() method.
    
    Attributes:
        _value (FieldValue): Protected field value (UserString)
        _field_type (FieldType): Protected field type (Enum)
    
    Properties:
        value (str): Public field value
        field_type (FieldType): Public field type
    """
    
    def __init__(self, value: str) -> None:
        """
        Initialize field.
        
        Args:
            value: Field value
        """
        self._value: FieldValue = FieldValue(value)  # Protected attribute
        self._field_type: FieldType = FieldType.NAME  # Protected attribute
    
    @property
    def value(self) -> str:
        """Public property for accessing value"""
        return self._value.data
    
    @value.setter
    def value(self, val: str) -> None:
        """Setter for value with validation"""
        self._validate_value(val)
        self._value = FieldValue(val)
    
    @property
    def field_type(self) -> FieldType:
        """Public property for field type"""
        return self._field_type
    
    @abstractmethod
    def _validate_value(self, value: str) -> bool:
        """Abstract method for value validation"""
        pass
    
    def __str__(self) -> str:
        """Polymorphism - override __str__ method"""
        return str(self.value)
    
    def __repr__(self) -> str:
        """Object representation"""
        return f"{self.__class__.__name__}({self.value})"


class Name(Field):
    """
    Class for storing contact name.
    
    Required field with validation for non-empty value.
    Inherits from Field.
    
    Args:
        value: Contact name
    """
    
    def __init__(self, value: str) -> None:
        super().__init__(value)
        self._field_type = FieldType.NAME
    
    def _validate_value(self, value: str) -> bool:
        """Name validation"""
        if not value or not value.strip():
            raise ValidationError("Name cannot be empty")
        return True


class Phone(Field):
    """
    Class for storing phone number.
    
    Has format validation: exactly 10 digits.
    Inherits from Field.
    Raises PhoneValidationError for invalid numbers.
    
    Args:
        value: Phone number (10 digits)
    
    Raises:
        PhoneValidationError: If number doesn't contain exactly 10 digits
    """
    
    def __init__(self, value: str) -> None:
        super().__init__(value)
        self._field_type = FieldType.PHONE
        # Validation on creation
        if not self._validate_value(self.value):
            raise PhoneValidationError("Phone number must contain exactly 10 digits")
    
    def _validate_value(self, value: str) -> bool:
        """Protected method for phone validation"""
        if not value.isdigit():
            raise PhoneValidationError("Phone number must contain only digits")
        if len(value) != 10:
            raise PhoneValidationError("Phone number must contain exactly 10 digits")
        return True


class Birthday(Field):
    """
    Class for storing birthday date.
    
    Has format validation: DD.MM.YYYY.
    Inherits from Field.
    Raises BirthdayValidationError for invalid dates.
    
    Args:
        value: Birthday date in format DD.MM.YYYY
    
    Raises:
        BirthdayValidationError: If date format is invalid
    """
    
    def __init__(self, value: str) -> None:
        try:
            # Validate and convert string to datetime object
            self._validate_value(value)
            # Store the validated value
            super().__init__(value)
            self._field_type = FieldType.BIRTHDAY
        except ValueError as e:
            raise BirthdayValidationError(f"Invalid date format. Use DD.MM.YYYY") from e
    
    def _validate_value(self, value: str) -> bool:
        """Protected method for birthday validation"""
        try:
            # Try to parse date in DD.MM.YYYY format
            datetime.strptime(value, "%d.%m.%Y")
            return True
        except ValueError:
            raise BirthdayValidationError(f"Invalid date format. Use DD.MM.YYYY")
    
    def to_date(self) -> datetime:
        """
        Convert birthday string to datetime.date object.
        
        Returns:
            datetime.date object
        """
        return datetime.strptime(self.value, "%d.%m.%Y").date()


# ==================== Composition and Aggregation ====================
@dataclass
class Record:
    """
    Class for storing contact information.
    
    Uses composition: contains Name object and PhoneList with Phone objects.
    Uses dataclass for simplified initialization.
    
    Attributes:
        __name (Name): Private attribute for name (accessed via property)
        _phones (PhoneList): Protected attribute for phone list
        _birthday (Optional[Birthday]): Protected attribute for birthday (optional)
    
    Methods:
        add_phone: Adds phone to record
        remove_phone: Removes phone from record
        edit_phone: Edits phone in record
        find_phone: Finds phone in record
        add_birthday: Adds birthday to record
    
    Args:
        _name_value: Contact name (InitVar for dataclass)
    """
    _name_value: InitVar[str]
    __name: Name = field(init=False, repr=False)  # Private attribute
    _phones: PhoneList = field(default_factory=PhoneList)  # Protected attribute
    _birthday: Optional[Birthday] = field(default=None, init=False)  # Protected attribute
    
    def __post_init__(self, _name_value: str) -> None:
        """
        Initialization after object creation (dataclass post-init).
        
        Args:
            _name_value: Contact name
        """
        self.__name = Name(_name_value)
        if not isinstance(self._phones, PhoneList):
            self._phones = PhoneList(self._phones)
    
    @property
    def name(self) -> Name:
        """Public property for accessing name"""
        return self.__name
    
    @property
    def phones(self) -> PhoneList:
        """Public property for accessing phones"""
        return self._phones
    
    @property
    def birthday(self) -> Optional[Birthday]:
        """Public property for accessing birthday"""
        return self._birthday
    
    def add_phone(self, phone: str) -> None:
        """Add phone to record"""
        try:
            phone_obj = Phone(phone)
            self._phones.append(phone_obj)
        except PhoneValidationError as e:
            raise PhoneValidationError(f"Cannot add phone: {e}")
    
    def remove_phone(self, phone: str) -> bool:
        """Remove phone from record"""
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self._phones.remove(phone_to_remove)
            return True
        return False
    
    def edit_phone(self, old_phone: str, new_phone: str) -> bool:
        """Edit phone in record"""
        phone_to_edit = self.find_phone(old_phone)
        if not phone_to_edit:
            return False
        
        try:
            new_phone_obj = Phone(new_phone)
            phone_to_edit.value = new_phone_obj.value
            return True
        except PhoneValidationError:
            return False
    
    def find_phone(self, phone: str) -> Optional[Phone]:
        """Find phone in record"""
        for p in self._phones:
            if p.value == phone:
                return p
        return None
    
    def add_birthday(self, birthday: str) -> None:
        """
        Add birthday to record.
        
        Args:
            birthday: Birthday date in format DD.MM.YYYY
        
        Raises:
            BirthdayValidationError: If date format is invalid
        """
        try:
            self._birthday = Birthday(birthday)
        except BirthdayValidationError as e:
            raise BirthdayValidationError(f"Cannot add birthday: {e}")
    
    def __str__(self) -> str:
        """Override __str__ method"""
        birthday_str = f", birthday: {self._birthday}" if self._birthday else ""
        return f"Contact name: {self.__name.value}, phones: {self._phones}{birthday_str}"


# ==================== UserDict ====================
class AddressBook(UserDict):
    """
    Class for storing and managing records.
    
    Inherits from UserDict for convenient dictionary operations.
    Uses aggregation: stores references to Record objects.
    
    Methods:
        add_record: Adds record to book
        find: Finds record by name
        delete: Deletes record by name
        get_upcoming_birthdays: Returns list of users with birthdays in next week
    """
    
    def add_record(self, record: Record) -> None:
        """
        Add record to address book.
        
        Args:
            record: Record object to add
        
        Raises:
            TypeError: If not a Record instance is passed
        """
        if not isinstance(record, Record):
            raise TypeError("Record must be an instance of Record class")
        self.data[record.name.value] = record
    
    def find(self, name: str) -> Optional[Record]:
        """
        Find record by name.
        
        Args:
            name: Name to search for
        
        Returns:
            Record object or None if not found
        """
        return self.data.get(name)
    
    def delete(self, name: str) -> bool:
        """
        Delete record by name.
        
        Args:
            name: Record name to delete
        
        Returns:
            True if record deleted, False if not found
        """
        if name not in self.data:
            return False
        del self.data[name]
        return True
    
    def get_upcoming_birthdays(self) -> List[dict]:
        """
        Returns list of users with birthdays in the next 7 days.
        
        Adapted from homework 3, task 4.
        For contacts with birthdays within next 7 days, adjusts for weekends:
        - Saturday birthdays move to Monday
        - Sunday birthdays move to Monday
        
        Returns:
            List of dictionaries with 'name' and 'congratulation_date' keys
        """
        today = datetime.today().date()
        upcoming = []
        
        for record in self.data.values():
            if record.birthday is None:
                continue
            
            # Get birthday date object
            birthday = record.birthday.to_date()
            
            # Get birthday for this year
            birthday_this_year = birthday.replace(year=today.year)
            
            # If birthday already passed this year, consider next year
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)
            
            # Calculate difference in days
            days_until_birthday = (birthday_this_year - today).days
            
            # Check if birthday is within next 7 days (including today)
            if 0 <= days_until_birthday <= 7:
                congratulation_date = birthday_this_year
                
                # If birthday falls on weekend, move to next Monday
                weekday = congratulation_date.weekday()
                if weekday == 5:  # Saturday
                    congratulation_date += timedelta(days=2)
                elif weekday == 6:  # Sunday
                    congratulation_date += timedelta(days=1)
                
                upcoming.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                })
        
        return upcoming
    
    def __str__(self) -> str:
        """Address book representation"""
        if not self.data:
            return "Address book is empty"
        return "\n".join(str(record) for record in self.data.values())
