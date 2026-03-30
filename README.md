# SkillLoop API

The Django REST Framework backend for SkillLoop — a skill-sharing platform where users can offer skills, browse others, and request skill exchanges.

Live site: https://skillloopfrontend-952dcb19a921.herokuapp.com
Backend API: https://skillloop-api-hbica-3bb338c1557b.herokuapp.com
---

## Table of Contents

1. [Project Purpose](#project-purpose)
2. [Database Schema](#database-schema)
3. [API Endpoints](#api-endpoints)
4. [Features](#features)
5. [Tech Stack](#tech-stack)
6. [Testing](#testing)
7. [Bugs](#bugs)
8. [Deployment](#deployment)
9. [Credits](#credits)

---

## Project Purpose

SkillLoop API provides a RESTful backend for the SkillLoop frontend. It handles user authentication, skill management, skill exchange requests, user profiles and contact messages.

### Project Goals

| Goal | Implementation |
|---|---|
| Secure user authentication | dj-rest-auth Token authentication |
| Store and manage skills | Skill model with full CRUD |
| Enable skill exchanges between users | SkillExchange model with status workflow |
| User profiles | Profile model auto-created on registration |
| Contact messages | Contact model, open POST endpoint |

---

## Database Schema

### Entity Relationship Diagram

```
USER (Django built-in)
  id (PK)
  username
  email
  password

PROFILE
  id (PK)
  user (FK -> USER, OneToOne)
  bio
  location
  avatar
  created_at

SKILL
  id (PK)
  owner (FK -> USER)
  title
  description
  category
  level (beginner / intermediate / advanced)
  is_remote (boolean)
  created_at

SKILLEXCHANGE
  id (PK)
  requester (FK -> USER)
  recipient (FK -> USER)
  skill_offered (FK -> SKILL)
  skill_requested (FK -> SKILL)
  message
  status (pending / accepted / declined / completed)
  created_at
  updated_at

CONTACT
  id (PK)
  name
  email
  subject
  message
  created_at
  is_resolved (boolean)
```

### Relationships

- One USER has one PROFILE (OneToOne)
- One USER can have many SKILLs (ForeignKey)
- One USER can send many SKILLEXCHANGEs as requester
- One USER can receive many SKILLEXCHANGEs as recipient
- One SKILLEXCHANGE references two SKILLs (offered and requested)

---

## API Endpoints

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| / | GET | No | API root — lists available endpoints |
| /admin/ | GET | Admin | Django admin panel |
| /dj-rest-auth/login/ | POST | No | Login, returns token |
| /dj-rest-auth/logout/ | POST | Yes | Logout |
| /dj-rest-auth/user/ | GET | Yes | Get current user |
| /dj-rest-auth/registration/ | POST | No | Register new user |
| /api/profiles/ | GET | No | List all profiles |
| /api/profiles/:id/ | GET | No | Retrieve a profile |
| /api/profiles/:id/ | PUT/PATCH | Yes (owner) | Update a profile |
| /api/profile/me/ | GET | Yes | Get own profile |
| /api/profile/me/ | PATCH | Yes | Update own profile |
| /api/skills/ | GET | No | List all skills (supports ?search= and ?category=) |
| /api/skills/ | POST | Yes | Create a skill |
| /api/skills/:id/ | GET | No | Retrieve a skill |
| /api/skills/:id/ | PUT/PATCH | Yes (owner) | Update a skill |
| /api/skills/:id/ | DELETE | Yes (owner) | Delete a skill |
| /api/exchanges/ | GET | Yes | List exchanges (requester or recipient) |
| /api/exchanges/ | POST | Yes | Create exchange request |
| /api/exchanges/:id/ | GET | Yes | Retrieve an exchange |
| /api/exchanges/:id/ | PATCH | Yes | Update exchange status |
| /api/exchanges/:id/ | DELETE | Yes | Delete an exchange |
| /api/contact/ | POST | No | Submit a contact message |

---

## Features

### Authentication
- Token-based authentication via dj-rest-auth
- Registration creates a user account
- Login returns a token used in all subsequent authenticated requests
- Custom RegisterSerializer extends dj-rest-auth to accept optional bio and location fields

### Profiles
- Profile automatically created for each new user via Django signals (or dj-rest-auth hooks)
- Profile includes bio, location and avatar URL
- Nested skills serializer returns all skills owned by the user from the profile endpoint
- Only the profile owner can update their profile (IsOwnerOrReadOnly permission)

### Skills
- Full CRUD for authenticated users
- owner field automatically set to the logged-in user on create (perform_create)
- Search supported via ?search= query param (searches title, description, category)
- Category filter supported via ?category= query param
- Read access is public (IsAuthenticatedOrReadOnly)
- Write/delete restricted to owner (IsOwnerOrReadOnly)

### Skill Exchanges
- Authenticated users can create exchange requests
- requester automatically set to the logged-in user on create
- GET /api/exchanges/ returns only exchanges where the user is requester OR recipient
- Status workflow: pending → accepted / declined → completed
- Only authenticated users can view or modify exchanges

### Contact
- Public endpoint — no authentication required
- Stores name, email, subject, message and timestamp
- is_resolved field for admin management

### Permissions
- IsAuthenticatedOrReadOnly — used on Skills and Profiles (public read, auth write)
- IsAuthenticated — used on Exchanges and profile/me (fully protected)
- IsOwnerOrReadOnly — custom permission, checks object.owner or object.user == request.user
- AllowAny — used on Contact (public)

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3 | Backend language |
| Django 4 | Web framework |
| Django REST Framework | API framework |
| dj-rest-auth | Authentication endpoints |
| django-allauth | Registration support |
| django-cors-headers | CORS headers for frontend access |
| gunicorn | Production WSGI server |
| whitenoise | Static file serving |
| SQLite | Development database |
| PostgreSQL | Production database (Heroku) |

---

## Testing

### Manual Testing

| Feature | Action | Expected | Result |
|---|---|---|---|
| Register | POST /dj-rest-auth/registration/ with valid data | 201 response, token returned | Pass |
| Register duplicate username | POST with existing username | 400 response with error | Pass |
| Login | POST /dj-rest-auth/login/ with valid credentials | 200 response, token returned | Pass |
| Login wrong password | POST with wrong password | 400 response | Pass |
| List skills | GET /api/skills/ | 200 response, list of skills | Pass |
| Search skills | GET /api/skills/?search=python | Filtered results returned | Pass |
| Category filter | GET /api/skills/?category=Tech | Only Tech skills returned | Pass |
| Create skill | POST /api/skills/ with token | 201 response, skill created | Pass |
| Create skill no auth | POST /api/skills/ without token | 401 response | Pass |
| Edit own skill | PUT /api/skills/:id/ as owner | 200 response, skill updated | Pass |
| Edit other skill | PUT /api/skills/:id/ as non-owner | 403 response | Pass |
| Delete own skill | DELETE /api/skills/:id/ as owner | 204 response | Pass |
| Delete other skill | DELETE /api/skills/:id/ as non-owner | 403 response | Pass |
| List exchanges | GET /api/exchanges/ with token | Only own exchanges returned | Pass |
| Create exchange | POST /api/exchanges/ with token | 201 response | Pass |
| Update exchange status | PATCH /api/exchanges/:id/ | Status updated | Pass |
| Get own profile | GET /api/profile/me/ with token | Profile with skills returned | Pass |
| Update own profile | PATCH /api/profile/me/ with token | Profile updated | Pass |
| Submit contact | POST /api/contact/ no auth | 201 response | Pass |
| Admin panel | Visit /admin/ as superuser | Admin interface loads | Pass |

### Python Validation

- All Python code follows PEP8 style guidelines
- Checked using pycodestyle / flake8
- No significant issues found

---

## Bugs

### Fixed Bugs

**Bug 1 — Skills search and category filter not working**

SkillListCreateView originally used a static queryset = Skill.objects.all() with no filtering. The frontend was sending ?search= and ?category= params but they were ignored. Fixed by overriding get_queryset() to apply Q filters for search across title, description and category, and category__iexact filter for category.

**Bug 2 — CORS errors blocking frontend requests**

The React frontend on localhost:3000 was blocked by CORS policy when calling the API on localhost:8000. Fixed by installing django-cors-headers and adding CORS_ALLOWED_ORIGINS to settings.py.

### Known Issues

- Avatar field is a URLField — image upload not yet implemented
- No pagination on skills or exchanges endpoints (planned improvement)

---

## Deployment

### Prerequisites

- Python 3 installed
- Heroku CLI installed
- Heroku account created
- PostgreSQL addon available on Heroku

### Local Development

1. Clone the repository:
```
git clone https://github.com/HBica05/skillLoop-API.git
cd skillLoop-API
```

2. Create and activate virtual environment:
```
python -m venv venv
source venv/Scripts/activate  (Windows)
source venv/bin/activate       (Mac/Linux)
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Create a .env file:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
```

5. Run migrations and start server:
```
python manage.py migrate
python manage.py runserver
```

### Heroku Deployment Steps

1. Login to Heroku CLI:
```
heroku login
```

2. Create a Heroku app:
```
heroku create skillloop-api
```

3. Add PostgreSQL:
```
heroku addons:create heroku-postgresql:mini
```

4. Set environment variables:
```
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=skillloop-api.herokuapp.com
```

5. Add Heroku to ALLOWED_HOSTS in settings.py:
```python
ALLOWED_HOSTS = ['skillloop-api.herokuapp.com', 'localhost']
```

6. Add CORS allowed origins in settings.py:
```python
CORS_ALLOWED_ORIGINS = [
    'https://skillloop-frontend.herokuapp.com',
    'http://localhost:3000',
]
```

7. Make sure requirements.txt is up to date:
```
pip freeze > requirements.txt
```

8. Confirm Procfile exists:
```
web: gunicorn skillloop.wsgi:application
```

9. Deploy:
```
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main
```

10. Run migrations on Heroku:
```
heroku run python manage.py migrate
```

11. Create a superuser on Heroku:
```
heroku run python manage.py createsuperuser
```

### Environment Variables

| Variable | Description |
|---|---|
| SECRET_KEY | Django secret key — never commit this |
| DEBUG | Set to False in production |
| ALLOWED_HOSTS | Comma-separated list of allowed hosts |
| DATABASE_URL | Set automatically by Heroku PostgreSQL addon |

All secret values are stored in environment variables and never committed to the repository.

---

## Credits

### Technologies

- Django — https://www.djangoproject.com
- Django REST Framework — https://www.django-rest-framework.org
- dj-rest-auth — https://dj-rest-auth.readthedocs.io
- django-allauth — https://django-allauth.readthedocs.io
- django-cors-headers — https://github.com/adamchainz/django-cors-headers
- gunicorn — https://gunicorn.org
- whitenoise — https://whitenoise.readthedocs.io

### Learning Resources

- Code Institute — course material and project brief
- Django REST Framework documentation
- Python documentation

### Tools

- Claude AI — development assistance and code review
- ChatGPT — development assistance
- GitHub — version control

---

## Author

Haadiyah Bica  
GitHub: https://github.com/HBica05

---

*This project was created for educational purposes as part of the Code Institute Diploma in Full Stack Software Development (Advanced Front-End).*