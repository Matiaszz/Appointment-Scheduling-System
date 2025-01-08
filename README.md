# Project Overview

The Appointment Scheduling System is a web-based application designed to facilitate the scheduling of appointments between users and service providers. This system aims to streamline the booking process, reduce scheduling conflicts, and enhance user experience.

## Features

User Registration and Login: Users can create accounts and log in to manage their appointments.

Appointment Management: Users can view, reschedule, or cancel their appointments.

Admin Dashboard: Administrators can manage users, service providers, and appointments.

## Technologies Used

Frontend: HTML, CSS and JavaScript

Backend: Django, Django rest framework

APIs: Google Calendar

Database: Postgres with railway

## Installation Instructions

### Clone the Repository:

```
git clone https://github.com/Matiaszz/Appointment-Scheduling-System.git
```

### Navigate to the Project Directory:

```
cd Appointment-Scheduling-System
```

### Create a venv:

```
python -m venv venv
```

### Activate the venv:

```
windows: .\venv\scripts\activate
linux/macOS: source venv/bin/activate
```

### Install Dependencies:

```
pip install -r requirements.txt
npm install -D tailwindcss postcss autoprefixer
```

### Set Up Environment Variables:

Create a .env file inside of a folder named env in the ``Appointment-Scheduling-System`` directory and add your database connection string and other necessary configurations.
Run the Application:

```
python manage.py runserver
```

Access the application in your web browser at http://localhost:8000.
Register for an account or log in to start booking appointments.


## Contributing

Contributions are welcome! Please follow these steps:

## Fork the repository.

Create a new branch (git checkout -b feature/YourFeature).
Make your changes and commit them (git commit -m 'Add some feature').
Push to the branch (git push origin feature/YourFeature).
Open a pull request.
