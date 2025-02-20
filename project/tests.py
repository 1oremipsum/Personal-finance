from views import *
from models import *

class AccountTest():
    def __init__(self):
        self.result_view = AccountView(DBManager(engine))

    def create(self):
        account = Account(balance=0.0, bank=Banks.PAYPAL)
        return self.result_view.create_account(account)

    def get_all(self):
        return self.result_view.get_all_accounts()

    def get_many_by(self, condition):
        return self.result_view.get_many_accounts_by(Account.bank == condition)

    def get_by(self, condition):
        return self.result_view.get_account_by(Account.bank == condition)

    def disable_by_id(self, id):
        return self.account_view.deactivate_account_by_id(id)
    
    def transfer_balance(self, sender_id, recipient_id, value):
        return self.result_view.transfer_balance(sender_id, recipient_id, value)


success_result = AccountTest().transfer_balance(1, 2, 50)

if success_result:
    print(success_result)
    print("Successful action.")
else:
    print("Unsuccessful action.")
