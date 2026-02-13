# HBnB — Place Management

## 📄 Objective
The **Place Management module** handles all operations related to properties listed on HBnB.  
Its main goal is to allow users (hosts) to **create, update, search, and manage places**, while maintaining data integrity and availability.

---

## 🔹 Roles of Place Management

1. **Create a new place**  
   - Collect information: title, description, location, price, number of rooms, max guests, amenities.  
   - Validate input and availability.  
   - Assign a unique identifier (UUID) and timestamps.  

2. **Update place details**  
   - Allows hosts to change information.  
   - Validates new data and ensures consistency.  

3. **Search and retrieve places**  
   - Users can search by city, dates, or filters.  
   - Ensures only available places are returned.  

4. **Delete places**  
   - Soft delete preferred to keep historical booking data.  

5. **Manage amenities**  
   - Link amenities to a place.  
   - Maintain many-to-many relationships using junctions.  

---

## 🔹 Beginner Tips

- **Always validate data** before saving.  
- **Handle availability checks** to avoid double bookings.  
- **Keep relationships consistent** (Place ↔ Amenities).  
- **Alt / branch thinking**: handle unavailable places gracefully.  

---

## 🔹 How it Works (Step-by-Step)

1. **User submits request** (create, update, delete, search).  
2. **API layer receives request** → minimal checks, forwards to BL.  
3. **Business Logic Layer (BL)**  
   - Validates inputs.  
   - Checks rules (availability, max guests, etc.).  
   - Prepares data for the repository.  
4. **Repository Layer**  
   - Saves, updates, or queries the database.  
   - Returns results to BL.  
5. **BL formats results** → success/failure messages.  
6. **API returns response** to the user.  

---

## 🔹 Key Concepts

- **Availability check**: Ensures no conflicting bookings.  
- **Many-to-many relationships**: Places can have multiple amenities; managed via junction tables.  
- **Soft delete**: Retains historical booking data.  
- **Separation of concerns**: API → BL → Repo → DB.  

---

## 🔹 Summary

The Place Management module is crucial for the **HBnB user experience**, allowing hosts to list properties while ensuring **availability and consistency**.  
Beginners should **focus on flow and rules**, not just the database operations.



sequenceDiagram
    participant User
    participant API as PresentationLayer
    participant BL as BusinessLogicLayer
    participant Repo as RepositoryLayer
    participant DB as Database

    %% ================================
    %% CREATE PLACE
    %% ================================
    User->>API: POST /api/places {title, description, price, location, maxGuests, numberOfRooms}
    API->>BL: create_place(placeData)
    BL->>BL: validate_place_data(placeData)
    alt validation fails
        BL-->>API: ValidationError
        API-->>User: 400 Bad Request
    else validation succeeds
        BL->>BL: generate_uuid()
        BL->>BL: set_timestamps()
        BL->>Repo: save_place(place_object)
        Repo->>DB: INSERT INTO Places (id, host_id, title, description, price, latitude, longitude, maxGuests, numberOfRooms, created_at, updated_at)
        DB-->>Repo: place_saved_confirmation
        Repo-->>BL: place_saved
        BL-->>API: place_created
        API-->>User: 201 Created {id, title, description, price, location, maxGuests, numberOfRooms}
    end

    %% ================================
    %% GET PLACE BY ID
    %% ================================
    User->>API: GET /api/places/{id}
    API->>BL: get_place_by_id(placeId)
    BL->>Repo: find_place_by_id(placeId)
    Repo->>DB: SELECT * FROM Places WHERE id=placeId
    DB-->>Repo: place | null
    Repo-->>BL: place | null
    alt place exists
        BL-->>API: return_place(place)
        API-->>User: 200 OK {place details}
    else place not found
        BL-->>API: PlaceNotFoundError
        API-->>User: 404 Not Found
    end

    %% ================================
    %% UPDATE PLACE
    %% ================================
    User->>API: PUT /api/places/{id} {fields_to_update}
    API->>BL: update_place(placeId, data)
    BL->>BL: validate_update_data(data)
    alt validation fails
        BL-->>API: ValidationError
        API-->>User: 400 Bad Request
    else validation succeeds
        BL->>Repo: update_place(placeId, data)
        Repo->>DB: UPDATE Places SET ... WHERE id=placeId
        DB-->>Repo: updated_place
        Repo-->>BL: updated_place
        BL-->>API: return_updated_place(updated_place)
        API-->>User: 200 OK {updated fields}
    end

    %% ================================
    %% DELETE PLACE
    %% ================================
    User->>API: DELETE /api/places/{id}
    API->>BL: delete_place(placeId)
    BL->>Repo: delete_place(placeId)
    Repo->>DB: DELETE FROM Places WHERE id=placeId
    DB-->>Repo: success
    Repo-->>BL: success
    BL-->>API: return_success()
    API-->>User: 200 OK

    %% ================================
    %% ADD AMENITY TO PLACE
    %% ================================
    User->>API: POST /api/places/{id}/amenities {amenity_id}
    API->>BL: add_amenity_to_place(placeId, amenityId)
    BL->>Repo: link_place_amenity(placeId, amenityId)
    Repo->>DB: INSERT INTO PlaceAmenity (place_id, amenity_id)
    DB-->>Repo: link_saved
    Repo-->>BL: link_saved
    BL-->>API: amenity_added
    API-->>User: 201 Created {placeId, amenityId}

    %% ================================
    %% REMOVE AMENITY FROM PLACE
    %% ================================
    User->>API: DELETE /api/places/{id}/amenities/{amenityId}
    API->>BL: remove_amenity_from_place(placeId, amenityId)
    BL->>Repo: unlink_place_amenity(placeId, amenityId)
    Repo->>DB: DELETE FROM PlaceAmenity WHERE place_id=placeId AND amenity_id=amenityId
    DB-->>Repo: success
    Repo-->>BL: success
    BL-->>API: amenity_removed
    API-->>User: 200 OK
