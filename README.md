# 📝 Todo List API

This is a **Todo List API** built with **FastAPI**, designed to help users manage tasks by creating, updating, deleting, and searching todos. It follows RESTful principles and uses SQLite for testing and Supabase PostgreSQL for production.

📌 [Project Roadmap Source](https://roadmap.sh/projects/todo-list-api)

---

## 🚀 Features

- ✅ User registration & login with JWT authentication
- 🧾 Create, read, update, and delete todo items
- 🔍 Search todos by keyword
- 📄 Pagination support
- 🧪 Unit & Integration tests using `pytest` and SQLite
- 🧰 Production-ready with Supabase PostgreSQL

---

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Auth**: JWT (JSON Web Tokens)
- **Database**: SQLite (testing), Supabase PostgreSQL (production)
- **Testing**: Pytest, httpx, pytest-asyncio
- **Deployment**: None

---

## 📦 Installation

1. Clone the repository

```bash
git clone https://github.com/your-username/todo-list-api.git
cd todo-list-api
```

2. Create and activate a Virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
DATABASE_URL=sqlite:///./test.db  # or your Supabase URL
SECRET_KEY=your-secret
ALGORITHM=your-algorithm-key


5. Running Tests
``` bash
pytest
```


This project is licensed under the MIT License.
