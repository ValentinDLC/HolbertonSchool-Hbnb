flowchart TB

    %% ===================
    %% Presentation Layer
    %% ===================
    subgraph P["Presentation Layer"]
        direction TB
        API["API / Endpoints\n(Controllers / Routes)\n- getUser()\n- createPlace()"]
        SVC["Services\n(Request handling)"]
        API --> SVC
    end

    %% ===================
    %% Business Logic Layer
    %% ===================
    subgraph B["Business Logic Layer"]
        direction TB
        FACADE["HBnB Facade\n(Unified interface)\n- createUser()\n- getPlace()"]
        MODELS["Domain Models\n(User, Place, Review, Amenity)\n+ Business Rules"]
        FACADE --> MODELS
    end

    %% ===================
    %% Persistence Layer
    %% ===================
    subgraph D["Persistence Layer"]
        direction TB
        REPO["Repositories / Storage\n(Data access abstraction)\n- save()\n- findById()"]
        DB["Database\n(Persistent storage)"]
        REPO --> DB
    end

    %% ===================
    %% Layer Communication (Dependencies)
    %% ===================
    SVC -->|Calls Facade| FACADE
    MODELS -->|CRUD / Data operations| REPO
