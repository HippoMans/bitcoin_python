from lib.helper import little_endian_to_int
from src.Tx import Tx

# TxFetcher 클래스의 fetch 메서드가 원하는 트랜잭션에서 필요한 출력만을 반환하지 않고 왜 전체 트랜잭션을 반환할까?
# 이유는 네트워크를 통해서 들어오는 제 3자의 정보를 검증하기 위해서이다.
# 전체 트랜잭션을 반호나하면 수신자는 그 트랜잭션의 해시값(트랜잭션 내용에 대한 hash256 해시값을 계산) 검증해서 원하는 트랜잭션을 확인
# 특정 출력만을 반환하면 제 3자 수신자를 검증할 방법이 없다. 
class TxFetcher:
    cache = {}

    @classmethod
    def get_url(cls, testnet=False):
        if testnet:
            return 'http://testnet.programmingbitcoin.com'
        else:
            return 'http://mainnet.programmingbitcoin.com'

    @classmethod
    def fetch(cls, tx_id, testnet=False, fresh=False):
        if fresh or (tx_id not in cls.cache):
            url = '{}/tx/{}.hex'.format(cls.get_url(testnet), tx_id)
            response = requests.get(url)
            try:
                raw = bytes.fromhex(response.text.strip())
            except ValueError:
                raise ValueError('unexpected response: {}'.format(response.text))
            if raw[4] == 0:
                raw = raw[:4] + raw[6:]
                tx = Tx.parse(BytesIO(raw), testnet=testnet)
                tx.locktime = little_endian_to_int(raw[-4:])
            else:
                tx = Tx.parse(BytesIO(raw), testnet=testnet)

# 찾고자 하는 트랜잭션 해시값(ID)이 맞는지 확인하고 맞지 않으면 오류를 발생
            if tx.id() != tx_id:
                raise ValueError('not the same id : {} vs {}'.format(tx.id(), tx_id))

            cls.cache[tx_id] = tx
        cls.cache[tx_id].testnet = testnet
        return cls.cache[tx_id]
