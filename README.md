<h1 align="center">🏠 Smart PG Finder</h1><p align="center">
  <b>Reimagining the Way People Discover & Book PG Accommodations 🚀</b><br>
  <i>A full-stack web application delivering a seamless, structured, and user-centric housing experience</i>
</p><p align="center">
  <a href="https://pgbuddy-gycu.onrender.com/">
    <img src="https://img.shields.io/badge/🚀 Live Demo-Explore-green?style=for-the-badge">
  </a>
  <img src="https://img.shields.io/badge/Backend-Flask-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Database-SQLite-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/Frontend-HTML%20CSS%20JS-purple?style=for-the-badge">
</p>

🧭 Problem Statement

Finding a suitable PG (Paying Guest accommodation) is often time-consuming and inefficient due to:

- ❌ Scattered and unorganized listings
- ❌ Lack of filtering options
- ❌ No centralized booking system
- ❌ Poor user experience

This leads to decision fatigue and unreliable choices.

---

💡 Solution

Smart PG Finder addresses these challenges by providing a centralized digital platform that enables:

- Structured PG discovery
- Smart filtering based on user needs
- Seamless booking workflow
- Efficient listing management for owners

It bridges the gap between demand (users) and supply (owners) in a clean, scalable way.

---

⚡ Key Features

👤 User Panel

- 🔍 Advanced Search System
  Search PGs based on location and preferences

- 💰 Budget Filtering
  Instantly filter PGs within a specific price range

- ❤️ Wishlist Management
  Save and revisit preferred PGs

- 🏠 Detailed Listings
  View images, pricing, and property details

- ⭐ Rating & Review System
  Provide feedback and improve decision-making

- 📌 Recommendation Engine (Basic)
  Suggest PGs based on affordability and trends

- 💳 Booking + Payment Simulation
  End-to-end booking flow with UI-based payment system

---

🧑‍💼 Owner Panel

- ➕ Add PG Listings
  Upload property details with images

- ✏️ Edit Listings
  Update PG details dynamically

- 📊 Booking Management
  Track user bookings in real-time

- 🗑️ Delete Listings
  Maintain clean and updated inventory

---

🧠 System Architecture

Frontend (HTML/CSS/JS)
        ↓
Flask Backend (Routing + Logic)
        ↓
SQLite Database (Storage)
        ↓
Dynamic Rendering (Templates)

---

🛠️ Tech Stack

Layer| Technology
Frontend| HTML, CSS, JavaScript
Backend| Flask (Python)
Database| SQLite
Deployment| Render
Tools| Git, GitHub

---

📂 Project Structure

smart_pg_finder/
│
├── static/                # CSS, JavaScript, Images
│   ├── style.css
│   ├── script.js
│   └── uploads/
│
├── templates/            # HTML Templates
│   ├── index.html
│   ├── home.html
│   ├── login.html
│   ├── signup.html
│   ├── booking.html
│   ├── wishlist.html
│   ├── recommend.html
│   └── ...
│
├── app.py                # Main Flask application (routes + logic)
├── database.db           # SQLite database
├── requirements.txt      # Python dependencies
├── Procfile              # Deployment configuration (Render)
└── .gitignore            # Ignored files

---

🚀 Local Setup & Execution

git clone https://github.com/barsharajput/smart_pg_finder.git
cd smart_pg_finder
pip install -r requirements.txt
python app.py

---

☁️ Deployment Details

- 🌐 Hosted on Render
- ⚙️ Configured with Gunicorn
- 🔄 Continuous deployment via GitHub
- 📡 Publicly accessible application

---

📊 Project Highlights

- ✔ Full-stack development (Frontend + Backend + Database)
- ✔ Role-based architecture (User & Owner)
- ✔ Real-world problem solving approach
- ✔ End-to-end booking workflow
- ✔ Clean UI & functional backend integration
- ✔ Successfully deployed on cloud platform

---

🧠 Key Learnings

- Designing scalable full-stack applications
- Implementing role-based access control
- Managing relational data using SQLite
- Debugging real deployment and Git issues
- Structuring production-ready projects

---

🔮 Future Enhancements

- 🔐 Secure authentication (JWT / OAuth)
- 💳 Real payment gateway integration
- 📍 Google Maps API integration
- 📱 Fully responsive mobile UI
- 🤖 AI-powered recommendation system

---

<p align="center">
  🚀 Built with a strong focus on real-world problem solving & user experience
</p>
