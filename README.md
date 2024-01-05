# CA314-Group18

## How to run the flask app:

- The flask app requires a number of python libraries, all of which can be installed with pip
- It is common practice to use virtual environments for each separate python project as this means the pip packages can be stored in a requirements.txt file which can easily accessed and lock in package versions, some of which might differ on dependancies of the project or other packages

- Within this project there is a number of packages like wtforms which are broken by the latest version of Werkzeug breaks the login funcitonality, the latest known version to work as expected is Werkzeug 2.3.0, as refelcted in the requiretments.txt file.

## Using virtual environment
- in the root of the project, initialize a new virtual environment.
```sh
python -m venv env
```

- activate it.
```sh
# linux shell:
source env/bin/activate
```

install the pip packages
```sh
pip install -r requirements.txt
```

## How to run the Flask app:
- run using:
```sh
cd FlaskApp

python app.py
```

# Project Technical Summary

## Overview

This project is a Flask-based web application designed for real-time communication. It leverages Flask's capabilities to provide a robust backend, integrating features like user authentication, real-time messaging using SocketIO, and data storage with SQLAlchemy. The application's architecture is modular, with clear separation of concerns, ensuring maintainability and scalability.

## Key Features

1. **User Authentication**: Utilizes Flask-Login for handling user sessions and authentication.
2. **Real-Time Communication**: Implements Flask-SocketIO to facilitate real-time messaging capabilities.
3. **Data Management**: Uses SQLAlchemy for database interactions, including user data storage and retrieval.
4. **Form Handling**: Integrates Flask-WTF for secure form submission and validation.
5. **Password Security**: Employs Flask-Bcrypt for hashing and securing user passwords.

## Technical Stack

- **Framework**: Flask
- **Database**: SQLite (via SQLAlchemy)
- **Real-Time Engine**: Flask-SocketIO
- **Form Handling**: Flask-WTF
- **Password Hashing**: Flask-Bcrypt
- **User Session Management**: Flask-Login

## Project Structure

- `app.py`: The main entry point of the application, initializing the Flask app and its extensions.
- `routes.py`: Contains all the route definitions using Flask Blueprints for a clean and modular approach.
- `models.py`: Defines the SQLAlchemy models, primarily focused on the User model.
- `forms.py`: Houses the WTForms definitions for user registration and login.
- `templates/`: Folder containing the Jinja2 templates for rendering the frontend.

## Setup and Running

1. **Installation**: Set up a virtual environment and install dependencies from `requirements.txt`.
2. **Configuration**: Set the secret key in `app.py` and configure the database URI as needed.
3. **Initialization**: Run `python app.py` to start the Flask development server.
4. **Access**: The application will be accessible at `http://127.0.0.1:5000/` by default.

## Future Enhancements

- **UI/UX Improvements**: Enhance frontend design for a better user experience.
- **Additional Features**: Implement features like file sharing, group chats, etc.
- **Deployment**: Prepare the application for deployment in a production environment.
- **Testing**: Develop a comprehensive suite of unit and integration tests.

---
