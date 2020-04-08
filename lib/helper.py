from unittest import TestSuite, TextTestRunner
import hashlib

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
SIGHASH_ALL = 1
SIGHASH_NONE = 2
SIGHASH_SINGLE = 3

def run(test):
    suite = TestSuite()
    suite.addTest(test)
    TextTestRunner().run(suite)

# sha256 해시는 hashlib.sha256(s).digest()로 얻고 이를 바로 ripemd160 해시함수의 입력으로 넘겨준다.
def hash160(s):
    '''sha256 followed by ripemd160'''
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()

def hash256(s):
    '''two rounds of sha256'''
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()

def sha256(s):
    return hashlib.sha256(s).digest()

def h160_to_p2pkh_address(h160, testnet=False):
    if testnet:
        prefix = b'\x6f'
    else:
        prefix = b'\x00'
    return encode_base58_checksum(prefix + h160)

def h160_to_p2sh_address(h160, testnet=False):
    if testnet:
        prefix = b'\xc4'
    else:
        prefix = b'\x05'
    return encode_base58_checksum(prefix + h160)

def encode_base58(s):
    count = 0
    for c in s:             # 몇 바이트가 0바이트인지 알 수 있다.
        if c == 0:
            count += 1
        else:
            break
    num = int.from_bytes(s, 'big')
    prefix = '1' * count
    result = ''
    while num > 0:
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result
    return prefix + result           # 맨 앞부분에 0으로 된 부분을 1으로 변경

def encode_base58_checksum(b):
    return encode_base58(b + hash256(b)[:4])

def decode_base58(s):
    num = 0
    for c in s:      # Base58로 표현된 주소를 for 루프로 통해 숫자로 변환
        num *= 58
        num += BASE58_ALPHABET.index(c)
    # 숫자를 25바이트 빅엔디언으로 해석된 bytes형 배열로 변환
    combined = num.to_bytes(25, byteorder = 'big')
    checksum = combined[-4:]
    if hash256(combined[:-4])[:4] != checksum:
        raise ValueError('bad address: {} {}'.format(checksum, hash256(combined[:-4])[:-4]))
# 중간의 20바이트를 공개키의 hash160 해시값으로 반환. 첫번째 바이트는 메인넷/테스트넷 표시 바이트이고 마지막 4바이트는 체크섬이다.
    return combined[1:-4]


'''little_endian_to_int는 byte값을 받아 little-endian 정수값으로 변환'''
def little_endian_to_int(b):
    '''return an integer '''
    return int.from_bytes(b, 'little')
  

'''endian_to_little_endian는 int값을 받아 little-endian bytes형으로 값을 반환 '''
def int_to_little_endian(n, length):
    '''return byte sequence'''
    return n.to_bytes(length, 'little')

'''
가변 정수 표현(Varints)
아래와 같은 규칙으로 0에서 2**64 -1사이의 정숫값을 표현합니다
  정수범위      |             Varints           |    예
0 ~ 252         | 1바이트로 표현                | 정수 100 -> 0x64(Varints표현)
253 ~ 2**16-1   | 접두부0xfd 이후 2바이트를     | 255->0xfdff00
                | 리틀엔디언으로 표현           | 555->0xfd2b02
2**16 ~ 2**32-1 | 접두부0xfe 이후 4바이트를     | 70015 -> 0xfe7f110110
                | 리틀엔디언으로 표현           |
2**32 ~ 2**64-1 | 접두부0xff 이후 8바이트를     | 18005558675309 -> 0xff6dc7ed3e60100000
                | 리틀엔디언으로 표현           |
'''
# read_varint()는 스트림으로부터 필요한 바이트 개수만큼 읽고 이를 정수로 반환
def read_varint(s):
    '''read_varint reads a variable integer from a stream'''
    i = s.read(1)[0]
    if i == 0xfd:
        #0xfd means the next two bytes are the number
        return little_endian_to_int(s.read(2))
    elif i == 0xfe:
        #0xfe means the next four bytes are the number
        return little_endian_to_int(s.read(4))
    elif i == 0xff:
        #0xff means the next eight bytes are the number
        return little_endian_to_int(s.read(8))
    else:
        # anything else is just the integer
        return i

# encode_varint()는 정수값을 읽어서 스트림으로 반환
def encode_varint(i):
    '''encodes an integer as a varint'''
    if i < 0xfd:
        return bytes([i])
    elif i < 0x10000:
        return b'\xfd' + int_to_little_endian(i, 2)
    elif i < 0x100000000:
        return b'\xfe' + int_to_little_endian(i, 4)
    elif i < 0x10000000000000000:
        return b'\xff' + int_to_little_endian(i, 8)
    else:
        raise ValueError('integer too large: {}'.format(i))

