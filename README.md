# SkillLoop API Documentation

## Base URL

For local development:

http://127.0.0.1:8000/


All custom endpoints are prefixed with `/api/`, for example:

http://127.0.0.1:8000/api/skills/


Authentication endpoints from `dj-rest-auth` live under:

http://127.0.0.1:8000/dj-rest-auth/

---

## 🔐 Authentication

The API uses **token-based authentication**.

### **Register**
**POST** `/api/register/`  
Creates a new user and their profile.

**Request Body**
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password1": "Testpass123!",
  "password2": "Testpass123!",
  "bio": "Optional short bio",
  "location": "Optional location"
}

Response

{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com"
}
Login
POST /dj-rest-auth/login/

Request

{
  "username": "testuser",
  "password": "Testpass123!"
}
Response

{
  "key": "your-auth-token-string"
}

Include token in all authenticated requests:

Authorization: Token your-auth-token-string
Logout
POST /dj-rest-auth/logout/
Invalidates the token.

📘 Endpoints Overview
| Resource        | Method | URL                     | Auth? | Description             |
| --------------- | ------ | ----------------------- | ----- | ----------------------- |
| Register        | POST   | `/api/register/`        | No    | Create user + profile   |
| Login           | POST   | `/dj-rest-auth/login/`  | No    | Get token               |
| Logout          | POST   | `/dj-rest-auth/logout/` | Yes   | Logout                  |
| Skills          | GET    | `/api/skills/`          | Yes   | List skills             |
| Skills          | POST   | `/api/skills/`          | Yes   | Create skill            |
| Skill Exchanges | GET    | `/api/exchanges/`       | Yes   | List exchange requests  |
| Skill Exchanges | POST   | `/api/exchanges/`       | Yes   | Create exchange request |
| Contact Form    | POST   | `/api/contact/`         | No    | Public contact form     |


🧠 Skills Endpoints
List / Create Skills
GET /api/skills/
Returns all skills.

Example response:

[
  {
    "id": 1,
    "owner": 1,
    "title": "Piano Lessons",
    "description": "Beginner piano lessons for kids and adults.",
    "category": "Music",
    "level": "beginner",
    "is_remote": true,
    "created_at": "2025-11-26T11:30:00Z"
  }
]
Create Skill
POST /api/skills/

Request

{
  "title": "Piano Lessons",
  "description": "Beginner piano lessons.",
  "category": "Music",
  "level": "beginner",
  "is_remote": true
}
Response

{
  "id": 2,
  "owner": 1,
  "title": "Piano Lessons",
  "description": "Beginner piano lessons.",
  "category": "Music",
  "level": "beginner",
  "is_remote": true,
  "created_at": "2025-11-26T12:00:00Z"
}

🔄 Skill Exchanges
A SkillExchange is a request between two users to trade skills.

List / Create Skill Exchanges
GET /api/exchanges/
Returns requests.

Example response:

[
  {
    "id": 1,
    "requester": 1,
    "recipient": 2,
    "skill_offered": 1,
    "skill_requested": 2,
    "message": "Want to swap piano lessons for coding?",
    "status": "pending",
    "created_at": "2025-11-26T12:10:00Z",
    "updated_at": "2025-11-26T12:10:00Z"
  }
]
Create Skill Exchange
POST /api/exchanges/

Request

{
  "recipient": 2,
  "skill_offered": 1,
  "skill_requested": 2,
  "message": "Want to swap piano lessons for coding?"
}
Response

{
  "id": 2,
  "requester": 1,
  "recipient": 2,
  "skill_offered": 1,
  "skill_requested": 2,
  "message": "Want to swap piano lessons for coding?",
  "status": "pending",
  "created_at": "2025-11-26T12:15:00Z",
  "updated_at": "2025-11-26T12:15:00Z"
}
📩 Contact Form
POST /api/contact/
Public contact form.

Request

{
  "name": "Haadiyah",
  "email": "you@example.com",
  "subject": "Question about a skill",
  "message": "I'd like to know more about Python mentoring."
}
Response

{
  "id": 2,
  "name": "Haadiyah",
  "email": "you@example.com",
  "subject": "Question about a skill",
  "message": "I'd like to know more about Python mentoring.",
  "created_at": "2025-11-26T12:44:00Z",
  "is_resolved": false
}
🔍 Browsable API
When DEBUG=True, DRF provides a test interface:

http://127.0.0.1:8000/api/register/

http://127.0.0.1:8000/api/skills/

http://127.0.0.1:8000/api/exchanges/

http://127.0.0.1:8000/api/contact/

You can log in and interact with all endpoints directly from the browser.
