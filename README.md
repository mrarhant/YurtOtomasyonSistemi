# 🏢 Dormitory Management System

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Django](https://img.shields.io/badge/Django-5.x-green?style=flat&logo=django)
![Frontend](https://img.shields.io/badge/HTML5%20%26%20CSS3-Modern-orange)
![Status](https://img.shields.io/badge/Status-MVP%20Completed-brightgreen)

A comprehensive **Full Stack Web Application** designed to digitize and automate dormitory operations. This system bridges the gap between dormitory management and students, handling payments, permission requests, and administrative tasks in a seamless interface.

---

## 🚀 Key Features

### 👨‍🎓 For Students
* **Modern Dashboard:** A responsive interface showing current debt status, payment deadlines, and recent activities.
* **Online Payment Simulation:** Secure-feeling credit card modal to pay monthly dormitory fees instantly (simulated).
* **Permission System:** Digital leave requests (Evci İzni). Track status as *Pending*, *Approved*, or *Rejected*.
* **History Tracking:** View detailed logs of past payments and permission requests.

### 👮‍♂️ For Administrators (The Boss Panel)
* **Analytics Dashboard:** Real-time statistics on Total Income, Occupancy, Pending Requests, and Unpaid Invoices.
* **Student CRM:** Advanced search (Name/Room No), add/remove students, and view detailed student profiles.
* **Automated Invoicing ("Magic Button"):** A one-click feature to generate monthly debts for all active students instantly.
* **Permission Moderation:** Approve or reject leave requests directly from the dashboard with visual status indicators.
* **Debt Tracking:** Visual warnings (Red Badges) for students with outstanding debts.

---

## 🛠️ Tech Stack

* **Backend:** Python, Django Framework
* **Frontend:** HTML5, CSS3, JavaScript (Vanilla), Fetch API
* **Database:** SQLite (Development)
* **Architecture:** MVT (Model-View-Template) & REST API

---

## 💻 Installation & Setup

If you want to run this project locally:

1. **Clone the repository**
   ```bash
   git clone [https://github.com/mrarhant/YurtOtomasyonSistemi.git](https://github.com/mrarhant/YurtOtomasyonSistemi.git)
   cd YurtOtomasyonSistemi
2.Install dependencies
```bash
pip install -r requirements.txt
```
3.Apply database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
4.Create an admin user
```bash
python manage.py createsuperuser
```
5.Run the server
```bash
python manage.py runserver
```
---

## 🧪 Usage Guide
Log in as Admin
Go to /patron/ or log in with your superuser credentials.

Use the "Manage Students" tab to add new students.

Use the "Distribute Invoices" button to generate debts for the current month.

Log in as Student
Use the credentials created by the Admin.

Check your debt on the dashboard.
Click "Pay Debt" to simulate a payment transaction.
Submit a permission request and wait for admin approval.

---
## 👤 Author
Arhan Topal

Mathematics Engineering Student at Istanbul Technical University (ITU).

Full Stack Development Enthusiast.

This project was built for educational purposes to demonstrate Full Stack capabilities with Django.
