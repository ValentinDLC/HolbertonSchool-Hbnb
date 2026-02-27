from app.models import BaseModel

class Place(BaseModel):
    """
        Place model representing a place to stay.
    """

    def __init__(self, name, title, description, price, latitude, longitude, owner_id):
        """
            Initialize a Place instance
            Args:
                name (str): Short identifier for the place (e.g., "Cozy Cottage")
                title (str): Full marketing title for the place (e.g., "Cozy Cottage in the Woods")
                description (str): Detailed description of the place
                price (float): Price per night
                latitude (float): GPS latitude (private)
                longitude (float): GPS longitude (private)
                owner_id (str): UUID of the user who owns this place
        """
        super().__init__() # Call __init__ of BaseModel
        self.name = name
        self.title = title
        self.description = description
        self.price = price
        self._latitude = latitude # Private attribute for latitude
        self._longitude = longitude # Private attribute for longitude
        self.owner_id = owner_id
        self.amenities = [] # List of amenities (e.g., ["WiFi", "Pool"])

    @property
    def latitude(self):
        """Getter for latitude (private)"""
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """Setter for latitude with validation"""
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = value

    @property
    def longitude(self):
        """Getter for longitude (private)"""
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """Setter for longitude with validation"""
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = value

    def add_amenity(self, amenity_id):
        """
            Add an amenity to the place

            Args:
                amenity_id (str): UUID of the amenity to add
        """
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)

    def to_dict(self):
        """
            Convert Place to dictionary
            Includes coordinates (they're needed for display)
            but they are private attributes, so we will handle them carefully.
        """
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'name': self.name,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self._latitude, # Include latitude in dict
            'longitude': self._longitude, # Include longitude in dict
            'owner_id': self.owner_id,
            'amenities': self.amenities
        }

    # Static methods (class-level, not instance-level)
    @staticmethod
    def list_all():
        """List all places (to be implemented in Part3)"""
        pass

    @staticmethod
    def get_by_criteria(criteria):
        """
            Get places by search criteria (to be implemented in Part3)

            Args:
                criteria (dict): Search filters (price_max, city, etc.)

            Returns:
                list: List of Place objects matching criteria
        """
        pass

    def get_all_reservations(self):
        """
            Get all reservations for this place (to be implemented in Part3)
            Private method for owner use only
        """
        pass
