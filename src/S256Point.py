from src.FieldElement import FieldElement
from src.Point import Point
from src.S256Field import S256Field

A = 0
B = 7
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

# secp256k1 곡선 위 점인 공개키 P와 서명키 z로 주어진 2개의 정보에서 서명(r,s)이 유효한지 검증

class S256Point(Point):
    def __init__(self, x, y, a = None, b = None):
        a = S256Field(A)
        b = S256Field(B)
        if type(x) == int:
            X = S256Field(x)
            Y = S256Field(y)
            super().__init__(X, Y, a, b)
        else:
            super().__init__(x, y, a, b)

    def verify(self, G, z, sig):
        # 군의 위수이며 소수인 N(=n)을 페르마의 소정리를 적용하여 s_inv(=1/s)를 계산
        s_inv = pow(sig.s, N-2, N)
        # u = z/s군의 위수인 N으로 나머지 연산(%)을 적용
        u = (z * s_inv) % N
        # v = r/s군의 위수인 N으로 나머지 연산(%)을 적용
        v = (sig.r * s_inv) % N
        # total(=u*G + v*P)은 sig.r(=R)와 같아야 한다.
        total = (u * G + v * self)
        # total.x.num(=x)좌표가 sig.r(=r)와 같은지 확인 검증
        return total.x.num == sig.r

    def __rmul__(self, coefficient):
        coef = coefficient % N
        return super().__rmul__(coef)
