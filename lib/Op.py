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

# 최상위 스택 값이 False가 아닌 경우 명령문이 실행됩니다. 상단 스택 값이 제거됩니다.
def op_if(stack, items):
    if len(stack) < 1:
        return False
    true_items = []
    false_items = []
    current_array = true_items
    found = False
    num_endifs_needed = 1                  # 조건을 사용할 때 if 닫는 endif가 필요한 숫자
    while len(items) > 0:
        item = items.pop(0)                # 첫번째 위치의 list값을 pop()
        if item in (99, 100):              # 입력 명령이 OP_IF와 OP_NOTIF인 경우 
            num_endifs_needed += 1
            current_array.append(item)
        elif num_endifs_needed == 1 and item == 103:   # 입력 명령이 OP_ELSE인 경우 -> 끝
            current_array = false_items
        elif item == 104:                  # 입력 명령이 OP_ENDIF인 경우
            if num_endifs_needed == 1:
                found = True
                break                      # if나 notif가 1개이면 endif가 1개로 설정 -> 끝
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

# 최상위 스택 값이 False이면 명령문이 실행됩니다. 상단 스택 값이 제거됩니다.
def op_notif(stack, items):
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
        items[:0] = true_items
    else:
        items[:0] = false_items
    return True

# 최상위 스택 값이 true가 아닌 경우 트랜잭션을 유효하지 않은 것으로 표시합니다. 상단 스택 값이 제거됩니다.
def op_verify(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    if decode_num(element) == 0:
        return False
    return True

# 거래를 유효하지 않은 것으로 표시합니다. 비트 코인 0.9 이후, 트랜잭션에 추가 데이터를 연결하는 표준 방법은 OP_RETURN과 그 뒤에 데이터로 구성된 scriptPubKey를 사용하여 값이 0 인 출력을 추가하는 것입니다. 이러한 출력은 UTXO 세트의 스토리지에서 지출이 불가능하고 특별히 버려 지므로 네트워크 비용이 줄어 듭니다. 0.12부터 표준 릴레이 규칙은 OP_RETURN 이후에 전체 scriptPubKey 길이가 최대 83 바이트 인 경우 OP_RETURN을 사용한 단일 출력을 허용합니다. 여기에는 OP_RETURN 이후의 모든 푸시 문 (또는 OP_RESERVED)이 포함됩니다.
def op_return(stack):
    return False


# 입력을 alt 스택의 맨 위에 놓습니다. 메인 스택에서 제거합니다.
def op_toaltstack(stack, altstack):
    if len(stack) < 1:
        return False
    altstack.append(stack.pop())
    return True

# 입력을 기본 스택의 맨 위에 놓습니다. alt스택에서 제거합니다.
def op_fromaltstack(stack, altstack):
    if len(altstack) < 1:
        return False
    stack.append(altstack.pop())
    return True

# 맨 위 두 개의 스택 항목을 제거합니다. 
def op_2drop(stack):
    if len(stack) < 2:
        return False
    stack.pop()
    stack.pop()
    return True

# 상위 2 개의 스택 항목을 복제합니다.
# append()는 object를 맨 뒤에 추가
# extend()는 iterable 객체(리스트, 튜플, 딕셔너리 등)의 엘레멘트를 list에 appending합니다.
def op_2dup(stack):
    if len(stack) < 2:
        return False
    stack.extend(stack[-2:])    
    return True

# 상위 3 개의 스택 항목을 복제합니다.
def op_3dup(stack):
    if len(stack) < 3:
        return False
    stack.extend(stack[-3:])
    return True

# 한 쌍의 항목을 스택의 앞뒤로 두 칸 복사합니다.
def op_2over(stack):
    if len(stack) < 4:
        return False
    stack.extend(stack[-4:-2])
    return True

# 5 번째와 6 번째 항목은 스택의 맨 위로 이동합니다.
def op_2rot(stack):
    if len(stack) < 6:
        return False
    stack.extend(stack[-6:-4])
    return True

# 상위 두 쌍의 항목을 교환합니다.
def op_2swap(stack):
    if len(stack) < 4:
        return False
    stack[-4:] = stack[-2:] + stack[-4:-2]
    return True

# 상단 스택 값이 0이 아니면 복제하십시오.
def op_ifdup(stack):
    if len(stack) < 1:
        return False
    if decode_num(stack[-1]) != 0:
        stack.append(stack[-1])
    return True

# 스택 항목 수를 스택에 넣습니다.
def op_depth(stack):
    stack.append(encode_num(len(stack)))
    return True

# 상단 스택 항목을 제거합니다.
def op_drop(stack):
    if len(stack) < 1:
        return False
    stack.pop()
    return True

# 상단 스택 항목을 복제합니다.
def op_dup(stack):
    if len(stack) < 1:
        return False
    stack.append(stack[-1])
    return True

# 끝에서 두 번째 항목을 제거합니다.
def op_nip(stack):
    if len(stack) < 2:
        return False
    stack[-2:] = stack[-1:]
    return True

# 맨 위에서 두 번째 값을 스택 항목을 맨 위에 복사합니다.
def op_over(stack):
    if len(stack) < 2:
        return False
    stack.append(stack[-2])
    return True

# 스택에 있는 항목에 stack의 개수 n을 맨 위로 복사됩니다.
def op_pick(stack):
    if len(stack) < 1:
        return False
    n = decode_num(stack.pop())
    if len(stack) < n + 1:
        return False
    stack.append(stack[-n -1])
    return True
 
# 스택에있는 항목에 stack의 개수 n을 맨위로 옮긴다.
def op_roll(stack):
    if len(stack) < 1:
        return False
    n = decode_num(stack.pop())
    if len(stack) < n + 1:
        return False
    if n == 0:
        return True
    stack.append(stack.pop(-n - 1))
    return True

# 스택의 상단 3 번째 값을 pop해서 그 값을 스택의 맨 위에 추가합니다.
def op_rot(stack):
    if len(stack) < 3:
        return False
    stack.append(stack.pop(-3))
    return True

# 스택의 상단 2번째 값을 pop해서 그 값을 스택의 맨 위에 추가합니다.
def op_swap(stack):
    if len(stack) < 2:
        return False
    stack.append(stack.pop(-2))
    return True

# 스택 맨 위에서 두 번째 값을 맨 위 항목에 복사되어 삽입합니다.
def op_tuck(stack):
    if len(stack) < 2:
        return False
    stack.insert(-2, stack[-1])
    return True

# 스택 맨 위 요소의 문자열 길이를 스택에 추가한다. (단, pop()가 없다.)
def op_size(stack):
    if len(stack) < 1:
        return False
    stack.append(encode_num(len(stack[-1])))
    return True

# stack의 상위 2개가 정확히 같으면 1을, 그렇지 않으면 0을 반환합니다.
def op_equal(stack):
    if len(stack) < 2:
        return False
    element1 = stack.pop()
    element2 = stack.pop()
    if element1 == element2:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True 

# op_equal()이 1이고 op_verify()이 1인 경우만 1이다.
def op_equalverify(stack):
    return op_equal(stack) and op_verify(stack)

#  stack의 맨 위 input을 +1하여 stack에 추가됩니다.
def op_1add(stack):
    if len(stack) < 1:
        return False
    element = decode_num(stack.pop())
    stack.append(encode_num(element + 1))
    return True

# stack의 맨 위 input을 -1하여 stack에 추가됩니다.
def op_1sub(stack):
    if len(stack) < 1:
        return False
    element = decode_num(stack.pop())
    stack.append(encode_num(element - 1))
    return True

# stack의 맨 위 input 값 부호를 변경합니다. 
def op_negate(stack):
    if len(stack) < 1:
        return False
    element = decode_num(stack.pop())
    stack.append(encode_num(-element))
    return True 

# stack의 맨 위 값을 절대값으로 변경합니다. 
def op_abs(stack):
    if len(stack) < 1:
        return False
    element = decode_num(stack.pop())
    if element < 0:
        stack.append(encode_num(-element))
    else:
        stack.append(encode_num(element))
    return True

# 입력이 0 또는 1이면 뒤집 힙니다. 그렇지 않으면 출력은 0이됩니다.
def op_not(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    if decode_num(element) == 0:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True

# 입력이 0이면 0을, 그렇지 않으면 1을 반환합니다. 
def op_0notequal(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    if decode_num(element) == 0:
        stack.append(encode_num(0))
    else:
        stack.append(encode_num(1))
    return True 

# stack의 상위 2개(a,b)를 더하여 stack에 추가됩니다.
def op_add(stack):
    if len(stack) < 2:
        return False
    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    stack.append(encode_num(element1 + element2))
    return True

# stack의 두번째 값 b에 첫번째 값 a를 해서 stack에 추가됩니다. 
def op_sub(stack):
    if len(stack) < 2:
        return False
    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    stack.append(encode_num(element2 - element1))
    return True

# a와 b가 모두 0이 아닌 경우 출력은 1입니다. 그렇지 않으면 0입니다.
def op_booland(stack):
    if len(stack) < 2:
        return False
    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    if element1 and element2:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True

# a 또는 b가 0이 아닌 경우 출력은 1입니다. 그렇지 않으면 0입니다.
def op_boolor(stack):
    if len(stack) < 2:
        return False
    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    if element1 or element2:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
  
# stack의 상위 2개(a,b)가 같으면 1이 stack에 들어가고, 다르면 0이 stack에 들어간다.
def op_numequal(stack):
    if len(stack) < 2:
        return False
    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    if element1 == element2:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True

# OP_NUMEQUAL()가 먼저 실행 된 후 같은 경우  OP_VERIFY를 실행하여 true이면 true를 return
def op_numequalverify(stack):
    return op_numequal(stack) and op_verify(stack)

# 숫자가 같지 않으면 1을, 그렇지 않으면 0을 반환합니다. 
def op_numnotequal(stack):
    if len(stack) < 2:
        return False
    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    if element1 == element2:
        stack.append(encode_num(0))
    else:
        stack.append(encode_num(1))
    return True

# stack의 최상위 값 a와 두번재 값 b를 비교한다. 이때 b가 a보다 작은 경우 1이고, 그렇지 않으면 0을 반환합니다.
def op_lessthan(stack):
    if len(stack) < 2:
        return False
    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    if element2 < element1:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True
 
# stack의 최상위 값 a와 두번재 값 b를 비교한다. 이때 a가 b보다 작은 경우 1이고, 그렇지 않으면 0을 반환합니다.
def op_greaterthan(stack):
    if len(stack) < 2:
        return False
    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    if element2 > element1:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True

# b가 a보다 작거나 같으면 1을, 그렇지 않으면 0을 반환합니다.
def op_lessthanorequal(stack):
    if len(stack) < 2:
        return False
    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    if element2 <= element1:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True

# b가 a보다 크거나 같으면 1을, 그렇지 않으면 0을 반환합니다.
def op_greaterthanorequal(stack):
    if len(stack) < 2:
        return False
    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    if element1 <= element2:
        stack.append(encode_num(element1))
    else:
        stack.append(encode_num(element2))
    return True

# a와 b 중 작은 값을 반환합니다.
def op_min(stack):
    if len(stack) < 2:
        return False
    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    if element1 < element2:
        stack.append(encode_num(element1))
    else:
        stack.append(encode_num(element2))
    return True

# a와 b 중 큰 값을 반환합니다.
def op_max(stack):
    if len(stack) < 2:
        return False
    element1 = decode_num(stack.pop())
    element2 = decode_num(stack.pop())
    if element1 > element2:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True

# element가 지정된 범위 내에 있으면 1을, 그렇지 않으면 0을 반환합니다.
# stack.pop()을 처음 한 것을 maximum으로 설정한다.
# stack.pop()을 두번째 한 것을 minimum으로 설정한다.
# stack.pop()을 세번째 한 것을 element로 하여 maximum과 minimum을 비교한다.
def op_within(stack):
    if len(stack) < 3:
        return False
    maximum = decode_num(stack.pop())
    minimum = decode_num(stack.pop())
    element = decode_num(stack.pop())
    if element >= minimum and element < maximum:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True

# RIPEMD-160을 사용하여 해시한 후 stack에 값을 대입합니다.
def op_ripemd160(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(hashlib.new('ripemd160', element).digest())
    return True

# sha-1을 사용하여 해시한 후 stack에 대입합니다.
def op_sha1(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(hashlib.sha1(element).digest())
    return True

# sha-256을 사용하여 해시한 후 stack에 대입합니다.
def op_sha256(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(hashlib.sha256(element).digest())
    return True


# 두 번 해시됩니다. 먼저 SHA-256을 사용한 다음 RIPEMD-160을 사용하여 stack에 대입합니다.
def op_hash160(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(hash160(element))
    return True

# SHA-256으로 두 번 해시한 후 stack에 대입합니다.
def op_hash256(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(hash256(element))
    return True

# 전체 트랜잭션의 출력, 입력 및 스크립트 (가장 최근에 실행 된 OP_CODESEPARATOR에서 끝까지)가 해시됩니다. OP_CHECKSIG에서 사용하는 서명은 해시 및 공개 키에 유효한 서명이어야합니다. a만약 값이 1이면 1이 반환되고 그렇지 않으면 0이 반환됩니다.
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

# OP_CHECKSIG와 동일하지만 나중에 OP_VERIFY가 실행됩니다.
def op_checksigverify(stack, z):
    return op_checksig(stack, z) and op_verify(stack) 

# ECDSA 일치를 찾을 때는 첫 번째 서명을 각 공개 키와 비교합니다. 후속 공개 키로 시작하여 ECDSA 일치를 찾을 때까지 두 번째 서명을 나머지  공개 키들과 비교합니다. 모든 서명이 확인되거나 충분한 공개 키가 남아있어 성공적인 결과를 얻을 때까지 프로세스가 반복됩니다. 모든 서명은 공개 키와 일치해야합니다. 공개 키는 서명 비교에 실패하면 다시 확인되지 않으므로 해당 공개 키가 scriptPubKey 또는 redeemScript에 배치 된 순서와 동일한 순서로 서명을 scriptSig에 배치해야합니다. 모든 서명이 유효하면 1이 반환되고 그렇지 않으면 0이 반환됩니다. 버그로 인해 스택에서 사용되지 않은 하나의 추가 값이 제거됩니다.
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

# OP_CHECKMULTISIG와 동일하지만 나중에 OP_VERIFY가 실행됩니다.
# op_checkmultisig()를 통해 true가 된 후 op_verify()가 true가 되어야 1이 된다.
def op_checkmultisigverify(stack, z):
    return op_checkmultisig(stack, z) and op_verify(stack)


# 최상위 스택 항목이 트랜잭션의 nLockTime 필드보다 큰 경우 트랜잭션을 유효하지 않은 것으로 표시합니다. 그렇지 않으면 OP_NOP가 실행 된 것처럼 스크립트 평가가 계속됩니다. 
# 1. 스택이 비어 있으면 트랜잭션도 유효하지 않습니다. 
# 2. 상단 스택 항목이 음수이거나 
# 3. 최상위 스택 항목이 500000000보다 크거나 같고 트랜잭션의 nLockTime 필드가 500000000보다 작거나 그 반대 인 경우
# 4. 입력의 nSequence 필드는 0xffffffff와 같습니다.
# 위 조건에 해당하면 op_checklocktimeverify()함수 false를 출력한다.
def op_checklocktimeverify(stack, locktime, sequence):
    if sequence == 0xffffffff:
        return False
    if len(stack) < 1:
        return False
    element = decode_num(stack[-1])
    if element < 0:
        return False
    if element < 500000000 and locktime > 500000000:
        return False
    if locktime <element:
        return False
    return True

# 입력의 상대 잠금 시간(relative lock time)이 상위 스택 항목의 값보다 크거나 같지 않으면 트랜잭션을 유효하지 않은 것으로 표시합니다.
def op_checksequenceverify(stack, version, sequence):
    if sequence & (1 << 31) == (1 << 31):
        return False
    if len(stack) < 1:
        return False
    element = decode_num(stack[-1])
    if element < 0:
        return False
    if element & (1 << 31) == (1 << 31):
        if version < 2:
            return False
        elif sequence & (1 << 31) == (1 << 31):
            return False
        elif element & (1 << 22) != sequence & (1 << 22):
            return False
        elif element & 0xffff > sequence & 0xffff:
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
    97: op_nop,
    99: op_if,
    100: op_notif,
    105: op_verify,
    106: op_return,
    107: op_toaltstack,
    108: op_fromaltstack,
    109: op_2drop,
    110: op_2dup,
    111: op_3dup,
    112: op_2over,
    113: op_2rot,
    114: op_2swap,
    115: op_ifdup,
    116: op_depth,
    117: op_drop,
    118: op_dup,
    119: op_nip,
    120: op_over,
    121: op_pick,
    122: op_roll,
    123: op_rot,
    124: op_swap,
    125: op_tuck,
    130: op_size,
    135: op_equal,
    136: op_equalverify,
    139: op_1add,
    140: op_1sub,
    143: op_negate,
    144: op_abs,
    145: op_not,
    146: op_0notequal,
    147: op_add,
    148: op_sub,
    154: op_booland,
    155: op_boolor,
    156: op_numequal,
    157: op_numequalverify,
    158: op_numnotequal,
    159: op_lessthan,
    160: op_greaterthan,
    161: op_lessthanorequal,
    162: op_greaterthanorequal,
    163: op_min,
    164: op_max,
    165: op_within,
    166: op_ripemd160,
    167: op_sha1,
    168: op_sha256,
    169: op_hash160,
    170: op_hash256,
    172: op_checksig,
    173: op_checksigverify,
    174: op_checkmultisig,
    175: op_checkmultisigverify,
    176: op_nop,
    177: op_checklocktimeverify,
    178: op_checksequenceverify,
    179: op_nop,
    180: op_nop,
    181: op_nop,
    182: op_nop,
    183: op_nop,
    184: op_nop,
    185: op_nop,
}

OP_CODE_NAMES = {
    0: 'OP_0',
    76: 'OP_PUSHDATA1',
    77: 'OP_PUSHDATA2',
    78: 'OP_PUSHDATA4',
    79: 'OP_1NEGATE',
    81: 'OP_1',
    82: 'OP_2',
    83: 'OP_3',
    84: 'OP_4',
    85: 'OP_5',
    86: 'OP_6',
    87: 'OP_7',
    88: 'OP_8',
    89: 'OP_9',
    90: 'OP_10',
    91: 'OP_11',
    92: 'OP_12',
    93: 'OP_13',
    94: 'OP_14',
    95: 'OP_15',
    96: 'OP_16',
    97: 'OP_NOP',
    99: 'OP_IF',
    100: 'OP_NOTIF',
    103: 'OP_ELSE',
    104: 'OP_ENDIF',
    105: 'OP_VERIFY',
    106: 'OP_RETURN',
    107: 'OP_TOALTSTACK',
    108: 'OP_FROMALTSTACK',
    109: 'OP_2DROP',
    110: 'OP_2DUP',
    111: 'OP_3DUP',
    112: 'OP_2OVER',
    113: 'OP_2ROT',
    114: 'OP_2SWAP',
    115: 'OP_IFDUP',
    116: 'OP_DEPTH',
    117: 'OP_DROP',
    118: 'OP_DUP',
    119: 'OP_NIP',
    120: 'OP_OVER',
    121: 'OP_PICK',
    122: 'OP_ROLL',
    123: 'OP_ROT',
    124: 'OP_SWAP',
    125: 'OP_TUCK',
    130: 'OP_SIZE',
    135: 'OP_EQUAL',
    136: 'OP_EQUALVERIFY',
    139: 'OP_1ADD',
    140: 'OP_1SUB',
    143: 'OP_NEGATE',
    144: 'OP_ABS',
    145: 'OP_NOT',
    146: 'OP_0NOTEQUAL',
    147: 'OP_ADD',
    148: 'OP_SUB',
    154: 'OP_BOOLAND',
    155: 'OP_BOOLOR',
    156: 'OP_NUMEQUAL',
    157: 'OP_NUMEQUALVERIFY',
    158: 'OP_NUMNOTEQUAL',
    159: 'OP_LESSTHAN',
    160: 'OP_GREATERTHAN',
    161: 'OP_LESSTHANOREQUAL',
    162: 'OP_GREATERTHANOREQUAL',
    163: 'OP_MIN',
    164: 'OP_MAX',
    165: 'OP_WITHIN',
    166: 'OP_RIPEMD160',
    167: 'OP_SHA1',
    168: 'OP_SHA256',
    169: 'OP_HASH160',
    170: 'OP_HASH256',
    171: 'OP_CODESEPARATOR',
    172: 'OP_CHECKSIG',
    173: 'OP_CHECKSIGVERIFY',
    174: 'OP_CHECKMULTISIG',
    175: 'OP_CHECKMULTISIGVERIFY',
    176: 'OP_NOP1',
    177: 'OP_CHECKLOCKTIMEVERIFY',
    178: 'OP_CHECKSEQUENCEVERIFY',
    179: 'OP_NOP4',
    180: 'OP_NOP5',
    181: 'OP_NOP6',
    182: 'OP_NOP7',
    183: 'OP_NOP8',
    184: 'OP_NOP9',
    185: 'OP_NOP10',
}


