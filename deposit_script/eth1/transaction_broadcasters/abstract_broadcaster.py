import abc
from utils.types import (
    SerializedTransaction,
    Transaction,
)


class TxBroadcaster(metaclass=abc.ABCMeta):
    @staticmethod
    def serialize_tx(tx: Transaction) -> SerializedTransaction:
        # TODO: Replace with actual RLP encoding mechainism
        return str(tx).encode('utf-8')

    @abc.abstractmethod
    def broadcast_tx(self, tx: Transaction) -> bool:
        pass
