# Simple Python API

I built this API where users can:

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

Data is stored in a relational database using **SQLAlchemy**.

There are two tables: **User** and **Game**. These tables have a **1:M (one-to-many) relationship**, where:

* One user can have multiple games.
* Each game is associated with one user.
* Users and games are linked using a `user_id` attribute, allowing games to be associated with their respective users.

## Routes

* Root (`/`): This displays login status
    * Profile (`/get_user_info/user_id`): This allows users to `GET` their id and username.
    * Login (`/login`): This allows users to `POST` login details and login to their accounts.
    * Logout (`/logout`): This allows users to `POST` a request to logout of their accounts.
    * Create Account (`/create-account`): This allows users to `POST` a username and password for a new account.
    * List Reviews (`/games`): This allows users to `GET` their collection of game reviews.
        * Get Specific Review (`/games/game_id`): This allows users to `GET` a specific review.
            * Update Specific Review (`/games/game_id/update`): This allows users to `PUT` different values into an existing review.
            * Delete Specific Review (`/games/game_id/delete`): This allows users to `DELETE` a specific review.
    * Create Review (`/create-game`): This allows users to `POST` specifics of a new review to add to their collection.

## Security & Authentication

Security and authentication are handled using Flask's **Werkzeug Security** module. Passwords are securely **hashed** before being stored in the database rather than being stored as plain text.

## Requirements

All required Python libraries are listed in `requirements.txt`.

To install all required libraries, run:

```bash
pip install -r requirements.txt
```
