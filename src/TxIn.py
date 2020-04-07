from lib.helper import little_endian_to_int
from lib.helper import int_to_little_endian
#from src.TxFetcher import TxFetcher
from src.Script import Script


class TxIn:
    def __init__(self, prev_tx, prev_index, script_sig=None, sequence=0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index

# TxIN 생성자 호출시 script_sig 인수의 값이 주어지지 않으면 self.script_sig를 Script()로 초기화
# Script 클래스 생성자는 그냥 빈 클래스를 반환한다.
        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig
        self.sequence = sequence

    def __repr__(self):
        return '{}:{}'.format(self.prev_tx.hex(), self.prev_index)


#Takes a byte stream and parses the tx_input at the start
    @classmethod
    def parse(cls, s):
        prev_tx = s.read(32)[::-1]
        prev_index = little_endian_to_int(s.read(4))
        script_sig = Script.parse(s)
        sequence = little_endian_to_int(s.read(4))
        '''return a TxIn object'''
        return cls(prev_tx, prev_index, script_sig, sequence)

    def serialize(self):
        result = self.prev_tx[::-1]
        result += int_to_little_endian(self.prev_index, 4)
        result += self.script_sig.serialize()
        result += int_to_little_endian(self.sequence, 4)
        '''return the byte serialization of the transaction input'''
        return result

    # 이전 트랜잭션을 가져오는 메서드
    def fetch_tx(self, testnet=False):
        return TxFetcher.fetch(self.prev_tx.hex(), testnet=testnet)

    '''Get the output value by looking up the tx hash'''
    # 이전 트랜잭션의 출력상의 금액
    def value(self, testnet=False):
        tx = self.fetch_tx(testnet=testnet)
        '''return a amount in satoshi'''
        return tx.tx_outs[self.prev_index].amount

    '''Get the ScriptPubKEy by loking up the tx hash'''
    # 잠금 스크립트
    def script_pubkey(self, testnet=False):
        tx = self.fetch_tx(testnet=testnet)
        return tx.tx_outs[self.prev_index].script_publickey

