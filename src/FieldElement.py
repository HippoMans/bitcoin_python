class FieldElement:
#FieldElement 객체에 내부값을 초기화(생성자)
    def __init__(self, num, prime):
        if num >= prime or num < 0:
            error = 'Num {} not in filed range 0 to {}'.format(num, prime-1)
            raise ValueError(error)
        self.num = num
        self.prime = prime

#어떤 객체를 인자로 하면 객체의 클래스에 정의된 __repr__를 실행하여 출력
    def __repr__(self):
        return 'FieldElement_{}({})'.format(self.prime, self.num)

#두 객체가 같은지 확인
    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime

#두 객체가 다른지 확인
    def __ne__(self, other):
        if other is None:
            return False
        return not (self == other)

#두 객체의 합
    def __add__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot add two numbers in different Fields')
        num = (self.num + other.num) % self.prime
        return self.__class__(num, self.prime)

#두 객체의 차
    def __sub__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot add two numbers in different Fields')
        num = (self.num - other.num) % self.prime
        return self.__class__(num, self.prime)

#두 객체의 곱
    def __mul__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot add two numbers in different Fields')
        num = (self.num * other.num) % self.prime
        return self.__class__(num, self.prime)

#두 객체의 제곱
    def __pow__(self, exponent):
        n = exponent % (self.prime - 1)
        num = pow(self.num, n, self.prime)
        return self.__class__(num, self.prime)

#두 객체의 나누기
    def __truediv__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot add two numbers in different Fields')
        num = self.num * pow(other.num, self.prime -2, self.prime) % self.prime
        return self.__class__(num, self.prime)

#int와 객체의 곱(서로 다른 type을 곱하기 위해)
    def __rmul__(self, coefficient):
        num = (self.num * coefficient) % self.prime
        return self.__class__(num, self.prime)
