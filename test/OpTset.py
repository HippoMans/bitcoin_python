import os
import sys

path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(os.path.abspath(path))

from logging import getLogger
from unittest import TestCase
from lib.helper import run
from lib.helper import hash160
from lib.helper import hash256
from src.Signature import Signature
from src.PrivateKey import PrivateKey

from lib.Op import op_hash160
from lib.Op import op_checksig
from lib.Op import decode_num
from lib.Op import op_checkmultisig
from lib.Op import op_0
from lib.Op import op_1negate
from lib.Op import op_1
from lib.Op import op_16
from lib.Op import op_nop
from lib.Op import op_1add
from lib.Op import op_1sub
from lib.Op import op_0notequal
from lib.Op import op_toaltstack
from lib.Op import op_fromaltstack
from lib.Op import op_2dup
from lib.Op import op_2over
from lib.Op import op_2rot
from lib.Op import op_2swap
from lib.Op import op_depth
from lib.Op import op_drop
from lib.Op import op_nip
from lib.Op import op_size
from lib.Op import op_equal
from lib.Op import op_equalverify
from lib.Op import op_abs
from lib.Op import op_not
from lib.Op import op_0notequal
from lib.Op import op_add
from lib.Op import op_sub
from lib.Op import op_booland
from lib.Op import op_boolor
from lib.Op import op_numequal
from lib.Op import op_numnotequal


LOGGER = getLogger(__name__)

