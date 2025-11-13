# ✔️ To-Do App (Tkinter + PostgreSQL)

A desktop To-Do application built with **Python**, featuring a graphical user interface using **Tkinter** and persistent storage powered by **PostgreSQL**.  
The project demonstrates clean separation between GUI, business logic, and database operations.

---

## 🔧 Features

- Simple and intuitive graphical interface (Tkinter)
- PostgreSQL-backed persistence layer
- Add, complete, and delete tasks
- Modular architecture (GUI, model, DB connections)
- Automatic database and table initialization

---

## 📦 Requirements

- Python **3.8+**
- PostgreSQL installed and running locally

---

## 🛠 Installation

1. **Clone the repository**

```bash
git clone https://github.com/YOUR-USER/todo_app.git
cd todo_app
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure the database connection**

Copy the example configuration file:

```bash
cp config/config_example.json config/config.json
```

Edit `config/config.json` with your PostgreSQL credentials:

```json
{
  "DB_NAME": "todo_app_db",
  "DB_USER": "your_user",
  "DB_PASSWORD": "your_password",
  "DB_HOST": "localhost",
  "DB_PORT": 5432
}
```

4. (Optional) **Create the PostgreSQL database manually**  
If you skip this step, the initialization script will handle it for you.

---

## 🗄️ Database Initialization

Before running the GUI for the first time, initialize the database and required tables:

```bash
python __init__.py
```

This script will:

- Check if the database exists (and create it if missing)
- Create the `tasks` table if it does not exist

---

## ▶️ Running the Application

```bash
python main.py
```

The application will connect to your PostgreSQL instance and launch the Tkinter window with your To-Do list.

---

## 📁 Project Structure

```
todo_app/
│
├── main.py                   # Application entry point
├── __init__.py               # DB + table initialization script
├── requirements.txt
├── config/
│   ├── config.json           # Database connection configuration
│   └── config_example.json   # Example config
├── db/
│   └── connection.py         # PostgreSQL connection logic
├── models/
│   └── task.py               # Task model
├── gui/
│   └── app_window.py         # Tkinter GUI implementation
```

---

## 📘 Notes

- Tkinter is used for the GUI layer.
- PostgreSQL is used instead of SQLite to simulate a real production-like environment.
- This app can be packaged into an executable using *PyInstaller* for distribution.

---

## 📄 License

This project is open-source.  
Feel free to modify or use it according to your needs.
