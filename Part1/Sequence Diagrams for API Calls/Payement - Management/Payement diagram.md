# HBnB — Payment Management

## 📄 Objective
The **Payment Management module** handles **all payments for bookings**, including creation, retrieval, and refunds.  
It ensures **secure transactions and proper linking to bookings and users**.

---

## 🔹 Roles of Payment Management

1. **Create a payment**  
   - Triggered after booking creation.  
   - Validates payment data (amount, currency, method).  

2. **Retrieve payment info**  
   - Fetch payment status for user or admin review.  

3. **Process a refund**  
   - Allow refunds according to rules.  
   - Update payment status accordingly.  

---

## 🔹 Beginner Tips

- **Always link payments to bookings** for consistency.  
- **Validate amounts** to prevent errors.  
- **Alt / branch thinking**: handle success vs failed transactions.  
- **Security is critical**: handle sensitive data carefully.  

---

## 🔹 How it Works (Step-by-Step)

1. **BL validates payment info**.  
2. **Repo saves payment to DB**.  
3. **BL returns confirmation** to API.  
4. **API responds to user** with payment status.  
5. **Refunds** follow a similar path with validation and database update.  

---

## 🔹 Key Concepts

- **Transaction consistency**: Payment must match booking.  
- **Refund policies**: Enforce cancellation and refund rules.  
- **Separation of concerns**: API → BL → Repo → DB.  

---

## 🔹 Summary

Payment Management is **critical for revenue and user trust**.  
Beginners should understand **how payments flow through layers** and how validations prevent errors.


sequenceDiagram
    participant User
    participant API as PresentationLayer
    participant BL as BusinessLogicLayer
    participant Repo as RepositoryLayer
    participant DB as Database

    %% ================================
    %% CREATE PAYMENT
    %% ================================
    User->>API: POST /api/payments {bookingId, amount, currency}
    API->>BL: create_payment(paymentData)
    BL->>BL: validate_payment_data(paymentData)
    alt validation fails
        BL-->>API: ValidationError
        API-->>User: 400 Bad Request
    else validation succeeds
        BL->>Repo: save_payment(paymentData)
        Repo->>DB: INSERT INTO Payments (id, booking_id, user_id, amount, currency, status, created_at, updated_at)
        DB-->>Repo: payment_saved(paymentId)
        Repo-->>BL: payment_saved
        BL-->>API: return_payment(paymentId)
        API-->>User: 201 Created {paymentId, bookingId, amount, status}
    end

    %% ================================
    %% GET PAYMENT BY ID
    %% ================================
    User->>API: GET /api/payments/{id}
    API->>BL: get_payment_by_id(paymentId)
    BL->>Repo: find_payment_by_id(paymentId)
    Repo->>DB: SELECT * FROM Payments WHERE id=paymentId
    DB-->>Repo: payment | null
    Repo-->>BL: payment | null
    alt payment exists
        BL-->>API: return_payment(payment)
        API-->>User: 200 OK {payment details}
    else payment not found
        BL-->>API: PaymentNotFoundError
        API-->>User: 404 Not Found
    end

    %% ================================
    %% REFUND PAYMENT
    %% ================================
    User->>API: POST /api/payments/{id}/refund
    API->>BL: process_refund(paymentId)
    BL->>Repo: refund_payment(paymentId)
    Repo->>DB: UPDATE Payments SET status='refunded' WHERE id=paymentId
    DB-->>Repo: success/failure
    Repo-->>BL: refund_status
    alt refund success
        BL-->>API: return_refund_status('success')
        API-->>User: 200 OK {paymentId, status: refunded}
    else refund failure
        BL-->>API: return_refund_status('failure')
        API-->>User: 400 Bad Request {error: refund failed}
    end
