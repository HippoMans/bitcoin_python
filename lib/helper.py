from unittest import TestSuite, TextTestRunner

import hashlib


def run(test):
    suite = TestSuite()
    suite.addTest(test)
    TextTestRunner().run(suite)


def hash256(s):
    '''two rounds of sha256'''
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()


# sha256 해시는 hashlib.sha256(s).digest()로 얻고 이를 바로 ripemd160 해시함수의 입력으로 넘겨준다.
def hash160(s):
    '''sha256 followed by ripemd160'''
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()


BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

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
