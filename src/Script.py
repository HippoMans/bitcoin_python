from lib.helper import little_endian_to_int
from lib.helper import read_varint
from lib.helper import int_to_little_endian
from lib.helper import encode_varint
from io import BytesIO
from src.Op import OP_CODE_FUNCTIONS #OP_CODE_NAMES

# 해시값을 p2pkh스크립트로 변환한다는 의미로 이 함수를 p2pkh_script라고 한다.
# 0x76은 OP_DUP
# 0xa9는 OP_HASH160
# h160은 인수로 주어진 20바이트 공개키 해시값
# 0x88은 OP_EQUALVERIFY
# 0xac는 OP_CHECKSIG
def p2pkh_script(h160):
    return Script([0x76, 0xa9, h160, 0x88, 0xac])

class Script:
    def __init__(self, cmds=None):
        if cmds is None:
            self.cmds = []
        else:
            self.cmds = cmds            # 각 명령어는 실행할 연산자이거나 스택에 올릴 원소

    @classmethod
    def parse(cls, s):
        length = read_varint(s)          # 스크립트 직렬화는 항상 전체 스크립트의 길이를 읽는 것으로 시작
        cmds = []
        count = 0
        while count < length:           # 정확히 전체 스크립트 길이만큼만 파싱
# 한 바이트를 읽습니다. 이를 통해 다음에 원소가 오는지 여부에 따라 연산자의 오피코드인지를 판단한다.
            current = s.read(1)
            count += 1
            current_byte = current[0]   # 파이썬의 bytes형 값을 int형으로 변환
            if current_byte >= 1 and current_byte <= 75:    # 1~75 범위의 숫자라면 다음 n바이트가 한 원소
                n = current_byte
                cmds.append(s.read(n))
                count += n
            elif current_byte == 76:    # 76은 OP_PUSHDATA1을 의미. 한 바이트를 더 읽어 파싱할 원소의 길이
                data_length = little_endian_to_int(s.read(1))
                cmds.append(s.read(data.length))
                count += data_length + 1
            elif current_byte == 77:    # 77은 OP_PUSHDATA2를 의미. 2바이트를 더 읽어 파싱할 원소의 길이 
                data_length = little_endian_to_int(s.read(2))
                cmds.append(s.read(data_length))
                count += data_lenght + 2
            else:                       # current_byte 자체가 오피코드입니다. 
                op_code = current_byte
                cmds.append(op_code)
        if count != length:             # 스크립트 파싱이 정확히 스크립트 시작 부분에서 설정된 길이 확인
            raise SyntaxError('parsing script failed')
        return cls(cmds)

    def raw_serialize(self):
        result = b''
        for cmd in self.cmds:
            if type(cmd) == int:        # 명령어가 정숫값이라면 연산자의 오피코드를 의미한다.
                result += int_to_little_endian(cmd, 1)
            else:
                length = len(cmd)
                # 길이가 1~75범위라면 그 길이를 1바이트로 표현
                if length < 75:
                    result += int_to_little_endian(length, 1)
                # 1~255범위라면 OP_PUSHDATA1을 삽입. 그리고 1바이트로 그 길이를 표현
                elif length > 75 and length < 0x100:
                    result += int_to_little_endian(76, 1)
                    result += int_to_little_endian(length, 1)
                # 256~520 범위라면 OP_PUSHDATA2를 삽입. 그리고 2바이트로 리틀엔디언으로 그 길이를 표현
                elif length >= 0x100 and length <= 520:
                    result += int_to_little_endian(77, 1)
                    result += int_to_little_endian(length, 2)
                # 520바이트를 초과하는 긴 원소는 직렬화될 수 없습니다.
                else:
                    raise ValueError('too long an cmd')
                result += cmd
        return result    

    # 직렬화
    def serialize(self):
        result = self.raw_serialize()
        total = len(result)
        return encode_varint(total) + result    # 직렬화된 스크립트의 길이을 앞에 위치한다.


    def __add__(self, other):
        return Script(self.cmds + other.cmds)


    def evaluate(self, z):
# 스크립트 명령집합 안에 명령어가 실행되면서 명령어가 하나씩 삭제되므로 스크립트 명령집합을 cmds변수에 복사하여 사용
        cmds = self.cmds[:]
        stack = []
        altstack = []
        while len(cmds) > 0:      # 모든 스크립트 명령어가 소진될 때까지 실행
            cmd = cmds.pop(0)
            if type(cmd) == int:
# OP_CODE_FUNCTIONS 배열은 오피코드에 해당하는 연산자를 내어줍니다. (OP_DUP, OP_CHECKSIG) 
                operation = OP_CODE_FUNCTIONS[cmd]
                if cmd in (99, 100):   # 99와 100은 각각 OP_IF와 OP_NOTIF에 해당하는 오피코드
                    if not operation(stack, cmds):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
                elif cmd in (107, 108): #OP_TOALTSTACK과 OP_FROMALTSTACK에 해당하는 오피코드
                    if not operation(stack, altstack):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
# OP_CHECKSIG, OP_CHECKSIGVERIFY, OP_CHECKMULTISIG, OP_CHECKMULTISIGVERIFY에 해당하는 오피코
                elif cmd in (172, 173, 174, 175):
                    if not operation(stack, z):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
                else:
                    if not operation(stack):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
            else:
                stack.append(cmd)    # 명령어가 원소라면 스택 위에 올립니다.
                if len(cmds) == 3 and cmds[0] == 0xa9 and type(cmds[1]) == bytes and len(cmds[1]) == 20 and cmds[2] == 0x87:
                cmds.pop()
                h160 = cmds.pop()
                cmds.pop()
                if not op_hash160(stack):
                    return False
                stack.append(h160)
                if not op_equal(stack):
                    return False
                if not op_verify(stack):
                    LOGGER.info('bad p2sh h160')
                    return False
                redeem_script = encode_varint(len(cmd)) + cmd
                stream = BytesIO(redeem_script)
                cmds.extend(Script.parse(stream).cmds)
# 모든 명령어를 실행한 후 스택이 비어있으면 스크립트 유효성 실패의 의미로 False 반환
        if len(stack) == 0:
            return False 
# 스택의 최상위 원소가 공 바이트(b '')이면 역시 스크립트 유효성 실패로 False 반환
        if stack.pop() == b'':
            return False
        return True     # 스크립트가 유효한 경우로 True를 반환


