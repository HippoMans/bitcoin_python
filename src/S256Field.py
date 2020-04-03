from src.FieldElement import FieldElement
from src.Point import Point

P = 2**256 - 2 ** 32 - 977

#FieldElement 클래스를 상속받는다. -> S256Field는 FieldElement의 자식 클래스
class S256Field(FieldElement):
    def __init__(self, num, prime = None):
        super().__init__(num, prime = P)

#2진수로 2**256 -> 16 ** 64 : 16진수로 64자리이고, 빈 자리를 b'0'으로 채운다.
    def __repr__(self):
        return '{:x}'.format(self.num).zfill(64)

# P % 4 = 3임으로 (P + 1) % 4 = 0이 된다. 
# (P + 1) // 4 = 정수가 됨으로 
# y ** 2 = x -> y = x ** ((P-1) // 4)
    def sqrt(self):
        return self**((P + 1) // 4)     # 제곱값을 가져 나온다.
