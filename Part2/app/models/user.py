from app.models import BaseModel
import re


class User(BaseModel):
    """
    User model representing a user in the system.
    Can be a guest or a property owner.
    """

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    # ===================== EMAIL =====================

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = self._validate_email(value)

    @staticmethod
    def _validate_email(email):
        """
        Validate email format.
        """
        if not email or not isinstance(email, str):
            raise ValueError("Email is required and must be a string")

        email = email.strip().lower()

        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")

        return email

    # ===================== PASSWORD =====================

    @property
    def password(self):
        """Getter for password (returns None for security reasons)"""
        return None

    @password.setter
    def password(self, value):
        self._password = value

    def validate_password(self):
        return len(self._password) >= 8