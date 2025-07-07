# Expense Tracker API & UI

This project is a full-featured Expense Tracker application built with FastAPI and SQLite. It allows users to register, log in, and manage their personal expenses with category support, filtering, and a user-friendly dashboard. The backend is protected with JWT-based authentication.

> **Project idea based on:** [roadmap.sh Expense Tracker API](https://roadmap.sh/projects/expense-tracker-api)

## Features

- **User Authentication**
  - Register and log in with secure password hashing
  - JWT-based authentication for API endpoints
- **Expense Management**
  - Add, update, and delete expenses
  - Filter expenses by category and date
  - Categories include: Groceries, Leisure, Electronics, Utilities, Clothing, Health, Others
- **User Dashboard**
  - View all expenses, totals, and filter by category/date
- **User Management**
  - View and update user info
  - Change password
- **Admin Features**
  - Admin-only endpoints for managing users and expenses

## Technology Stack

- **Backend:** FastAPI
- **Database:** SQLite (via SQLAlchemy ORM)
- **Authentication:** JWT (JSON Web Token)
- **Frontend:** Jinja2 templates (for dashboard and auth pages)

## Project Structure

```
App/
  main.py           # FastAPI entry point
  db.py             # Database setup (SQLAlchemy)
  models.py         # SQLAlchemy models for Users and Expenses
  routers/          # API routers (auth, user, expenses, dashboard, admin)
  templates/        # Jinja2 HTML templates
  static/           # Static files (CSS, JS, images)
app.db              # SQLite database file
```

## Getting Started

### Prerequisites

- Python 3.8+
- (Recommended) Create and activate a virtual environment

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   uvicorn App.main:app --reload
   ```

4. **Access the app:**
   - API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Dashboard: [http://localhost:8000/dashboard](http://localhost:8000/dashboard)

## API Endpoints

- `/auth/register` - Register a new user
- `/auth/login` - User login
- `/expenses/` - CRUD operations for expenses (protected)
- `/user/` - User info and password management
- `/dashboard/` - User dashboard (HTML)

## UI/UX & Design

- The dashboard features a modern, visually appealing card-based layout.
- Each expense is displayed in a two-column row: the left side shows the title, description, and category/date; the right side shows the amount and action buttons (edit/delete), all clearly separated and aligned.
- The add button is full width and visually prominent, while all other buttons are styled for clarity and accessibility.
- The dashboard is centered on the page with a soft background, rounded corners, and subtle shadows for a clean, professional look.
- All styles are managed in the external `App/static/css/dashboard.css` file for easy customization and maintenance.
- The layout is responsive and works well on both desktop and mobile devices.

## License

This project is for educational purposes and based on the [roadmap.sh Expense Tracker API project idea](https://roadmap.sh/projects/expense-tracker-api). 