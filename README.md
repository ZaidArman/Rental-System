Car Rental System - Project Documentation
📁 Project Repositories
- 🔧 Backend (Django): https://github.com/ZaidArman/Rental-System
- 🌐 Frontend (ReactJS): https://github.com/ZaidArman/Car-Rental-ReatJS_Node
🛠 Backend Setup (Django)
✅ Prerequisites
• Python 3.8+
• pip (Python package manager)
• Virtual environment (recommended)
📦 Installation Steps

1. Clone the repository
```bash
git clone https://github.com/ZaidArman/Rental-System.git
cd Rental-System
```
2. (Optional) Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Apply database migrations
```bash
python manage.py migrate
```
5. (Optional) Create a superuser
```bash
python manage.py createsuperuser
```
6. Run the development server
```bash
python manage.py runserver
```

🔗 API Base URL: http://127.0.0.1:8000/
💻 Frontend Setup (ReactJS + Node)
✅ Prerequisites
• Node.js (v14+)
• npm or yarn
📦 Installation Steps

1. Clone the frontend repo
```bash
git clone https://github.com/ZaidArman/Car-Rental-ReatJS_Node.git
cd Car-Rental-ReatJS_Node
```
2. Install dependencies
```bash
npm install
```
3. Start the React development server
```bash
npm run dev
```

🌐 Frontend runs at: http://localhost:3000/
🔗 Integration Guide

1. Ensure the Django backend is running at http://127.0.0.1:8000/.
2. In the frontend React code (inside Car-Rental-ReatJS_Node), check where the API URL is set and update it if needed:
   Example:
```js
const API_BASE_URL = 'http://127.0.0.1:8000/api/';
```
3. Once both servers are running, your frontend will communicate with the backend APIs smoothly.

📂 Project Structure

Rental-System/
├── manage.py
├── rental/
├── templates/
├── static/
├── db.sqlite3
└── requirements.txt

Car-Rental-ReatJS_Node/
├── backend(NodeJS)
├── public/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   └── App.js
├── .env
└── package.json

📌 Features

- 🔐 User authentication and registration
- 🚘 Car listings and filtering
- 📅 Booking system with availability
- 👤 Profile management
- 📊 Admin panel for car and user management (Django admin)

📧 Contact
Zaid Ullah
📬 
🌐 https://github.com/ZaidArman
📝 License
This project is licensed under the MIT License.
