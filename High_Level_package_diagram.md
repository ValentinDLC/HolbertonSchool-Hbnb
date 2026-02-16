classDiagram
%% ===============================================
%% PRESENTATION LAYER
%% ===============================================
class PresentationLayer {
    <<Interface / API Service>>
    + UserAPI.handleRequest()
    + PlaceAPI.handleRequest()
    + BookingAPI.handleRequest()
    + ReviewAPI.handleRequest()
    + AmenityAPI.handleRequest()
    + verifyJWT()
    + checkAdminRole()
    + sendResponse()
    - parseRequestBody()
    - handleError()
}

%% ===============================================
%% BUSINESS LOGIC LAYER
%% ===============================================
class BusinessLogicLayer {
    <<Models / Services>>
    + User.create()
    + User.authenticate()
    + User.hashPassword()
    + Place.create()
    + Place.calculateRating()
    + Place.validatePrice()
    + Booking.create()
    + Booking.checkAvailability()
    + Booking.calculateTotalPrice()
    + Review.create()
    + Review.validateRating()
    + Review.validateBooking()
    + Amenity.add()
    + Amenity.validateUniqueName()
    # validateData()
    # applyBusinessRules()
    # enforceConstraints()
    - generateUUID()
    - setTimestamps()
}

%% ===============================================
%% PERSISTENCE LAYER
%% ===============================================
class PersistenceLayer {
    <<Repositories>>
    + UserRepo.save()
    + UserRepo.findById()
    + UserRepo.findByEmail()
    + UserRepo.update()
    + UserRepo.delete()
    + PlaceRepo.save()
    + PlaceRepo.findAll()
    + PlaceRepo.findById()
    + PlaceRepo.update()
    + PlaceRepo.delete()
    + BookingRepo.save()
    + BookingRepo.checkAvailability()
    + BookingRepo.findByUser()
    + BookingRepo.update()
    + BookingRepo.delete()
    + ReviewRepo.save()
    + ReviewRepo.findByPlace()
    + ReviewRepo.findByUser()
    + ReviewRepo.update()
    + ReviewRepo.delete()
    + AmenityRepo.save()
    + AmenityRepo.findAll()
    + AmenityRepo.findById()
    + AmenityRepo.delete()
    - dbConnection
    - buildQuery()
    - executeQuery()
}

%% ===============================================
%% DATABASE LAYER
%% ===============================================
class Database {
    <<MySQL>>
    + connect()
    + executeQuery()
    + disconnect()
    + beginTransaction()
    + commit()
    + rollback()
    - connectionString
    - connectionPool
    - validateConnection()
}

%% ===============================================
%% RELATIONSHIPS
%% ===============================================
PresentationLayer --> BusinessLogicLayer : uses (Facade Pattern)
BusinessLogicLayer --> PersistenceLayer : requests data
PersistenceLayer --> Database : executes SQL queries

%% ===============================================
%% NOTES
%% ===============================================
note for PresentationLayer "API Layer (HTTP Interface)\n- Receives HTTP requests\n- Validates JWT tokens\n- Checks user roles\n- Returns HTTP responses"
note for BusinessLogicLayer "Business Logic Layer\n- Validates data\n- Applies business rules\n- Enforces constraints\n- Manages workflows"
note for PersistenceLayer "Data Access Layer\n- Handles CRUD operations\n- Manages database queries\n- Abstracts data storage"
note for Database "Database Layer (MySQL)\n- Stores data permanently\n- Tables: users, places, bookings\n  reviews, amenities, place_amenities\n- Manages transactions"