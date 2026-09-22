# Student Portal

A Django student portal with separate student and staff dashboards.

## Features

- Login with Django authentication
- Student and teacher/admin dashboards
- Student groups managed by staff users
- Teachers and admins can edit groups
- Teachers and admins can add homework
- Teachers and admins can add marks from 0 to 100
- Students can view only their own marks
- Secure logout with session clearing
- Django admin management for users, students, teachers, groups, homework, and marks

## Setup

Use the project virtual environment on Windows:

```powershell
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py createsuperuser
.venv\Scripts\python.exe manage.py runserver
```

Open the application at `http://127.0.0.1:8000/`.

## User Roles

### Students

Students are regular Django users. A staff member must create a `Student` profile and connect it to the user account in the admin panel.

Students can:

- View their student dashboard
- View groups they belong to
- View homework for their groups
- View only their own marks

### Teachers and admins

Teachers and admins must have a Django user account with staff access. Create a `Teacher` or `Admin` profile and connect it to the account in the admin panel.

Staff users can:

- Create and edit student groups
- Add students to groups
- Add homework and deadlines
- Add student marks and comments
- Manage records through Django admin

## Important URLs

- `/login/` - login page
- `/` - role-based dashboard redirect
- `/student/` - student dashboard
- `/staff/` - staff dashboard
- `/staff/groups/` - student group management
- `/admin/` - Django admin panel

## Development Checks

```powershell
.venv\Scripts\python.exe manage.py check
.venv\Scripts\python.exe manage.py test
```
