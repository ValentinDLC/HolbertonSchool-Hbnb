sequenceDiagram
    participant User
    participant API
    participant BL as Business Logic
    participant Repo as Repository
    participant DB as Database

%% ================================
%% USER REGISTRATION
%% ================================
User->>API: POST /api/users {firstName, lastName, email, password}
API->>BL: register_user(userData)
BL->>BL: validate_user_data(userData)
alt validation fails
    BL-->>API: ValidationError
    API-->>User: 400 Bad Request
else validation succeeds
    BL->>BL: check_email_unique(email)
    alt email already exists
        BL-->>API: EmailAlreadyExistsError
        API-->>User: 409 Conflict
    else email is unique
        BL->>BL: hash_password(userData.password)
        BL->>BL: generate_uuid()
        BL->>BL: set_role(default='user')
        BL->>BL: set_timestamps()
        BL->>Repo: save_user(user_object)
        Repo->>DB: INSERT INTO Users (id, firstName, lastName, email, passwordHash, role, createdAt, updatedAt)
        DB-->>Repo: user_saved_confirmation
        Repo-->>BL: user_saved
        BL-->>API: user_created
        API-->>User: 201 Created {id, firstName, lastName, email, role}
    end
end

%% ================================
%% USER LOGIN
%% ================================
User->>API: POST /api/auth/login {email, password}
API->>BL: authenticate_user(email, password)
BL->>Repo: find_user_by_email(email)
Repo->>DB: SELECT * FROM Users WHERE email=email
DB-->>Repo: user | null
Repo-->>BL: user | null
alt user not found
    BL-->>API: InvalidCredentialsError
    API-->>User: 401 Unauthorized
else user found
    BL->>BL: verify_password(password, user.passwordHash)
    alt password invalid
        BL-->>API: InvalidCredentialsError
        API-->>User: 401 Unauthorized
    else password valid
        BL->>BL: generate_jwt_token(user.id, user.role)
        BL-->>API: return_token(token, user)
        API-->>User: 200 OK {token, userId, role}
    end
end

%% ================================
%% GET USER BY ID
%% ================================
User->>API: GET /api/users/{id}
API->>API: verify_jwt_token()
alt token invalid
    API-->>User: 401 Unauthorized
else token valid
    API->>BL: get_user_by_id(userId)
    BL->>Repo: find_user_by_id(userId)
    Repo->>DB: SELECT * FROM Users WHERE id=userId
    DB-->>Repo: user | null
    Repo-->>BL: user | null
    alt user exists
        BL-->>API: return_user(user)
        API-->>User: 200 OK {id, firstName, lastName, email, role}
    else user not found
        BL-->>API: UserNotFoundError
        API-->>User: 404 Not Found
    end
end

%% ================================
%% UPDATE USER
%% ================================
User->>API: PUT /api/users/{id} {fieldsToUpdate}
API->>API: verify_jwt_token()
alt token invalid or userId mismatch
    API-->>User: 403 Forbidden
else authorized
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
        BL->>BL: set_updated_timestamp()
        BL-->>API: return_updated_user(updated_user)
        API-->>User: 200 OK {updated fields}
    end
end

%% ================================
%% DELETE USER
%% ================================
User->>API: DELETE /api/users/{id}
API->>API: verify_jwt_token()
alt not authorized
    API-->>User: 403 Forbidden
else authorized (self or admin)
    API->>BL: delete_user(userId)
    BL->>Repo: delete_user(userId)
    Repo->>DB: DELETE FROM Users WHERE id=userId
    DB-->>Repo: success
    Repo-->>BL: success
    BL-->>API: return_success()
    API-->>User: 200 OK
end

%% ================================
%% ADMIN: GET ALL USERS
%% ================================
User->>API: GET /api/admin/users
API->>API: verify_jwt_token()
API->>API: check_admin_role()
alt not admin
    API-->>User: 403 Forbidden
else is admin
    API->>BL: get_all_users()
    BL->>Repo: find_all_users()
    Repo->>DB: SELECT * FROM Users
    DB-->>Repo: users[]
    Repo-->>BL: users[]
    BL-->>API: return_users(users)
    API-->>User: 200 OK {users[]}
end

%% ================================
%% ADMIN: PROMOTE USER TO ADMIN
%% ================================
User->>API: POST /api/admin/users/{id}/promote
API->>API: verify_jwt_token()
API->>API: check_admin_role()
alt not admin
    API-->>User: 403 Forbidden
else is admin
    API->>BL: promote_user_to_admin(userId)
    BL->>Repo: update_user_role(userId, role='admin')
    Repo->>DB: UPDATE Users SET role='admin' WHERE id=userId
    DB-->>Repo: success
    Repo-->>BL: success
    BL-->>API: return_success()
    API-->>User: 200 OK {userId, role='admin'}
end

%% ================================
%% ADMIN: BAN USER
%% ================================
User->>API: POST /api/admin/users/{id}/ban
API->>API: verify_jwt_token()
API->>API: check_admin_role()
alt not admin
    API-->>User: 403 Forbidden
