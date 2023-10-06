# FastAPI SQLAlchemy Auditing Demo

This repository demonstrates a FastAPI application integrated with SQLAlchemy for database operations and includes auditing functionality to store request and response details.

## Features

- **SQLAlchemy Integration**: Utilizes SQLAlchemy for database operations, providing an efficient and scalable approach to interact with the database.

- **Middleware for Auditing**: Implements FastAPI middleware to capture and store auditing information in the database for each incoming request.

## Project Structure

The project is organized into the following modules and functions:

### Modules

1. **`database.py`**: Manages the database connection and includes the SQLAlchemy logic for interacting with the database.

2. **`modules.py`**: Defines the database schema, including an example `Audit` table for storing auditing information.

### Functions

1. **`get_db`**: A FastAPI dependency that creates a new SQLAlchemy `SessionLocal` for each request and closes it once the request is completed.

2. **`db_session_middleware`**: Middleware function executed for each request, capturing details both before and after the endpoint function is executed. It includes logic to store auditing information.

3. **`store_audit`**: Function responsible for storing auditing information in the database.

### How to Run

1. Clone this repository:

   ```bash
   git clone https://github.com/dannielshalev/fastapi_alchemy_auditing_demo.git
   cd fastapi_alchemy_auditing_demo

2. create virtualenv

```
virtualenv -v python3.x venv
```

3. Install requierments.txt:

```
pip install -r requierments.txt

```

4. Run app:


```
uvicorn main:app --reload --host 0.0.0.0 --port 8000

```

### Installing and configure postgress section

#### install 

```
sudo apt install postgresql
```

#### Configure

```
# go to os default posgress user
sudo su postgres

# enter DB

```
psql

```

#### create user
create user your-user with encrypted password 'your-password';

# grant perrmisions 
grant ALL ON DATABASE postgres to your-user ;

exit

```
