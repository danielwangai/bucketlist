from app import db, manager
from app.models import User, Bucketlist, Task

if __name__ == '__main__':
    manager.run()