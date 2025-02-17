import os
from sqlmodel import SQLModel
from settings import engine
from models import Account

def create_tables():
    # Create the tables in the database
    if not os.path.exists("database"):
        os.makedirs("database")

    SQLModel.metadata.create_all(engine)

def main():
    create_tables()

if __name__ == "__main__":
    main()
