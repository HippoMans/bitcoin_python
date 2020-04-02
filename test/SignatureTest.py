import os
import sys

path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(os.path.abspath(path))

from unittest import TestCase
from lib.helper import run
from src.Signature import Signature

class SignatureTest(TestCase):
    def exerciseTest1(self):
        print("********** [signature 초기화 확인] **********")
        sig = Signature(100, 200)
        print(sig)

# 서명 학습 과정에서 얻은 예제 실험
run(SignatureTest("exerciseTest1"))
