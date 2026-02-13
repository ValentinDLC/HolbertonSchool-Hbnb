# HBnB — Admin Management

## 📄 Objective
The **Admin Management module** allows administrators to manage users, content, and permissions.  
It ensures **proper authorization, moderation, and system control**.

---

## 🔹 Roles of Admin Management

1. **Create an admin**  
   - Assign permissions.  
   - Validate uniqueness and security rules.  

2. **Ban or moderate users**  
   - Prevent misuse of platform.  
   - Mark users as banned in the system.  

3. **Rate or moderate content**  
   - Approve or flag reviews, messages, or places.  

---

## 🔹 Beginner Tips

- **Always check permissions** before any admin operation.  
- **Alt / branch thinking**: handle unauthorized vs authorized actions.  
- **Keep audit logs** to track admin actions.  

---

## 🔹 How it Works (Step-by-Step)

1. **Admin sends request** (create, ban, rate).  
2. **API layer** validates authentication.  
3. **BL checks permissions** and applies rules.  
4. **Repo updates the database** accordingly.  
5. **BL returns confirmation**.  
6. **API responds** with success or error.  

---

## 🔹 Key Concepts

- **Permission checks**: Only authorized admins can perform actions.  
- **Audit and logging**: Track all admin actions.  
- **Separation of concerns**: API → BL → Repo → DB.  

---

## 🔹 Summary

Admin Management is **essential for platform control and moderation**.  
Beginners should understand **how BL enforces rules and permissions**.


sequenceDiagram
    participant Admin
    participant API as PresentationLayer
    participant BL as BusinessLogicLayer
    participant Repo as RepositoryLayer
    participant DB as Database

    %% ================================
    %% CREATE ADMIN
    %% ================================
    Admin->>API: POST /api/admins {userId, permissions}
    API->>BL: create_admin(adminData)
    BL->>BL: validate_admin_data(adminData)
    alt validation fails
        BL-->>API: ValidationError
        API-->>Admin: 400 Bad Request
    else validation succeeds
        BL->>Repo: save_admin(adminData)
        Repo->>DB: INSERT INTO Admins (id, user_id, permissions, created_at, updated_at)
        DB-->>Repo: admin_saved(adminId)
        Repo-->>BL: admin_saved
        BL-->>API: return_admin(adminId)
        API-->>Admin: 201 Created {adminId, userId, permissions}
    end

    %% ================================
    %% BAN USER
    %% ================================
    Admin->>API: POST /api/users/{id}/ban {reason}
    API->>BL: ban_user(userId, reason)
    BL->>BL: check_permissions(adminId)
    alt not permitted
        BL-->>API: PermissionError
        API-->>Admin: 403 Forbidden
    else permitted
        BL->>Repo: mark_user_banned(userId, reason)
        Repo->>DB: UPDATE Users SET banned=true, ban_reason=reason WHERE id=userId
        DB-->>Repo: success
        Repo-->>BL: success
        BL-->>API: return_success()
        API-->>Admin: 200 OK
    end

    %% ================================
    %% RATE USER
    %% ================================
    Admin->>API: POST /api/users/{id}/rate {rating}
    API->>BL: rate_user(userId, rating)
    BL->>BL: validate_rating(rating)
    alt validation fails
        BL-->>API: ValidationError
        API-->>Admin: 400 Bad Request
    else validation succeeds
        BL->>Repo: save_user_rating(userId, rating)
        Repo->>DB: INSERT INTO UserRatings (user_id, rating, created_at)
        DB-->>Repo: user_rating_saved
        Repo-->>BL: user_rating_saved
        BL-->>API: return_success()
        API-->>Admin: 201 Created {userId, rating}
    end
