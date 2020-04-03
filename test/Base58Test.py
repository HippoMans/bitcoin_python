import os
import sys

path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(os.path.abspath(path))

from unittest import TestCase
from lib.helper import run
from lib.helper import encode_base58


class Base58Test(TestCase):
    def exerciseTest1(self):
        print("********** [encode_base58() 함수 결과 확인] **********")
        print("첫 번째")
        h = '7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d'
        bytes_value = bytes.fromhex(h)         # 16진수(hex)를 bytes로 변경
        print(encode_base58(bytes_value))

        print("\n두 번째")
        h = 'eff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c'
        bytes_value = bytes.fromhex(h)
        print(encode_base58(bytes_value))

        print("\n세 번째")
        h = 'c7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6'
        bytes_value = bytes.fromhex(h)
        print(encode_base58(bytes_value))


# 서명 학습 과정에서 얻은 예제 실험
run(Base58Test("exerciseTest1"))
