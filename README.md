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
	- Role based user access
	- Secure password check
	- Save password


- Check In Management:
	- Online check in
	- Baggage Check-In
	- Customer Support and Assistance
	- Seat Selection
	- Generate and display flight ticket

- Flight Search and Booking
	- Search flights
	- Booking confirmation
	- Display real time flight status
- Admin panel
	- Manage flights, passengers, and booking

 
- User Authentication interacts with database to create, update, retrieve, or delete user data for user creating, deletion, or user information update
- User authentication also interacts with Check In Management system to authenticate user for online check in process
- Check In Management system will interact with database to only retrieve flight and user data to manage customer check in process
- Check In Management system will also interact with Email service to send confirmation and E-ticket to user
- Flight Search and Booking system will interact with Check In Management to update CIM with booking detail
- Flight Search and Booking system will also interact database to create query to display flights based on user input and it will also create new booking information and store in database
- Admin panel will interact with Database to manage flight, user, booking and perform CRUD operation in DB
- Admin panel will also interact with Check In Management system to manipulate/update check in data

	<img width="527" alt="Screenshot 2024-05-28 at 2 18 32 AM" src="https://github.com/BaloneyBoy97/PSD-TEAM/assets/142546682/7dc93fe0-ceb6-474b-aa87-0105529db9d6">
	<img width="552" alt="Screenshot 2024-06-11 at 11 31 23 PM" src="https://github.com/BaloneyBoy97/PSD-TEAM/assets/142546682/740b79d6-2aaf-4ecb-916c-c4f392ac4062">
**Team Expertise**

Zanxiang Wang:

Python: back end server logic

SQL: database design

Charitha Vennapusala:

HTML,CSS: front end web design

JS: back front end web design

MySQL: database design

Deepak Sarun Yuvachandran: 

HTML, CSS: front end web development

JS and React: front end web development

Nandini Reddy Bhumula:  

Java Script: front end web development

Agile principles: software development

Database Connection Management , API Connection Management: database design

**User Stories and Estimation**

- As a new customer, I want to register an account so that I can access the airport check-in system.
- Overall story points: 5
- Justification:
	- Creating a new use requires creating a register form
	- Validating accounting information
	- Hashing password and storing new user data in database
	- The step requires front end design and back end server logic and data creation. It is moderately complex
- As a registered customer, I want to log in with my email and password so that I can access my account and check-in for flights.
- Overall story points: 1
- Justification:
	- Existing user login requires credential verification i.e email and password and managing user session.
	- The process is straightforward and simple
- As a registered customer, I want to make multiple attempts if my login attempt fails so that I can try again or reset my password.
- Overall story points: 1
- Justification:
	- Notifying user of their failed login attempts requires simple error handling and messaging
	- It is a fairly simply process
- As a registered customer, I want to log out of my account so that my session is securely terminated.
- Overall story points: 1
- Justification:
	- Logging out of a existing session requires session handling and invalidation
	- This is a straightforward process
- As an admin, I want to have access to admin panel so that I can add new flights to the system
- Overall story points: 5
- Justification: 
	- Admin account require a different authentication process (medium difficulty, can be build upon existing user authentication process)
	- Manipulating flight data require data validation and form for input (fairly complex, require proper data storage and updating flight management - system)
	- The overall process to create an admin role can be built up on the existing user authentication process.
- As an admin, I want to delete user accounts so that I can remove problematic users from the system.
- Overall  story points: 3
- Justification: 
	- To delete a user account requires a delete  function and a message to confirm the delete.
	- This is a single function on back end server logic as well as a front end display confirming deletion of user accounts. The complexity is fairly simple.
- As an admin, I want to view a list of all registered users so that I can manage user accounts.
- Overall story points: 3
- Justification:
	- Displaying lists of users can be achieved by fetching data and rendering it the process if fairly simple
- As an unregistered customer, I want to search for flights without logging in so that I can explore flight options before creating an account.
- Overall story points: 1
- Justification:
	- Implementing a flight search feature accessible without authentication is straightforward because it does not involve user authentication or session management.
	- Displaying search results based on user input is simple as it requires querying the database and presenting the results.
- As a registered customer, I want to search for flights by entering departure and arrival locations, dates, and number of passengers so that I can find suitable flight options for my trip.
- Overall story points: 2
- Justification
	- Designing and implementing a search form involves creating a user-friendly interface.
	- Querying the database to return matching flights involves moderate complexity due to the need for accurate data retrieval and handling user input.
