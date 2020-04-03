class Signature:
    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __repr__(self):
        return 'Signature({:x},{:x})'.format(self.r, self.s)

# DER 서명 형식 정의
# 1. 0x30바이트로 시작
# 2. 서명의 길이를 붙입니다. 보통은 0x44(10진수로 68)나 0x45가 됩니다. 
# 3. r값의 시작을 표시하는 표식 바이트로 0x02를 붙입니다.
# 4. 빅엔디언 정수로 r값을 표현합니다. 그결과의 첫 번째 바이트가 0x80보다 크거나 같으면
# 00을 앞에 붙입니다. 이후 바이트 단위의 길이를 다시 앞에 붙입니다. 구한 최종 결과를 3번 결과# 뒤에 더 합니다.
# 5. s값의 시작을 표시하는 표식 바이트로 0x02를 붙입니다.
# 6. 빅엔디언 정수로 s값을 표현합니다. 그 결과의 첫 번재 바이트가 0x80보다 크거나 같으면 00을 앞에 붙입니다. 이후, 바이트 단위의 길이를 다시 앞에 붙입니다. 구한 최정 결과를 5번 결과 뒤에 더합니다.

    def der(self):
        # r의 binary값
        rbin = self.r.to_bytes(32, 'big')
        # remove all null bytes at the begining.... 맨 앞의 'x00을 제거'
        rbin = rbin.lstrip(b'\x00')
        #if rbin has a high bit, add a \x00
        if rbin[0] & 0x80:
            rbin = b'\x00' + rbin
        # 정수 리스트를 bytes([])을 통해 bytes형식으로 변환 가능
        result = bytes([2, len(rbin)]) + rbin
        sbin = self.s.to_bytes(32, 'big')
        # remove all null bytes at the begining... 맨 앞의 '0x00을 제거'
        sbin = sbin.lstrip(b'\x00')
        # if sbin has a high bit at the begining 
        if sbin[0] & 0x80:
            sbin = b'\x00' + sbin
        result += bytes([2, len(sbin)]) + sbin
        return bytes([0x30, len(result)]) + result
