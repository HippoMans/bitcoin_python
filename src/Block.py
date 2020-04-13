from lib.helper import little_endian_to_int
from lib.helper import int_to_little_endian
from lib.helper import hash256
from lib.byte_helper import bits_to_target
from lib.merkle_helper import merkle_root

class Block:
    def __init__(self, version, prev_block, merkle_root, timestamp, bits, nonce, tx_hashes=None):
        self.version = version
        self.prev_block = prev_block
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = nonce
        self.tx_hashes = tx_hashes

    # byte stream 형식과 블록을 파싱한다.
    @classmethod
    def parse(cls, s):
        # s.read(4) 형식은 4바이트를 stream형식으로 리턴한다.
        # version은 4bytes로 little endian을 byte형식으로 변환한다. 
        version = little_endian_to_int(s.read(4))
        # little_endian형식으로 32bytes로 출력 (배열이 -1임으로 역으로 전환하여 prev_block에 입력)
        prev_block = s.read(32)[::-1]
        # little_endian형식으로 32bytes로 출력 (배열이 -1임으로 역으로 전환하여 merkle_root에 입력)
        merkle_root = s.read(32)[::-1]
        # s.read(4)으로 4bytes를 stream으로 변환하여 little_endian형식으로 timestamp에 저장
        timestamp = little_endian_to_int(s.read(4))
        # bits는 4bytes이다.
        bits = s.read(4)
        # nonce는 4bytes이다.
        nonce = s.read(4)
        # block의 객체를 리턴
        return cls(version, prev_block, merkle_root, timestamp, bits, nonce)

    def serialize(self):
        # version의 4bytes를 result에 저장한다. 이때 저장되는 형식은 little_endian이다.
        result = int_to_little_endian(self.version, 4)
        # prev_block의 32bytes를 result에 저장한다. 이때 저장되는 형식은 little_endian이다.
        result += self.prev_block[::-1]
        # merkle_root의 32bytes를 result에 저장한다. 이때 저장되는 형식은 little_endian이다.
        result += self.merkle_root[::-1]
        # timestamp는 4bytes를 result에 저장한다. 이때 저자오디는 형식은 little_endian이다.
        result += int_to_little_endian(self.timestamp, 4)
        # bits는 4bytes를 result에 저장한다.
        result += self.bits
        # nonce는 4bytes를 result에 저장한다.
        result += self.nonce
        return result

    def hash(self):
        s = self.serialize()
        sha = hash256(s)    
        return sha[::-1]

# BIP9은 오른족에 있는 29개의 비트를 오른쪽으로 밀어 버리고 맨 왼쪽 3개의 비트만 남겼습니다.
# 그 후 0b001과 같은지 확인한다. 
    def bip9(self):
        return self.version >> 29 == 0b001

# BIP91은 오른쪽에 있는 4개의 비트를 오른쪽으로 밀어버리고 1비트를 사용하는지 확인한다.
    def bip91(self):
        return self.version >> 4 & 1 == 1

# BIP141은 오른쪽에 있는 1개의 비트를 오른쪽으로 밀어버리고 1비트를 사용하는지 확인한다.
    def bip141(self):
        return self.version >> 1 & 1 == 1

# lowest difficulty은 0xffff001d입니다.
    def difficulty(self):
        lowest = 0xffff * 256**(0x1d - 3)
        return lowest / self.target()

# 블록을 직렬화하여 hash256 해시값을 만들어서 little_endian으로 변경한다.
# proof가 target()보다 작아야만 POW에 참(1)이 나온다.
    def check_pow(self):
        sha = hash256(self.serialize())
        proof = little_endian_to_int(sha)
        return proof < self.target()

# POW의 target을 결정하는 target함수 
    def target(self):
        return bits_to_target(self.bits)

# tx_hashes에서 h를 역순으로 하여 hashes에 가져온다.
# 그 후 merkle_root를 hashes에 넣어서 root값에 대입한다.
# merkle_root가 root와 같은 경우 true가 된다.
    def validate_merkle_root(self):
        hashes = [h[::-1] for h in self.tx_hashes]
        root = merkle_root(hashes)[::-1]
        return root == self.merkle_root    
