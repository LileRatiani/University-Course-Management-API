# University Course Management API

A RESTful backend API for managing university courses, students, professors, assignments, enrollments, and submissions. Built with Django REST Framework and designed with role-based access control and JWT authentication.

---

## Features

### User Management & Authentication

- **Custom User Roles**  
  Custom Django user model with three distinct roles:
  - `Student`
  - `Professor`
  - `Admin`

- **JWT Authentication**  
  Secure authentication using **SimpleJWT** with access and refresh tokens.

- **Role-Based Permissions**
  - **Students** can manage their own profiles, enroll in courses, and submit assignments.
  - **Professors** can create courses, post assignments, and grade student submissions.
  - **Admins** have full access to the system.

### Course Management

- Create and manage university courses.
- Enroll students in courses.
- Prevent duplicate enrollment.
- Enforce maximum course capacity.
- Search courses by title or description.
- Filter courses by professor.

### API Documentation

- Fully integrated **Swagger UI**.
- Test API endpoints directly from the browser.
- View available endpoints, request parameters, and responses.

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Programming language |
| **Django** | Backend framework |
| **Django REST Framework** | REST API development |
| **SQLite** | Database |
| **SimpleJWT** | JWT authentication |
| **drf-yasg** | Swagger API documentation |
| **Docker** | Containerization |
| **Docker Compose** | Container orchestration |

---

## Project Structure

```text
university-course-management/
│
├── users/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── courses/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── assignments/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── manage.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt