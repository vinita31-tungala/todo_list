📝 To-Do List Web Application

A full-featured **To-Do List Web App** built using **Python Flask**, **SQLite**, and **HTML/CSS/JS** that allows users to register, log in, and manage their tasks efficiently. Users can add, edit, complete, delete, and reorder tasks with a clean, user-friendly interface.

 🚀 Features

- ✅ **User Registration & Login**
- 📌 **Add, Edit, Complete, and Delete Tasks**
- 🔍 **Task Filtering**: View tasks by `Pending`, `Completed`, `Deleted`, or `All`
- 🕑 **Set Deadlines** for each task
- 🔁 **Drag-and-Drop** task reordering
- 🎨 **Responsive UI** with custom background styling
- 🔐 **Session Management** to keep users logged in securely

🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python (Flask)
- **Database**: SQLite
- **Libraries**: jQuery (for drag-and-drop & AJAX)

📂 Project Structure

todo_app/
│
├── static/
│ ├── style.css # CSS styling
│ └── OIP.webp # Background image
│
├── templates/
│ ├── index.html # Main task dashboard
│ ├── login.html # Login page
│ └── register.html # Registration page
│
├── todo.db # SQLite database (auto-created)
├── app.py # Flask application
└── README.md # Project README

🔧 Setup Instructions

1. **Clone the repository:**

bash
git clone https://github.com/your-username/todo-flask-app.git
cd todo-flask-app
Create a virtual environment and install dependencies:

bash
python -m venv venv
source venv/bin/activate    # For Windows: venv\Scripts\activate
pip install Flask
Run the application:
bash
python app.py
Open in your browser:
http://127.0.0.1:5000/
