import rlp
from typing import List
from utils.typing import (
    Transaction,
)
from utils.constants import TX_BROADCASTING_URLS


def save_tx_to_disk(tx: Transaction, location: str='./transaction.tx') -> bool:
    with open(location, 'w+') as f:
        f.write(rlp.encode(tx))
        return True
    return False


def get_urls(tx: Transaction) -> List[str]:
    encoded_tx = rlp.encode(tx)
    return list(map(lambda x: x % encoded_tx, TX_BROADCASTING_URLS))
