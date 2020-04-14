import os
import sys

path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(os.path.abspath(path))

from unittest import TestCase
from lib.helper import run
from lib.helper import hash160
from lib.helper import hash256
from lib.helper import sha256
from lib.helper import h160_to_p2pkh_address
from lib.helper import h160_to_p2sh_address
from lib.helper import encode_base58
from lib.helper import encode_base58_checksum
from lib.helper import decode_base58
from lib.helper import little_endian_to_int
from lib.helper import int_to_little_endian

class HelperTest(TestCase):
    def Test_hash160(self):
        s = b'Hello World'
        result = hash160(s)
        print(result)

    def Test_hash256(self):
        s = b'Good'
        result = hash256(s)
        print(result)

    def Test_sha256(self):
        s = b'Hello World'
        result = sha256(s)
        print(result)

    def Test_h160_to_p2pkh_address(self):
        h160 = bytes.fromhex('74d691da1574e6b3c192ecfb52cc8984ee7b6c56')
        print("Test_h160_to_p2pkh_address : ", h160)
        want = '1BenRpVUFK65JFWcQSuHnJKzc4M8ZP8Eqa'
        result = h160_to_p2pkh_address(h160, testnet=False)
        print(result)
        self.assertEqual(result, want)
        want = 'mrAjisaT4LXL5MzE81sfcDYKU3wqWSvf9q'
        result = h160_to_p2pkh_address(h160, testnet=True)
        print(result)
        self.assertEqual(result, want)

    def Test_h160_to_p2sh_address(self):
        h160 = bytes.fromhex('74d691da1574e6b3c192ecfb52cc8984ee7b6c56')
        print("Test_h160_to_p2sh_address : ", h160)
        want = '3CLoMMyuoDQTPRD3XYZtCvgvkadrAdvdXh'
        result = h160_to_p2sh_address(h160, testnet=False)
        print(result)
        self.assertEqual(result, want)
        want = '2N3u1R6uwQfuobCqbCgBkpsgBxvr1tZpe7B'
        result = h160_to_p2sh_address(h160, testnet=True)
        print(result)
        self.assertEqual(result, want)

    def Test_encode_base58(self):
        s = b'Hello World'
        result = encode_base58(s)
        print(result)

    def Test_encode_base58_checksum(self):
        s = b'Hello World'
        result = encode_base58_checksum(s)
        print(result)

    def Test_decode_base58(self):
        addr = 'mnrVtF8DWjMu839VW3rBfgYaAfKk8983Xf'
        h160 = decode_base58(addr).hex()
        print(h160)
        want = '507b27411ccf7f16f10297de6cef3f291623eddf'
        self.assertEqual(h160, want)
        got = encode_base58_checksum(b'\x6f' + bytes.fromhex(h160))
        print(got)
        self.assertEqual(got, addr)

    def Test_little_endian_to_int(self):
        s = b'Hello World'
        result = little_endian_to_int(s)
        print(result)

    def Test_int_to_little_endian(self):
        n = 121404708493354166158910792
        length = 27
        result = int_to_little_endian(n, length)
        print(result)

# Helper.py를 실행하는 예제 실험
run(HelperTest("Test_hash160"))
run(HelperTest("Test_hash256"))
run(HelperTest("Test_sha256"))
run(HelperTest("Test_h160_to_p2pkh_address"))
run(HelperTest("Test_h160_to_p2sh_address"))
run(HelperTest("Test_encode_base58"))
run(HelperTest("Test_encode_base58_checksum"))
run(HelperTest("Test_decode_base58"))
run(HelperTest("Test_little_endian_to_int"))
run(HelperTest("Test_int_to_little_endian"))
