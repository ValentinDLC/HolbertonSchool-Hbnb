# HBnB — Review Management

## 📄 Objective
The **Review Management module** handles everything related to user reviews of places.  
It ensures that **reviews are valid, linked to bookings, and ratings are calculated correctly**.

---

## 🔹 Roles of Review Management

1. **Post a review**  
   - User can submit a comment and rating for a place they booked.  
   - Validate that the booking exists and belongs to the user.  

2. **Update a review**  
   - Users can edit their review if needed.  
   - Update average ratings for the place automatically.  

3. **Retrieve reviews**  
   - Fetch reviews by review ID, user, or place.  

4. **Report a review**  
   - Users can report inappropriate reviews.  
   - Admins can take action.  

---

## 🔹 Beginner Tips

- **Always validate** that the user actually stayed at the place before accepting a review.  
- **Update average ratings** after any create or update to keep stats accurate.  
- **Alt / branch thinking**: success vs invalid review paths.  
- **Separation of concerns**: BL handles validation and calculations, Repo handles database CRUD.

---

## 🔹 How it Works (Step-by-Step)

1. **User submits a review**.  
2. **API layer** receives it and forwards to BL.  
3. **Business Logic Layer (BL)**  
   - Validates booking ownership.  
   - Validates rating value (e.g., 1–5).  
   - Updates average rating for the place.  
4. **Repository Layer**  
   - Saves or updates review in the database.  
5. **BL returns result** to API.  
6. **API responds** with success or error message.  

---

## 🔹 Key Concepts

- **Validation**: Only allow reviews for confirmed bookings.  
- **Average rating**: Keep updated whenever reviews change.  
- **Reporting system**: Supports moderation.  
- **Separation of concerns**: API → BL → Repo → DB.

---

## 🔹 Summary

Review Management ensures **trustworthy feedback** for places.  
Beginners should focus on **flow, validation, and automatic calculations**.


sequenceDiagram
    participant User
    participant API as PresentationLayer
    participant BL as BusinessLogicLayer
    participant Repo as RepositoryLayer
    participant DB as Database

    %% ================================
    %% CREATE REVIEW
    %% ================================
    User->>API: POST /api/reviews {placeId, bookingId, rating, comment}
    API->>BL: create_review(reviewData)
    BL->>BL: validate_review_data(reviewData)

    %% VERIFY BOOKING
    BL->>Repo: verify_booking(bookingId, userId)
    Repo->>DB: SELECT * FROM Bookings WHERE id=bookingId AND guest_id=userId AND status='completed'
    DB-->>Repo: booking | null
    Repo-->>BL: booking valid / invalid
    alt booking invalid
        BL-->>API: returnError("Booking invalid for review")
        API-->>User: 400 Bad Request
    else booking valid
        %% SAVE REVIEW
        BL->>Repo: save_review(reviewData)
        Repo->>DB: INSERT INTO Reviews (id, place_id, user_id, rating, comment, created_at, updated_at)
        DB-->>Repo: review_saved(reviewId)
        Repo-->>BL: review_saved

        %% UPDATE AVERAGE RATING
        BL->>Repo: update_average_rating(placeId)
        Repo->>DB: UPDATE Places SET averageRating = (SELECT AVG(rating) FROM Reviews WHERE place_id=placeId)
        DB-->>Repo: rating_updated
        Repo-->>BL: rating_updated

        %% RETURN SUCCESS
        BL-->>API: return_review(reviewId)
        API-->>User: 201 Created {reviewId, placeId, rating, comment}
    end

    %% ================================
    %% GET REVIEW BY ID
    %% ================================
    User->>API: GET /api/reviews/{id}
    API->>BL: get_review_by_id(reviewId)
    BL->>Repo: find_review_by_id(reviewId)
    Repo->>DB: SELECT * FROM Reviews WHERE id=reviewId
    DB-->>Repo: review | null
    Repo-->>BL: review | null
    alt review exists
        BL-->>API: return_review(review)
        API-->>User: 200 OK {review details}
    else review not found
        BL-->>API: ReviewNotFoundError
        API-->>User: 404 Not Found
    end

    %% ================================
    %% UPDATE REVIEW
    %% ================================
    User->>API: PUT /api/reviews/{id} {fields_to_update}
    API->>BL: update_review(reviewId, data)
    BL->>BL: validate_update_data(data)
    alt validation fails
        BL-->>API: ValidationError
        API-->>User: 400 Bad Request
    else validation succeeds
        BL->>Repo: update_review(reviewId, data)
        Repo->>DB: UPDATE Reviews SET ... WHERE id=reviewId
        DB-->>Repo: updated_review
        Repo-->>BL: updated_review

        %% UPDATE AVERAGE RATING
        BL->>Repo: update_average_rating(placeId)
        Repo->>DB: UPDATE Places SET averageRating = (SELECT AVG(rating) FROM Reviews WHERE place_id=placeId)
        DB-->>Repo: rating_updated
        Repo-->>BL: rating_updated

        BL-->>API: return_updated_review(updated_review)
        API-->>User: 200 OK {updated fields}
    end

    %% ================================
    %% REPORT REVIEW
    %% ================================
    User->>API: POST /api/reviews/{id}/report {reason}
    API->>BL: report_review(reviewId, reason)
    BL->>Repo: mark_review_reported(reviewId, reason)
    Repo->>DB: UPDATE Reviews SET reported=true, report_reason=reason WHERE id=reviewId
    DB-->>Repo: success
    Repo-->>BL: success
    BL-->>API: return_success()
    API-->>User: 200 OK
