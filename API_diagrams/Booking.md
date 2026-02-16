sequenceDiagram
    participant User as User (Presentation)
    participant API as API Layer (Presentation)
    participant BL as Business Logic
    participant Repo as Repository (Persistence)
    participant DB as Database (Persistence)

%% ================================
%% 1. CREATE BOOKING
%% ================================
    Note over User,DB: 1. CREATE BOOKING
    User->>API: POST /api/bookings {placeId, checkInDate, checkOutDate}
    API->>API: verify_jwt_token()
    API->>BL: create_booking(bookingData, userId)
    BL->>BL: validate_booking_data(bookingData)
    BL->>BL: validate_dates(checkInDate, checkOutDate)
    BL->>Repo: find_place_by_id(placeId)
    Repo->>DB: SELECT * FROM Places WHERE id=?
    DB-->>Repo: place
    Repo-->>BL: place
    BL->>Repo: check_availability(placeId, checkInDate, checkOutDate)
    Repo->>DB: SELECT * FROM Bookings WHERE placeId=? AND dates overlap
    DB-->>Repo: overlapping bookings
    Repo-->>BL: availability status
    BL->>BL: calculate_total_price(pricePerNight, numberOfNights)
    BL->>BL: generate_uuid()
    BL->>BL: set_status('pending')
    BL->>Repo: save_booking(booking_object)
    Repo->>DB: INSERT INTO Bookings
    DB-->>Repo: booking_saved
    Repo-->>BL: booking_saved
    BL-->>API: booking_created
    API-->>User: 201 Created {id, placeId, checkInDate, checkOutDate, totalPrice, status}

