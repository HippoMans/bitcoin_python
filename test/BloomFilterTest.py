import os
import sys

path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(os.path.abspath(path))

from unittest import TestCase
from lib.helper import run
from lib.helper import hash256
from src.BloomFilter import BloomFilter

class BloomFilterTest(TestCase):
    def Test_add(self):
        bloom = BloomFilter(10, 5, 99)
        item = b'Hello World'
        bloom.add(item)
        expected = '00000480400000840000'
        result = bloom.filter_bytes().hex()
        print(result)
        self.assertEqual(result, expected)

        item = b'GoodBye~~~'
        bloom.add(item)
        result = bloom.filter_bytes().hex()
        expected = '080044804000808e0000'
        print(result)
        self.assertEqual(result, expected)

    def Test_filterload(self):
        bloom = BloomFilter(10, 5, 99)
        item = b'Hello World'
        bloom.add(item)
        result = bloom.filterload().serialize().hex()
        print(result)
        expected = '0a00000480400000840000050000006300000001'
        self.assertEqual(result, expected)
        item = b'GoodBye~~~'
        bloom.add(item)
        result = bloom.filterload().serialize().hex()
        print(result)
        expected = '0a080044804000808e0000050000006300000001'
        self.assertEqual(result, expected)

# 타원곡선의 학습 과정에서 예제 실험
run(BloomFilterTest("Test_add"))
run(BloomFilterTest("Test_filterload"))
