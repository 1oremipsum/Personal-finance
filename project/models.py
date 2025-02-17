from sqlmodel import SQLModel, Field
from enum import Enum

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

class Account(SQLModel, table=True):
    id: int = Field(primary_key=True)
    balance: float
    bank: Banks = Field(nullable=False)
    status: Status = Field(default=Status.ACTIVE)
