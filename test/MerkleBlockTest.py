import os
import sys

path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(os.path.abspath(path))

from unittest import TestCase
from lib.helper import run
from lib.helper import hash256
from lib.helper import little_endian_to_int
from lib.byte_helper import bytes_to_bit_field
from io import BytesIO
from src.MerkleBlock import MerkleBlock


class MerkleBlockTest(TestCase):
    def Test_parse(self):
        hex_merkle_block = '00000020df3b053dc46f162a9b00c7f0d5124e2676d47bbe7c5d0793a500000000000000ef445fef2ed495c275892206ca533e7411907971013ab83e3b47bd0d692d14d4dc7c835b67d8001ac157e670bf0d00000aba412a0d1480e370173072c9562becffe87aa661c1e4a6dbc305d38ec5dc088a7cf92e6458aca7b32edae818f9c2c98c37e06bf72ae0ce80649a38655ee1e27d34d9421d940b16732f24b94023e9d572a7f9ab8023434a4feb532d2adfc8c2c2158785d1bd04eb99df2e86c54bc13e139862897217400def5d72c280222c4cbaee7261831e1550dbb8fa82853e9fe506fc5fda3f7b919d8fe74b6282f92763cef8e625f977af7c8619c32a369b832bc2d051ecd9c73c51e76370ceabd4f25097c256597fa898d404ed53425de608ac6bfe426f6e2bb457f1c554866eb69dcb8d6bf6f880e9a59b3cd053e6c7060eeacaacf4dac6697dac20e4bd3f38a2ea2543d1ab7953e3430790a9f81e1c67f5b58c825acf46bd02848384eebe9af917274cdfbb1a28a5d58a23a17977def0de10d644258d9c54f886d47d293a411cb6226103b55635'
        block = MerkleBlock.parse(BytesIO(bytes.fromhex(hex_merkle_block)))
        print("version : ", block.version)
        print("prev_vlock : ", block.prev_block.hex())
        print("merkle_root : ", block.merkle_root.hex())
        print("timestamp : ", block.timestamp)
        print("bits : ", block.bits.hex())
        print("nonce : ", block.nonce.hex())
        print("total : ", block.total)
        print("hashes")
        for i in range(0, len(block.hashes)):
            print(block.hashes[i].hex())
        print("flags : ", block.flags.hex())

        print("\nMerkle Block")
        mblock = MerkleBlock.parse(BytesIO(bytes.fromhex(hex_merkle_block)))

        print("MerkleBlock versoin : ", mblock.version)
        version = 0x20000000
        self.assertEqual(mblock.version, version)

        print("MerkleBlock prev_block : ", mblock.prev_block.hex())
        prev_block = '00000000000000a593075d7cbe7bd476264e12d5f0c7009b2a166fc43d053bdf'
        self.assertEqual(mblock.prev_block.hex(), prev_block)

        print("MerkleBlock merkle_root : ", mblock.merkle_root.hex())
        merkle_root_hex = 'ef445fef2ed495c275892206ca533e7411907971013ab83e3b47bd0d692d14d4'
        merkle_root = bytes.fromhex(merkle_root_hex)[::-1]
        self.assertEqual(mblock.merkle_root, merkle_root)

        print("MerkleBlock timestamp : ", mblock.timestamp)
        timestamp = little_endian_to_int(bytes.fromhex('dc7c835b'))
        self.assertEqual(mblock.timestamp, timestamp)


        print("MerkleBlock bits : ", mblock.bits.hex())
        bits = bytes.fromhex('67d8001a')
        self.assertEqual(mblock.bits, bits)


        print("MerkleBlock nonce : ", mblock.nonce.hex())
        nonce = bytes.fromhex('c157e670')
        self.assertEqual(mblock.nonce, nonce)

        print("MerkleBlock total : ", mblock.total)
        total = little_endian_to_int(bytes.fromhex('bf0d0000'))
        self.assertEqual(mblock.total, total)

        print("\nMerkleBlock hashes : ")
        for i in range(0, len(mblock.hashes)):
            print("hashes{} : {}".format(i, mblock.hashes[i].hex()))

        hex_hashes = [
            'ba412a0d1480e370173072c9562becffe87aa661c1e4a6dbc305d38ec5dc088a',
            '7cf92e6458aca7b32edae818f9c2c98c37e06bf72ae0ce80649a38655ee1e27d',
            '34d9421d940b16732f24b94023e9d572a7f9ab8023434a4feb532d2adfc8c2c2',
            '158785d1bd04eb99df2e86c54bc13e139862897217400def5d72c280222c4cba',
            'ee7261831e1550dbb8fa82853e9fe506fc5fda3f7b919d8fe74b6282f92763ce',
            'f8e625f977af7c8619c32a369b832bc2d051ecd9c73c51e76370ceabd4f25097',
            'c256597fa898d404ed53425de608ac6bfe426f6e2bb457f1c554866eb69dcb8d',
            '6bf6f880e9a59b3cd053e6c7060eeacaacf4dac6697dac20e4bd3f38a2ea2543',
            'd1ab7953e3430790a9f81e1c67f5b58c825acf46bd02848384eebe9af917274c',
            'dfbb1a28a5d58a23a17977def0de10d644258d9c54f886d47d293a411cb62261',
        ]
        hashes = [bytes.fromhex(x)[::-1] for x in hex_hashes]
        self.assertEqual(mblock.hashes, hashes)

        print("MerkleBlock flags : ", mblock.flags.hex())
        flags = bytes.fromhex('b55635')
        self.assertEqual(mblock.flags, flags)


# Test_is_valid에서 is_valid()가 오류가 있다. 반드시 확인해야 한다.

#    def Test_is_valid(self):
#        hex_merkle_block = '00000020df3b053dc46f162a9b00c7f0d5124e2676d47bbe7c5d0793a500000000000000ef445fef2ed495c275892206ca533e7411907971013ab83e3b47bd0d692d14d4dc7c835b67d8001ac157e670bf0d00000aba412a0d1480e370173072c9562becffe87aa661c1e4a6dbc305d38ec5dc088a7cf92e6458aca7b32edae818f9c2c98c37e06bf72ae0ce80649a38655ee1e27d34d9421d940b16732f24b94023e9d572a7f9ab8023434a4feb532d2adfc8c2c2158785d1bd04eb99df2e86c54bc13e139862897217400def5d72c280222c4cbaee7261831e1550dbb8fa82853e9fe506fc5fda3f7b919d8fe74b6282f92763cef8e625f977af7c8619c32a369b832bc2d051ecd9c73c51e76370ceabd4f25097c256597fa898d404ed53425de608ac6bfe426f6e2bb457f1c554866eb69dcb8d6bf6f880e9a59b3cd053e6c7060eeacaacf4dac6697dac20e4bd3f38a2ea2543d1ab7953e3430790a9f81e1c67f5b58c825acf46bd02848384eebe9af917274cdfbb1a28a5d58a23a17977def0de10d644258d9c54f886d47d293a411cb6226103b55635'
#        mblock = MerkleBlock.parse(BytesIO(bytes.fromhex(hex_merkle_block)))
#        self.assertTrue(mblock.is_valid())


# MerkleBlock의 함수를 학습 과정에서 예제 실험
run(MerkleBlockTest("Test_parse"))
#run(MerkleBlockTest("Test_is_valid"))

