from lib.helper import hash256
from lib.helper import int_to_little_endian
from lib.helper import little_endian_to_int
from lib.helper import encode_varint
from lib.helper import read_varint
from src.TxIn import TxIn
from src.TxOut import TxOut
from src.Script import Script
    
class Tx:
    def __init__(self, version, tx_ins, tx_outs, locktime, testnet=False):
        self.version = version
        self.tx_ins = tx_ins         # 입력 생성자의 인수 tx_ins를 초기화
        self.tx_outs = tx_outs       # 출력 생성자의 인수 tx_outs를 초기화
        self.locktime = locktime
        self.testnet = testnet       # 트랜잭션을 검증하기 위해서는 트랜잭션의 네트워크 설정 필요

    def __repr__(self):
        tx_ins = ''
        for tx_in in self.tx_ins:
            tx_ins += tx_in.__repr__() + '\n'
        tx_outs = ''
        for tx_out in self.tx_outs:
            tx_outs += tx_out.__repr__() + '\n'
        return 'tx: {}\nversion: {}\ntx_ins: {}\ntx_outs: {}\nlocktime: {}'.format(self.id(), self.version, tx_ins, tx_outs, self.locktime)

# id() 메서드는 트랜잭션 자체를 hash256 해시함수에 넣어 얻은 해시값을 16진수 형식으로 반환
# id() 메서드를 통해 얻은 값은 블록탐색기 등에서 트랜잭션을 탐색할 때 사용한다.
    def id(self): 
        '''Human-readable hexadecimal of the transaction hash '''
        return self.hash().hex()

# hash() 메서드는 트랜잭션 자체의 hash256 해시값을 반환한다.
# 해시값을 구하기 위해 먼저 serialize() 메서드를 통해 직렬화한다.
# 직렬화한 값을 hash256() 메서드에 넣은 후 해시값을 계산한다.
# 해시값을 리틀엔지언으로 읽은 값을 반환한다. 
#Binary hash of the legacy serialization
    def hash(self):
        return hash256(self.serialize())[::-1]

# 트랜잭션 파싱에 관한 내용
# parse 메서드는 Tx 클래스의 인스턴스를 반환하기 때문에 클래스 매서드
    @classmethod
    def parse(cls, s, testnet=False):
        version = little_endian_to_int(s.read(4))     # 현재 스트림 버퍼에 있는 4바이트를 읽어와 파싱 시작
        num_inputs = read_varint(s)
        inputs = []
        for _ in range(num_inputs):
            inputs.append(TxIn.parse(s))

        outputs = []
        num_outputs = read_varint(s)
        for _ in range (num_outputs):
            outputs.append(TxOut.parse(s))           
        locktime = little_endian_to_int(s.read(4))
        return cls(version, inputs, outputs, locktime, testnet=testnet)


# 주어진 트랜잭션 직렬화하기
    def serialize(self):
        result = int_to_little_endian(self.version, 4)      # 버전을 정수로 변경
        result += encode_varint(len(self.tx_ins))           # 트랜잭션 입력 개수를 가변정수로 변경 추가
        for tx_in in self.tx_ins:                           # 트랜잭션 입력 직렬화
            result += tx_in.serialize()
        result += encode_varint(len(self.tx_outs))          # 트랜잭션 출력 갯수를 가변정수로 변경 추가
        for tx_out in self.tx_outs:                         # 트랜잭션 출력 직렬화
            result += tx_out.serialize()
        result += int_to_little_endian(self.locktime, 4)    # locktime 직렬화
        # return bytes results(직렬화된 트랜잭션 객체)
        return result

    def is_coinbase(self):
        if len(self.tx_ins) != 1:
            return False
        first_input = self.tx_ins[0]
        if first_input.prev_tx != b'\x00' * 32:
            return False
        if first_input.prev_index != 0xffffffff:
            return False
        return True

    def coinbase_height(self):
        if not self.is_coinbase():
            return None
        element = self.tx_ins[0].script_sig.cmds[0]
        return little_endian_to_int(element)

# 비트코인 합의 규칙 : 모든 트랜잭션의 입력 합은 출력의 합보다 같거나 커야한다는 것
# 비트코인의 입력과 출력이 같은 경우는 거의 없다. 이유는 수수료때문이다.
# 수수료 = 입력의 합 - 출력의 합
# 수수료 계산
# 트랜잭션 입력에서 비트코인이 얼마나 들어있는지 알려주는 value()메서드를 통해 트랜잭션 수수료를 계산    
    def fee(self, testnet):
        input_sum = 0
        output_sum = 0
        for tx_in in self.tx_ins:
            input_sum += tx_in.value(testnet=testnet)
        for tx_out in self.tx_outs:
            output_sum += tx_out.amount
        return input_sum - output_sum


# 나머지 전체 트랜잭션의 검증
    def verify(self):
        if self.fee() < 0: # 수수료가 마이너스 값이 아닌 것을 확인해서 코인이 발행되지 않도록한다.
            return False
        for i in range(len(self.tx_ins)):
            if not self.verify_input(i):    # 각 입력이 올바른 해제 스크립트를 가지고 잇는지 확인
                return False
        return True

    def sig_hash(self, input_index, redeem_script=None):
        s = int_to_little_endian(self.version, 4)
        s += encode_varint(len(self.tx_ins))
        for i, tx_in in enumerate(self.tx_ins):
            if i == input_index:
                if redeem_script:
                    script_sig = reddem_script
                else:
                    script_sig = tx_in.script_pubkey(self.testnet)
            else:
                script_sig = None
            s += TxIn(
                prev_tx=tx_in.prev_tx,
                prev_index=tx_in.prev_index,
                script_sig=script_sig,
                sequence=tx_in.sequence,
            ).serialize()
        s += encode_varint(len(self.tx_outs))
        for tx_out in self.tx_outs:
            s += tx_out.serialize()
        s += int_to_little_endian(self.locktime, 4)
        s += int_to_little_endian(SIGHASH_ALL, 4)
        h256 = hash256(s)
        return int.from_bytes(h256, 'big')

    def verify_input(self, input_index):
        tx_in = self.tx_ins[input_index]
        script_pubkey = tx_in.script_pubkey(testnet=self.testnet)
        if script_pubkey.is_p2sh_script_pubkey():
            cmd = tx_in.script_sig.cmds[-1]
            raw_redeem = encode_varint(len(cmd)) + cmd
            redeem_script = Script.parse(BytesIO(raw_redeem))
        else:
            redeem_script = None
        z = self.sig_hash(input_index, redeem_script)
        combined = tx_in.script_sig + script_pubkey
        return combined.evaluate(z)

    def sign_input(self, input_index, private_key):
        z = self.sig_hash(input_index)
        der = private_key.sign(z).der()
        sig = der + SIGHASH_ALL.to_bytes(1, 'big')
        sec = private_key.point.sec()
        self.tx_ins[input_index].script_sig = Script([sig, sec])
        return self.verify_input(input_index)


