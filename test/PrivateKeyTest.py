import os
import sys

path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(os.path.abspath(path))

from unittest import TestCase
from lib.helper import run
from lib.helper import hash256
from lib.helper import hash160
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
        
    def exerciseTest2(self):
        print("********** [비밀키를 WIF 형식으로 출력] **********")
        print("5003 공개키는 압축 SEC형식으로 테스트넷에서 사용")
        priv = PrivateKey(5003)
        print(priv.wif(compressed=True, testnet=True))

    def exerciseTest3(self):
        print("********** [비밀키를 WIF 형식으로 출력] **********")
        print("2021**5 공개키는 비압축 SEC형식으로 테스트넷에서 사용")
        priv = PrivateKey(2021**5)
        print(priv.wif(compressed=False, testnet=True))

    def exerciseTest4(self):
        print("********** [비밀키를 WIF 형식으로 출력] **********")
        print("0x54321deadbeef 공개키는 압축 SEC 형식으로 메인넷에서 사용")
        priv = PrivateKey(0x54321deadbeef)
        print(priv.wif(compressed=True, testnet=False))  

    def exerciseTest5(self):
        print("개인키와 비트코인 주소 생성을 위한 연습 -> 향후 비슷하게 사용")
        passwordString = b"HippoMans"
        privateSecret = hash160(passwordString)
        privateSecret = int.from_bytes(privateSecret, 'big')
        priv = PrivateKey(secret=privateSecret)
        bitcoinAddress = priv.point.address(compressed=True, testnet=True)
        print("비트코인 주소 : ", bitcoinAddress)

# 서명 생성  과정에서 얻은 예제 실험
run(PrivateKeyTest("exerciseTest1"))
run(PrivateKeyTest("exerciseTest2"))
run(PrivateKeyTest("exerciseTest3"))
run(PrivateKeyTest("exerciseTest4"))
run(PrivateKeyTest("exerciseTest5"))

# PrivateKey 객체에 선언된 함수들을 실험
run(PrivateKeyTest("test_sign"))
run(PrivateKeyTest("test_hex"))
run(PrivateKeyTest("test_deterministic_k"))
