# HBnB — User Management

## 📄 Objective
The **User Management module** handles everything related to user accounts in HBnB.  
Its main goal is to **ensure users can register, update profiles, authenticate, and be managed by admins**, while keeping the system secure and consistent.

---

## 🔹 Roles of User Management

1. **Register a new user**  
   - Collect first name, last name, email, and password.  
   - Validate input (format, required fields).  
   - Hash passwords before storing.  
   - Generate a unique identifier for each user.

2. **Authenticate users**  
   - Check the entered password against the hashed password.  
   - Grant access only if credentials are correct.  

3. **Update user profiles**  
   - Allow changing fields like name or email.  
   - Validate updated data.  

4. **Delete users**  
   - Prefer **soft delete** to keep historical data intact.  
   - Ensure relationships (bookings, reviews) are not broken.  

5. **Retrieve user information**  
   - Provide user details to other modules (bookings, messages, reviews).  

---

## 🔹 Beginner Tips

- **Never store plain passwords** — always hash and salt them.  
- **Validation is critical** — both in API and business logic.  
- **Alt / branch thinking**: always consider success and failure paths.  
- **Keep your API consistent** — e.g., 201 Created for successful creation, 400 Bad Request for validation errors, 404 Not Found when user does not exist.  
- **Think layers**: API handles requests, BL handles logic, Repo handles DB access.  

---

## 🔹 How it Works (Step-by-Step)

1. **User sends a request** (e.g., register or login).  
2. **API layer receives request** → acts as a **facade**.  
   - Does minimal checks, forwards data to BL.  
3. **Business Logic Layer (BL)**  
   - Validates data.  
   - Applies rules (e.g., password hashing, unique email).  
   - Determines next steps depending on validation (success/failure).  
4. **Repository Layer**  
   - Interacts with database for create, read, update, delete (CRUD).  
   - Returns results to BL.  
5. **BL returns results to API**  
   - Formats response for user (success or error).  
6. **API responds to the user**  
   - Provides feedback: created user, updated profile, error messages, etc.  

---

## 🔹 Key Concepts

- **Validation**: Ensures data is correct before any database operation.  
- **Hashing passwords**: Protects user credentials.  
- **Soft delete vs hard delete**: Soft delete keeps historical data; hard delete removes it permanently.  
- **Separation of concerns**: Each layer does **one job**:  
  - API → entry point / formatting  
  - BL → rules & logic  
  - Repo → database access  

---

## 🔹 Summary

The User Management module is **the foundation of all interactions**. Every other module (booking, reviews, messaging) depends on accurate and secure user data.  
For beginners, focus on **understanding the flow**: request → validation → business rules → repository → database → response.  
Visualize **success vs failure paths** in your mind to understand alt/branches logic.





sequenceDiagram
    participant User
    participant API as PresentationLayer
    participant BL as BusinessLogicLayer
    participant Repo as RepositoryLayer
    participant DB as Database

    %% ================================
    %% USER REGISTRATION
    %% ================================
    User->>API: POST /api/users {first_name, last_name, email, password}
    API->>BL: register_user(userData)
    BL->>BL: validate_user_data(userData)
    alt validation fails
        BL-->>API: ValidationError
        API-->>User: 400 Bad Request
    else validation succeeds
        BL->>BL: hash_password(userData.password)
        BL->>BL: generate_uuid()
        BL->>BL: set_timestamps()
        BL->>Repo: save_user(user_object)
        Repo->>DB: INSERT INTO Users (id, first_name, last_name, email, password_hash, created_at, updated_at)
        DB-->>Repo: user_saved_confirmation
        Repo-->>BL: user_saved
        BL-->>API: user_created
        API-->>User: 201 Created {id, first_name, last_name, email}
    end

    %% ================================
    %% GET USER BY ID
    %% ================================
    User->>API: GET /api/users/{id}
    API->>BL: get_user_by_id(userId)
    BL->>Repo: find_user_by_id(userId)
    Repo->>DB: SELECT * FROM Users WHERE id=userId
    DB-->>Repo: user | null
    Repo-->>BL: user | null
    alt user exists
        BL-->>API: return_user(user)
        API-->>User: 200 OK {id, first_name, last_name, email}
    else user not found
        BL-->>API: UserNotFoundError
        API-->>User: 404 Not Found
    end

    %% ================================
    %% UPDATE USER
    %% ================================
    User->>API: PUT /api/users/{id} {fields_to_update}
    API->>BL: update_user(userId, data)
    BL->>BL: validate_update_data(data)
    alt validation fails
        BL-->>API: ValidationError
        API-->>User: 400 Bad Request
    else validation succeeds
        BL->>Repo: update_user(userId, data)
        Repo->>DB: UPDATE Users SET ... WHERE id=userId
        DB-->>Repo: updated_user
        Repo-->>BL: updated_user
        BL-->>API: return_updated_user(updated_user)
        API-->>User: 200 OK {updated fields}
    end

    %% ================================
    %% DELETE USER
    %% ================================
    User->>API: DELETE /api/users/{id}
    API->>BL: delete_user(userId)
    BL->>Repo: delete_user(userId)
    Repo->>DB: DELETE FROM Users WHERE id=userId
    DB-->>Repo: success
    Repo-->>BL: success
    BL-->>API: return_success()
    API-->>User: 200 OK