else is admin
    API->>BL: ban_user(userId)
    BL->>Repo: ban_user(userId)
    Repo->>DB: UPDATE Users SET isBanned=true WHERE id=userId
    DB-->>Repo: success
    Repo-->>BL: success
    BL-->>API: return_success()
    API-->>User: 200 OK {userId, isBanned=true}
endsequenceDiagram
    participant User as User (Presentation)
    participant API as API Layer (Presentation)
    participant BL as Business Logic
    participant Repo as Repository (Persistence)
    participant DB as Database (Persistence)

%% ================================
%% 1. USER REGISTRATION
%% ================================
    Note over User,DB: 1. USER REGISTRATION
    User->>API: POST /api/users {firstName, lastName, email, password}
    API->>BL: register_user(userData)
    BL->>BL: validate_user_data(userData)
    BL->>BL: check_email_unique(email)
    BL->>BL: hash_password(password)
    BL->>BL: generate_uuid()
    BL->>BL: set_role(default='user')
    BL->>Repo: save_user(user_object)
    Repo->>DB: INSERT INTO Users
    DB-->>Repo: user_saved
    Repo-->>BL: user_saved
    BL-->>API: user_created
    API-->>User: 201 Created {id, firstName, lastName, email, role}

%% ================================
%% 2. USER LOGIN
%% ================================
    Note over User,DB: 2. USER LOGIN
    User->>API: POST /api/auth/login {email, password}
    API->>BL: authenticate_user(email, password)
    BL->>Repo: find_user_by_email(email)
    Repo->>DB: SELECT * FROM Users WHERE email=?
    DB-->>Repo: user
    Repo-->>BL: user
    BL->>BL: verify_password(password, passwordHash)
    BL->>BL: generate_jwt_token(userId, role)
    BL-->>API: token + user
    API-->>User: 200 OK {token, userId, role}

%% ================================
%% 3. GET USER BY ID
%% ================================
    Note over User,DB: 3. GET USER BY ID
    User->>API: GET /api/users/{id}
    API->>API: verify_jwt_token()
    API->>BL: get_user_by_id(userId)
    BL->>Repo: find_user_by_id(userId)
    Repo->>DB: SELECT * FROM Users WHERE id=?
    DB-->>Repo: user
    Repo-->>BL: user
    BL-->>API: user
    API-->>User: 200 OK {id, firstName, lastName, email, role}

%% ================================
%% 4. UPDATE USER
%% ================================
    Note over User,DB: 4. UPDATE USER
    User->>API: PUT /api/users/{id} {fieldsToUpdate}
    API->>API: verify_jwt_token()
    API->>BL: update_user(userId, data)
    BL->>BL: validate_update_data(data)
    BL->>Repo: update_user(userId, data)
    Repo->>DB: UPDATE Users SET ... WHERE id=?
    DB-->>Repo: updated_user
    Repo-->>BL: updated_user
    BL->>BL: set_updated_timestamp()
    BL-->>API: updated_user
    API-->>User: 200 OK {updated fields}

%% ================================
%% 5. DELETE USER
%% ================================
    Note over User,DB: 5. DELETE USER
    User->>API: DELETE /api/users/{id}
    API->>API: verify_jwt_token()
    API->>BL: delete_user(userId)
    BL->>Repo: delete_user(userId)
    Repo->>DB: DELETE FROM Users WHERE id=?
    DB-->>Repo: success
    Repo-->>BL: success
    BL-->>API: success
    API-->>User: 200 OK

%% ================================
%% 6. GET ALL USERS (ADMIN)
%% ================================
    Note over User,DB: 6. GET ALL USERS (Admin only)
    User->>API: GET /api/admin/users
    API->>API: verify_jwt_token()
    API->>API: check_admin_role()
    API->>BL: get_all_users()
    BL->>Repo: find_all_users()
    Repo->>DB: SELECT * FROM Users
    DB-->>Repo: users[]
    Repo-->>BL: users[]
    BL-->>API: users[]
    API-->>User: 200 OK {users[]}

%% ================================
%% 7. PROMOTE USER TO ADMIN
%% ================================
    Note over User,DB: 7. PROMOTE USER TO ADMIN (Admin only)
    User->>API: POST /api/admin/users/{id}/promote
    API->>API: verify_jwt_token()
    API->>API: check_admin_role()
    API->>BL: promote_user_to_admin(userId)
    BL->>Repo: update_user_role(userId, role='admin')
    Repo->>DB: UPDATE Users SET role='admin' WHERE id=?
    DB-->>Repo: success
    Repo-->>BL: success
    BL-->>API: success
    API-->>User: 200 OK {userId, role='admin'}

%% ================================
%% 8. BAN USER (ADMIN)
%% ================================
    Note over User,DB: 8. BAN USER (Admin only)
    User->>API: POST /api/admin/users/{id}/ban
    API->>API: verify_jwt_token()
    API->>API: check_admin_role()
    API->>BL: ban_user(userId)
    BL->>Repo: ban_user(userId)
    Repo->>DB: UPDATE Users SET isBanned=true WHERE id=?
    DB-->>Repo: success
    Repo-->>BL: success
    BL-->>API: success
    API-->>User: 200 OK {userId, isBanned=true}