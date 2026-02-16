classDiagram
%% ===============================================
%% BASE MODEL (Abstract shared class)
%% ===============================================
class BaseModel {
    <<abstract>>
    # id : UUID
    - createdAt : DateTime
    - updatedAt : DateTime
    + save() void
    + delete() void
    + toDict() Dictionary
}

%% ===============================================
%% USER MODEL (Users)
%% ===============================================
class User {
    <<entity>>
    + email : String
    + password : String
    + firstName : String
    + lastName : String
    + role : String
    + create() User
    + authenticate(email, password) Token
    + updateProfile() User
    + hashPassword(password) String
    + verifyPassword(password) Boolean
    + validateEmail(email) Boolean
    + getFullName() String
}

%% ===============================================
%% PLACE MODEL (Accommodations)
%% ===============================================
class Place {
    <<entity>>
    # ownerId : UUID
    + title : String
    + description : String
    + pricePerNight : Float
    + latitude : Float
    + longitude : Float
    + create() Place
    + updateDetails() Place
    + calculateRating() Float
    + validatePrice(price) Boolean
    + validateCoordinates(lat, long) Boolean
    + isAvailableForDates(start, end) Boolean
    + addAmenity(amenityId) void
    + removeAmenity(amenityId) void
}

%% ===============================================
%% BOOKING MODEL (Reservations)
%% ===============================================
class Booking {
    <<entity>>
    # placeId : UUID
    # userId : UUID
    + startDate : Date
    + endDate : Date
    + totalPrice : Float
    + status : String
    + create() Booking
    + calculateTotalPrice(place, start, end) Float
    + checkAvailability(placeId, start, end) Boolean
    + validateDates(start, end) Boolean
    + cancel() Booking
    + canCancel() Boolean
    + updateStatus(status) Booking
}

%% ===============================================
%% REVIEW MODEL (Reviews)
%% ===============================================
class Review {
    <<entity>>
    # placeId : UUID
    # userId : UUID
    # bookingId : UUID
    + rating : Integer
    + comment : String
    + create() Review
    + validateRating(rating) Boolean
    + validateBooking(userId, placeId) Boolean
    + update() Review
    + delete() Boolean
    + isAuthor(userId) Boolean
}

%% ===============================================
%% AMENITY MODEL (Amenities)
%% ===============================================
class Amenity {
    <<entity>>
    + name : String
    + description : String
    + add() Amenity
    + validateUniqueName(name) Boolean
    + findAll() List~Amenity~
    + findById(id) Amenity
}

%% ===============================================
%% INHERITANCE
%% ===============================================
BaseModel <|-- User
BaseModel <|-- Place
BaseModel <|-- Booking
BaseModel <|-- Review
BaseModel <|-- Amenity

%% ===============================================
%% RELATIONSHIPS
%% ===============================================
%% User relationships
User "1" --o "*" Place : owns
User "1" --o "*" Booking : makes
User "1" --o "*" Review : writes

%% Place relationships
Place "1" --o "*" Booking : receives
Place "1" --o "*" Review : has
Place "*" --o "*" Amenity : includes

%% Booking relationships
Booking "1" --o "0..1" Review : generates

%% ===============================================
%% EXPLANATORY NOTES
%% ===============================================
note for BaseModel "Abstract class shared by all entities.Contains common attributes: id, createdAt, updatedAt"
note for User "Manages authentication, roles (user/admin) and user profiles"
note for Place "Manages accommodations with price, GPS location and availability"
note for Booking "Orchestrates reservations with statuses (pending, confirmed, cancelled, completed)"
note for Review "Validates reviews (rating 1-5, comment min 10 chars) and updates place ratings"
note for Amenity "Manages amenities (WiFi, Pool, etc.) with unique names"