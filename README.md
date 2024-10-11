# Fetch Loyalty & Reward RESTApis

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
git clone https://github.com/Thongnguyentam/Rewarding-App-Program.git
```
2. Navigate into the project directory:
```bash
cd Rewarding-App-Program
```

3. Run the application using Docker
```bash
docker-compose up --build
```
4. Log in to PgAdmin at `http://localhost:5050`
    + Username: admin@admin.com
    + Password: root

5. Connect to Postgres database
    + Find the `CONTAINER ID` with the IMAGE `postgres`:
        ```bash
        docker container ls
        ```
    + Find IP address of the database server:
        ```bash
        docker inspect <CONTAINER ID>
        ```
    + In General tab of pgAdmin, set the server name
    + In Connection tab:
        + Hostname/ IP address: found in the previous step
        + Port: 5432
        + Maintainance database: postgres
        + Username: postgres
        + Password: 123456

6. Create the first user (**required**)
    + Call the API to create your user (*NOTE*: For demonstration purpose, just use this endpoint once.)
    + See below

## Endpoints (using port 8000)

### Add user (use one time ONLY)
`POST` `http://localhost:8000/new-user`

Example request:
```
{
    "username": "user"
}
```

Example response:
```
{
    "created_at": "2024-10-11T03:41:50.689551",
    "updated_at": "2024-10-11T03:41:50.689551",
    "balance": 0,
    "username": "user",
    "id": 1
}
```
*NOTE*: After creating your first user, you will use this account for all future point-related operations (e.g., adding and spending points).
### Add Points
`POST` `http://localhost:8000/add`

```
BODY Content-Type: application/json

Key | Validation Rules

payer | string, required
points | integer, required
timestamp | Iso-8601 format, required 
```
Example request:
```
{
    "payer" : "DANNON",
    "points" : 5000,
    "timestamp" : "2020-11-02T14:00:00Z"
}
```

Example response:
```
{
    "detail": "Successfully added points"
}
```

### Spend Points (The user will spend the oldest points they get from specific payers)
`POST` `http://localhost:8000/spend`
```
BODY Content-Type: application/json

Key | Validation Rules

points | integer, required
```
Example request:
```
{
    "points" : 13500
}
```

Example response:
```
[
    {
        "payer": "DANNON",
        "points": -12000
    },
    {
        "payer": "UNI",
        "points": -1500
    }
]
```
### Get Point Balance
`GET` `http://localhost:8000/balance`

Example response:
```
{
    "DANNON": 0,
    "UNI": 500
}
```

*NOTE*: If user spends more points than they currently have, they will get an error
```
{
    "detail": "You don't have enough points"
}
```

## Author(s)
- Dylan Nguyen (Thong Nguyen)- thongnguyentam@gmail.com