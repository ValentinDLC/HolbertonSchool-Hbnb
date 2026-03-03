from app.models import BaseModel
import re

class User(BaseModel):
    """
        User model representing a user in the system.
        Can be a guest or a property owner.
    """

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """
        Initialize User instance with provided attributes.

        Args:
            first_name (str): User's first name
            last_name (str): User's last name
            email (str): User's email address (must be unique)
            password (str): User's password (will be hashed in Part3)
            is_admin (bool): Flag indicating if user is an admin
        """
        super().__init__() # Call __init__ of BaseModel
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password # In Part3, this will be hashed for security
        self.is_admin = is_admin

    @property
    def password(self):
        """Getter for password (returns None for security reasons)"""
        return None # Never return password for security reasons

    @password.setter
    def password(self, value):
        """Setter for password (stores hashed version)"""
        # In Part3, we will implement password hashing here
        self._password = value

    def validate_email(self):
        """
            Validate email format using regex
            Returns:
                bool: True if email is valid
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, self.email) is not None

    def validate_password(self):
        """
            Validate password strength
            Returns:
                bool: True if password is strong enough
        """
        # For simplicity, we will just check length here
        return len(self._password) >= 8

    def to_dict(self):
        """
            Convert User to dictionary
            Excludes password for security reasons
        """
        user_dict = super().to_dict() # Get base attributes from BaseModel
        user_dict['first_name'] = self.first_name
        user_dict['last_name'] = self.last_name
        user_dict['email'] = self.email
        user_dict['is_admin'] = self.is_admin
        # Remove password if present (security)
        user_dict.pop('_password', None)
        return user_dict

    # Placeholder methods for future database interactions
    def register(self):
        """Register the user in the database (to be implemented in Part3)"""
        pass

    def authenticate(self, password):
        """
            Authenticate user with password
            Args:
                password (str): Password to verify
            Returns:
                bool: True if authentication is successful
        """
        # In Part3, we will implement password verification here
        return self._password == password

    def add_place(self, title, description, price, latitude, longitude):
        """Add a place for the user (to be implemented in Part3)"""
        pass

    def has_reserved(self, place):
        """Check if user has reserved a place (to be implemented in Part3)"""
        pass

    def add_review(self, text, rating):
        """Add a review for a place (to be implemented in Part3)"""
        pass

    def add_amenity(self, name, description):
        """Add an amenity for the user (to be implemented in Part3)"""
        pass
