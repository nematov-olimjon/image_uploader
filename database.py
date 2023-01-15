from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ

db_admin = environ.get("MYSQL_ADMIN")
db_password = environ.get("MYSQL_PASSWORD")
db_url = environ.get("MYSQL_ADDRESS")
db_table = environ.get("MYSQL_TABLE")

# Create a sqlite engine instance
engine = create_engine(f"mysql+pymysql://{db_admin}:{db_password}@{db_url}/{db_table}")

# Create a DeclarativeMeta instance
Base = declarative_base()

# Create SessionLocal class from sessionmaker factory
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

