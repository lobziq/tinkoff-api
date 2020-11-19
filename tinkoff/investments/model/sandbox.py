from dataclasses import dataclass
from decimal import Decimal

from tinkoff.investments.model.base import BaseModel, Currency, FigiName
from tinkoff.investments.model.user.accounts import (
    BrokerAccountID,
    BrokerAccountType,
)


@dataclass
class SandboxAccount(BaseModel):
    brokerAccountType: BrokerAccountType
    brokerAccountId: BrokerAccountID


@dataclass
class SandboxAccountRegisterRequest(BaseModel):
    brokerAccountType: BrokerAccountType


@dataclass
class SandboxSetCurrencyBalanceRequest(BaseModel):
    currency: Currency
    balance: Decimal


@dataclass
class SandboxSetPositionBalanceRequest(BaseModel):
    figi: FigiName
    balance: Decimal


__all__ = [
    'SandboxAccount',
    'SandboxAccountRegisterRequest',
    'SandboxSetCurrencyBalanceRequest',
    'SandboxSetPositionBalanceRequest',
]
