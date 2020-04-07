from src.S256Point import S256Point
from src.Signature import Signature

def encode_num(num):
    if num == 0:
        return b''
    abs_num = abs(num)         # 절대값
    negative = num < 0         # num이 음수이면 negative는 true이다. num이 양수이면 negative는 False이다.
    result = bytearray()       # 빈 바이트 배열 객체를 생성
    while abs_num:
        result.append(abs_num & 0xff)
        abs_num >>= 8
    if result[-1] & 0x80:
        if negative:
            result.append(0x80)
        else:
            result.append(0)
    elif negative:
        result[-1] |= 0x80
    return bytes(result)

def decode_num(element):
    if element == b'':
        return 0
    big_endian = element[::-1]
    if big_endian[0] & 0x80:
        negative = True
        result = big_endian[0] & 0x7f
    else:
        negative = False
        result = big_endian[0]
    for c in big_endian[1:]:
        result <<= 8
        result += c
    if negative:
        return -result
    else:
        return result

def op_dup(stack):
    if len(stack) < 1:
        return False
    stack.append(stack[-1])
    return True

def op_hash160(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(hash160(element))
    return True


def op_hash256(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(hash256(element))
    return True

def op_checksig(stack, z):
    if len(stack) < 2:
        return False
    sec_pubkey = stack.pop()
    der_signature = stack.pop()[:-1]
    try:
        point = S256Point.parse(sec_pubkey)
        sig = Signature.parse(der_signature)
    except (ValueError, SyntaxError) as e:
        return False
    if point.verify(z, sig):
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True

def op_checkmultisig(stack, z):
    if len(stack) < 1:
        return False
    n = decode_num(stack.pop())
    if len(stack) < n + 1:
        return False
    sec_pubkeys = []
    for _ in range(n):
        sec_pubkeys.append(stack.pop())
    m = decode_num(stack.pop())
    if len(stack) < m + 1:
        return False
    der_signatures = []
    for _ in range(m):
# 각 DER 서명은 해시유형 SIGHASH_ALL로 서명된 것으로 간주 
       der_signatures.append(stack.pop()[:-1])
# off-by-one 버그와 같이 스택 위에서 원소 하나를 더 가져오고 아무 일도 하지 않는다.
    stack.pop()
    try:
        points = [S256Point.parse(sec) for sec in sec_pubkeys]
        sigs = [Signature.parse(der) for der in der_signatures]
        for sig in sigs:
            if len(points) == 0:
                return False
            while points:
                point = points.pop(0)
                if point.verify(z, sig):
                    break
        stack.append(encode_num(1))
    except (ValueError, SyntaxError):
        return False
    return True

def op_0(stack):
    stack.append(encode_num(0))
    return True

OP_CODE_FUNCTIONS = {
      0: op_0,
    118: op_dup,
    169: op_hash160,
    170: op_hash256,
    172: op_checksig
    
}
