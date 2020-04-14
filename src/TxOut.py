from lib.helper import little_endian_to_int
from lib.helper import int_to_little_endian
from src.Script import Script

class TxOut:
    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    def __repr__(self):
        return '{}:{}'.format(self.amount, self.script_pubkey)

    @classmethod
    def parse(cls, s):
        amount = little_endian_to_int(s.read(8))
        script_pubkey = Script.parse(s)
        '''returns a TxOut object'''
        return cls(amount, script_pubkey)
       
#트랜잭션 직렬화 코등 
    def serialize(slef):
        result = int_to_little_endian(self.amount, 8)
        result += self.script_pubkey.serialize()
        '''return the byte serialization of the transaction output'''
        return result
