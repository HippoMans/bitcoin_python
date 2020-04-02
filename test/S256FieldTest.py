import os
import sys

path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(os.path.abspath(path))

from unittest import TestCase
from lib.helper import run
from src.FieldElement import FieldElement
from src.Point import Point
from src.S256Field import S256Field

class S256FieldTest(TestCase):
    def exerciseTest1(self):
        gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
        gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
        p = 2**256 - 2**32 - 977
        print(gy**2 % p == (gx**3 + 7) % p)

    def exerciseTest2(self):
        gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
        gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
        p = 2**256 - 2**32 - 977
        n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
        x = FieldElement(gx, p)
        y = FieldElement(gy, p)
        seven = FieldElement(7, p)
        zero = FieldElement(0, p)
        G = Point(x, y, zero, seven)   # 생성점 확인
        result = n*G     # 숫자에 객체를 곱한 값이 곡선 위에 있는지 확인
        print(result.x, result.y)

    def exerciseTest3(self):
        print("*********** [S256Filed 기본 초기화 설정 확인] **********")
        a = S256Field(10)
        b = S256Field(20)
        c = S256Field(100000000)
        print(a)
        print(b)        
        print(c)

    def exerciseTest4(self):
        print("********** [S256Field에 FieldElement 기본 초기화 설정 확인] **********")
        p = 2**256 - 2**32 - 977
        x = FieldElement(10, p)
        y = FieldElement(20, p)
        a = S256Field(x.num)
        b = S256Field(y.num)
        print(a)
        print(b)

## 학습 과정에서 타원곡선 암호 예제 학습
run(S256FieldTest("exerciseTest1"))
run(S256FieldTest("exerciseTest2"))
run(S256FieldTest("exerciseTest3"))
run(S256FieldTest("exerciseTest4"))
