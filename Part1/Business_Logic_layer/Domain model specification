# HBnB —  Architecture 

## 📄 Objective

This document explains how the **HBnB application** works. It is written for **beginners**, but in a professional style.  

We use **object-oriented design** with **layered architecture**:  

- **Presentation Layer** – API / interface with users  
- **Business Logic Layer** – rules and application logic  
- **Persistence Layer** – data storage management  
- **Database Layer** – MySQL storage  

This README explains **every class/role** and gives **small tips** for beginners.

---

## 🏷️ Classes and Roles

### 1️⃣ BaseModel

**Definition:**  
The **BaseModel** is the parent of all entities. It provides **common attributes and methods**.  

**Attributes / Methods:**  
- `# id` → unique identifier for every object  
- `- createdAt / updatedAt` → internal timestamps (private)  
- `+ create(), update(), delete()` → methods to persist data  

Always inherit from `BaseModel` so all your entities have a unique ID and audit info automatically.  

---

### 2️⃣ User

**Definition:**  
Represents a **person using the platform** (guest or host).  

**Key Responsibilities:**  
- Register and update their profile  
- Authenticate to the system  
- Access bookings and write reviews  

**Attributes / Methods:**  
- `- passwordHash` → always keep passwords private!  
- `+ firstName, lastName, email, isAdmin` → visible info  
- `+ register(), updateProfile(), authenticate(password)`  
- `+ getFullName(), verifyPassword(), verifyEmail()`  


- Never store plain passwords, always use hashed passwords.  
- Use `getFullName()` to display the user’s name consistently.

---

### 3️⃣ Place

**Definition:**  
Represents a **property** that can be booked.  

**Key Responsibilities:**  
- Track availability  
- Store details (title, description, price, location)  
- Manage amenities  

**Attributes / Methods:**  
- `# hostId` → owner of the place  
- `+ title, description, pricePerNight, latitude, longitude, numberOfRooms, maxGuests`  
- `+ create(), updateDetails(), isAvailable()`  
- `+ addAmenity(), removeAmenity()`  


- Always check `isAvailable()` before creating a booking.  
- Use `addAmenity()` for extra features like Wifi or Pool.

---

### 4️⃣ Booking

**Definition:**  
Represents a **reservation** made by a user for a place.  

**Attributes / Methods:**  
- `# placeId, # guestId` → references to the place and user  
- `+ checkInDate, checkOutDate, numberOfGuests, totalPrice`  
- `+ create(), calculateTotalPrice(), canCancel()`  

**Tips:**  
- Always calculate total price before saving.  
- Use `canCancel()` to enforce cancellation rules.

---

### 5️⃣ Review

**Definition:**  
Represents a **feedback** from a user about a place.  

**Attributes / Methods:**  
- `# placeId, # userId` → links to place and author  
- `+ rating, comment`  
- `+ post(), validateRating()`  
- `+ listedByPlace(), listedByUser(), listedByDate()`  


- Validate ratings are between 1–5 before posting.  
- Reviews help future users choose better places.

---

### 6️⃣ Amenity

**Definition:**  
Represents **extra features** available in a place (e.g., Wifi, Pool).  

**Attributes / Methods:**  
- `# placeId` → connected place  
- `+ name, description`  
- `+ add(), list()`  


- Keep a consistent naming for amenities so users can filter easily.

---

### 7️⃣ Payment

**Definition:**  
Represents a **financial transaction** for a booking.  

**Attributes / Methods:**  
- `# bookingId, # userId` → linked to booking and payer  
- `+ amount, currency, status`  
- `+ process(), refund()`  

 
- Always check the payment status before confirming a booking.  
- Use `refund()` for cancellations or disputes.

---

### 8️⃣ Admin

**Definition:**  
Represents an **administrator** who manages users and can moderate content.  

**Attributes / Methods:**  
- `# userId` → internal reference  
- `+ permissions` → what the admin can do  
- `+ appointUser(), banUser(), canManageAdmins()`  
- `+ postReview()` → optional if admins can test reviews  

**Tips:**  
- Use permissions carefully to avoid giving too much access.  
- Admins can manage users but should not bypass normal business rules.

---

### 9️⃣ Message

**Definition:**  
Represents **communication** between users (or between admin and users).  

