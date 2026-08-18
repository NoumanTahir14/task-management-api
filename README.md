# Task Management API

A clean and scalable RESTful API for managing tasks, built with **FastAPI** and **PostgreSQL**. The project provides complete CRUD functionality with environment-based configuration, database persistence, validation, and parameterized SQL queries.

## Features

* RESTful task management API
* Create, read, update, and delete tasks
* PostgreSQL database integration
* Parameterized SQL queries
* Environment-based configuration
* Automatic database table initialization
* Initial task seeding
* Request validation
* Health-check endpoint
* Interactive API documentation with Swagger UI

## Tech Stack

* **Python 3.10+**
* **FastAPI**
* **PostgreSQL**
* **Psycopg**
* **Uvicorn**
* **Pydantic**
* **python-dotenv**

## Project Structure

```text
task-management-api/
│
├── app.py
├── schema.sql
├── requirements.txt
├── .env.example
├── .gitignore
├── test_commands.txt
└── README.md
```

## Getting Started

### Prerequisites

Make sure you have the following installed:

* Python 3.10 or higher
* PostgreSQL

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/task-management-api.git
cd task-management-api
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a PostgreSQL database:

```sql
CREATE DATABASE tasks;
```

Copy `.env.example` to `.env`:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/tasks
```

Replace `your_password` with your PostgreSQL password.

> Never commit your `.env` file or database credentials to GitHub.

### 5. Start the API

```bash
uvicorn app:app --reload --port 3000
```

The API will be available at:

```text
http://localhost:3000
```

Interactive Swagger documentation:

```text
http://localhost:3000/docs
```

## API Endpoints

| Method | Endpoint      | Description                   |
| ------ | ------------- | ----------------------------- |
| GET    | `/tasks`      | Retrieve all tasks            |
| GET    | `/tasks/{id}` | Retrieve a specific task      |
| POST   | `/tasks`      | Create a new task             |
| PUT    | `/tasks/{id}` | Update an existing task       |
| DELETE | `/tasks/{id}` | Delete a task                 |
| GET    | `/health`     | Check API and database status |

## Example Request

### Create a Task

```http
POST /tasks
Content-Type: application/json
```

```json
{
  "title": "Complete backend project",
  "done": false
}
```

### Example Response

```json
{
  "id": 1,
  "title": "Complete backend project",
  "done": false
}
```

## Database

The application uses PostgreSQL to persist task data.

The `tasks` table contains:

| Column  | Type    | Description            |
| ------- | ------- | ---------------------- |
| `id`    | SERIAL  | Unique task identifier |
| `title` | TEXT    | Task title             |
| `done`  | BOOLEAN | Task completion status |

The database table is automatically created when the application starts if it does not already exist.

## Health Check

The `/health` endpoint verifies that the API can successfully communicate with PostgreSQL.

```http
GET /health
```

Example:

```json
{
  "status": "ok",
  "db": "ok"
}
```

## Security

The project follows several basic backend security practices:

* Database credentials are stored in environment variables.
* `.env` is excluded from Git.
* SQL queries use parameters instead of string concatenation.
* Request data is validated before database operations.
* Database errors and invalid resource IDs are handled through appropriate HTTP responses.

## Development

Run the application in development mode:

```bash
uvicorn app:app --reload --port 3000
```

After making changes, the development server automatically reloads.

## Future Improvements

Potential improvements include:

* Authentication and authorization
* User-specific task management
* Pagination and filtering
* Task categories and priorities
* Search functionality
* Automated unit and integration tests
* Database migrations with Alembic
* Production deployment configuration
* API rate limiting
* Structured application logging

## Author

**Nouman Tahir**

Backend Developer | Python | FastAPI | PostgreSQL
