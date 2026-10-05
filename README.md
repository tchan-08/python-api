# Simple Python API
I built this game website where users can:
- Create Accounts
- Login/Logout
- Create game reviews
- Read game reviews
- Update game reviews
- Delete game reviews
These game reviews store:
- Name
- Game hours
- Completion status (100% or normal)
- Rating (0-10)
- Review
The Architecture of the application is handled by **Flask**
The Front-End of the application will be handled by **PyQt6** *(WIP)*
Data is stored in a relational database using **SQLAlchemy**
There are two tables: **User** and **Game** where:
- There is a 1:M relationship between user and game
- Users and games are linked together by a user ID attribute, allowing games to be associated with users and vice versa  
Security and authentication is handled by Flask's Werkzeug.security module, in which a password encoding and decrypted system is used
All library requirements will be handled in `requirements.txt`
To install all libraries, run `pip install -r requirements.txt`
