import os
import sys

path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(os.path.abspath(path))

from unittest import TestCase
from lib.helper import run
from lib.helper import hash256
from lib.byte_helper import bit_field_to_bytes
from src.GetDataMessage import GetDataMessage

TX_DATA_TYPE = 1
BLOCK_DATA_TYPE = 2
FILTERED_BLOCK_DATA_TYPE = 3
COMPACT_BLOCK_DATA_TYPE = 4

NETWORK_MAGIC = b'\xf9\xbe\xb4\xd9'
TESTNET_NETWORK_MAGIC = b'\x0b\x11\x09\x07'



class GetDataMessageTest(TestCase):
    def Test_serialize(self):
        hex_msg = '020300000030eb2540c41025690160a1014c577061596e32e426b712c7ca00000000000000030000001049847939585b0652fba793661c361223446b6fc41089b8be00000000000000'
        get_data1 = GetDataMessage()
        print("get_data1 : ", get_data1.command)
        print("data1 : ", get_data1.data)
        block1 = bytes.fromhex('00000000000000cac712b726e4326e596170574c01a16001692510c44025eb30')
        print("block1 : ", block1.hex())
        get_data1.add_data(FILTERED_BLOCK_DATA_TYPE, block1)
        result = get_data1.serialize()
        print("get_data1.serialize(3, block1) : ", result.hex())

        print()
        get_data2 = GetDataMessage()
        print("get_data2 : ", get_data2.command)
        print("data2 : ", get_data2.data)
        block2 = bytes.fromhex('00000000000000beb88910c46f6b442312361c6693a7fb52065b583979844910')
        print("block2 : ", block2.hex())
        get_data2.add_data(FILTERED_BLOCK_DATA_TYPE, block2)
        result = get_data2.serialize()
        print("get_data2.serialize(3, block2) : ", result.hex())

        print()
        get_data3 = GetDataMessage()
        print("get_data3 : ", get_data3.command)
        get_data3.add_data(FILTERED_BLOCK_DATA_TYPE, block1)
        get_data3.add_data(FILTERED_BLOCK_DATA_TYPE, block2)
        result = get_data3.serialize()
        print("get_data3.serialize() : ", result.hex())



# Version Message 실험
run(GetDataMessageTest("Test_serialize"))
