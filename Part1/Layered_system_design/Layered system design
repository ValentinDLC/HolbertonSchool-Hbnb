# HBnB — Layered System Design (Beginner-Friendly Architecture)

## 📄 Objective

This document explains how the **HBnB application** is structured. We use a **layered architecture**, where each layer has a specific role.  

The goals are to:  
- Separate responsibilities so each layer does **one main thing**  
- Make the system **easy to understand and maintain**  
- Help beginners **understand the flow of data**  

The system has four main layers:  
1. **Presentation Layer** – User interface / API  
2. **Business Logic Layer** – Application logic (the “brain”)  
3. **Persistence Layer** – Data management (CRUD)  
4. **MySQL Database Layer** – Physical storage  

---

## 1️⃣ Presentation Layer (Interface / API)

### Simple Definition
The **Presentation Layer** is what the user or front-end application interacts with. It is the **entry point for requests**.  

### Concrete Example
- A user wants to book a place → clicks “Book” → the **Presentation Layer** receives the request.

### Responsibilities
- Receive requests from users  
- Validate data (e.g., valid dates)  
- Control access (authentication / authorization)  
- Format responses for the front-end  

### API Modules
- `UserAPI` → manage users  
- `PlaceAPI` → manage places  
- `BookingAPI` → manage bookings  
- `ReviewAPI` → manage reviews  
- `PaymentAPI` → manage payments  
- `AmenityAPI` → manage amenities  
- `AdminAPI` → manage administrators  

This layer **does not contain business logic**, it just passes the request to the next layer.

---

## 2️⃣ Business Logic Layer (Application Logic)

### Simple Definition
This is the **brain of the application**. It contains **the rules and logic**.  

### Concrete Example
- To create a booking:  
  - Check if the place is available  
  - Calculate the total price  
  - Create the booking in the system  

### Main Components
- `User` → represents a user  
- `Place` → represents a place / property  
- `Booking` → represents a booking  
- `Review` → represents a review  
- `Payment` → handles payments  
- `Amenity` → manages available amenities  
- `Admin` → manages administrators  
- `UserRating` → calculates user ratings  
- `Message` → handles sending messages  

### Responsibilities
- Apply business rules  
- Ensure everything is correct before saving to the database  
- Prepare data for the Persistence Layer  

 This layer only deals with **what to do**, not **how to store it**.

---

## 3️⃣ Persistence Layer (Data Management)

### Simple Definition
This layer is responsible for **saving and retrieving data** from the database. We often use a **Repository Pattern** here.

### Concrete Example
- To save a booking → `BookingRepo.save()` writes it to the MySQL database.

### Main Components
- `UserRepo`  
- `PlaceRepo`  
- `BookingRepo`  
- `ReviewRepo`  
- `PaymentRepo`  

### Responsibilities
- CRUD: Create, Read, Update, Delete  
- Transaction management  
- Prepare data for storage  

The business layer **never touches the database directly**, it uses the **repositories** instead.

---

## 4️⃣ MySQL Database Layer (Physical Storage)

### Simple Definition
The **MySQL database** is where **all data is stored** permanently.

### Concrete Example
- A booking is created → it is saved in MySQL → it remains even if the server restarts.

### Responsibilities
- Store data permanently  
- Ensure consistency (transactions, constraints)  
- Optimize queries for performance  

Almost no front-end code interacts directly with MySQL; it always goes through the upper layers.

---

## Mermaid Diagram (Layered Architecture)

```mermaid
classDiagram
%% ===============================================
%% PRESENTATION LAYER
%% ===============================================
class PresentationLayer {
    <<Interface / Service API>>
    +UserAPI.handleRequest()
    +PlaceAPI.handleRequest()
    +BookingAPI.handleRequest()
    +ReviewAPI.handleRequest()
    +PaymentAPI.handleRequest()
    +AmenityAPI.handleRequest()
    +AdminAPI.handleRequest()
    -- Notes --
    "Receives user requests"
}

%% ===============================================
%% BUSINESS LOGIC LAYER
%% ===============================================
class BusinessLogicLayer {
    +User.create()
    +Place.create()
    +Booking.create()
    +Review.create()
    +Payment.process()
    +Amenity.add()
    +Admin.manage()
    +UserRating.calculate()
    +Message.send()
    #validateData()
    -internalCache
    -- Notes --
    "Applies business logic"
}

%% ===============================================
%% PERSISTENCE LAYER
%% ===============================================
class PersistenceLayer {
    +UserRepo.save()
    +UserRepo.update()
    +UserRepo.delete()
    +PlaceRepo.save()
    +PlaceRepo.update()
    +PlaceRepo.delete()
    +BookingRepo.save()
    +BookingRepo.update()
    +BookingRepo.delete()
    +ReviewRepo.save()
    +ReviewRepo.update()
    +ReviewRepo.delete()
    +PaymentRepo.save()
    +PaymentRepo.update()
    +PaymentRepo.delete()
    -dbConnection
    -- Notes --
    "Manages database access"
}

%% ===============================================
%% DATABASE LAYER
%% ===============================================
class MySQL {
    +Database.connect()
    +Database.query()
    +Database.disconnect()
    -connectionString
    -- Notes --
    "Stores all data permanently"
}

%% ===============================================
%% RELATIONS
%% ===============================================
PresentationLayer --> BusinessLogicLayer : Facade Pattern
BusinessLogicLayer --> PersistenceLayer : Database Operations
PersistenceLayer --> MySQL : SQL Access
