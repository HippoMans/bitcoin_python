import os
import sys

path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(os.path.abspath(path))

from unittest import TestCase
from lib.helper import run
from lib.helper import hash256
from src.FieldElement import FieldElement
from src.Point import Point
from src.S256Field import S256Field
from src.S256Point import S256Point, N
from src.Signature import Signature
from src.PrivateKey import PrivateKey
from src.Block import Block
from io import BytesIO



GENESIS_BLOCK = bytes.fromhex('0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c')

TESTNET_GENESIS_BLOCK = bytes.fromhex('0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4adae5494dffff001d1aa4ae18')

LOWEST_BITS = bytes.fromhex('ffff001d')


class BlockTest(TestCase):
    def exerciseTest1(self):
        block_raw = bytes.fromhex('020000208ec39428b17323fa0ddec8e887b4a7c53b8c0a0a220cfd0000000000000000005b0750fce0a889502d40508d39576821155e9c9e3f5c3157f961db38fd8b25be1e77a759e93c0118a4ffd71d')
        stream = BytesIO(block_raw)
        block = Block.parse(stream)
        print(block.version)
        print(block.prev_block)
        print(block.merkle_root)
        print(block.timestamp)
        print(block.bits)
        print(block.nonce)
        print(block.tx_hashes)
        # version
        self.assertEqual(block.version, 0x20000002)
        # prev_block
        prev = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfd\x0c"\n\n\x8c;\xc5\xa7\xb4\x87\xe8\xc8\xde\r\xfa#s\xb1(\x94\xc3\x8e'
        self.assertEqual(block.prev_block, prev)
        # merkle_root
        merkle = b'\xbe%\x8b\xfd8\xdba\xf9W1\\?\x9e\x9c^\x15!hW9\x8dP@-P\x89\xa8\xe0\xfcP\x07['
        self.assertEqual(block.merkle_root, merkle) 
        # timestamp
        time = 1504147230
        self.assertEqual(block.timestamp, time)
        # bits
        bit = b'\xe9<\x01\x18'
        self.assertEqual(block.bits, bit)
        # nonce 
        non = b'\xa4\xff\xd7\x1d'
        self.assertEqual(block.nonce, non)
        # tx_hashes 
        tx = None
        self.assertEqual(block.tx_hashes, tx)

    def test_serialize(self):
        block_raw = bytes.fromhex('020000208ec39428b17323fa0ddec8e887b4a7c53b8c0a0a220cfd0000000000000000005b0750fce0a889502d40508d39576821155e9c9e3f5c3157f961db38fd8b25be1e77a759e93c0118a4ffd71d')
        stream = BytesIO(block_raw)
        block = Block.parse(stream)
        result = block.serialize()
        print(result)
        block_serialize = b'\x02\x00\x00 \x8e\xc3\x94(\xb1s#\xfa\r\xde\xc8\xe8\x87\xb4\xa7\xc5;\x8c\n\n"\x0c\xfd\x00\x00\x00\x00\x00\x00\x00\x00\x00[\x07P\xfc\xe0\xa8\x89P-@P\x8d9Wh!\x15^\x9c\x9e?\\1W\xf9a\xdb8\xfd\x8b%\xbe\x1ew\xa7Y\xe9<\x01\x18\xa4\xff\xd7\x1d'
        self.assertEqual(result, block_serialize)

    def test_hash(self):
        block_raw = bytes.fromhex('020000208ec39428b17323fa0ddec8e887b4a7c53b8c0a0a220cfd0000000000000000005b0750fce0a889502d40508d39576821155e9c9e3f5c3157f961db38fd8b25be1e77a759e93c0118a4ffd71d')
        stream = BytesIO(block_raw)
        block = Block.parse(stream)
        result = block.hash()
        print(result)
        block_hash = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00~\x9eLXd9\xb0\xcd\xbe\x13\xb17\x0b\xdd\x945\xd7jdM\x04u#'
        self.assertEqual(result, block_hash)

    def test_bip9(self):
        block_raw = bytes.fromhex('020000208ec39428b17323fa0ddec8e887b4a7c53b8c0a0a220cfd0000000000000000005b0750fce0a889502d40508d39576821155e9c9e3f5c3157f961db38fd8b25be1e77a759e93c0118a4ffd71d')
        stream = BytesIO(block_raw)
        block = Block.parse(stream)
        result = block.version >> 29
        self.assertEqual(result, block.bip9())
        self.assertTrue(result)
        # 실패 경우
        block_raw = bytes.fromhex('0400000039fa821848781f027a2e6dfabbf6bda920d9ae61b63400030000000000000000ecae536a304042e3154be0e3e9a8220e5568c3433a9ab49ac4cbb74f8df8e8b0cc2acf569fb9061806652c27')
        stream = BytesIO(block_raw)
        block = Block.parse(stream)
        result = block.version >> 29
        self.assertEqual(result, block.bip9()) 
        self.assertFalse(result)

    def test_bip91(self):
        block_raw = bytes.fromhex('1200002028856ec5bca29cf76980d368b0a163a0bb81fc192951270100000000000000003288f32a2831833c31a25401c52093eb545d28157e200a64b21b3ae8f21c507401877b5935470118144dbfd1')
        stream = BytesIO(block_raw)
        block = Block.parse(stream)
        result = block.version >> 4 & 1
        self.assertEqual(result, block.bip91())
        self.assertTrue(result)
        block_raw = bytes.fromhex('020000208ec39428b17323fa0ddec8e887b4a7c53b8c0a0a220cfd0000000000000000005b0750fce0a889502d40508d39576821155e9c9e3f5c3157f961db38fd8b25be1e77a759e93c0118a4ffd71d')
        stream = BytesIO(block_raw)
        block = Block.parse(stream)
        result = block.version >> 4 & 1
        self.assertEqual(result, block.bip91())
        self.assertFalse(result)

    def test_bip141(self):
        block_raw = bytes.fromhex('020000208ec39428b17323fa0ddec8e887b4a7c53b8c0a0a220cfd0000000000000000005b0750fce0a889502d40508d39576821155e9c9e3f5c3157f961db38fd8b25be1e77a759e93c0118a4ffd71d')
        stream = BytesIO(block_raw)
        block = Block.parse(stream)
        result = block.version >> 1 & 1
        self.assertTrue(result, block.bip141())
        block_raw = bytes.fromhex('0000002066f09203c1cf5ef1531f24ed21b1915ae9abeb691f0d2e0100000000000000003de0976428ce56125351bae62c5b8b8c79d8297c702ea05d60feabb4ed188b59c36fa759e93c0118b74b2618')
        stream = BytesIO(block_raw)
        block = Block.parse(stream)
        result = block.version >> 1 & 1
        self.assertFalse(result, block.bip141())

    def test_difficulty(self):
        block_raw = bytes.fromhex('020000208ec39428b17323fa0ddec8e887b4a7c53b8c0a0a220cfd0000000000000000005b0750fce0a889502d40508d39576821155e9c9e3f5c3157f961db38fd8b25be1e77a759e93c0118a4ffd71d')     
        stream = BytesIO(block_raw)
        block = Block.parse(stream)
        result = block.difficulty()
        print(result)
        self.assertEqual(result, block.difficulty())

    def test_target(self):
        block_raw = bytes.fromhex('020000208ec39428b17323fa0ddec8e887b4a7c53b8c0a0a220cfd0000000000000000005b0750fce0a889502d40508d39576821155e9c9e3f5c3157f961db38fd8b25be1e77a759e93c0118a4ffd71d')
        stream = BytesIO(block_raw)
        block = Block.parse(stream)
        result = block.target()
        print(result)
        self.assertEqual(result, block.target())

    def test_check_pow(self):
        block_raw = bytes.fromhex('04000000fbedbbf0cfdaf278c094f187f2eb987c86a199da22bbb20400000000000000007b7697b29129648fa08b4bcd13c9d5e60abb973a1efac9c8d573c71c807c56c3d6213557faa80518c3737ec1')
        stream = BytesIO(block_raw)
        block = Block.parse(stream)
        result = block.check_pow()
        print(result)
        self.assertEqual(result, block.check_pow())

        block_raw = bytes.fromhex('04000000fbedbbf0cfdaf278c094f187f2eb987c86a199da22bbb20400000000000000007b7697b29129648fa08b4bcd13c9d5e60abb973a1efac9c8d573c71c807c56c3d6213557faa80518c3737ec0')
        stream = BytesIO(block_raw)
        block = Block.parse(stream)
        result = block.check_pow()
        print(result)
        self.assertEqual(result, block.check_pow())

    def test_validate_merkle_root(self):
        hashes_hex = [
            'f54cb69e5dc1bd38ee6901e4ec2007a5030e14bdd60afb4d2f3428c88eea17c1',
            'c57c2d678da0a7ee8cfa058f1cf49bfcb00ae21eda966640e312b464414731c1',
            'b027077c94668a84a5d0e72ac0020bae3838cb7f9ee3fa4e81d1eecf6eda91f3',
            '8131a1b8ec3a815b4800b43dff6c6963c75193c4190ec946b93245a9928a233d',
            'ae7d63ffcb3ae2bc0681eca0df10dda3ca36dedb9dbf49e33c5fbe33262f0910',
            '61a14b1bbdcdda8a22e61036839e8b110913832efd4b086948a6a64fd5b3377d',
            'fc7051c8b536ac87344c5497595d5d2ffdaba471c73fae15fe9228547ea71881',
            '77386a46e26f69b3cd435aa4faac932027f58d0b7252e62fb6c9c2489887f6df',
            '59cbc055ccd26a2c4c4df2770382c7fea135c56d9e75d3f758ac465f74c025b8',
            '7c2bf5687f19785a61be9f46e031ba041c7f93e2b7e9212799d84ba052395195',
            '08598eebd94c18b0d59ac921e9ba99e2b8ab7d9fccde7d44f2bd4d5e2e726d2e',
            'f0bb99ef46b029dd6f714e4b12a7d796258c48fee57324ebdc0bbc4700753ab1',
        ]
        hashes = [bytes.fromhex(x) for x in hashes_hex]
        block_raw = bytes.fromhex('00000020fcb19f7895db08cadc9573e7915e3919fb76d59868a51d995201000000000000acbcab8bcc1af95d8d563b77d24c3d19b18f1486383d75a5085c4e86c86beed691cfa85916ca061a00000000')
        stream = BytesIO(block_raw)
        block = Block.parse(stream)
        block.tx_hashes = hashes
        print(type(len(hashes_hex)))
        for i in range(0, len(hashes_hex)):
            print("block의 tx_hashes[",i,"] :") 
            print(block.tx_hashes[i])
        result = block.validate_merkle_root()
        print("merkle_root : ",result)
        self.assertTrue(block.validate_merkle_root())


# 타원곡선의 학습 과정에서 예제 실험
run(BlockTest("exerciseTest1"))
run(BlockTest("test_serialize"))
run(BlockTest("test_hash"))
run(BlockTest("test_bip9"))
run(BlockTest("test_bip91"))
run(BlockTest("test_bip141"))
run(BlockTest("test_difficulty"))
run(BlockTest("test_target"))
run(BlockTest("test_check_pow"))
run(BlockTest("test_validate_merkle_root"))
