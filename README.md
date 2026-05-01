# Assignment Tracker

## Purpose
The Assignment Tracker is a full-stack web application designed to help students and professionals manage their tasks, deadlines, and study sessions effectively. It provides a personalized dashboard where users can create, update, and track their assignments. Additionally, it features a built-in study timer that allows users to log the time they spend working on specific tasks, promoting better time management and productivity. The app ensures privacy and security by offering a robust user authentication system, meaning each user only sees their own tasks.

## How It's Made
The application follows a traditional client-server architecture:

1. **Backend Logic & Routing:** The core of the application is built using **Flask**, a lightweight Python web framework. The `app.py` file handles all HTTP requests (GET, POST), manages user sessions, and defines the application's routes (e.g., `/login`, `/register`, `/`, `/timer`).
2. **Database Integration:** Data persistence is managed via **SQLite**. The app interacts directly with a local `database.db` file using Python's built-in `sqlite3` library. The schema consists of two main tables: `users` (for authentication data) and `assignments` (for task details linked to specific users via foreign keys).
3. **User Authentication:** Security is prioritized using the `werkzeug.security` library. Passwords are never stored in plain text; instead, they are hashed using `generate_password_hash` upon registration and verified using `check_password_hash` during login. User sessions are securely managed using Flask's `session` object.
4. **Frontend Rendering:** The user interface is generated server-side using **Jinja2** templates. Flask passes data from the backend to HTML templates (like `index.html`, `login.html`, `timer.html`), which then render the dynamic content for the user. Form submissions are handled via POST requests back to the server.

## Tech Stack & Technologies Used

- **Backend:** 
  - **Python 3:** The core programming language.
  - **Flask:** The web framework used for routing and handling requests.
  - **Werkzeug:** A comprehensive WSGI web application library (used specifically for secure password hashing).
- **Database:**
  - **SQLite:** A C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.
- **Frontend:**
  - **HTML5:** For the structure of the web pages.
  - **CSS:** For styling and visual presentation (within the templates).
  - **Jinja2:** The templating engine for Python used to generate dynamic HTML pages.

## Getting Started

1. Clone the repository or download the project files.
2. Ensure you have Python installed.
3. Install the required dependencies (typically `flask` and `werkzeug`, which comes with Flask).
   ```bash
   pip install Flask
   ```
4. Initialize the database by running the setup script (if applicable, e.g., `python init_db.py`).
5. Run the application:
   ```bash
   python assignment_tracker/app.py
   ```
6. Open your web browser and navigate to `http://127.0.0.1:5000` to start using the Assignment Tracker.
