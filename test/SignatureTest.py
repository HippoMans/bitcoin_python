import os
import sys

path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(os.path.abspath(path))

from unittest import TestCase
from lib.helper import run
from lib.helper import hash256
from src.Signature import Signature
from src.PrivateKey import PrivateKey


class SignatureTest(TestCase):
    def exerciseTest1(self):
        print("********** [signature 초기화 확인] **********")
        sig = Signature(100, 200)
        print(sig)

    def test_der(self):
        print("********** [r과 s값의 서명을 DER 형식 확인] **********")
        z = int.from_bytes(hash256(b'HippoMans'), 'big')
        key = PrivateKey(10000)
        sig = PrivateKey.sign(key, z)
        mySig = Signature(sig.r, sig.s)
        print("Signature : ", mySig)
        print("r : ", mySig.r)
        print("s : ", mySig.s)
        print("\n\nsignature을 DER형식으로 압축한 결과")
        print(Signature.der(mySig).hex())

    def exerciseTest2(self):
        r = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6
        s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec
        sig = Signature(r, s)
        print("\nsignature을 DER형식으로 압축한 결과")
        print(Signature.der(sig).hex())

# 서명 학습 과정에서 얻은 예제 실험
run(SignatureTest("exerciseTest1"))
run(SignatureTest("test_der"))
run(SignatureTest("exerciseTest2"))
