




## 📺 Project Demo Video
You can watch the full video demonstration of this Event Registration System on [Google Drive](https://drive.google.com/file/d/1qY7hNN7wcvWI_2AUQQ4ChX4xImJaYm6F/view?usp=drivesdk)





# 🎟️ Event Registration System (Django + PostgreSQL + DRF)

A backend system built with **Django, Django REST Framework, and PostgreSQL** that allows users to create events, register for events, and manage registrations with strict constraints like seat limits, duplicate prevention, and race-condition safety.

---

## 🚀 Features

### 📅 Event Management

- Create events with:
  - Unique event name
  - Total seats (> 0)
  - Event date (must be in future)
- View all events
- Filter upcoming events
- Sort events by date

---

### 👤 User Registration

- Register user for an event
- Prevent duplicate registrations (same user + event)
- Prevent overbooking (seat limit enforcement)
- Store registration timestamp

---

### ❌ Cancel Registration

- Cancel active registration
- Freed seat becomes available automatically
- Cancelled users excluded from active counts

---

## ⚠️ Business Rules

- Event name must be unique
- Total seats must be greater than 0
- Event date must be in the future
- Same user cannot register twice for same event
- No overbooking allowed
- Race condition protection enabled
- Proper error handling for all edge cases

---

## 🏗️ Tech Stack

- Python 3.x
- Django 5+
- Django REST Framework
- PostgreSQL
- HTML + Bootstrap (optional frontend)
- Virtual Environment (venv)

---

## 📁 Project Structure

event_registration/
│
├── event_registration/ # Django project settings
│ ├── settings.py
│ ├── urls.py
│
├── events/ # Main app
│ ├── migrations/
│ ├── models.py
│ ├── views.py
│ ├── serializers.py
│ ├── services.py
│ ├── utils.py
│ ├── urls.py
│ ├── templates/
│ ├── static/
│
├── eventsenv
├── templates
├── .env
├── manage.py
└── README.md

---

## ⚙️ Setup Instructions

### 1️⃣ Clone repository

```bash
git clone <repo-url>
cd event_registration
```

2️⃣ Create virtual environment
python -m venv venv

Activate:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Setup PostgreSQL
CREATE DATABASE event_db;

CREATE USER event_user WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE event_db TO event_user;
5️⃣ Create .env file
DB_NAME=event_db
DB_USER=event_user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
6️⃣ Run migrations
python manage.py makemigrations
python manage.py migrate

7️⃣ Create superuser
python manage.py createsuperuser

8️⃣ Run server
python manage.py runserver

🔗 API Endpoints
📅 Events
Method Endpoint Description
POST /api/events/create/ Create event
GET /api/events/ List events
👤 Registration
Method Endpoint Description
POST /api/register/ Register user
POST /api/cancel/ Cancel registration
📥 Example Requests
Create Event
{
"name": "Django Workshop",
"total_seats": 50,
"event_date": "2026-12-30T10:00:00Z"
}
Register User
{
"user_name": "Ali",
"event_id": 1
}
Cancel Registration
{
"user_name": "Ali",
"event_id": 1
}
🧠 Key Concepts Used
Django ORM
Django REST Framework APIs
PostgreSQL database
Transaction management (atomic)
Row locking (select_for_update)
Service layer architecture
Input validation
Error handling best practices
🛡️ Race Condition Handling
transaction.atomic() ensures safe execution
select_for_update() locks event row during registration
Prevents overbooking in concurrent requests

👨‍💻 Author

Backend system built using Django + PostgreSQL for learning and assessment purposes.
