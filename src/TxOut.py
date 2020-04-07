from lib.helper import little_endian_to_int
from lib.helper import int_to_little_endian
from src.Script import Script

class TxOut:
    def __init__(self, amount, script_publickey):
        self.amount = amount
        self.script_publickey = script_publickey

    def __repr__(self):
        return '{}:{}'.format(self.amount, self.script_publickey)

    @classmethod
    def parse(cls, s):
        amount = little_endian_to_int(s.read(8))
        script_publickey = Script.parse(s)
        '''returns a TxOut object'''
        return cls(amount, script_publickey)
       
#트랜잭션 직렬화 코등 
    def serialize(slef):
        result = int_to_little_endian(self.amount, 8)
        result += self.script_publickey.serialize()
        '''return the byte serialization of the transaction output'''
        return result
