# 1 User Registration

```mermaid
%%{init: {'theme':'base', 'themeVariables': {
  'actorBkg':'#E3F2FD',
  'actorBorder':'#2196F3',
  'primaryColor':'#E3F2FD',
  'primaryBorderColor':'#2196F3',
  'primaryTextColor':'#1565C0',
  'signalColor':'#2196F3',
  'signalTextColor':'#FFFFFF',
  'labelTextColor':'#1565C0'
}}}%%
sequenceDiagram
    %% Layers:
    %% Presentation: User, API
    %% Business Logic: Facade, BusinessLogic, Repository
    %% Persistence: Database

    actor User
    participant API as API (Presentation Layer)
    participant Facade as Facade
    participant BusinessLogic as Business Logic
    participant Repository as Repository (Interface)
    participant Database as Database

    User ->> API: POST /users with data
    API ->> Facade: create_user(data)

    alt "Missing required fields"
        Facade -->> API: 400 Bad Request - Missing fields
        API -->> User: Please fill all required fields
    else "Invalid email format"
        Facade -->> API: 400 Bad Request - Invalid email
        API -->> User: Invalid email address
    else "Password too short"
        Facade -->> API: 400 Bad Request - Weak password
        API -->> User: Password must be at least 8 characters
    else "Email already exists"
        Facade -->> API: 409 Conflict - Email already registered
        API -->> User: Email already in use
    else "Valid data"
        Facade ->> BusinessLogic: create_user_instance(data)
        BusinessLogic --> BusinessLogic: User(user_data)
        BusinessLogic ->> Repository: save(user)
        Repository ->> Database: INSERT user
        alt "Database error"
            Database -->> Repository: 500 Internal Server Error
            Repository -->> BusinessLogic: Persistence failed
            BusinessLogic -->> Facade: 500 Internal Server Error
            Facade -->> API: 500 Internal Server Error
            API -->> User: An error occurred, please try again
        else "Success"
            Database -->> Repository: OK + user_id
            Repository -->> BusinessLogic: User saved + user_id
            BusinessLogic -->> Facade: return user + user_id
            Facade -->> API: 201 Created + user object
            API -->> User: Success + user_id
        end
    end
```

# 2 Place Creation

```mermaid
%%{init: {'theme':'base', 'themeVariables': {
  'actorBkg':'#E3F2FD',
  'actorBorder':'#2196F3',
  'primaryColor':'#E3F2FD',
  'primaryBorderColor':'#2196F3',
  'primaryTextColor':'#1565C0',
  'signalColor':'#2196F3',
  'signalTextColor':'#FFFFFF',
  'labelTextColor':'#1565C0'
}}}%%
sequenceDiagram
    %% Layers:
    %% Presentation: User, API
    %% Business Logic: Facade, PlaceLogic, Repository
    %% Persistence: Database

    actor User
    participant API as API (Presentation Layer)
    participant Facade as Facade
    participant PlaceLogic as Business Logic
    participant Repository as Repository (Interface)
    participant Database as Database

    User ->> API: POST /places with place data
    API ->> Facade: create_place(data)

    alt Missing required fields
        Facade -->> API: 400 - Missing required fields
        API -->> User: Fill all required fields
    else Invalid price or location
        Facade -->> API: 400 - Invalid price/location
        API -->> User: Check your data
    else Invalid amenities
        Facade -->> API: 400 - Invalid amenities
        API -->> User: Provide valid amenities
    else Valid data
        Facade ->> PlaceLogic: validate and build place
        PlaceLogic --> PlaceLogic: Place(place_data)
        PlaceLogic ->> Repository: save(place_object)
        Repository ->> Database: INSERT place
        alt Database error
            Database -->> Repository: 500 Internal Server Error
            Repository -->> PlaceLogic: Persistence failed
            PlaceLogic -->> Facade: 500 Internal Server Error
            Facade -->> API: 500 Internal Server Error
            API -->> User: An error occurred, please try again
        else Success
            Database -->> Repository: OK + place_id
            Repository -->> PlaceLogic: Place saved + place_id
            PlaceLogic -->> Facade: Return place object
            Facade -->> API: 201 Created + place info
            API -->> User: Place successfully created
        end
    end
```

