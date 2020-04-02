import os
import sys

path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(os.path.abspath(path))

from unittest import TestCase
from lib.helper import run
from src.FieldElement import FieldElement
from src.Point import Point
from src.S256Field import S256Field
from src.S256Point import S256Point, N
from src.Signature import Signature
from lib.helper import hash256

class S256PointTest(TestCase):
    def exerciseTest1(self):
        print("********** [타원곡선을 위한 결과 학인] **********")        
        G = S256Point(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
        print(G.x.num, G.y.num)


    def exerciseTest2(self):
        print("********** [N*G] **********")
        G = S256Point(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
        N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
        result = N * G
        print(result.x, result.y)

    def exerciseTest3(self):
        print("********** [서명 검증 실습 확인] **********")
        z = 0xbc62d4b80d9e36da29c16c5d4d9f11731f36052c72401a76c23c0fb5a9b74423
        r = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6
        s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec
        px = 0x04519fac3d910ca7e7138f7013706f619fa8f033e6ec6e09370ea38cee6a7574
        py = 0x82b51eab8c27c66e26c858a079bcdf4f1ada34cec420cafc7eac1a42216fb6c4
        G = S256Point(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
        point = S256Point(px, py)
        s_inv = pow(s, N-2, N)
        u = ( z * s_inv ) % N
        v = ( r * s_inv ) % N
        result = ( u * G + v * point).x.num 
        print("r : ", r)
        print("(u*G + v*P)", result)
        print(result == r)

    def exerciseTest4(self):
        print("********** [서명 검증 실습 예제 1] **********")
        P = S256Point(0x887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e4da568744d06c,0x61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34)
        G = S256Point(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
        z = 0xec208baa0fc1c19f708a9ca96fdeff3ac3f230bb4a7ba4aede4942ad003c0f60
        r = 0xac8d1c87e51d0d441be8b3dd5b05c8795b48875dffe00b7ffcfac23010d3a395
        s = 0x68342ceff8935ededd102dd876ffd6ba72d6a427a3edb13d26eb0781cb423c4
        s_inv = pow(s, N-2, N)
        u = (z * s_inv) % N
        v = (r * s_inv) % N
        result = (u * G + v * P).x.num
        print("r : ", r)
        print("(u * G + v * P) : ", result)
        print(r == result)

    def exerciseTest5(self):
        print("********** [서명 검증 실습 예제 2] **********")
        P = S256Point(0x887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e4da568744d06c,0x61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34)
        G = S256Point(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
        z = 0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d
        r = 0xeff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c
        s = 0xc7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6
        s_inv = pow(s, N-2, N)
        u = (z * s_inv) % N
        v = (r * s_inv) % N
        result = (u * G + v * P).x.num
        print("r : ", r)
        print("(u * G + v * P) : ", result)
        print(r == result)

    def exerciseTest6(self):
        print("********** [서명 검증 실습 예제3] **********")
        G = S256Point(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
        # e는 비밀키
        e = int.from_bytes(hash256(b'my secret'), 'big')
        # z는 서명해시 -> 메시지 해시 
        z = int.from_bytes(hash256(b'my message'), 'big')
        # k는 무작위값으로 R = kG을 통해 값을 가져온다.
        k = 1234567890
        # r은 R = kG로부터의 R의 x좌표값 r을 가지고 온것
        r = (k*G).x.num
        k_inv = pow(k, N-2, N)
        # s = (z + re)/k, 위수 n의 순환군이기에 n으로 나머지 연산. 
        s = (z + r*e) * k_inv % N
        # 검증자는 공개키에 해당하는 point를 이미 알고 있다고 가정한다. point가 공개키이다.
        point = e*G
        print("공개키 : ", point.x.num, point.y.num)
        print("서명 해시 : ", hex(z))
        print("R = KG로부터의 R의 x좌표값 r : ", hex(r))
        print("s = (z + re) * k_inv % N : ",hex(s))
        s_inv = pow(s, N-2, N)
        u = (z * s_inv) % N
        v = (r * s_inv) % N
        result = (u *G + v * point).x.num
        print("(u*G+v*P) : ", result)
        print(r == result)

    def exerciseTest7(self):
        print("********** [서명 검증 실습 예제4] **********")
        G = S256Point(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
        # e는 비밀키
        e = int.from_bytes(hash256(b'12345'), 'big')
        # z는 서명 해시(메시지 해시)
        z = int.from_bytes(hash256(b'Programming Bitcoin!'), 'big')
        # k는 무작위값으로 R = kG를 통해 값
        k = 1234567890
        # r은 R = kG로부터의 R의 x좌표값 r을 가지고 온것
        r = (k*G).x.num
        k_inv = pow(k, N-2, N)
        # s = (z +re)/k, 위수 n의 순환군이기에 n으로 나머지 연산
        s = (z + r*e) * k_inv % N
        # 검증자는 공개키에 해당하는 point를 이미 알고 있다고 가정한다. point가 공개키이다.
        point = e * G
        print("공개키 : ", point.x.num, point.y.num)
        print("서명 해시 : ", hex(z))
        print("R = kG로부터의 R의 x좌표값 r : ", hex(r))
        print("s = (z + re) *k_int % N : ", hex(s))
        s_inv = pow(s, N-2, N)
        u = (z * s_inv) % N
        v = (r * s_inv) % N
        result = (u * G + v * point).x.num
        print("(u*G + v*P) : ", result)
        print(r == result)

    def exerciseTest8(self):
        print("********** [__rmul__() 사용] **********")
        G = S256Point(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
        A = 3 * G
        print(A.x.num)

    def test__verify(self):
        print("********** [서명 검증 확인] **********")
        G = S256Point(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
        # e는 비밀키
        e = int.from_bytes(hash256(b'12345'), 'big')
        # z는 서명 해시(메시지 해시)
        z = int.from_bytes(hash256(b'Programming Bitcoin!'), 'big')
        # k는 무작위값으로 R = kG를 통해 값
        k = 1234567890
        # r은 R = kG로부터의 R의 x좌표값 r을 가지고 온것
        r = (k*G).x.num
        k_inv = pow(k, N-2, N)
        # s = (z +re)/k, 위수 n의 순환군이기에 n으로 나머지 연산
        s = (z + r*e) * k_inv % N
        # 검증자는 공개키에 해당하는 point를 이미 알고 있다고 가정한다. point가 공개키이다.
        point = e * G
        s_inv = pow(s, N-2, N)
        u = (z * s_inv) % N
        v = (r * s_inv) % N
        result = (u * G + v * point).x.num 
        sig = Signature(r, s)
        print("검증 : ", S256Point.verify(point ,G, z, sig))

# 타원곡선의 학습 과정에서 예제 실험
run(S256PointTest("exerciseTest1"))
run(S256PointTest("exerciseTest2"))
run(S256PointTest("exerciseTest3"))
run(S256PointTest("exerciseTest4"))
run(S256PointTest("exerciseTest5"))
run(S256PointTest("exerciseTest6"))
run(S256PointTest("exerciseTest7"))
run(S256PointTest("exerciseTest8"))
run(S256PointTest("test__verify"))