**Attributes / Methods:**  
- `# senderId, # receiverId, # bookingId`  
- `+ content, isRead`  
- `+ send(), markAsRead()`  

 
- Mark messages as read after displaying to the user.  
- Always link messages to a booking if relevant.

---

### 🔟 Junction Entities

**PlaceAmenity** – Connects a **place** to its **amenities**.  

**UserRole** – Connects a **user** to a **role** (e.g., guest, host).  

 
- Many-to-many relationships are handled here.  
- Never store redundant information; always use junction entities.

---

## 🖼️ Mermaid Diagram 
classDiagram
%% ===============================================
%% Base Model
%% ===============================================
class BaseModel {
    # id : UUID
    - createdAt : Date
    - updatedAt : Date
    + create() : void
    + update() : void
    + delete() : void
}

%% ===============================================
%% User
%% ===============================================
class User {
    - passwordHash : String
    + firstName : String
    + lastName : String
    + email : String
    + isAdmin : Boolean
    + register() : void
    + updateProfile() : void
    + authenticate(password) : Boolean
    + getFullName() : String
    + verifyPassword(password) : Boolean
    + verifyEmail() : Boolean
}

%% ===============================================
%% Place
%% ===============================================
class Place {
    # hostId : UUID
    + title : String
    + description : String
    + pricePerNight : Float
    + latitude : Float
    + longitude : Float
    + numberOfRooms : Integer
    + maxGuests : Integer
    + create() : void
    + updateDetails() : void
    + isAvailable(startDate, endDate) : Boolean
    + getPrice() : Float
    + setPrice(price) : void
    + getLocation() : String
    + setLocation(lat, long) : void
    + addAmenity(amenityId) : void
    + removeAmenity(amenityId) : void
}

%% ===============================================
%% Review
%% ===============================================
class Review {
    # placeId : UUID
    # userId : UUID
    + rating : Integer
    + comment : String
    + post() : void
    + validateRating() : Boolean
    + listedByPlace() : List
    + listedByUser() : List
    + listedByDate() : List
}

%% ===============================================
%% Amenity
%% ===============================================
class Amenity {
    # placeId : UUID
    + name : String
    + description : String
    + add() : void
    + list() : List
}

%% ===============================================
%% Booking
%% ===============================================
class Booking {
    # placeId : UUID
    # guestId : UUID
    + checkInDate : Date
    + checkOutDate : Date
    + numberOfGuests : Integer
    + totalPrice : Float
    + create() : void
    + calculateTotalPrice() : Float
    + canCancel() : Boolean
}

%% ===============================================
%% Payment
%% ===============================================
class Payment {
    # bookingId : UUID
    # userId : UUID
    + amount : Float
    + currency : String
    + status : String
    + process() : void
    + refund() : void
}

%% ===============================================
%% Admin
%% ===============================================
class Admin {
    # userId : UUID
    + permissions : List<String>
    + appointUser(userId) : void
    + banUser(userId) : void
    + canManageAdmins() : Boolean
    + postReview(reviewData) : void
}

%% ===============================================
%% Message
%% ===============================================
class Message {
    # senderId : UUID
    # receiverId : UUID
    # bookingId : UUID
    + content : String
    + isRead : Boolean
    + send() : void
    + markAsRead() : void
}

%% ===============================================
%% Junction Entities
%% ===============================================
class PlaceAmenity {
    # placeId : UUID
    # amenityId : UUID
}

class UserRole {
    # userId : UUID
    + roleName : String
}

%% ===============================================
%% Inheritance
%% ===============================================
BaseModel <|-- User
BaseModel <|-- Place
BaseModel <|-- Review
BaseModel <|-- Booking
BaseModel <|-- Amenity
BaseModel <|-- Payment
BaseModel <|-- Admin
BaseModel <|-- Message
BaseModel <|-- PlaceAmenity
BaseModel <|-- UserRole

%% ===============================================
%% Relationships
%% ===============================================
User "1" --> "*" Booking : guest
User "1" --> "*" Review : author
User "1" --> "*" Message : sends
Place "1" --> "*" Booking
Place "1" --> "*" Review
Booking "1" --> "1" Payment
Admin "1" --> "*" User : manages

%% ===============================================
%% Many-to-Many via junctions
%% ===============================================
Place "1" --> "*" PlaceAmenity : links
Amenity "1" --> "*" PlaceAmenity : links
User "1" --> "*" UserRole : assigned roles
