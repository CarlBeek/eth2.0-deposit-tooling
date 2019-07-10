import abc
from utils.typing import (
    Gwei,
    Nonce,
    Transaction,
)


class Account(metaclass=abc.ABCMeta):
    online = False

    @abc.abstractproperty
    def balance(self) -> Gwei:
        pass

    @abc.abstractproperty
    def nonce(self, increment: bool=False) -> Nonce:
        pass

    @abc.abstractmethod
    def sign_tx(self, transaction: Transaction) -> Transaction:
        pass
