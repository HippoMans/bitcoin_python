import os
import sys

path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(os.path.abspath(path))

from unittest import TestCase
from lib.helper import run
from lib.helper import hash256
from lib.byte_helper import bit_field_to_bytes
from src.GetHeadersMessage import GetHeadersMessage


class GetHeadersMessageTest(TestCase):
    def Test_serialize(self):
        block_hex = '0000000000000000001237f46acddf58578a37e213d2a6edc4884a2fcad05ba3'
        GHMessage = GetHeadersMessage(start_block=bytes.fromhex(block_hex))
        print(GHMessage)
        print(GHMessage.command)
        print("GetHeadersMessage version : ", GHMessage.version)
        print("GetHeadersMessage num_hashes : ", GHMessage.num_hashes)
        print("GetHeadersMessage start_block : ", GHMessage.start_block.hex())
        print("GetHeadersMessage end_block : ", GHMessage.end_block.hex())

        print("\nGetHeadersMessage.serialize()")
        result = GHMessage.serialize()
        print(result.hex())

# GetHeadersMessage 실험
run(GetHeadersMessageTest("Test_serialize"))