# 3 Review Submission

```mermaid
%%{init: {'theme':'base', 'themeVariables': {
  'actorBkg':'#E3F2FD',
  'actorBorder':'#2196F3',
  'primaryColor':'#E3F2FD',
  'primaryBorderColor':'#2196F3',
  'primaryTextColor':'#1565C0',
  'signalColor':'#2196F3',
  'signalTextColor':'#FFFFFF',
  'labelTextColor':'#1565C0'
}}}%%
sequenceDiagram
    actor User
    participant API as API (Presentation)
    participant Facade as Facade
    participant Logic as Business Logic
    participant Repository as Repository (Interface)
    participant Database as Database

    User ->> API: POST /reviews with data
    API ->> Facade: create_review(data)

    alt Invalid input (missing or bad rating)
        Facade -->> API: 400 Bad Request
        API -->> User: Review data invalid
    else No reservation
        Facade ->> Logic: validate_reservation(user_id, place_id)
        Logic ->> Repository: check_reservation(user_id, place_id)
        Repository ->> Database: SELECT reservation
        Database -->> Repository: No match
        Repository -->> Logic: Forbidden
        Logic -->> Facade: 403 Forbidden
        Facade -->> API: Review not allowed
        API -->> User: Must reserve place first
    else Valid input + reserved
        Facade ->> Logic: create_review_instance(data)
        Logic --> Logic: Review(data)
        Logic ->> Repository: save(review)
        Repository ->> Database: INSERT review
        alt Database error
            Database -->> Repository: 500 Internal Server Error
            Repository -->> Logic: Persistence failed
            Logic -->> Facade: 500 Internal Server Error
            Facade -->> API: 500 Internal Server Error
            API -->> User: An error occurred, please try again
        else Success
            Database -->> Repository: OK + review_id
            Repository -->> Logic: Review saved + review_id
            Logic -->> Facade: review object (id, rating, text, date)
            Facade -->> API: 201 Created
            API -->> User: Review submitted
        end
    end
```

# 4 Fetching List of Places

```mermaid
%%{init: {'theme':'base', 'themeVariables': {
  'actorBkg':'#E3F2FD',
  'actorBorder':'#2196F3',
  'primaryColor':'#E3F2FD',
  'primaryBorderColor':'#2196F3',
  'primaryTextColor':'#1565C0',
  'signalColor':'#2196F3',
  'signalTextColor':'#FFFFFF',
  'labelTextColor':'#1565C0'
}}}%%
sequenceDiagram
    actor User
    participant API as API (Presentation)
    participant Facade as Facade
    participant BusinessLogic as Business Logic
    participant Repository as Repository (Interface)
    participant Database as Database

    User->>API: GET /api/v1/places?filters

    alt Invalid parameters
        API-->>User: 400 Bad Request
    else Authentication/Authorization error
        API-->>User: 401 Unauthorized / 403 Forbidden
    else Valid request
        API->>Facade: get_places(filters)
        Facade->>BusinessLogic: get_places(filters)
        BusinessLogic->>Repository: find_places(query)
        Repository->>Database: SELECT * FROM places WHERE ...

        alt Database error
            Database-->>Repository: SQL Error
            Repository-->>BusinessLogic: Technical error
            BusinessLogic-->>Facade: Technical error
            Facade-->>API: Technical error
            API-->>User: 500 Internal Server Error
        else No results found
            Database-->>Repository: Empty ResultSet
            Repository-->>BusinessLogic: Empty list
            BusinessLogic-->>Facade: PlaceCollectionDTO (empty list, metadata)
            Facade-->>API: PlaceCollectionDTO
            API-->>User: 200 OK (empty list)
        else Results found
            Database-->>Repository: ResultSet
            Repository-->>BusinessLogic: List of Place objects
            BusinessLogic-->>Facade: PlaceCollectionDTO (list, metadata)
            Facade-->>API: PlaceCollectionDTO
            API-->>User: 200 OK + places data
        end
    end
```
