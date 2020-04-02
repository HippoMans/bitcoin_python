import os
import sys
# os.path.split를 통해 파일과 디렉토리 부분을 분리한다.
# os.path.abspath는 현재 경로의 Prefix를 붙여서 절대경로로 바궈서 반환한다.
# 입력받은 파일/디렉토리의 경로를 반환한다. 
# /root/bitcoin_python을 path으로 값 설정
path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0] 

# sys.path는 파이썬 라이브러리들이 설치되어 있는 디렉터리들을 보여준다.
# 파이썬 라이브러리에 디렉토리 경로 설정 /root/bitcoin_python
sys.path.append(os.path.abspath(path))

# 단위 테스트의 프레임워크 
from unittest import TestCase

# 생성한 class를 사용
from lib.helper import run
from src.FieldElement import FieldElement

class FieldElementTest(TestCase):
    def exerciseTest1(self):
        print("********** [같은 유한체인지 확인] **********")
        a = FieldElement(7, 13)
        b = FieldElement(6, 13)
        print("두 FieldElement 객체가 같은지 확인 ? ", a == b)
        print("두 FieldElement 객체가 같은지 확인 ? ", a == a)

    def exerciseTest2(self):
        print("********** [유한체 덧셈한 결과와 유한체를 비교하여 같은지 확인] **********")
        a = FieldElement(7, 13)
        b = FieldElement(12, 13)
        c = FieldElement(6, 13)
        print("두 FiledElement 객체를 더하여서 c와 같은지 확인")
        print(a+b == c)

    def exerciseTest3(self):
        print("********** [유한체 F57 에 덧셈, 뺄셈 연산 확인] **********")
        a = FieldElement(44, 57)
        b = FieldElement(33, 57)
        print("44 +f 33 = ", a + b)
        a = FieldElement(9, 57)
        b = FieldElement(29, 57)
        print("9 -f 29 = ", a - b)
        a = FieldElement(17, 57)
        b = FieldElement(42, 57)
        c = FieldElement(49, 57)
        print("17 +f 42 +f 49 = ", a + b + c)
        a = FieldElement(52, 57)
        b = FieldElement(30, 57)
        c = FieldElement(38, 57)
        print("52 -f 30 -f 38 = ", a - b - c)

    def exerciseTest4(self):
        print("********** [유한체 F97 에서 곱셈과 거듭제곱 연산 확인] **********")
        a = FieldElement(95, 97)
        b = FieldElement(45, 97)
        c = FieldElement(31, 97)
        print("95 *f 45 *f 31 = ", a * b * c)
        a = FieldElement(17, 97)
        b = FieldElement(13, 97)
        c = FieldElement(19, 97)
        d = FieldElement(44, 97)
        print("17 *f 13 *f 19 *f 44 = ", a * b * c * d)
        a = FieldElement(12, 97)
        b = FieldElement(77, 97)
        exponent_a = 7
        exponent_b = 49
        print("(12 ** 7) *f (77 ** 49) = ", (a ** exponent_a) * (b ** exponent_b))

    def exerciseTest5(self):
        print("********** [k가 각각 1, 3, 7, 13, 18 인 경우 유한체 f19 에서 집합 확인] **********")
        print("********** [집합 {k *f 0, k *f 1, k *f 2, ... k *f 18}] **********")
        prime = 19
        print("기본 순서")
        for k in (1, 3, 7, 13, 18):
            print([(k * i) % prime for i in range(prime)])

        print("\nsorted()함수를 통해 정렬") 
        for k in (1, 3, 7, 13, 18):
            print(sorted([(k * i) % prime for i in range(prime)]))

    def exerciseTest6(self):
        print("********** [7, 11, 17, 31 인 p 값에 대해 유한체 Fp 에서 집합을 확인] **********")
        print("********** [{1^(p-1), 2^(p-1), 3^(p-1), 4^(p-1), (p-1)^(p-1)}] **********")
        for prime in (7, 11, 17, 31):
            print([pow(i, prime-1, prime) for i in range(1, prime)])

    def exerciseTest7(self):
        print("********** [유한체 31, F31 에서 나눗셈, 역수 계산 확인] **********")
        a = FieldElement(3, 31)
        b = FieldElement(24, 31)
        print("3 /f 24", a / b)
        a = FieldElement(17, 31)
        exponent = -3
        print("17^-3", a ** exponent)
        a = FieldElement(4, 31)
        b = FieldElement(11, 31)
        exponent = -4
        print("4^-4 *f 11", a ** exponent * b)

    def test_eq(self):
        print("********** [유한체가 같은지 확인] **********")
        a = FieldElement(4, 31)
        b = FieldElement(4, 31)
        c = FieldElement(15, 31)
        self.assertEqual(a, b)
        self.assertTrue(a != c)
        self.assertFalse(a != b)

    def test_ne(self):
        print("********** [유한체가 다른지 확인] **********")
        a = FieldElement(2, 31)
        b = FieldElement(2, 31)
        c = FieldElement(15, 31)
        self.assertEqual(a, b)
        self.assertTrue(a != c)
        self.assertFalse(a != b)

    def test_add(self):
        print("********** [유한체 덧셈] **********")
        a = FieldElement(2, 31)
        b = FieldElement(15, 31)
        self.assertEqual(a + b, FieldElement(17, 31))
        a = FieldElement(17, 31)
        b = FieldElement(21, 31)
        self.assertEqual(a + b, FieldElement(7, 31))

    def test_sub(self):
        print("********** [유한체 뺄셈] **********")
        a = FieldElement(29, 31)
        b = FieldElement(4, 31)
        self.assertEqual(a - b, FieldElement(25, 31))
        a = FieldElement(15, 31)
        b = FieldElement(30, 31)
        self.assertEqual(a - b, FieldElement(16, 31))

    def test_mul(self):
        print("********** [유한체 곱셈] **********")
        a = FieldElement(24, 31)
        b = FieldElement(19, 31)
        self.assertEqual(a * b, FieldElement(22, 31))

    def test_pow(self):
        print("********** [유한체 거듭 제곱] **********")
        a = FieldElement(17, 31)
        self.assertEqual(a**3, FieldElement(15, 31))
        a = FieldElement(5, 31)
        b = FieldElement(18, 31)
        self.assertEqual(a**5 * b, FieldElement(16, 31))

    def test_div(self):
        print("********** [유한체 나눗셈] **********")
        a = FieldElement(3, 31)
        b = FieldElement(24, 31)
        self.assertEqual(a / b, FieldElement(4, 31))
        a = FieldElement(17, 31)
        self.assertEqual(a**-3, FieldElement(29, 31))
        a = FieldElement(4, 31)
        b = FieldElement(11, 31)
        self.assertEqual(a**-4 * b, FieldElement(13, 31))

    def test_rmul(self):
        print("********** [유한체 숫자 * 객체] **********")
        a = FieldElement(3, 31)
        b = FieldElement(9, 31)
        c = 3 * a
        self.assertEqual(b, c)

## 학습 과정에서 유한체 예제 학습 
run(FieldElementTest("exerciseTest1"))
run(FieldElementTest("exerciseTest2"))
run(FieldElementTest("exerciseTest3"))
run(FieldElementTest("exerciseTest4"))
run(FieldElementTest("exerciseTest5"))
run(FieldElementTest("exerciseTest6"))
run(FieldElementTest("exerciseTest7"))

## 유한체 클래스 기능 테스트셈
run(FieldElementTest("test_eq"))
run(FieldElementTest("test_ne"))
run(FieldElementTest("test_add"))
run(FieldElementTest("test_sub"))
run(FieldElementTest("test_mul"))
run(FieldElementTest("test_pow"))
run(FieldElementTest("test_div"))
run(FieldElementTest("test_rmul"))
