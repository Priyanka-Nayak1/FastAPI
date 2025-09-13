# 🚀 FastAPI Employee Management API

This is a **FastAPI-based REST API** for managing employees with **authentication (Admin)**.  
It uses **MongoDB** as the database, **JWT tokens** for authentication, and **Motor** for async DB operations.  

---

## ✨ Features
- 🔑 User registration & login with JWT authentication
- 📂 CRUD operations on employees
- 🔒 Protected routes for admin-only operations
    1. To Check it after running the file simply register yourself.
    2. Then on the top of fastapi swagger page there is a lock icon.
    3. Click that lock icon and provide your username and password and click on authorize.
    4. Now you can do all the authorized operations like create, update, delete.
- 🛠️ Employee self-service (view own Profile)

---

## 📦 Tech Stack
- [FastAPI](https://fastapi.tiangolo.com/) – Web framework
- [Uvicorn](https://www.uvicorn.org/) – ASGI server
- [MongoDB](https://www.mongodb.com/) – Database
- [Motor](https://motor.readthedocs.io/) – Async MongoDB driver
- [Python-JOSE](https://python-jose.readthedocs.io/) – JWT handling
- [Passlib](https://passlib.readthedocs.io/) – Password hashing

---

## ⚙️ Installation & Setup

### 
1️⃣ Clone the repository
git clone https://github.com/<your-username>/FastAPI.git
cd FastAPI

2️⃣ Create a virtual environment
python -m venv venv
# activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the app
uvicorn main:app --reload
