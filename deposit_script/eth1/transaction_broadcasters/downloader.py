from .abstract_broadcaster import TxBroadcaster
from utils.types import (
    Transaction
)


class TxDownloader(TxBroadcaster):
    folder = r'\.'
    file_name = 'deposit_transaction.hex'

    @property
    def file_folder(self):
        return self.file_name + self.file_name

    def broadcast_tx(self, tx: Transaction) -> bool:
        with open(self.file_folder, 'w+') as f:
            f.write(self.serialize_tx(tx))
            return True
        return False
