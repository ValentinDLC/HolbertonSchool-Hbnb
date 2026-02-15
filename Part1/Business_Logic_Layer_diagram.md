classDiagram
direction TB

    %% ===================
    %% Base class (shared attributes and methods)
    %% ===================
    class BaseModel {
        <<abstract>>
        - id : UUID
        - created_at : DateTime
        - updated_at : DateTime
        # save() void
        # update() void
        # delete() void
        + to_dict() dict
    }

    %% ===================
    %% User class
    %% ====================
    class User {
        + String first_name
        + String last_name
        + String email
        - String password
        + Boolean is_admin
        + register() bool
        + authenticate() bool
        + add_place(title, description, price, latitude, longitude) bool
        + add_amenity(name, description) bool
        + has_reserved(place) bool
        + add_review(text, rating) bool
    }

    %% ===================
    %% Place class
    %% ====================
    class Place {
        + String name
        + String title
        + String description
        + Float price
        - Float latitude
        - Float longitude
        + String owner_id
        + List~Amenity~ amenities
        + list_all() List~Place~
        + get_by_criteria(criteria) List~Place~
        - get_all_reservation() List
    }

    %% ===================
    %% Review class
    %% ====================
    class Review {
        + String text
        + Int rating
        + String user_id
        + String place_id
        + list_by_place(place_id) List~Review~
    }

    %% ===================
    %% Amenity class
    %% ====================
    class Amenity {
        + String name
        + String description
        + list_all() List~Amenity~
    }

    %% ===================
    %% Inheritance relationships
    %% ===================
    BaseModel <|-- User : inherits
    BaseModel <|-- Place : inherits
    BaseModel <|-- Review : inherits
    BaseModel <|-- Amenity : inherits

    %% ===================
    %% Associations
    %% ===================
    User "1" --> "0..*" Place : manages
    User "1" --> "0..*" Review : writes
    Place "0..*" --> "0..*" Amenity : offers
    Review "0..*" --> "1" Place : about

    %% ===================
    %% Styling
    %% ===================
    style BaseModel fill:#E3F2FD,stroke:#2196F3,stroke-width:2px,color:#1565C0
    style User fill:#F5F5F5,stroke:#616161,stroke-width:1px,color:#212121
    style Place fill:#F5F5F5,stroke:#616161,stroke-width:1px,color:#212121
    style Review fill:#F5F5F5,stroke:#616161,stroke-width:1px,color:#212121
    style Amenity fill:#F5F5F5,stroke:#616161,stroke-width:1px,color:#212121
