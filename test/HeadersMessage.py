import os
import sys

path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(os.path.abspath(path))

from unittest import TestCase
from lib.helper import run
from lib.helper import hash256
from io import BytesIO
from src.HeadersMessage import HeadersMessage
from src.Block import Block


class HeadersMessageTest(TestCase):
    def Test_serialize(self):
        print(HeadersMessage.command)
        hex_msg = '0200000020df3b053dc46f162a9b00c7f0d5124e2676d47bbe7c5d0793a500000000000000ef445fef2ed495c275892206ca533e7411907971013ab83e3b47bd0d692d14d4dc7c835b67d8001ac157e670000000002030eb2540c41025690160a1014c577061596e32e426b712c7ca00000000000000768b89f07044e6130ead292a3f51951adbd2202df447d98789339937fd006bd44880835b67d8001ade09204600'
        stream = BytesIO(bytes.fromhex(hex_msg))
        print("stream : ", stream)
        headers = HeadersMessage.parse(stream)
        print("\nheaders blocks")
        for i in range(0, len(headers.blocks)):
            print("headers[{}] version : {}".format(i, headers.blocks[i].version))
            print("headers[{}] prev_block : {}".format(i, headers.blocks[i].prev_block.hex()))
            print("headers[{}] merkle_root : {}".format(i, headers.blocks[i].merkle_root.hex()))
            print("headers[{}] timestamp : {}".format(i, headers.blocks[i].timestamp))
            print("headers[{}] bits : {}".format(i, headers.blocks[i].bits.hex()))
            print("headers[{}] nonce : {}".format(i, headers.blocks[i].nonce.hex()))
            print("headers[{}] tx_hashes : {}".format(i, headers.blocks[i].tx_hashes))
            print()
        self.assertEqual(len(headers.blocks), 2)
        # 첫번째 headers는 Block 클래스가 list로 있다.
        print("headers.block class : ", headers.blocks.__class__)
        self.assertEqual(headers.blocks.__class__, list)

        result = headers.blocks[0].__class__
        print("headers.block[0] class : ", result)
        self.assertEqual(result, Block)

        result = headers.blocks[1].__class__
        print("headers.block[1] class : ", result)
        self.assertEqual(result, Block)

# Headers Message 실험
run(HeadersMessageTest("Test_serialize"))
