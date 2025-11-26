# SkillLoop API

Backend API for **SkillLoop**, a skill-sharing / mentoring platform built with Django and Django REST Framework.

The API allows users to:

- Create & list skills they can offer.
- Request skill exchanges with other users.
- Send contact messages to the site owner (e.g. general enquiries, mentoring requests).

This repo only contains the **backend** – a separate frontend (React) can consume these endpoints.

---

## Tech stack

- **Python 3.11**
- **Django 5.2.4**
- **Django REST Framework**
- **dj-rest-auth** (authentication helper)
- **django-allauth**
- **SQLite** (development)
- **Whitenoise** (static files, production-ready)

---

## Project structure (relevant apps)

- `skillloop/` – main Django project
- `users/` – app with:
  - `Skill` model & API views
  - `SkillExchange` model & API views
  - `Contact` model & contact endpoint

---

## Getting started (local development)

### 1. Clone and install dependencies

```bash
git clone <your-repo-url>
cd skillLoop-API

# create & activate virtualenv (Windows example)
python -m venv venv
venv\Scripts\activate

# install dependencies
pip install -r requirements.txt
