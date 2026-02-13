# HBnB — Message Management

## 📄 Objective
The **Message Management module** allows users to send, receive, and view messages related to bookings or general communication.  
It ensures **messages are linked to users and bookings, and read status is maintained**.

---

## 🔹 Roles of Message Management

1. **Send a message**  
   - Attach sender, receiver, booking reference.  
   - Validate content and participants.  

2. **Retrieve conversation**  
   - Fetch messages between two users.  
   - Filter by booking if needed.  

3. **Mark messages as read**  
   - Track read/unread status for better UX.  

---

## 🔹 Beginner Tips

- **Always link messages to bookings** when applicable.  
- **Alt / branch thinking**: handle missing users or bookings.  
- **Separation of concerns**: BL handles logic, Repo handles storage.  

---

## 🔹 How it Works (Step-by-Step)

1. **User sends a message** → API receives request.  
2. **BL validates content** and user permissions.  
3. **Repo saves** message in DB.  
4. **BL updates read/unread status** if needed.  
5. **API returns success/error** response.  
6. **Users can fetch conversation** → BL queries DB via Repo.  

---

## 🔹 Key Concepts

- **Read/unread tracking** improves UX.  
- **Booking linkage** ensures context.  
- **Separation of concerns**: API → BL → Repo → DB.  

---

## 🔹 Summary

Message Management enables **communication between users** in a structured way.  
Beginners should focus on **flow, validation, and linking messages to bookings**.


sequenceDiagram
    participant User
    participant API as PresentationLayer
    participant BL as BusinessLogicLayer
    participant Repo as RepositoryLayer
    participant DB as Database

    %% ================================
    %% SEND MESSAGE
    %% ================================
    User->>API: POST /api/messages {senderId, receiverId, bookingId, content}
    API->>BL: send_message(messageData)
    BL->>BL: validate_message_data(messageData)
    alt validation fails
        BL-->>API: ValidationError
        API-->>User: 400 Bad Request
    else validation succeeds
        BL->>Repo: save_message(messageData)
        Repo->>DB: INSERT INTO Messages (id, sender_id, receiver_id, booking_id, content, is_read, created_at, updated_at)
        DB-->>Repo: message_saved(messageId)
        Repo-->>BL: message_saved
        BL-->>API: return_message(messageId)
        API-->>User: 201 Created {messageId, senderId, receiverId, content}
    end

    %% ================================
    %% GET CONVERSATION
    %% ================================
    User->>API: GET /api/messages/conversation?user1={id}&user2={id}
    API->>BL: get_conversation(user1, user2)
    BL->>Repo: find_conversation(user1, user2)
    Repo->>DB: SELECT * FROM Messages WHERE (sender_id=user1 AND receiver_id=user2) OR (sender_id=user2 AND receiver_id=user1) ORDER BY created_at
    DB-->>Repo: messages[]
    Repo-->>BL: messages[]
    alt conversation exists
        BL-->>API: return_messages(messages)
        API-->>User: 200 OK {messages[]}
    else no messages
        BL-->>API: NoMessagesFound
        API-->>User: 404 Not Found
    end
