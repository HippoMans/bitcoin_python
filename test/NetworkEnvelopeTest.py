import os
import sys

path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(os.path.abspath(path))

from unittest import TestCase
from lib.helper import run
from lib.helper import hash256
from src.NetworkEnvelope import NetworkEnvelope
from io import BytesIO

class NetworkEnvelopeTest(TestCase):
    def Test_parse(self):
        print("[첫번째]")
        msg = bytes.fromhex('f9beb4d976657261636b000000000000000000005df6e0e2')
        print(msg)
        stream = BytesIO(msg)
        print(stream)
        envelope = NetworkEnvelope.parse(stream)
        print("\nenvelope")
        print(envelope)
        print("envelope.command : ", envelope.command)
        print("envelope.payload : ", envelope.payload)
        self.assertEqual(envelope.command, b'verack')
        self.assertEqual(envelope.payload, b'')

        print("\n[두번째]")
        msg = bytes.fromhex('f9beb4d976657273696f6e0000000000650000005f1a69d2721101000100000000000000bc8f5e5400000000010000000000000000000000000000000000ffffc61b6409208d010000000000000000000000000000000000ffffcb0071c0208d128035cbc97953f80f2f5361746f7368693a302e392e332fcf05050001')
        print(msg.hex())
        stream = BytesIO(msg)
        print(stream)
        envelope = NetworkEnvelope.parse(stream)
        print(envelope)
        print("envelope.command : ", envelope.command)
        print("envelope.payload : ", envelope.payload.hex())
        pay = '721101000100000000000000bc8f5e5400000000010000000000000000000000000000000000ffffc61b6409208d010000000000000000000000000000000000ffffcb0071c0208d128035cbc97953f80f2f5361746f7368693a302e392e332fcf05050001'
        self.assertEqual(envelope.command, b'version')
        self.assertEqual(envelope.payload.hex(), pay)


    def Test_serialize(self):
        print("[첫번째]")
        msg = bytes.fromhex('f9beb4d976657261636b000000000000000000005df6e0e2')
        print("msg : ", msg)
        stream = BytesIO(msg)
        envelope = NetworkEnvelope.parse(stream)
        result = envelope.serialize()
        print("envelope.serialize : ", result)
        self.assertEqual(result, msg)

        print("\n[두번째]")
        msg = bytes.fromhex('f9beb4d976657273696f6e0000000000650000005f1a69d2721101000100000000000000bc8f5e5400000000010000000000000000000000000000000000ffffc61b6409208d010000000000000000000000000000000000ffffcb0071c0208d128035cbc97953f80f2f5361746f7368693a302e392e332fcf05050001')
        print("msg : ", msg)
        print()
        stream = BytesIO(msg)
        envelope = NetworkEnvelope.parse(stream)
        result = envelope.serialize()
        print("envelope.serialize : ", result)
        self.assertEqual(result, msg)
        

# 비트코인 네트워크 테스트
run(NetworkEnvelopeTest("Test_parse"))
run(NetworkEnvelopeTest("Test_serialize"))
