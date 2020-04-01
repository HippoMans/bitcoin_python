import os
import sys
path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(os.path.abspath(path))
from unittest import TestCase
from lib.helper import run
from src.Point import Point

class PointTest(TestCase):
    def exerciseTest1(self):
        print("********** y**2 = x**3 + 5*x + 7 위에 (2,5), (-1,-1), (18, 77), (5,7) 확인 **********")
        print("(2,5)가 y**2 = x**3 + 5*x + 7 위에 있는지 확인")
        a = Point(2, 5, 5, 7)

        print("(-1,-1)가 y**2 = x**3 + 5*x + 7 위에 있는지 확인")
        b = Point(-1, -1, 5, 7)

        print("(18,77)가 y**2 = x**3 + 5*x + 7 위에 있는지 확인")
        a = Point(18, 77, 5, 7)

        print("(3,7)가 y**2 = x**3 + 5*x + 7 위에 있는지 확인 ")
        a = Point(3, 7, 5, 7)

    def exerciseTest2(self):
        print("********** 무한대 값을 더하기로 활용한 결과 확인 **********")
        p1 = Point(-1, -1, 5, 7)
        p2 = Point(-1, 1, 5, 7)
        inf = Point(None, None, 5, 7)

        result = p1 + inf
        print(result.x, result.y)

        result = inf + p2
        print(result.x, result.y)

        result = p1 + p2
        print(result.x, result.y)

    def exerciseTest3(self):
        print("********** 한 점에 그의 역원을 더하는 경우를 확인 **********")
        p1 = Point(-1, -1, 5, 7)
        p2 = Point(-1, 1, 5, 7)
        result = p1 + p2
        print(result.x, result.y)

    def exerciseTest4(self):
        print("********** y**2 = x**3 + 5*x + 7 위의 두점(2,5),(-1-1)을 더한 점의 결과 확인 **********")
        p1 = Point(2, 5, 5, 7)
        p2 = Point(-1, -1, 5, 7)
        result = p1 + p2
        print(result.x, result.y)

    def exerciseTest5(self):
        print("********** y**2 = x**3 + 5*x + 7 위의 점(-1, -1)을 두번 더하는 연산 결과 **********")
        p1 = Point(-1, -1, 5, 7)
        p2 = Point(-1, -1, 5, 7)
        result = p1 + p2
        print(result.x, result.y)

    def test_eq(self):
        print("********** [타원곡선 상의 점이 같은지 확인] **********")
        a = Point(2, 5, 5, 7)
        b = Point(2, 5, 5, 7)
        self.assertTrue(a == b)
        self.assertFalse(a != b)

    def test_ne(self):
        print("********** [타원곡선 상의 점이 다른지 확인] **********")
        a = Point(2, 5, 5, 7)
        b = Point(3, 7, 5, 7)
        self.assertFalse(a != b)
        self.assertTrue(a == a)

    def test_add0(self):
        print("********** [타원곡선 상의 점 덧셈] - 점과 항등원, 역원의 덧셈 결과 확인 **********")
        a = Point(None, None, 5, 7)
        b = Point(2, 5, 5, 7)
        c = Point(2, -5, 5, 7)
        self.assertEqual(a + b, b)
        self.assertEqual(a + c, c)
        self.assertEqual(b + c, a)

    def test_add1(self):
        print("********** [타원곡선 상의 점 덧셈] - 서로 다른 두점을 덧셈한 결과 학인 **********")
        a = Point(3, 7, 5, 7)
        b = Point(-1, -1, 5, 7)
        c = Point(2.0, -5.0, 5, 7)
        self.assertEqual((a + b).x, c.x)
        self.assertEqual((a + b).y, c.y)

    def test_add2(self):
        print("********** [타원곡선 상의 점 덧셈] - 같은 두 점의 덧셈 결과 확인 **********")
        a = Point(-1, -1, 5, 7)
        self.assertEqual(a + a, Point(18, 77, 5, 7))

# 타원곡선 관련된 테스트 코드 구현
run(PointTest("exerciseTest1"))
run(PointTest("exerciseTest2"))
run(PointTest("exerciseTest3"))
run(PointTest("exerciseTest4"))
run(PointTest("exerciseTest5"))

# 타원곡선 관련 기능 테스트 코드 구현
run(PointTest("test_eq"))
run(PointTest("test_ne"))
run(PointTest("test_add0"))
run(PointTest("test_add1"))
run(PointTest("test_add2"))
