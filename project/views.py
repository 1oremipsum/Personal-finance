from models import Account, Banks, Status
from settings import engine
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import SQLModel
from typing import Type, Union


class DBManager:
    def __init__(self, engine):
        self.engine = engine

    def create_object(self, obj: Union[Account, Type[SQLModel]]) -> bool:
        try:
            with Session(self.engine) as session:
                session.add(obj)
                session.commit()
                return True
        except SQLAlchemyError as e:
            print(f"Error creating object: {e}")
            return False
        
    def update_object(self, obj: Union[Account, Type[SQLModel]]) -> bool:
        try:
            with Session(self.engine) as session:
                existing_obj = session.get(type(obj), obj.id)
                if not existing_obj:
                    print(f"Erro: Objeto do tipo {type(obj).__name__} com ID {obj.id} não encontrado.")
                    return False

                for key, value in obj.model_dump().items():
                    setattr(existing_obj, key, value)

                session.commit()
                return True
        except SQLAlchemyError as e:
            print(f"Error updating object: {e}")
            return False

    def select_all_objects(self, obj: Union[Account, type[SQLModel]]):
        try:
            with Session(self.engine) as session:
                statement = select(obj)
                result = session.exec(statement).all()
            return result
        except SQLAlchemyError as e:
            print(f"Error selecting objects: {e}")
            return None

    def select_one_object_or_more_by(self, 
        obj: Union[Account, type[SQLModel]], 
        condition: Union[Account, type[SQLModel]],
        fetch_one=False):

        try:
            with Session(self.engine) as session:
                statement = select(obj).where(condition)
                if fetch_one:
                    result = session.exec(statement).first()
                else:
                    result = session.exec(statement).all()
                return result
        except SQLAlchemyError as e:
            print(f"Error selecting object(s): {e}")
            return None


class AccountView:
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    def create_account(self, account: Account) -> bool:
        return self.db_manager.create_object(account)
    
    def get_all_accounts(self):
        return self.db_manager.select_all_objects(Account)
    
    def get_accounts_by(self, condition):
        return self.db_manager.select_one_object_or_more_by(Account, condition, True)

    def get_account_by(self, condition):
        return self.db_manager.select_one_object_or_more_by(Account, condition)
    
    def deactivate_account_by_id(self, id):
        account = self.get_account_by(Account.id==id)
        if account[0].balance > 0:
            raise ValueError("The account cannot be deactivated as it still has a balance")
        account[0].status = Status.INACTIVE
        return self.db_manager.update_object(account[0])


db_manager = DBManager(engine)
account_view = AccountView(db_manager)

#Creating account
# account = Account(balance=0.0, bank=Banks.PAYPAL)
# success_result = account_view.create_account(account)

# Return all results
# success_result = account_view.get_all_accounts()

# Return results for a condition
# success_result = account_view.get_accounts_by(Account.bank == "PAYPAL")

# Selecting and Updating by id
# success_result = account_view.deactivate_account_by_id(3)

# if success_result:
#     print(success_result)
#     print("Successful action.")
# else:
#     print("Unsuccessful action.")