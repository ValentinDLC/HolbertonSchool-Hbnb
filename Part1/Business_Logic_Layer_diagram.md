classDiagram

    %% ===================
    %% Base class (shared attributes and methods)
    %% ===================
    class BaseModel {
        +String UUid
        +DateTime created_at
        +DateTime updated_at
        +save()
        +update()
        +delete()
    }

    %% ===================
    %% User, Place, Review, Amenity classes
    %% ====================
    class User {
        +String first_name
        +String last_name
        +String email
        +String password
        +Boolean is_admin
        +register()
    }

    class Place {
        +String title
        +String description
        +Float price
        +Float latitude
        +Float longitude
        +create()
        +list_all()
    }

    class Review {
        +String text
        +Int rating
        +post()
    }

    class Amenity {
        +String name
        +String description
    }

    %% ===================
    %% Inheritance relationships
    %% ===================
    User <|-- BaseModel
    Place <|-- BaseModel
    Review <|-- BaseModel
    Amenity <|-- BaseModel

    %% ===================
    %% Associations
    %% ===================

    %% User can own multiple Places...
    User "1" -- "0..*" Place : owns

    %% each Place can have multiple Reviews...
    Place "1" -- "0..*" Review : receives

    %% each Review is written by a User...
    User "1" -- "0..*" Review : writes

    %% and each Place can have multiple Amenities.
    Place "1" -- "0..*" Amenity : has
