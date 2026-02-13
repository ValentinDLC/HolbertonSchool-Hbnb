# HBnB — Amenity Management

## 📄 Objective
The **Amenity Management module** manages amenities linked to places.  
It ensures **places have correct, searchable amenities**.

---

## 🔹 Roles of Amenity Management

1. **Add an amenity**  
   - Create a new amenity with name, description, and category.  
   - Link amenity to one or multiple places.  

2. **Retrieve an amenity**  
   - Get details by amenity ID.  
   - List amenities for a specific place.  

---

## 🔹 Beginner Tips

- **Use junction tables** for many-to-many relationships (Place ↔ Amenity).  
- **Validate amenity data** before saving.  
- **Alt / branch thinking**: handle duplicates or missing data gracefully.  

---

## 🔹 How it Works (Step-by-Step)

1. **User or host adds an amenity**.  
2. **API layer receives request**, passes to BL.  
3. **BL validates** and prepares the data.  
4. **Repo saves** amenity in the database.  
5. **BL returns confirmation** to API.  
6. **API responds** with success or error message.  

---

## 🔹 Key Concepts

- **Many-to-many relationships**: Amenity ↔ Place.  
- **Separation of concerns**: API → BL → Repo → DB.  
- **Validation**: Prevents duplicate amenities or invalid data.  

---

## 🔹 Summary

Amenity Management ensures **places are correctly described and searchable**.  
Beginners should focus on **how BL links amenities to places and maintains consistency**.


sequenceDiagram
    participant User
    participant API as PresentationLayer
    participant BL as BusinessLogicLayer
    participant Repo as RepositoryLayer
    participant DB as Database

    %% ================================
    %% CREATE AMENITY
    %% ================================
    User->>API: POST /api/amenities {name, description, category}
    API->>BL: create_amenity(amenityData)
    BL->>BL: validate_amenity_data(amenityData)
    alt validation fails
        BL-->>API: ValidationError
        API-->>User: 400 Bad Request
    else validation succeeds
        BL->>Repo: save_amenity(amenityData)
        Repo->>DB: INSERT INTO Amenities (id, name, description, category, created_at, updated_at)
        DB-->>Repo: amenity_saved(amenityId)
        Repo-->>BL: amenity_saved
        BL-->>API: return_amenity(amenityId)
        API-->>User: 201 Created {amenityId, name, description, category}
    end

    %% ================================
    %% GET AMENITY BY ID
    %% ================================
    User->>API: GET /api/amenities/{id}
    API->>BL: get_amenity_by_id(amenityId)
    BL->>Repo: find_amenity_by_id(amenityId)
    Repo->>DB: SELECT * FROM Amenities WHERE id=amenityId
    DB-->>Repo: amenity | null
    Repo-->>BL: amenity | null
    alt amenity exists
        BL-->>API: return_amenity(amenity)
        API-->>User: 200 OK {amenity details}
    else amenity not found
        BL-->>API: AmenityNotFoundError
        API-->>User: 404 Not Found
    end

    %% ================================
    %% UPDATE AMENITY
    %% ================================
    User->>API: PUT /api/amenities/{id} {fields_to_update}
    API->>BL: update_amenity(amenityId, data)
    BL->>BL: validate_update_data(data)
    alt validation fails
        BL-->>API: ValidationError
        API-->>User: 400 Bad Request
    else validation succeeds
        BL->>Repo: update_amenity(amenityId, data)
        Repo->>DB: UPDATE Amenities SET ... WHERE id=amenityId
        DB-->>Repo: updated_amenity
        Repo-->>BL: updated_amenity
        BL-->>API: return_updated_amenity(updated_amenity)
        API-->>User: 200 OK {updated fields}
    end

    %% ================================
    %% DELETE AMENITY
    %% ================================
    User->>API: DELETE /api/amenities/{id}
    API->>BL: delete_amenity(amenityId)
    BL->>Repo: delete_amenity(amenityId)
    Repo->>DB: DELETE FROM Amenities WHERE id=amenityId
    DB-->>Repo: success
    Repo-->>BL: success
    BL-->>API: return_success()
    API-->>User: 200 OK