%% ================================
%% 2. GET ALL BOOKINGS (USER)
%% ================================
    Note over User,DB: 2. GET ALL BOOKINGS (User's bookings)
    User->>API: GET /api/bookings
    API->>API: verify_jwt_token()
    API->>BL: get_user_bookings(userId)
    BL->>Repo: find_bookings_by_user(userId)
    Repo->>DB: SELECT b.*, p.title FROM Bookings b JOIN Places p WHERE userId=?
    DB-->>Repo: bookings[]
    Repo-->>BL: bookings[]
    BL-->>API: bookings[]
    API-->>User: 200 OK {bookings[]}

%% ================================
%% 3. GET BOOKING BY ID
%% ================================
    Note over User,DB: 3. GET BOOKING BY ID
    User->>API: GET /api/bookings/{id}
    API->>API: verify_jwt_token()
    API->>BL: get_booking_by_id(bookingId, userId)
    BL->>Repo: find_booking_by_id(bookingId)
    Repo->>DB: SELECT b.*, p.title, u.firstName FROM Bookings b JOIN Places p JOIN Users u
    DB-->>Repo: booking
    Repo-->>BL: booking
    BL->>BL: verify_access(booking.userId, userId)
    BL-->>API: booking
    API-->>User: 200 OK {booking details}

%% ================================
%% 4. UPDATE BOOKING STATUS
%% ================================
    Note over User,DB: 4. UPDATE BOOKING STATUS
    User->>API: PUT /api/bookings/{id}/status {status}
    API->>API: verify_jwt_token()
    API->>BL: update_booking_status(bookingId, status, userId)
    BL->>Repo: find_booking_by_id(bookingId)
    Repo->>DB: SELECT * FROM Bookings WHERE id=?
    DB-->>Repo: booking
    Repo-->>BL: booking
    BL->>BL: verify_authorization(userId, booking)
    BL->>BL: validate_status_transition(currentStatus, newStatus)
    BL->>Repo: update_booking_status(bookingId, status)
    Repo->>DB: UPDATE Bookings SET status=?, updatedAt=NOW() WHERE id=?
    DB-->>Repo: updated_booking
    Repo-->>BL: updated_booking
    BL-->>API: updated_booking
    API-->>User: 200 OK {booking with new status}

%% ================================
%% 5. CANCEL BOOKING
%% ================================
    Note over User,DB: 5. CANCEL BOOKING
    User->>API: DELETE /api/bookings/{id}
    API->>API: verify_jwt_token()
    API->>BL: cancel_booking(bookingId, userId)
    BL->>Repo: find_booking_by_id(bookingId)
    Repo->>DB: SELECT * FROM Bookings WHERE id=?
    DB-->>Repo: booking
    Repo-->>BL: booking
    BL->>BL: verify_user_is_owner(booking.userId, userId)
    BL->>BL: check_cancellation_policy(booking.checkInDate)
    BL->>Repo: update_booking_status(bookingId, 'cancelled')
    Repo->>DB: UPDATE Bookings SET status='cancelled', updatedAt=NOW() WHERE id=?
    DB-->>Repo: success
    Repo-->>BL: success
    BL-->>API: success
    API-->>User: 200 OK {message: "Booking cancelled"}

%% ================================
%% 6. GET PLACE BOOKINGS (OWNER)
%% ================================
    Note over User,DB: 6. GET PLACE BOOKINGS (Place owner only)
    User->>API: GET /api/places/{placeId}/bookings
    API->>API: verify_jwt_token()
    API->>BL: get_place_bookings(placeId, userId)
    BL->>Repo: find_place_by_id(placeId)
    Repo->>DB: SELECT * FROM Places WHERE id=?
    DB-->>Repo: place
    Repo-->>BL: place
    BL->>BL: verify_ownership(place.ownerId, userId)
    BL->>Repo: find_bookings_by_place(placeId)
    Repo->>DB: SELECT b.*, u.firstName FROM Bookings b JOIN Users u WHERE placeId=?
    DB-->>Repo: bookings[]
    Repo-->>BL: bookings[]
    BL-->>API: bookings[]
    API-->>User: 200 OK {bookings[]}

%% ================================
%% 7. CONFIRM BOOKING (OWNER)
%% ================================
    Note over User,DB: 7. CONFIRM BOOKING (Place owner only)
    User->>API: POST /api/bookings/{id}/confirm
    API->>API: verify_jwt_token()
    API->>BL: confirm_booking(bookingId, userId)
    BL->>Repo: find_booking_by_id(bookingId)
    Repo->>DB: SELECT * FROM Bookings WHERE id=?
    DB-->>Repo: booking
    Repo-->>BL: booking
    BL->>Repo: find_place_by_id(booking.placeId)
    Repo->>DB: SELECT * FROM Places WHERE id=?
    DB-->>Repo: place
    Repo-->>BL: place
    BL->>BL: verify_ownership(place.ownerId, userId)
    BL->>BL: validate_status(booking.status == 'pending')
    BL->>Repo: update_booking_status(bookingId, 'confirmed')
    Repo->>DB: UPDATE Bookings SET status='confirmed', updatedAt=NOW() WHERE id=?
    DB-->>Repo: updated_booking
    Repo-->>BL: updated_booking
    BL-->>API: updated_booking
    API-->>User: 200 OK {booking confirmed}

%% ================================
%% 8. REJECT BOOKING (OWNER)
%% ================================
    Note over User,DB: 8. REJECT BOOKING (Place owner only)
    User->>API: POST /api/bookings/{id}/reject
    API->>API: verify_jwt_token()
    API->>BL: reject_booking(bookingId, userId)
    BL->>Repo: find_booking_by_id(bookingId)
    Repo->>DB: SELECT * FROM Bookings WHERE id=?
    DB-->>Repo: booking
    Repo-->>BL: booking
    BL->>Repo: find_place_by_id(booking.placeId)
    Repo->>DB: SELECT * FROM Places WHERE id=?
    DB-->>Repo: place
    Repo-->>BL: place
    BL->>BL: verify_ownership(place.ownerId, userId)
    BL->>BL: validate_status(booking.status == 'pending')
    BL->>Repo: update_booking_status(bookingId, 'rejected')
    Repo->>DB: UPDATE Bookings SET status='rejected', updatedAt=NOW() WHERE id=?
    DB-->>Repo: updated_booking
    Repo-->>BL: updated_booking
    BL-->>API: updated_booking
    API-->>User: 200 OK {booking rejected}

%% ================================
%% 9. COMPLETE BOOKING (AUTOMATIC)
%% ================================
    Note over User,DB: 9. COMPLETE BOOKING (System automatic process)
    User->>API: POST /api/bookings/{id}/complete
    API->>API: verify_jwt_token()
    API->>BL: complete_booking(bookingId)
    BL->>Repo: find_booking_by_id(bookingId)
    Repo->>DB: SELECT * FROM Bookings WHERE id=?
    DB-->>Repo: booking
    Repo-->>BL: booking
    BL->>BL: validate_checkout_date_passed(booking.checkOutDate)
    BL->>Repo: update_booking_status(bookingId, 'completed')
    Repo->>DB: UPDATE Bookings SET status='completed', updatedAt=NOW() WHERE id=?
    DB-->>Repo: updated_booking
    Repo-->>BL: updated_booking
    BL-->>API: updated_booking
    API-->>User: 200 OK {booking completed}