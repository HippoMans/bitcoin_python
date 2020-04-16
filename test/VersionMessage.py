import os
import sys

path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(os.path.abspath(path))

from unittest import TestCase
from lib.helper import run
from lib.helper import hash256
from lib.byte_helper import bit_field_to_bytes
from src.VersionMessage import VersionMessage


class VersionMessageTest(TestCase):
    def Test_serialize(self):
        vmessage = VersionMessage(timestamp=0, nonce=b'\x00' * 8)
        print("객체 : ",vmessage)
        result = vmessage.serialize()
        print("Version Message Serial : ", result)
        want = '7f11010000000000000000000000000000000000000000000000000000000000000000000000ffff00000000208d000000000000000000000000000000000000ffff00000000208d0000000000000000182f70726f6772616d6d696e67626974636f696e3a302e312f0000000000'
        print("\nVersion Message Serial hex : ", result.hex())
        print("want : ", want)
        print("\n\nVersionMessage")
        print("VersionMessage version : ", vmessage.version)
        print("VersionMessage services : ", vmessage.services)
        print("VersionMessage timestamp : ", vmessage.timestamp)
        print("VersionMessage receiver_services : ", vmessage.receiver_services)
        print("VersionMessage receiver_ip : ", vmessage.receiver_ip.hex())
        print("VersionMessage receiver_port : ", vmessage.receiver_port)
        print("VersionMessage sender_services : ", vmessage.sender_services)
        print("VersionMessage sender_ip : ", vmessage.sender_ip.hex())
        print("VersionMessage sender_port : ", vmessage.sender_port)
        print("VersionMessage nonce : ", vmessage.nonce.hex())
        print("VersionMessage user_agent : ", bit_field_to_bytes(vmessage.user_agent).hex())
        print("VersionMessage latest_block : ", vmessage.latest_block)
        print("VersionMessage relay : ", vmessage.relay)
        self.assertEqual(result.hex(), want)


# Version Message 실험
run(VersionMessageTest("Test_serialize"))
