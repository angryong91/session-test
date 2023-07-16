## Project info
- python version: 3.11
- framework: fastapi
- database: sqlite, sqlalchemy, alembic

## Features
- signup
  - get email, first name, last name, privacy & policy accept
  - return verify url
- verify
  - active user
- signin
  - create session
  - return cookie
- get user info

## Hot to Run
- virtualenv venv --python=python3.11
- source venv/bin/activate
- pip3 install -r requirements.txt
- uvicorn app.main:app --port 8080
- swagger url: http://localhost:8080/Ib75lIvT7AbUrgUa/swagger#
- redoct url: http://localhost:8080/Ib75lIvT7AbUrgUa/redoc
