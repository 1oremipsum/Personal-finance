from sqlmodel import create_engine

# creating the database connection

sqlite_file_name = "personal_finance.db"
sql_url = f"sqlite:///database/{sqlite_file_name}"
engine = create_engine(sql_url, echo=True, future=True)