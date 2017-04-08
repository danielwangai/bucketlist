import os


basedir = os.path.abspath(os.path.dirname(__name__))

# path to the database file
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'bucketlist.db')
# the directory storing migration files
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')