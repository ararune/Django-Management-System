## Student Management System

This is a Student Management System web application developed using Django, a Python web framework. It provides functionality for managing students, professors, and courses within an educational institution.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)


## Features

| Feature            | Description                                                         |
|---------------------|---------------------------------------------------------------------|
| User Roles    | Supports three user roles: administrator, professor, and student.                |
| User Registration               | New users can register with the system by providing required information.                  |
| User Login/Logout      | Registered users can log in and log out of the system.                         |
| User Profile Editing         | Users can edit their profile information such as name, email, and password.                                 |
| Course Management | Create, update, and delete courses.                       |
| Enrollment | Students can view available courses and enroll in them.               |
| Enrollment List  | 	Professors and administrators can view a list of enrolled students. |
| User Access Control | Restricts access to certain functionalities based on user roles and permissions.         |

## Installation

Follow these steps to install and run the Student Management System:

```bash
git clone https://github.com/your-username/student-management-system.git
```

Create a virtual environment for the project:

```bash
python -m venv venv
```
Activate the virtual environment:

- Windows 
```powershell
venv\Scripts\activate
```
- Linux/macOS
```bash
source venv/bin/activate
```
Install the project dependencies:
```bash
pip install django
```
Apply database migrations:
```bash
python manage.py migrate
```
Create a superuser (administrator) account (optional step): 
```bash
python manage.py createsuperuser
```
Start the development server:
```bash
python manage.py runserver
```
Access the application in your web browser at http://localhost:8000.

## Usage

1. Access the login page by visiting http://localhost:8000/accounts/login
2. Log in to the system using your credentials, for starters you can use admin user with username `admin` and password `admin`
3. Under 'Dodaj Predmet' tab you can create some courses.
4. After that you can go ahead and Register some professors and then some students.


