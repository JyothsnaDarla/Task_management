# 📝 Task Management Web App

A simple yet powerful **Task Management application** built with **Flask, SQLAlchemy, WTForms, and Flask-Login**.  
It allows users to register, log in, and manage their personal tasks with CRUD functionality, filters, and interactive UI.

---
## Demo 

<!-- Failed to upload "Screen Recording 2025-12-29 203446.mp4" -->

## 🚀 Features
- 🔐 **User Authentication** (Register, Login, Logout)
- ✅ **Task CRUD** (Create, Read, Update, Delete)
- 🎯 **Quick Add Form** for fast task creation
- 📅 **Due Dates & Priorities**
- 🔍 **Search & Filter** tasks by status, keyword, or priority
- 🎨 **Interactive UI/UX** with Bootstrap 5 and modals
- 🛡️ **CSRF Protection** and secure password hashing

---

## 📂 Project Structure
Task_management/
│── app.py               # Main Flask app
│── models.py            # Database models (User, Task)
│── forms.py             # WTForms for Register, Login, Task
│── templates/          # HTML templates (Jinja2)
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── task_form.html
│── static/             # CSS, JS, images
│   └── styles.css

---
## **Tech Stack**
Backend: Flask, SQLAlchemy, Flask-Login, WTForms

Frontend: Bootstrap 5, Jinja2 templates

Database: SQLite (default), PostgreSQL (production-ready)
