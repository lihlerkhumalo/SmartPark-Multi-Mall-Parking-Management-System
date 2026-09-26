SmartPark – Multi-Mall Parking Management System
Overview

SmartPark is a Python-based parking management system designed to manage parking operations across multiple shopping centres.

The system allows customers to register and manage vehicles, enter and exit parking facilities, calculate parking fees, view parking history, and manage payments.

The project also provides administrative functionality for monitoring parking capacity, daily activity, revenue, and operations across multiple malls.

The project was developed to apply Python programming, object-oriented programming, authentication, file handling, business logic, data processing, and reporting to a practical real-world scenario.

Problem Statement

Large shopping centres need effective systems for managing parking capacity, vehicle movement, parking sessions, payments, and operational information.

A manual parking management process can make it difficult to:

Track available parking spaces
Record vehicle entry and exit
Calculate parking fees
Maintain customer records
Monitor revenue
Review parking activity
Manage multiple parking facilities

SmartPark provides a software-based solution for these processes.

Objectives

The main objectives of SmartPark are to:

Manage customer accounts.
Register and manage vehicles.
Record vehicle entry and exit.
Calculate parking fees.
Track parking sessions.
Record payment information.
Monitor parking capacity.
Generate operational information and reports.
Support multiple shopping centres.
Provide different functionality for different user roles.
Key Features
Customer Registration

Customers can create accounts and provide the required information for using the parking management system.

Authentication

The system provides user authentication to control access to different areas of the application.

Vehicle Management

Customers can register and manage vehicle information.

Parking Entry

The system records when a vehicle enters a parking facility.

Parking Exit

When a vehicle leaves the facility, the system can calculate the parking duration and determine the applicable parking fee.

Parking Fee Calculation

The system supports parking fee calculations based on the configured pricing rules.

Parking History

Users can review previous parking sessions.

Payment Management

The system records payment-related information associated with parking sessions.

Parking Capacity

The system monitors parking availability and occupancy.

Daily Activity

The application provides information about daily parking activity.

Revenue Reporting

The system can calculate and display parking revenue.

Multi-Mall Management

The application is designed to support parking operations across multiple shopping centres.

Technologies Used
Python
Object-Oriented Programming
File Handling
Data Structures
Authentication
Input Validation
Business Logic
Report Generation
Data Processing
System Architecture

The application can be viewed conceptually as:

                SmartPark
                    │
          ┌─────────┴─────────┐
          │                   │
       Customer            Administrator
          │                   │
          ▼                   ▼
     Authentication      Authentication
          │                   │
          ▼                   ▼
   Vehicle Management    Mall Management
          │                   │
          ▼                   ▼
   Parking Sessions      Capacity Monitoring
          │                   │
          ▼                   ▼
      Payments          Revenue Reports
          │                   │
          └─────────┬─────────┘
                    ▼
              Data Storage
Main Functional Areas
Customer Side

Customers can interact with functionality related to:

Account management
Vehicle registration
Parking
Parking sessions
Parking history
Payments
Administrative Side

Administrators can access functionality related to:

Mall management
Parking capacity
Parking activity
Revenue
Operational reports
Data Management

The current version uses file-based persistence to store application information.

This approach was selected for the current prototype to demonstrate persistent data storage without requiring an external database server.

Future Database Development

A future version can migrate the application's persistent data to a relational database such as:

SQLite
PostgreSQL
MySQL

A database-based version could separate information into related entities such as:

Users
   │
   ▼
Vehicles
   │
   ▼
Parking Sessions
   │
   ▼
Payments

This would allow more advanced SQL queries, relationships, reporting, and data integrity.

Example Database Design for Future Development

A future relational implementation could contain tables such as:

users
vehicles
malls
parking_sessions
payments

Example relationship:

User
 │
 └── Vehicle
       │
       └── Parking Session
              │
              └── Payment
Project Structure

A simplified structure of the project is:

SmartPark/
│
├── Python source files
├── Data files
├── Configuration files
├── Reports
│
└── README.md

The exact structure may change as the project continues to be refactored and expanded.

How to Run
Requirements
Python 3.x
A Python-compatible IDE or terminal

Examples include:

Visual Studio Code
PyCharm
Python IDLE
Run the Application

From the project directory:

python main.py

If the main Python file has a different filename, run the corresponding entry-point file.

Example System Flow
Start
  │
  ▼
Login / Registration
  │
  ├───────────────┐
  ▼               ▼
Customer       Administrator
  │               │
  ▼               ▼
Vehicle         Mall
Management      Management
  │               │
  ▼               ▼
Parking        Capacity
Session        Monitoring
  │               │
  ▼               ▼
Payment        Reports
  │               │
  └───────┬───────┘
          ▼
      Data Storage
Learning Outcomes

Developing SmartPark strengthened my understanding of:

Python programming
Object-oriented programming
Classes and objects
Application architecture
Authentication
Input validation
File handling
Business logic
Data processing
Calculations
Reporting
Debugging
Designing software around a real-world problem
Security Considerations

The current version is an academic/portfolio prototype.

Future versions should improve security through:

Password hashing
Stronger authentication
Input sanitisation
Improved access control
Secure database storage
Environment variables for sensitive configuration

Sensitive credentials should not be stored in the source code or committed to a public repository.

Future Improvements

Potential future improvements include:

SQL database integration
PostgreSQL support
Password hashing
Automated testing
Improved user interface
Advanced reporting
Database-backed analytics
Parking-space tracking
Reservation functionality
Improved error handling
API integration
Deployment as a larger-scale application
Project Status

Current status: Functional prototype

The current project demonstrates the core functionality of a multi-mall parking management system using Python.

Future versions can expand the system through database integration, improved security, testing, and additional functionality.



Langelihle Khumalo
 Information Technology Student

Interested in:

Software Engineering
C++
Python
Java
SQL
Data and Technolo
