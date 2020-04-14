from lib.helper import encode_varint
from lib.helper import int_to_little_endian

class GetDataMessage:
    command = b'getdata'

    def __init__(self):
        self.data = []

    def add_data(self, data_type, identifier):
        self.data.append((data_type, identifier))

    def serialize(self):
        result = encode_varint(len(self.data))
        for data_type, identifier in self.data:
            result += int_to_little_endian(data_type, 4)
            result += identifier[::-1]
        return result
