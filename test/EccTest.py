import os
import sys

path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(os.path.abspath(path))

from unittest import TestCase
from lib.helper import run
from src.FieldElement import FieldElement
from src.Point import Point

class EccTest(TestCase):
    def exerciseTest1(self):
        print("********** F223에서 정의된 곡선 y**2 = x**3 + 7위에 있는지 확인 **********")
        print("(192, 105)")
        prime = 223
        x = FieldElement(192, prime)
        y = FieldElement(105, prime)
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        p1 = Point(x, y, a, b)
        print(p1)
        print(p1.x.num, p1.y.num, p1.a.num, p1.b.num)

        print("\n(17, 56)")
        x = FieldElement(17, prime)
        y = FieldElement(56, prime)
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        p1 = Point(x, y, a, b)
        print(p1)
        print(p1.x.num, p1.y.num, p1.a.num, p1.b.num)

#        에러 발생    
#        print("\n(200, 119)")
#        x = FieldElement(200, prime)
#        y = FieldElement(119, prime)
#        a = FieldElement(0, prime)
#        b = FieldElement(7, prime)
#        p1 = Point(x, y, a, b)
#        print(p1)
#        print(p1.x.num, p1.y.num, p1.a.num, p1.b.num)

        print("\n(1, 193)")
        x = FieldElement(1, prime)
        y = FieldElement(193, prime)
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        p1 = Point(x, y, a, b)
        print(p1)
        print(p1.x.num, p1.y.num, p1.a.num, p1.b.num)

#       에러 발생
#        print("\n(42, 99)")
#        x = FieldElement(42, prime)
#        y = FieldElement(99, prime)
#        a = FieldElement(0, prime)
#        b = FieldElement(7, prime)
#        p1 = Point(x, y, a, b)
#        print(p1)
#        print(p1.x.num, p1.y.num, p1.a.num, p1.b.num)

    def exerciseTest2(self):
        print("********** 유한체에서 정의된 타원곡선 확인 **********")
        prime = 223
        a = FieldElement(0, prime) 
        b = FieldElement(7, prime)
        x = FieldElement(192, prime)
        y = FieldElement(105, prime)
        p1 = Point(x, y, a, b)
        print(p1)
        print(p1.x.num, p1.y.num, p1.a.num, p1.b.num)

    def test_on_curve(self):
        print("********** FieldElement와 Point를 함께 사용하여 타원곡성 생성 확인 **********")
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        valid_points = ((192, 105), (17, 56), (1, 193))
        invalid_points = ((200, 119), (42, 99))
        for x_raw, y_raw in valid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            Point(x, y, a, b)

        for x_raw, y_raw in invalid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            with self.assertRaises(ValueError):
                Point(x, y, a, b)

    def exerciseTest3(self):
        print("********** FieldElement로 초기화한 유한체에서의 점 덧셈 실행 결과 확인 **********")
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        x1 = FieldElement(192, prime)
        y1 = FieldElement(105, prime)
        x2 = FieldElement(17, prime)
        y2 = FieldElement(56, prime)
        p1 = Point(x1, y1, a, b)
        p2 = Point(x2, y2, a, b)
        result = p1 + p2
        print(result)
        print(result.x, result.y, result.a, result.b)
        print(result.x.num, result.y.num, result.a.num, result.b.num)

    def test_add(self):
        print("********** F223에 정의된 y**2 = x**3 + 7 위의 점들에 있는지 확인 **********")
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        valid_points = ((170, 142, 60, 139), (47, 71, 17, 56), (143, 98, 76, 66))
        for x1_raw, y1_raw, x2_raw, y2_raw in valid_points:
            x1 = FieldElement(x1_raw, prime)
            y1 = FieldElement(y1_raw, prime)
            x2 = FieldElement(x2_raw, prime)
            y2 = FieldElement(y2_raw, prime)
            p1 = Point(x1, y1, a, b)
            p2 = Point(x2, y2, a, b) 
            result = p1 + p2
            print(result.x.num, result.y.num, result.a.num, result.b.num)

    def exerciseTest4(self):
        print("********** F223에서 정의된 곡선 y**2 = x**3 +7에서 스칼라 곱셈을 확인 **********")
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        x = FieldElement(47, prime)
        y = FieldElement(71, prime)
        p = Point(x, y, a, b)
        for s in range(1, 21):
            result = s * p
            print('{}*(47,71)=({},{})'.format(s, result.x.num, result.y.num))

    def exerciseTest5(self):
        print("********** F223에서 정의된 곡선 y**2 = x**3 + 7 위 점 (15, 86)으로 생성된 군의 위수 확인 **********")
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        x = FieldElement(15, prime)
        y = FieldElement(86, prime)
        p = Point(x, y, a, b)
        result = 7 * p
        print(result.x, result.y)

    def test_rmul(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)

        multiplications = (
            # (coefficient, x1, y1, x2, y2)
            (2, 192, 105, 49, 71),
            (2, 143, 98, 64, 168),
            (2, 47, 71, 36, 111),
            (4, 47, 71, 194, 51),
            (8, 47, 71, 116, 55),
            (21, 47, 71, None, None),
        )

        for s, x1_raw, y1_raw, x2_raw, y2_raw in multiplications:
            x1 = FieldElement(x1_raw, prime)
            y1 = FieldElement(y1_raw, prime)
            p1 = Point(x1, y1, a, b)
            if x2_raw is None:
                p2 = Point(None, None, a, b)
            else:
                x2 = FieldElement(x2_raw, prime)
                y2 = FieldElement(y2_raw, prime)
                p2 = Point(x2, y2, a, b)

            self.assertEqual(s * p1, p2)

## 학습 과정에서 타원곡선 암호 예제 학습
run(EccTest("exerciseTest1"))
run(EccTest("exerciseTest2"))
run(EccTest("test_on_curve"))
run(EccTest("exerciseTest3"))
run(EccTest("test_add"))
run(EccTest("exerciseTest4"))
run(EccTest("exerciseTest5"))


## Point 객체 __rmul__()함수 실행 결과
run(EccTest("test_rmul"))
