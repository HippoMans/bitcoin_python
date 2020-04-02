# random 패키지 안에 randint함수를 가져온다. ->  무작위 정숫값을 가져온다.

from src.S256Point import S256Point
from src.Signature import Signature
from random import seed
from random import randint
from datetime import datetime
import hashlib
import hmac


G = S256Point(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141


# 메시지에 대한 서명을 생성하기 위해서 비밀키를 보관할 PrivateKey 클래스가 필요
class PrivateKey:
    def __init__(self, secret):
        self.secret = secret
        self.point = secret * G    # 공개키에 해당하는 self.point를 계산하여 보관

    def hex(self):
        return '{:x}'.format(self.secret).zfill(64)

    def sign(self, z):
        # k를 무작위로 선정하지 않고 비밀키(self)와 서명 해시(z)에 따라 결정하여 설정
        k = self.deterministic_k(z) 
        r = (k * G).x.num          # K * G의 x값을 r으로 사용
        k_inv = pow(k, N-2, N)     # 페르마 소정리 사용
        s = (z + r*self.secret) * k_inv % N  # s = (z + r*e) / k
        if s > N/2:    
            s = N - s
        return Signature(r, s)     # 정의한 (r, s)를 Signature 클래스의 인스턴스로 반환

    def deterministic_k(self, z):
        k = b'\x00' * 32
        v = b'\x01' * 32
        if z > N:
            z -= N
        z_bytes = z.to_bytes(32, 'big')    # to_bytes() 정수를 나타내는 바이트의 배열로 출력
        secret_bytes = self.secret.to_bytes(32, 'big')
        s256 = hashlib.sha256      # sha256으로 암호화
        # hmac 알고리즘 구현 -> 메시지 인증을 위한 키 해싱
        # hmac.new()를 통해 hmac 객체 생성
        # hamc.digest()를 통해 주어진 secret key와 digest로 msg의 digest를 반환한다.
        k = hmac.new(k, v + b'\x00' + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        k = hmac.new(k, v +b'\x01' + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        while True:
            v = hmac.new(k, v, s256).digest()
            candidate = int.from_bytes(v, 'big')
            if candidate >= 1 and candidate < N:
                return candidate
            k = hmac.new(k, v + b'\x00', s256).digest()
            v = hmac.new(k, v, s256).digest()
