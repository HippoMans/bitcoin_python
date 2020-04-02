import os
import sys

path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(os.path.abspath(path))

from unittest import TestCase
from lib.helper import run
from lib.helper import hash256
from src.PrivateKey import PrivateKey


class PrivateKeyTest(TestCase):
    def exerciseTest1(self):
        print("********** [Private 초기화 확인] **********")
        key = PrivateKey(10)
        print(key.secret)
        print(key.point.x.num)
        print(key.point.y.num)

    def test_sign(self):
        print("********** [Private sign()함수 사용 확인] **********")
        z = int.from_bytes(hash256(b'Hello Go World'), 'big')
        key = PrivateKey(10)
        result = PrivateKey.sign(key, z)
        print("PrivateKey.r : ", result.r)
        print("PrivateKEy.s : ", result.s)
        

    def test_hex(self):
        print("********** [Private hex] **********")
        z = int.from_bytes(hash256(b'hi'), 'big')
        key = PrivateKey(z)
        print("Privatekey : ", key.hex())
        print("PublicKey : ", key.point.x.num)

    def test_deterministic_k(self):
        print("********** [Private deterministic_k()함수 사용 확인] **********")
        z = int.from_bytes(hash256(b'HippoMans'), 'big')
        key = PrivateKey(1000000)
        PrivateKey.deterministic_k(key, z)
        

# 서명 생성  과정에서 얻은 예제 실험
run(PrivateKeyTest("exerciseTest1"))

# PrivateKey 객체에 선언된 함수들을 실험
run(PrivateKeyTest("test_sign"))
run(PrivateKeyTest("test_hex"))
run(PrivateKeyTest("test_deterministic_k"))
