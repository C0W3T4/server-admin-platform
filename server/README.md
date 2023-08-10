# Server Admin Platform Server API

## 🚀 How to run

- Clone the repository into a **linux server** because it requires **Crontab service** installed
- Activate virtual environment with `source .venv/Scripts/activate`
- Install the dependencies with `pip install -r requirements.txt`
- Create a **PostgreSQL** instance and database
- Create a `.env` file and add the variables as shown in the `env.example.txt` file
- Run migrations with `alembic upgrade <revision>`
- Start the development server with `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
- Create a **linux server** to use as **Ansible Tower**
