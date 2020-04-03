from src.FieldElement import FieldElement
from src.Point import Point
from src.S256Field import S256Field
from lib.helper import hash160
from lib.helper import encode_base58
from lib.helper import encode_base58_checksum
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

    # 비압축 SEC 형식 직렬화 -> 0x04 + 공개키.x + 공개키.y
    # to_bytes() 함수는 정수형 숫자를 bytes형으로 변경
    # to_bytes(첫번째 매개변수, 두번째 매개변수)
    # 첫번째 매개변수 = bytes형 상수의 길이
    # 두번째 매개변수 = 빅엔디언('big'), 리틀엔디언('little')
    def sec(self, compressed = True):
        '''공개키 P = (x, y)에 대한 압축 SEC 형식의 표현방법 '''
        '''y값이 짝수면 0x02, 홀수면 0x03인 1바이트 접두부로 시작'''
        '''x좌표를 32바이트 빅엔디언 정수로 표시'''
        '''return the binary version of the SEC format'''
        if compressed:
            if self.y.num % 2 == 0:
                return b'\x02' + self.x.num.to_bytes(32, 'big')
            else:
                return b'\x03' + self.x.num.to_bytes(32, 'big')
        else:
            return b'\x04' + self.x.num.to_bytes(32, 'big') + self.y.num.to_bytes(32, 'big')

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


#@classmethod는 함수를 사용하기 전에 반드시 self(클래스 자체)를 첫번째 인자로 넣어줘야한다.
#클래스 자기 자신의 인자를 사용하기 위해서 사용하는 방법이다.
#직렬화된 SEC형식의 공개키가 있으면 이로부터 (x,y)를 반환하는 parse메서드가 작성
    @classmethod
    def parse(self, sec_bin):
        '''return a Point object from a SEC binary (not hex)'''
        if sec_bin[0] == 4:          # 비압축 SEC 형식은 순서대로 x,y를 읽어온다.
            x = int.from_bytes(sec_bin[1:33], 'big')
            y = int.from_bytes(sec_bin[33:65], 'big')
            return S256Point(x,y)
        is_even = sec_bin[0] == 2    # y값이 짝수일 경우 is_even은 true이다. 
        x = S256Field(int.from_bytes(sec_bin[1:], 'big'))
        # right side of the equation y**2 = x**3 + 7
        alpha = x**3 + S256Field(B)
        # solve for left side
        beta = alpha.sqrt()       # y값을 얻기 위해 타원곡선 방정식의 오른쪽 변의 제곱근
        if beta.num % 2 ==0:
            even_beta = beta
            odd_beta = S256Field(P - beta.num)
        else:
            even_beta = S256Field(P - beta.num)
            odd_beta = beta
        if is_even:
            return S256Point(x, even_beta)
        else:
            return S256Point(x, odd_beta) 

    def hash160(self, compressed=True):
        return hash160(self.sec(compressed))

# 비토코인 주소 생성
# 33바이트의 SEC형식을 20바이트로 상당히 줄이는 비트코인 주소를 생성하는 방법
# 1. 메인넷(Mainnet)주소는 0x00으로 시작, 테스트넷(Testnet)주소는 0x6f로 시작
# 2. 압축(compressed) 혹은 비압축(decompressed) SEC 형식 주소를 sha256 해시 함수를 넣고 다시 ripemd160 해시 함수에 넣어 출력한다. 2개의 해시함수를 적용하는 방법을 hash160이라고 한다. 
# 3. 1의 접두 바이트와 2의 최종 해시 결과를 합칩니다.
# 4. 3에서 얻은 결과를 hash256로 해시하고 그 결과에서 첫 4바이트를 취합니다.
# 5. 3의 결과 뒤에 4의 결과를 붙이고 이를 Base58으로 부호화합니다.
    def address(self, compressed=True, testnet=False):
        '''Returns the address string '''
        h160 = self.hash160(compressed)
        if testnet:
            prefix = b'\x6f'
        else:
            prefix = b'\x00'
        return encode_base58_checksum(prefix + h160)

