from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
import datetime

class Banks(Enum):
    NUBANK = "Nubank"
    SANTANDER = "Santander"
    ITAU = "Itaú"
    BRADESCO = "Bradesco"
    CAIXA = "Caixa"
    BANCO_DO_BRASIL = "Banco do Brasil"
    INTER = "Inter"
    C6_BANK = "C6 Bank"
    PICPAY = "PicPay"
    PAYPAL = "PAYPAL"


class Status(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"


class MovementType(Enum):
    WITHDRAWAL = "Withdrawal"
    TRANSFER = "Transfer"
    DEPOSIT = "Deposit"


class Account(SQLModel, table=True):
    id: int = Field(primary_key=True)
    balance: float = Field(default=0.0, ge=0.0)
    bank: Banks = Field(nullable=False)
    status: Status = Field(default=Status.ACTIVE)


class Movement(SQLModel, table=True):
    id: int = Field(primary_key=True)
    origin_account_id: int = Field(foreign_key="account.id")
    target_account_id: int = Field(foreign_key="account.id")
    origin_account: Account = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "[Movement.origin_account_id]"
        }
    )
    target_account: Account = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "[Movement.target_account_id]"
        }
    )
    account: Account = Relationship()
    movement_type: MovementType = Field(default=MovementType.DEPOSIT)
    amount: float = Field(nullable=False)
    date: datetime.datetime = Field(default_factory=datetime.datetime.now, nullable=False)
    description: str = Field(nullable=True)