class OpTest(TestCase):

    def test_op_hash160(self):
        stack = [b'hello world']
        print(stack)
        self.assertTrue(op_hash160(stack))
        print("stack : ", stack[0].hex())
        self.assertEqual(stack[0].hex(), 'd7d5ee7824ff93f94c3055af9382c86c68b5ca92')

    def test_op_checksig(self):
        # z는 서명
        z = 0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d
        # sec은 
        sec = bytes.fromhex('04887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e4da568744d06c61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34')
        # sig는 
        sig = bytes.fromhex('3045022000eff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c022100c7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab601')
        stack = [sig, sec]
        self.assertTrue(op_checksig(stack, z))
        self.assertEqual(decode_num(stack[0]), 1)

    def test_op_checkmultisig(self):
        z = 0xe71bfa115715d6fd33796948126f40a8cdd39f187e4afb03896795189fe1423c
        sig1 = bytes.fromhex('3045022100dc92655fe37036f47756db8102e0d7d5e28b3beb83a8fef4f5dc0559bddfb94e02205a36d4e4e6c7fcd16658c50783e00c341609977aed3ad00937bf4ee942a8993701')
        sig2 = bytes.fromhex('3045022100da6bee3c93766232079a01639d07fa869598749729ae323eab8eef53577d611b02207bef15429dcadce2121ea07f233115c6f09034c0be68db99980b9a6c5e75402201')
        sec1 = bytes.fromhex('022626e955ea6ea6d98850c994f9107b036b1334f18ca8830bfff1295d21cfdb70')
        sec2 = bytes.fromhex('03b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ffac7fbdbd4bb71')
        stack = [b'', sig1, sig2, b'\x02', sec1, sec2, b'\x02']
        self.assertTrue(op_checkmultisig(stack, z))
        self.assertEqual(decode_num(stack[0]), 1)

    def test_op_0(self):
        stack = []
        self.assertTrue(op_0(stack))
        print(stack)
        self.assertEqual(stack[0], b'')

    def test_op_1negate(self):
        stack = []
        self.assertTrue(op_1negate(stack))
        print(stack)
        self.assertEqual(stack[0], b'\x81')

    def test_op_1(self):
        stack = []
        self.assertTrue(op_1(stack))
        print(stack) 
        self.assertEqual(stack[0], b'\01')

    def test_op_16(self):
        stack = []
        self.assertTrue(op_16(stack))
        print(stack)
        self.assertEqual(stack[0], b'\x10')

    def test_op_nop(self):
        stack = []
        self.assertTrue(op_nop(stack))
        print(stack)
        self.assertEqual(op_nop(stack), True)

    def test_op_1add(self):
        stack = [b'1',b'2',b'3']
        self.assertTrue(op_1add(stack))
        print(stack)
        self.assertEqual(stack, [b'1', b'2', b'4'])

    def test_op_1sub(self):
        stack = [b'1', b'2',b'3']
        self.assertTrue(op_1sub(stack)) 
        print(stack)
        self.assertEqual(stack, [b'1', b'2', b'2'])

    def test_op_0notequal(self):
        stack = [b'']
        self.assertTrue(op_0notequal(stack))
        print(stack) 

    def test_op_toaltstack(self):
        stack = [1,2,3,4]
        other = []
        self.assertTrue(op_toaltstack(stack, other))
        print("stack : ", stack)
        print("other : ", other)
        self.assertEqual(stack, [1,2,3])
        self.assertEqual(other, [4])

    def test_op_fromaltstack(self):
        stack = [1,2]
        other = [3,4]
        self.assertTrue(op_fromaltstack(stack, other))
        print("stack : ", stack)
        print("other : ", other)
        self.assertEqual(stack, [1,2,4])
        self.assertEqual(other, [3])

    def test_op_2dup(self):
        stack = [1,2,3,4]
        self.assertTrue(op_2dup(stack))
        print(stack)
        self.assertEqual(stack, [1,2,3,4,3,4])

    def test_op_2over(self):
        stack = [1,2,3,4]
        self.assertTrue(op_2over(stack))
        print(stack)
        self.assertEqual(stack, [1,2,3,4,1,2])

    def test_op_2rot(self):
        stack = [1,2,3,4,5,6]
        self.assertTrue(op_2rot(stack))
        print(stack)
        self.assertEqual(stack, [1,2,3,4,5,6,1,2])

    def test_op_2swap(self):
        stack = [1,2,3,4]
        self.assertTrue(op_2swap(stack))
        print(stack)
        self.assertEqual(stack, [3,4,1,2])

    def test_op_depth(self):
        stack = [1,2,3,100]
        self.assertTrue(op_depth(stack))
        print(stack)
        self.assertEqual(stack, [1,2,3,100, b'\x04'])

    def test_op_drop(self):
        stack = [1,2,3,4]
        self.assertTrue(op_drop(stack))
        print(stack)
        self.assertEqual(stack, [1,2,3])

    def test_op_nip(self):
        stack = [1,2,3]
        self.assertTrue(op_nip(stack))
        print(stack)
        self.assertEqual(stack, [1,3])

    def test_op_size(self):
        stack = [b'1',b'2',b'3',b'4']
        self.assertTrue(op_size(stack))
        print(stack)
        self.assertEqual(stack, [b'1', b'2', b'3', b'4', b'\x01'])

    def test_op_equal(self):
        stack = [1,2,3,3]
        self.assertTrue(op_equal(stack))
        print(stack)
        self.assertEqual(stack, [1,2, b'\x01'])

    def test_op_equalverify(self):
        stack = [b'1', b'2', b'3', b'3']
        self.assertTrue(op_equalverify(stack))
        print(stack)
        self.assertEqual(stack, [b'1',b'2'])

    def test_op_abs(self):
        stack = [b'1', b'-2']
        self.assertTrue(op_abs(stack))
        print(stack)
        self.assertEqual(stack, [b'1', b'-2'])

    def test_op_not(self):
        stack = [b'']
        self.assertTrue(op_not(stack))
        print(stack)
        self.assertEqual(stack, [b'\x01'])

    def test_op_0notequal(self):
        stack = [b'1', b'2']
        self.assertTrue(op_0notequal(stack))
        print(stack) 
        self.assertTrue(stack, [b'\x01'])

    def test_op_add(self):
        stack = [b'1', b'1']
        self.assertTrue(op_add(stack))
        print(stack)
        self.assertTrue(stack, [b'b'])

    def test_op_sub(self):
        stack = [b'3', b'2']
        self.assertTrue(op_sub(stack))
        print(stack)
        self.assertTrue(stack, [b'\x01'])

    def test_op_booland(self):
        stack = [b'1', b'2']
        self.assertTrue(op_booland(stack))
        print(stack)
        self.assertTrue(stack, [b'\x01'])

    def test_op_boolor(self):
        stack = [b'1', b'2',b'3']
        self.assertTrue(op_boolor(stack))
        print(stack)
        self.assertTrue(stack, [b'1', b'\x01'])

    def test_op_numequal(self):
        stack = [b'1', b'2']
        self.assertTrue(op_numequal(stack))
        print(stack)
        self.assertTrue(stack, [b''])

    def test_op_numnotequal(self):
        stack = [b'1', b'2']
        self.assertTrue(op_numnotequal(stack))
        print(stack)
        self.assertTrue(stack, [b'\x01'])


# lib 디렉토리에 있는 Op.py 파일을 실행
run(OpTest("test_op_hash160"))
run(OpTest("test_op_checksig"))
run(OpTest("test_op_checkmultisig"))
run(OpTest("test_op_0"))
run(OpTest("test_op_1negate"))
run(OpTest("test_op_1"))
run(OpTest("test_op_16"))
run(OpTest("test_op_nop"))
run(OpTest("test_op_1add"))
run(OpTest("test_op_1sub"))
run(OpTest("test_op_0notequal"))
run(OpTest("test_op_toaltstack"))
run(OpTest("test_op_fromaltstack"))
run(OpTest("test_op_2dup"))
run(OpTest("test_op_2over"))
run(OpTest("test_op_2rot"))
run(OpTest("test_op_2swap"))
run(OpTest("test_op_depth"))
run(OpTest("test_op_drop"))
run(OpTest("test_op_nip"))
run(OpTest("test_op_size"))
run(OpTest("test_op_equal"))
run(OpTest("test_op_equalverify"))
run(OpTest("test_op_abs"))
run(OpTest("test_op_not"))
run(OpTest("test_op_0notequal"))
run(OpTest("test_op_add"))
run(OpTest("test_op_sub"))
run(OpTest("test_op_booland"))
run(OpTest("test_op_boolor"))
run(OpTest("test_op_numequal"))
run(OpTest("test_op_numnotequal"))
