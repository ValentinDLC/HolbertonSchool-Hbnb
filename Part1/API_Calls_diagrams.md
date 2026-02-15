# 1 User Registration

```mermaid
sequenceDiagram
    %% Layers:
    %% Presentation: User, API
    %% Business Logic: Facade, BusinessLogic, Repository
    %% Persistence: Persistence

    actor User
    participant API as API (Presentation Layer)
    participant Facade as "Facade pattern"
    participant BusinessLogic as Business Logic
    participant Repository as "Repository (Interface)"
    participant Persistence as Persistence Layer

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
        BusinessLogic --> BusinessLogic: User(user_data)  # Création de l'instance
        BusinessLogic ->> Repository: save(user)
        Repository ->> Persistence: insert_user(user)
        alt "Persistence error"
            Persistence -->> Repository: 500 Internal Server Error
            Repository -->> BusinessLogic: Persistence failed
            BusinessLogic -->> Facade: 500 Internal Server Error
            Facade -->> API: 500 Internal Server Error
            API -->> User: An error occurred, please try again
        else "Persistence success"
            Persistence -->> Repository: OK + user_id
            Repository -->> BusinessLogic: User saved + user_id
            BusinessLogic -->> Facade: return user + user_id
            Facade -->> API: 201 Created + user object
            API -->> User: Success + user_id
        end
```

# 2 Place Creation

```mermaid
sequenceDiagram
    %% Layers:
    %% Presentation: User, API
    %% Business Logic: Facade, PlaceLogic, PlaceRepository
    %% Persistence: Database

    actor User
    participant API as API (Presentation Layer)
    participant Facade as Facade
    participant PlaceLogic as Business Logic
    participant PlaceRepository as Repository (Interface)
    participant Database as Persistence

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
        PlaceLogic --> PlaceLogic: Place(place_data)  # Création de l'instance
        PlaceLogic ->> PlaceRepository: save(place_object)
        PlaceRepository ->> Database: INSERT place_object
        alt Persistence error
            Database -->> PlaceRepository: 500 Internal Server Error
            PlaceRepository -->> PlaceLogic: Persistence failed
            PlaceLogic -->> Facade: 500 Internal Server Error
            Facade -->> API: 500 Internal Server Error
            API -->> User: An error occurred, please try again
        else Persistence success
            Database -->> PlaceRepository: OK
            PlaceRepository -->> PlaceLogic: Place saved
            PlaceLogic -->> Facade: Return place_id
            Facade -->> API: 201 Created + place info
            API -->> User: Place successfully created
        end
    end
```

# 3 Review Submission

```mermaid
sequenceDiagram
    actor User
    participant API as API (Presentation)
    participant Facade
    participant Logic as Business Logic
    participant Repo as Repository (interface)
    participant DB as Persistence

    User ->> API: POST /reviews with data
    API ->> Facade: create_review(data)

    alt Invalid input (missing or bad rating)
        Facade -->> API: 400 Bad Request
        API -->> User: Review data invalid
    else No reservation
        Facade ->> Logic: validate_reservation(user_id, place_id)
        Logic ->> Repo: check_reservation(user_id, place_id)
        Repo ->> DB: query_reservation()
        DB -->> Repo: No match
        Repo -->> Logic: Forbidden
        Logic -->> Facade: 403 Forbidden
        Facade -->> API: Review not allowed
        API -->> User: Must reserve place first
    else Valid input + reserved
        Facade ->> Logic: create_review_instance(data)
        Logic --> Logic: Review(data)  # Création de l'instance
        Logic ->> Repo: save(review)
        Repo ->> DB: insert_review()
        alt Persistence error
            DB -->> Repo: 500 Internal Server Error
            Repo -->> Logic: Persistence failed
            Logic -->> Facade: 500 Internal Server Error
            Facade -->> API: 500 Internal Server Error
            API -->> User: An error occurred, please try again
        else Persistence success
            DB -->> Repo: OK
            Repo -->> Logic: Done
            Logic -->> Facade: review object (id, rating, comment, date)
            Facade -->> API: 201 Created
            API -->> User: Review submitted
        end
    end
```

# 4 Fetching List of Places

```mermaid
sequenceDiagram
    actor User as User
    participant API as Presentation (API)
    participant Facade as Facade
    participant BusinessLogic as Business Logic
    participant Repository as Repository (Interface)
    participant Database as Persistence

    User->>API: GET /api/v1/places?filters

    alt Invalid parameters
        API-->>User: 400 Bad Request
    else Authentication/Authorization error
        API-->>User: 401 Unauthorized / 403 Forbidden
    else
        API->>Facade: getPlaces(filters)
        Facade->>BusinessLogic: getPlaces(filters)
        BusinessLogic->>Repository: findPlaces(query)
        Repository->>Database: SELECT ... WHERE ...

        alt Database error
            Database-->>Repository: SQL Error
            Repository-->>BusinessLogic: Technical error
            BusinessLogic-->>Facade: Technical error
            Facade-->>API: Technical error
            API-->>User: 500 Internal Server Error
        else No results found
            Database-->>Repository: Empty ResultSet
            Repository-->>BusinessLogic: Empty ResultSet
            BusinessLogic-->>Facade: PlaceCollectionDTO (empty list, metadata)
            Facade-->>API: PlaceCollectionDTO
            API-->>User: 200 OK (empty list)
        else Results found
            Database-->>Repository: ResultSet
            Repository-->>BusinessLogic: ResultSet
            BusinessLogic-->>Facade: PlaceCollectionDTO (list, metadata)
            Facade-->>API: PlaceCollectionDTO
            API-->>User: 200 OK (+ body)
        end
    end
```
