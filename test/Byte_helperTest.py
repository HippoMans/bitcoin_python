import os
import sys

path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(os.path.abspath(path))

from unittest import TestCase
from lib.helper import run
from lib.helper import hash256
from lib.byte_helper import bits_to_target
from lib.byte_helper import target_to_bits
from lib.byte_helper import calculate_new_bits
from lib.byte_helper import bit_field_to_bytes
from lib.byte_helper import bytes_to_bit_field
from io import BytesIO

class ByteHelperTest(TestCase):
    def Test_bits_to_target(self):
        bit = bytes.fromhex('54d80118')
        print(bit)
        result = bits_to_target(bit)
        print(result)

    def Test_target_to_bits(self):
        bit = bytes.fromhex('54d80118')
        target = bits_to_target(bit)
        result = target_to_bits(target)
        print(result)
        self.assertEqual(bit, result)

    def Test_calculate_new_bits(self):
        prev_bits = bytes.fromhex('54d80118')
        time_differential = 302400
        want = bytes.fromhex('00157617')
        result = calculate_new_bits(prev_bits, time_differential)
        print("prev_bits : ", prev_bits, "\t\tprev_bits(hex) : ", prev_bits.hex())
        print("want : ", want, "\t\twant(hex) : ", want.hex())
        print("result : ", result, "\t\tresult(hex) : ", result.hex())
        self.assertEqual(want, result)

    def Test_bit_field_to_bytes(self):
        bit_field = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        want = '4000600a080000010940'
        result = bit_field_to_bytes(bit_field)
        print("filed : ", result)
        print("bytes : ",result.hex())
        self.assertEqual(result.hex(), want)
        result = bytes_to_bit_field(bytes.fromhex(want))
        print(result)
        self.assertEqual(result, bit_field)


# 타원곡선의 학습 과정에서 예제 실험
run(ByteHelperTest("Test_bits_to_target"))
run(ByteHelperTest("Test_target_to_bits"))
run(ByteHelperTest("Test_calculate_new_bits"))
run(ByteHelperTest("Test_bit_field_to_bytes"))
