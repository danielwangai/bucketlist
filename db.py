import os.path

from config import configurations #QLALCHEMY_MIGRATE_REPO
from app import db, manager
from app.models import User, Bucketlist, Task

@manager.command
def create_db():
    if os.path.exists(configurations["development"].SQLALCHEMY_MIGRATE_REPO):
        print("Database already exists.")
    else:
        db.create_all()
        print("Database successfully created.")

if __name__ == '__main__':
    manager.run()