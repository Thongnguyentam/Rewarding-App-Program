# Fetch Loyalty & Reward RESTApi  

## Description
Our users have points in their accounts. Users only see a single balance in their account, but for reporting
purposes, we track their points per payer. A payer is the producer of the item that points were added through. For
example, a person who redeems yogurt may have points added through the payer DANNON. We track the payer
from whom points are added, as well as when the points were added, so we know which payer to bill when the user
spends their points on a reward.


## Project Structure

```
.
├── ...
├── constant/
├── database/
│   ├── models/
│   ├── query/
│   ├── ...
│   └── database.py
├── env/
├── logs/
├── middleware/
├── routers/
│   ├── __init__.py
│   └── user.py
├── schemas/
│   ├── __init__.py
│   └── ...
├── tests/
│   ├── __init__.py
│   └── conftest.py
├── utils/
├── .env
├── main.py
├── README.md
└── requirements.txt
```
- `constant`: define constants
- `database`: database config and operations. 
- `database/models`: class model orm for the database
- `database/query`: store database operations
- `env`: contains environment-related files.
- `logs`: contains csv logs files.
- `middleware`: hanle the middleware functions (write log)
- `schemas`: request, response models.
- `routers`: contains all routing in the application.
- `tests`: test module to test the API functionality of user-related API 
- `utils`: utility modules that are used across the project.
- .env: store environment variables
- main.py: entry point of my program.
- README.md: this file
- requirements.txt: lists the Python dependencies that need to be installed for the program.

## Installation
Follow these steps to install and run the project:
1. Clone the project from its repository:
```bash
git clone 
```
2. Navigate into the project directory:
```bash
cd Fetch
```
3. Create virtual environment
```bash
python -m venv env
```

4. Active virtual environment
```bash
env/Scripts/activate
```

5. Install the required Python packages.
```bash
pip install -r requirements.txt
```

6. Run the FastAPI server:
```bash
uvicorn main:app --reload
```

SQLALCHEMY_DATABASE_URL: postgreql://{user}:{pass}@{hostname}:{port}/{database_name} (Connection Chain to Postgresql Database)

## Authors
- Dylan Nguyen (Thong Nguyen)- thongnguyentam@gmail.com