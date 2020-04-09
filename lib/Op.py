import hashlib
from logging import getLogger
from src.S256Point import S256Point
from src.Signature import Signature
from lib.helper import hash160
from lib.helper import hash256

LOGGER = getLogger(__name__)

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

# 0을 스크립트 stack에 저장
def op_0(stack):
    stack.append(encode_num(0))
    return True

# -1을 스크립트 stack에 저장
def op_1negate(stack):
    stack.append(encode_num(-1))   
    return True 

# 1을 스크립트 stack에 저장
def op_1(stack):
    stack.append(encode_num(1))
    return True

# 2을 스크립트 stack에 저장
def op_2(stack):
    stack.append(encode_num(2))
    return True

# 3을 스크립트 stack에 저장
def op_3(stack):
    stack.append(encode_num(3))
    return True

# 4을 스크립트 stack에 저장
def op_4(stack):
    stack.append(encode_num(4))
    return True

# 5을 스크립트 stack에 저장
def op_5(stack):
    stack.append(encode_num(5))
    return True

# 6을 스크립트 stack에 저장
def op_6(stack):
    stack.append(encode_num(6))
    return True

# 7을 스크립트 stack에 저장
def op_7(stack):
    stack.append(encode_num(7))
    return True

# 8을 스크립트 stack에 저장
def op_8(stack):
    stack.append(encode_num(8))
    return True

# 9을 스크립트 stack에 저장
def op_9(stack):
    stack.append(encode_num(9))
    return True

# 10을 스크립트 stack에 저장
def op_10(stack):
    stack.append(encode_num(10))
    return True

# 11을 스크립트 stack에 저장
def op_11(stack):
    stack.append(encode_num(11))
    return True

# 12을 스크립트 stack에 저장
def op_12(stack):
    stack.append(encode_num(12))
    return True

# 13을 스크립트 stack에 저장
def op_13(stack):
    stack.append(encode_num(13))
    return True

# 14을 스크립트 stack에 저장
def op_14(stack):
    stack.append(encode_num(14))
    return True

# 15을 스크립트 stack에 저장
def op_15(stack):
    stack.append(encode_num(15))
    return True

# 16을 스크립트 stack에 저장
def op_16(stack):
    stack.append(encode_num(16))
    return True

# nop 또는 no operation은 어셈블리어명령에서 아무 일도 하지 않는다와 같은 의미이다.
def op_nop(stack):
    return True

# if()함수 
def op_if(stack, items):
    if len(stack) < 1:
        return False
    true_items = []
    false_items = []
    current_array = true_items
    found = False
    num_endifs_needed = 1
    while len(items) > 0:
        item = items.pop(0)
        if item in (99, 100):
            num_endifs_needed += 1
            current_array.append(item)
        elif num_endifs_needed == 1 and item == 103:
            current_array = false_items
        elif item == 104:
            if num_endifs_needed == 1:
                found = True
                break
            else:
                num_endifs_needed -= 1
                current_array.append(item)
        else:
            current_array.append(item)
    if not found:
        return False
    element = stack.pop()
    if decode_num(element) == 0:
        items[:0] = false_items
    else:
        items[:0] = true_items
    return True

    




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

OP_CODE_FUNCTIONS = {
    0: op_0,
    79: op_1negate,
    81: op_1,
    82: op_2,
    83: op_3,
    84: op_4,
    85: op_5,
    86: op_6,
    87: op_7,
    88: op_8,
    89: op_9,
    90: op_10,
    91: op_11,
    92: op_12,
    93: op_13,
    94: op_14,
    95: op_15,
    96: op_16,
    118: op_dup,
    169: op_hash160,
    170: op_hash256,
    172: op_checksig
    
}
