# 🛎️ Django In-App Task Reminder System with Celery, Redis & Celery Beat

This documentation provides an end-to-end explanation of a fully functional **in-app task reminder system** built using Django, Celery, Redis, and Celery Beat. The system automatically generates reminders for users when their tasks are due **the next day**, and displays them as in-app notifications.

---

## 🧠 Overview

### 🔍 What It Does:
- Automatically scans tasks every hour.
- Finds tasks that are **due tomorrow** and still **incomplete**.
- Creates **in-app notifications** for users.
- Allows users to view and delete these notifications.

### 🔧 Stack:
- **Django** – Core web framework
- **Celery** – Background task runner
- **Redis** – Broker for Celery
- **Celery Beat** – Scheduler to run tasks on intervals
- **Bootstrap** – For styled notifications frontend

---

## 📦 Technologies Used

| Component          | Technology               |
|-------------------|--------------------------|
| Backend Framework | Django                   |
| Task Queue        | Celery                   |
| Scheduler         | Celery Beat              |
| Broker            | Redis                    |
| Frontend UI       | Django Template + Bootstrap |
| Database          | PostgreSQL / SQLite      |

---







