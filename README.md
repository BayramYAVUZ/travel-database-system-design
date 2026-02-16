# Travel Booking & Reservation System

<p align="center">
  <img src="deneme-1.png" width="500">
</p>

<p align="center">
  <img src="logo-1.png" width="200">
</p>


## Student Information

| Field | Detail |
| :--- | :--- |
| **Student Name** | Bayram Yavuz |
| **Student ID** | 122200058 |
| **Course** | CMPE351 – Database Systems |
| **Project Theme** | Travel Booking & Reservation System (Based on ID last digit 8–9) |

---

## Project Overview

This project implements a fully functional Travel Booking & Reservation System as required by the CMPE351 term project guidelines. It features a normalized relational database, a Python-based backend, and an interactive Streamlit web interface.

The system allows comprehensive management of:
* Customers & Destinations  
* Travel Packages  
* Services (Flights + Hotels with Inheritance)  
* Rooms / Seats (Auto-generated)  
* Bookings, Payments, & Tickets  

### Tech Stack
* **Language:** Python 3.x  
* **Database:** SQLite3 (with PRAGMA foreign_keys = ON)  
* **Interface:** Streamlit  
* **Design:** Relational Schema + ER Model (Fully Compliant)  

---

## System Modules

### 1. Customers
* Add, Update, Delete, and List customers.  
* Holds personal details for booking associations.

### 2. Destinations
* Manage travel locations (Cities/Countries).  
* Destinations are linked to Hotels and Flights.

### 3. Services (Polymorphism / Inheritance)
Uses ISA generalization:
* **Parent:** Service  
* **Child 1: Flight** — auto-creates seats (1A, 1B, 2A, 2B)  
* **Child 2: Hotel** — auto-creates rooms (101, 102, 201, 202)  
* Cascade deletion supported.

### 4. Travel Packages
* Create packages.  
* Add services (flight/hotel) to packages.  
* Update name and price.

### 5. Bookings
* Connects Customer ↔ Package.  
* Auto-calculates payment amount.

### 6. Payments & Revenue
* Process payments.  
* Includes advanced JOIN queries.

### 7. Tickets & Reservations
* Auto-reserves Room/Seat  
* Auto-issues Ticket  

---

## Database Structure

12 Entities + 13 Relationships.

### Entities
Customer, Destination, TravelPackage, Booking, Payment, Reservation, Service, Hotel, Flight, Room, Seat, Ticket.

### Special Concepts
* **Weak Entity:** Payment  
* **Inheritance:** Service → Flight / Hotel  

### Relationships
Includes Makes, Selects, Offer, HAS_PAYMENT, HAS_R, Issues, Assigned_to, and more.

Foreign keys enforced with `PRAGMA foreign_keys = ON`.

---

## Reports & JOIN Queries

### 1. Booking Overview JOIN
Shows:
* Customer  
* Destination  
* Package Name  
* Total Payment  

### 2. Inventory JOIN
* Hotel → Room availability  
* Flight → Seat availability  

---

## How to Run the Project

### 1. Install Dependencies
```bash
pip install streamlit pandas
```

---

### 2. Run Streamlit App
```bash
streamlit run BayramYavuz_Code.py
```

---

### 3. Database Initialization
The database file is created automatically on first run:

```
travel_system_final.db
```

---

## Project File Structure
```
├── main.py                    # Main Streamlit Application (UI + Logic)
├── travel_system_final.db     # Auto-generated SQLite database
├── README.md                  # Project Documentation
├── deneme-1.png               # Project Banner Image (Used in UI)
└── logo-1.png                 # Personal logo shown in README & UI title
```

---

## Project Assessment & Requirements Met

- ✔ Full ER Model: 12 Entities & 13 Relationships  
- ✔ Fully Normalized Relational Schema  
- ✔ Advanced SQL (JOINs, FK, Cascade Delete)  
- ✔ ISA Inheritance implemented  
- ✔ Weak Entity implemented  
- ✔ Complete CRUD  
- ✔ Automated Reservations & Ticket issuing  
- ✔ Professional Streamlit interface  

---


