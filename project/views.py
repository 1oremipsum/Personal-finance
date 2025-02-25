from models import Account, Movement, Status
from settings import engine
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import SQLModel
from typing import Type, Union

class DBManager:
    def __init__(self, engine):
        self.engine = engine

    def create_object(self, obj: Union[Account, Movement, Type[SQLModel]]) -> bool:
        try:
            with Session(self.engine) as session:
                session.add(obj)
                session.commit()
                return True
        except SQLAlchemyError as e:
            print(f"Error creating object: {e}")
            return False
        
    def update_object(self, obj: Union[Account, Movement, Type[SQLModel]]) -> bool:
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

    def select_all_objects(self, obj: Union[Account, Movement, type[SQLModel]]):
        try:
            with Session(self.engine) as session:
                statement = select(obj)
                result = session.exec(statement).all()
            return result
        except SQLAlchemyError as e:
            print(f"Error selecting objects: {e}")
            return None

    def select_one_object_or_more_by(self, 
        obj: Union[Account, Movement, type[SQLModel]], 
        condition: Union[Account, Movement, type[SQLModel]],
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
        return self.db_manager.select_one_object_or_more_by(Account, condition)

    def get_account_by(self, condition):
        return self.db_manager.select_one_object_or_more_by(Account, condition, True)
    
    def deactivate_account_by_id(self, id):
        account = self.get_account_by(Account.id==id)
        if account[0].balance > 0:
            raise ValueError("The account cannot be deactivated as it still has a balance")
        account[0].status = Status.INACTIVE
        return self.db_manager.update_object(account[0])
    
    def transfer_balance(self, sender_id, recipient_id, value):
        sender = self.get_account_by(Account.id == sender_id)
        if sender.status == Status.INACTIVE:
            raise ValueError("The sender account is inactive")
        
        recipient = self.get_account_by(Account.id == recipient_id)
        if recipient.status == Status.INACTIVE:
            raise ValueError("The recipient account is inactive")
        elif sender.id == recipient.id:
            raise ValueError("The sender and recipient are the same account")
        elif sender.balance < value:
            raise ValueError("The sender does not have enough balance to perform the transfer")
            
        sender.balance -= value
        recipient.balance += value
        return self.db_manager.update_object(sender) and self.db_manager.update_object(recipient)
