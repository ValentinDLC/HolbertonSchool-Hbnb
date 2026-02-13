# HBnB — Booking Management

## 📄 Objective
The **Booking Management module** handles creating, updating, and canceling reservations for places.  
It ensures **availability, accurate pricing, and user authorization**.

---

## 🔹 Roles of Booking Management

1. **Create a booking**  
   - Collect guest, place, dates, number of guests.  
   - Validate availability.  
   - Calculate total price.  
   - Generate payment if needed.  

2. **Update a booking**  
   - Allows changing dates or number of guests.  
   - Checks for availability conflicts.  

3. **Cancel a booking**  
   - Verify cancellation rules (e.g., allowed time before check-in).  
   - Update database and related payments.  

4. **Retrieve bookings**  
   - Users can view their bookings.  
   - Admins can see all bookings.  

---

## 🔹 Beginner Tips

- **Check availability first** before creating a booking.  
- **Calculate total price carefully** considering guests and stay duration.  
- **Alt / branch thinking**: handle available vs unavailable.  
- **Always link bookings to payments** for consistency.  

---

## 🔹 How it Works (Step-by-Step)

1. **User sends booking request**.  
2. **API layer** receives it and forwards to BL.  
3. **Business Logic Layer (BL)**  
   - Validates input.  
   - Checks place availability.  
   - Calculates total price.  
   - Handles payment creation.  
4. **Repository Layer**  
   - Saves booking and payment in the database.  
5. **BL returns result** to API.  
6. **API responds** to the user with booking ID or error.  

---

## 🔹 Key Concepts

- **Availability check**: prevents double booking.  
- **Total price calculation**: applies business rules like seasonal pricing.  
- **Cancellation rules**: enforce policies.  
- **Separation of concerns**: BL handles rules, Repo handles database.

---

## 🔹 Summary

Booking Management is the **core module for reservations**, linking users, places, and payments. Beginners should **visualize the flow from request → BL → Repo → DB → response** to understand interactions.


sequenceDiagram
    participant User
    participant API as PresentationLayer
    participant BL as BusinessLogicLayer
    participant Repo as RepositoryLayer
    participant DB as Database

    %% ================================
    %% CREATE BOOKING
    %% ================================
    User->>API: POST /api/bookings {placeId, checkInDate, checkOutDate, numberOfGuests}
    API->>BL: create_booking(bookingData)
    BL->>BL: validate_booking_data(bookingData)

    %% CHECK AVAILABILITY
    BL->>Repo: check_availability(placeId, checkInDate, checkOutDate)
    Repo->>DB: SELECT bookings WHERE place_id=placeId AND date_overlap(checkInDate, checkOutDate)
    DB-->>Repo: bookings[]
    Repo-->>BL: available / unavailable
    alt place unavailable
        BL-->>API: returnError("Place unavailable")
        API-->>User: 409 Conflict
    else place available
        %% CALCULATE TOTAL PRICE
        loop for each night in stay
            BL->>BL: add_night_price(place.pricePerNight)
        end
        BL->>BL: calculate_total_price()

        %% SAVE BOOKING
        BL->>Repo: save_booking(bookingData, totalPrice)
        Repo->>DB: INSERT INTO Bookings (...)
        DB-->>Repo: booking_saved(bookingId)
        Repo-->>BL: booking_saved

        %% CREATE PAYMENT
        BL->>Repo: create_payment(bookingId, amount=totalPrice)
        Repo->>DB: INSERT INTO Payments (...)
        DB-->>Repo: payment_created(paymentId)
        Repo-->>BL: payment_created

        %% RETURN SUCCESS
        BL-->>API: return_booking(bookingId, totalPrice)
        API-->>User: 201 Created {bookingId, totalPrice, dates, placeId}
    end

    %% ================================
    %% GET BOOKING BY ID
    %% ================================
    User->>API: GET /api/bookings/{id}
    API->>BL: get_booking_by_id(bookingId)
    BL->>Repo: find_booking_by_id(bookingId)
    Repo->>DB: SELECT * FROM Bookings WHERE id=bookingId
    DB-->>Repo: booking | null
    Repo-->>BL: booking | null
    alt booking exists
        BL-->>API: return_booking(booking)
        API-->>User: 200 OK {booking details}
    else booking not found
        BL-->>API: BookingNotFoundError
        API-->>User: 404 Not Found
    end

    %% ================================
    %% UPDATE BOOKING
    %% ================================
    User->>API: PUT /api/bookings/{id} {fields_to_update}
    API->>BL: update_booking(bookingId, data)
    BL->>BL: validate_update_data(data)
    alt validation fails
        BL-->>API: ValidationError
        API-->>User: 400 Bad Request
    else validation succeeds
        BL->>Repo: update_booking(bookingId, data)
        Repo->>DB: UPDATE Bookings SET ... WHERE id=bookingId
        DB-->>Repo: updated_booking
        Repo-->>BL: updated_booking
        BL-->>API: return_updated_booking(updated_booking)
        API-->>User: 200 OK {updated fields}
    end

    %% ================================
    %% CANCEL BOOKING
    %% ================================
    User->>API: POST /api/bookings/{id}/cancel
    API->>BL: cancel_booking(bookingId)
    BL->>Repo: cancel_booking(bookingId)
    Repo->>DB: UPDATE Bookings SET status='cancelled' WHERE id=bookingId
    DB-->>Repo: success
    Repo-->>BL: success
    BL-->>API: return_success()
    API-->>User: 200 OK
