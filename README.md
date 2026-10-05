# Simple Python API

I built this game website where users can:

* Create accounts
* Log in and log out
* Create game reviews
* Read game reviews
* Update game reviews
* Delete game reviews

Each game review stores:

* Game name
* Hours played
* Completion status (`100%` or `Normal`)
* Rating (`0–10`)
* Review

## Architecture

The back-end architecture of the application is handled by **Flask**.

The front end of the application will be handled by **PyQt6** *(WIP)*.

Data is stored in a relational database using **SQLAlchemy**.

There are two tables: **User** and **Game**. These tables have a **1:M (one-to-many) relationship**, where:

* One user can have multiple games.
* Each game is associated with one user.
* Users and games are linked using a `user_id` attribute, allowing games to be associated with their respective users.

## Security & Authentication

Security and authentication are handled using Flask's **Werkzeug Security** module. Passwords are securely **hashed** before being stored in the database rather than being stored as plain text.

## Requirements

All required Python libraries are listed in `requirements.txt`.

To install all required libraries, run:

```bash
pip install -r requirements.txt
```