- As a customer, I want to filter my flight search results by price, duration, and number of stops so that I can find the best flight options according to my preferences.
- Overall story points: 3
- Justification
	- Implementing filter options in the search results requires additional UI elements and logic to handle user-selected filters.
	- Applying filters to the flight search query involves modifying the database queries to return the filtered results, adding moderate complexity.
- As a customer, I want to view detailed information about a selected flight, including departure and arrival times, layovers, and total travel time so that I can make an informed decision.
- Overall story points: 1
- Justification
	- Displaying detailed flight information upon selection involves fetching additional flight details from the database.
	- Presenting this information is straightforward but essential for user decision-making.
- As a customer, I want to book a flight by entering passenger details and payment information so that I can confirm my booking and receive a booking confirmation.
- Overall story points: 5
- Justification
	- Creating a booking form for passenger details and payment information involves designing the form and ensuring data validation.
	- Processing the payment and storing booking details in the database requires integrating payment gateways and ensuring secure transactions.
	- Sending a booking confirmation email to the user involves back-end logic to generate and send emails, adding to the overall complexity.
- As a registered customer, I want to check in online so that I can avoid long queues at the airport.
- Overall story points: 5
- Justification:
	- User interface for online check-in (front-end design).
	- Backend logic to validate the check-in process.
	- Updating flight records to reflect the check-in status.
	- Moderately complex as it involves both user interaction and backend processing.
- As a registered customer, I want to check in my baggage online so that I can save time at the airport.
- Overall story points: 3
- Justification:
	- User interface for baggage check-in (front-end design).
	- Backend logic for handling baggage details and updating records.
	- Integration with the flight management system to allocate baggage space.
	- Moderately complex due to integration with existing systems and handling additional baggage details.
- As a registered customer, I want to access customer support and assistance during the check-in process so that I can resolve any issues quickly.
- Overall story points: 3
- Justification:
	- Interface for customer support (FAQ).
	- Backend support for handling inquiries and issues.
	- Moderately simple but requires robust support and assistance mechanisms.
- As a registered customer, I want to select my seat during the check-in process so that I can choose a seat that meets my preferences.
- Overall story points: 3
- Justification:
	- User interface for seat selection (front-end design).
	- Backend logic to display available seats and update seat assignments.
	- Moderately simple as it involves interactive elements and real-time updates.
- As a registered customer, I want to generate and display my flight ticket after completing the check-in process so that I can have a digital copy for boarding.
- Overall story points: 3
- Justification:
	- Generation of digital flight tickets (PDF or e-ticket).
	- Display and download options for the ticket.
	- Integration with check-in and flight records to ensure accuracy.
	- Moderately simple but requires attention to detail to ensure ticket accuracy and usability.
- As an admin, I want to manage flights so that I can add, update, or remove flights from the system.
- Overall story points: 3 
- Justification:
	- Creating an interface for adding, updating, and deleting flights (front-end design).
	- Backend logic to handle flight data manipulation.
	- Validation of flight data and integration with existing flight schedules.
	- Moderately complex due to the need for robust data handling and validation.
- As an admin, I want to manage passengers so that I can view, update, or remove passenger details.
- Overall story points: 5 
- Justification:
	- Interface for viewing, updating, and deleting passenger details (front-end design).
	- Backend logic for passenger data management.
	- Ensuring data integrity and proper validation.
	- Complex, as it involves handling sensitive passenger information securely.
- As an admin, I want to manage bookings so that I can view, update, or cancel bookings.
- Overall story points: 3 
- Justification:
	- Interface for viewing, updating, and canceling bookings (front-end design).
	- Backend logic for booking management.
	- Ensuring accurate and secure handling of booking data.
	- Moderately simple due to straightforward data manipulation and validation.
   
**- Total Points: 59**


**Project Completion Plan**

Week 1: 
- Design project structure
- Implement user authentication
- Refine and test the application
- fix bugs
  
Week 2: 
- Implement the check-in management system
- Implement flight search and booking functionalities. 
- Refine and test the application
- fix bugs
  
Week 3: 
- Implement flight status display. 
- Implement an admin panel for managing flights. 
- Refine and test the application
- fix bugs

