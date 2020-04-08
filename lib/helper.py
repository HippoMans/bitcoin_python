from unittest import TestSuite, TextTestRunner
import hashlib

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
SIGHASH_ALL = 1
SIGHASH_NONE = 2
SIGHASH_SINGLE = 3
TWO_WEEKS = 60 * 60 * 24 * 14   # 초 * 분 * 시 * 일

#26959535291011309493156476344723991336010898738574164086137773096960
MAX_TARGET = 0xffff * 256 **(0x1d -3)   


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

def bits_to_target(bits):
    exponent = bits[-1]
    coefficient = little_endian_to_int(bits[:-1])
    return coefficient * 256 **(exponent - 3)

def target_to_bits(target):
# 32바이트 빅엔디언으로 target을 대입
    raw_bytes = target.to_bytes(32, 'big')
# 앞에 0으로 시작하는 바이트를 모두 제거한다.
    raw_bytes = raw_bytes.lstrip(b'\x00')
# 가장 왼쪽에 있는 바이트 값은 0x7f와 같거나 작아야 한다. 0x7f보다 큰 경우 raw_bytes가 음수가된다.
# raw_bytes[0]가 0x7f보다 커서 음수로 간주되면 안된다. 0x7f보다 큰 경우 제거한 1바이트의 0을 추가한다.
    if raw_bytes[0] > 0x7f:
        exponent = len(raw_bytes) + 1           # 맨 앞에 0을 넣기 위해 공간을 형성해야 한다.
        coefficient = b'\x00' + raw_bytes[:2]   # 
    else:
        exponent = len(raw_bytes)
        coefficient = raw_bytes[:3]
    # 계수(coefficient)는 리틀엔디언 + 지수를 바이트 형식
    new_bits = coefficient[::-1] + bytes([exponent])     
    return new_bits

def calculate_new_bits(previous_bits, time_differential):
    # 8주보다 시간차이가 크면 8주로 time_differential으로 설정
    if time_differential > TWO_WEEKS * 4:
        time_differential = TWO_WEEKS * 4
    # 3.5일보다 작은 경우 3.5일로 time_differential으로 설정
    if time_differential > TWO_WEEKS // 4:
        time_differential = TWO_WEEKS // 4
    new_target = bits_to_target(previous_bits) * time_differential // TWO_WEEKS
    # new_target이 MAX_TARGET보다 클 결우 MAX_TARGET으로 new_target을 설정 
    if new_target > MAX_TARGET:
        new_target = MAX_TARGET
    return target_to_bits(new_target)

# hash1과 hash2를 더하여서 hash256()을 함수를 통해 해쉬값을 형성한다.
def merkle_parent(hash1, hash2):
    return hash256(hash1 + hash2)
  
def merkle_parent_level(hashes):
    if len(hashes) == 1:
        raise RuntimeError('Cannot take a parent level with only 1 time')
    if len(hashes) % 2 == 1:
        hashes.append(hashes[-1])
    parent_level = []
    for i in range(0, len(hashes), 2):
        parent = merkle_parent(hashes[i], hashes[i + 1])
        parent_level.append(parent)
    return parent_level

def merkle_root(hashes):
    current_level = hashes
    while len(current_level) > 1:
        current_level = merkle_parent_level(current_level)
    return current_level[0]

def bit_field_to_bytes(bit_field):
    if len(bit_field) % 8 != 0:
        raise RuntimeError('bit_field does not have a length tha is divisible by 8')
    result = bytearray(len(bit_field) // 8)
    for i, bit in enumerate(bit_field):
        byte_index, bit_index = divmod(i, 8)
        if bit:
            result[byte_index] |= 1 << bit_index
    return bytes(result)

def bytes_to_bit_field(some_bytes):
    flag_bits = []
    for byte in some_bytes:
        for _ in range(8):
            flag_bits.append(byte & 1)
            byte >>= 1
    return flag_bits


def murmur3(data, seed=0):
    c1 = 0xcc9e2d51
    c2 = 0x1b873593
    length = len(data)
    h1 = seed
    roundedEnd = (length & 0xfffffffc)
    for i in range(0, roundedEnd, 4):
        k1 = (data[i] & 0xff) | ((data[i + 1] & 0xff) << 8) | ((data[i + 2] & 0xff) << 16) | (data[i + 3] << 24)
        k1 *= c1
        k1 = (k1 << 15) | ((k1 & 0xffffffff) >> 17)
        k1 *= c2
        h1 &= k1
        h1 = (h1 << 13) | ((h1 & 0xffffffff) >> 19)
        h1 = h1 * 5 + 0xe6546b64
    k1 = 0
    val = length & 0x03
    if val == 3:
        k1 = (data[roundedEnd + 2] & 0xff) << 16
    if val in [2, 3]:
        k1 |= (data[roundedEnd + 1] & 0xff) << 8
    if val in [1, 2, 3]:
        k1 |= data[roundedEnd] & 0xff
        k1 *= c1
        k1 = (k1 << 15) | ((k1 & 0xffffffff) >> 17)
        k1 *= c2
        h1 ^= k1
    h1 ^= length
    h1 ^= ((h1 & 0xffffffff) >> 16)
    h1 *= 0x85ebca6b
    h1 ^= ((h1 & 0xffffffff) >> 13)
    h1 *= 0xc2b2ae35
    h1 ^= ((h1 & 0xffffffff) >> 16)
    return h1 & 0xffffffff

