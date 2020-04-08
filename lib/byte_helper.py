from helper import little_endian_to_int
TWO_WEEKS = 60 * 60 * 24 * 14   # 초 * 분 * 시 * 일

#26959535291011309493156476344723991336010898738574164086137773096960
MAX_TARGET = 0xffff * 256 **(0x1d -3)

def bits_to_target(bits):
    exponent = bits[-1]
    coefficient = little_endian_to_int(bits[:-1])
    return coefficient * 256 **(exponent - 3)

def target_to_bits(target):
# 32바이트 빅엔디언으로 target을 대입
    raw_bytes = target.to_bytes(32, 'big')
# 앞에 0으로 시작하는 바이트를 모두 제거한다.
    raw_bytes = raw_bytes.lstrip(b'\x00')
# 가장 왼쪽에 있는 바이트 값은 0x7f와 같거나 작아야 한다. 0x7f보다 큰 경우 raw_bytes가 음수가된다.
# raw_bytes[0]가 0x7f보다 커서 음수로 간주되면 안된다. 0x7f보다 큰 경우 제거한 1바이트의 0을 추가한>다.
    if raw_bytes[0] > 0x7f:
        exponent = len(raw_bytes) + 1           # 맨 앞에 0을 넣기 위해 공간을 형성해야 한다.
        coefficient = b'\x00' + raw_bytes[:2]   #
    else:
        exponent = len(raw_bytes)
        coefficient = raw_bytes[:3]
    # 계수(coefficient)는 리틀엔디언 + 지수를 바이트 형식
    new_bits = coefficient[::-1] + bytes([exponent])
    return new_bits

def calculate_new_bits(previous_bits, time_differential):
    # 8주보다 시간차이가 크면 8주로 time_differential으로 설정
    if time_differential > TWO_WEEKS * 4:
        time_differential = TWO_WEEKS * 4
    # 3.5일보다 작은 경우 3.5일로 time_differential으로 설정
    if time_differential > TWO_WEEKS // 4:
        time_differential = TWO_WEEKS // 4
    new_target = bits_to_target(previous_bits) * time_differential // TWO_WEEKS
    # new_target이 MAX_TARGET보다 클 결우 MAX_TARGET으로 new_target을 설정
    if new_target > MAX_TARGET:
        new_target = MAX_TARGET
    return target_to_bits(new_target)

def bit_field_to_bytes(bit_field):
    if len(bit_field) % 8 != 0:
        raise RuntimeError('bit_field does not have a length tha is divisible by 8')
    result = bytearray(len(bit_field) // 8)
    for i, bit in enumerate(bit_field):
        byte_index, bit_index = divmod(i, 8)
        if bit:
            result[byte_index] |= 1 << bit_index

def bytes_to_bit_field(some_bytes):
    flag_bits = []
    for byte in some_bytes:
        for _ in range(8):
            flag_bits.append(byte & 1)
            byte >>= 1
    return flag_bits

