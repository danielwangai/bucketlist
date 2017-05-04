[![Build Status](https://travis-ci.org/danielwangai/bucketlist.svg?branch=master)](https://travis-ci.org/danielwangai/bucketlist)

# Bucketlist
A flask based API to avail resources for creation of bucketlists.

## Prerequisites
The development environment uses postgres db, hence install postgres before proceeding.
    - Mac OS - `brew install postgresql`
    - linux - `sudo apt-get install postgresql postgresql-contrib`
    - windows - Download postgres [here](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads#windows)

Once installed create a database named `bucketlist`
(for linux and mac OS users)
1. type `psql` in terminal.
2. On postgres interactive interface, type `CREATE DATABASE bucketlist;`
3. Grant privileges to the user by typing `GRANT ALL ON DATABASE bucketlist to <your-postgres-username>;`
## Installation
1. Clone the project - `git clone git@github.com:danielwangai/bucketlist.git`
2. create a virtual environment using virtualenv.
3. Install the dependencies - `pip install -r requirements.txt`.
4. run the following commands to set the database ready:-
  -- `flask db init`
  -- `flask db migrate`
  -- `flask db upgrade`
The following are the API endpoints:-

| EndPoint                                  | Functionality                    |
| ------------------------------            |:-------------------------------: |
| POST /auth/login                          | Logs a user in                   |
| POST /auth/register                       | Register a new user              |
| POST /bucketlists                         | Create a new bucket list         |
| GET /bucketlists/                         | List all bucketlists for currently logged in user|
| GET /bucketlists/<id>                     | Fetches a single bucketlist      |
| PUT /bucketlists/<id>                     | Update a bucketlist              |
| DELETE /bucketlists/<id>                  | Delete a single bucket list      |
| POST /bucketlists/<id>/items/             | Create a new bucketlist item     |
| PUT /bucketlists/<id>/items/<item_id>     | Updates a bucketlist item        |
| DELETE /bucketlists/<id>/items/<item_id>  | Deletes a bucketlist item        |

## Run the server
  6. Next is to start the server with the command `python run.py`
    The server should be running on [http://127.0.0.1:5000]

# Usage
  Use Postman (a Google chrome extension for api testing).
