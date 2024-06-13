# PAS-TEAM
**Software Engineering Project**

**Description**

Air View is a Web Application that connects the flights to its customers (ie) it is a platform for users to book flights, check-in their baggage and download their boarding passes in their local airport. This is a system to use for airport operations instead of a third party booking service or airline check in system.

**Objective :**
The objective of this project is to create a centralized system for airport management; normally, customers use third party booking services to book flights and check in at the airport using airline services. The goal of this project is to create a system which allows customers to book flights, check in luggages, and receive e-tickets within the application operated by airports.

**Scope :**
This project has user authentication, flight booking, check in management, update and display flight status, and admin management.
We are creating a mock database for the flights.

**Target Users :**
It focuses on general travelers, airport and airline administrations.

**Major Component**
- User Authentication:
	- Sign In/ Sign Up
	- Logout
	- Role based user access
	- Email notification
- Check In Management:
	- Online check in
	- Customer Support and Assistance
	- Seat Selection
	- Generate and display flight ticket
- Flight Search and Booking
	- Search flights
	- Baggage Check-In
	- Double booking prevention
	- Booking confirmation
	- Email notification
	- Display flight status
- Admin panel
	- Manage flights, booking
	- Sending notification for update

User Authentication interacts with database to create, update, retrieve, or delete user data for user creating, deletion, or user information update
User authentication also interacts with Check In Management system to authenticate user for online check in process
Check In Management system will interact with database to only retrieve flight and user data to manage customer check in process
Check In Management system will also interact with Email service to send confirmation and E-ticket to user
Flight Search and Booking system will interact with Check In Management to update CIM with booking detail
Flight Search and Booking system will also interact database to create query to display flights based on user input and it will also create new booking information and store in database
Admin panel will interact with Database to manage flight, user, booking and perform CRUD operation in DB
Admin panel will also interact with Check In Management system to manipulate/update check in data



  
**Steps to build and run application:**

- Download Docker Desktop Application
- Login to Docker account
- Retrieve .tar from this Google Drive link:
- Load the Docker image from the .tar file using the following command in your
terminal:

- docker load -i path_to_your_tar/my-python-app-v1.tar

- To ensure the image is now available on your system, list the Docker images:

- docker images

- Run a container from the image to see if it works:

- docker run <yourname>/my-python-app:v1

- Finally, enter the following link in your browser:

- http://127.0.0.1:5001



**Example:**

<img width="564" alt="Screenshot 2024-06-12 at 9 39 04 PM" src="https://github.com/BaloneyBoy97/PSD-TEAM/assets/142546682/625ac47d-dfb9-4bfd-99af-dfd61fea7066">

<img width="564" alt="Screenshot 2024-06-12 at 9 39 42 PM" src="https://github.com/BaloneyBoy97/PSD-TEAM/assets/142546682/a81f8767-ecaf-4e58-9599-a4265840da34">

<img width="1512" alt="Screenshot 2024-06-12 at 9 40 06 PM" src="https://github.com/BaloneyBoy97/PSD-TEAM/assets/142546682/e32cd17c-d50c-4533-81da-686ee80fb15d">
