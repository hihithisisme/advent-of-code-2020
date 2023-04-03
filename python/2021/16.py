import math
from typing import List
from utils import get_aoc_token 

import requests

AOC_COOKIE = get_aoc_token()
YEAR = '2021'

def get_input(day):
    req = requests.get(f'https://adventofcode.com/{YEAR}/day/{day}/input', 
                       headers={'cookie':'session='+AOC_COOKIE})
    return req.text

def get_example(day,offset=0):
    req = requests.get(f'https://adventofcode.com/{YEAR}/day/{day}',
                       headers={'cookie':'session='+AOC_COOKIE})
    return req.text.split('<pre><code>')[offset+1].split('</code></pre>')[0]

def submit(day, level, answer):
    print(f'You are about to submit the follwing answer:')
    print(f'>>>>>>>>>>>>>>>>> {answer}')
    input('Press enter to continue or Ctrl+C to abort.')
    data = {
      'level': str(level),
      'answer': str(answer)
    }

    response = requests.post(f'https://adventofcode.com/{YEAR}/day/{day}/answer',
                             headers={'cookie':'session='+AOC_COOKIE}, data=data)
    if 'You gave an answer too recently' in response.text:
        # You will get this if you submitted a wrong answer less than 60s ago.
        print('VERDICT : TOO MANY REQUESTS')
    elif 'not the right answer' in response.text:
        if 'too low' in response.text:
            print('VERDICT : WRONG (TOO LOW)')
        elif 'too high' in response.text:
            print('VERDICT : WRONG (TOO HIGH)')
        else:
            print('VERDICT : WRONG (UNKNOWN)')
    elif 'seem to be solving the right level.' in response.text:
        # You will get this if you submit on a level you already solved.
        # Usually happens when you forget to switch from `PART = 1` to `PART = 2`
        print('VERDICT : ALREADY SOLVED')
    else:
        print('VERDICT : OK !')

DAY = 16
# s = get_example(DAY).strip() # the daily input is stored in s
# print(s)
s = get_input(DAY).strip() # the daily input is stored in s

'''
Your code here
Put the result in `ans` as a str or int.
'''

hexa_mapping = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}

def hexa_to_binary(s: str) -> List[int]:
    res = []
    for ch in s:
        b = hexa_mapping[ch]
        res += [int(bi) for bi in b]
    return res

def binary_to_decimal(binary: List[int]) -> int:
    val = 0
    for i in range(len(binary)):
        val += 2**(len(binary) - 1 - i) * binary[i]
    return val

def get_type_id(binary: List[int], index: int) -> int:
    type = binary_to_decimal(binary[index+3:index+6])
    return type


class OperatorPacket:
    def __init__(self, binary: List[int], index: int) -> None:
        self.version = binary_to_decimal(binary[index:index+3])
        self.type = get_type_id(binary, index)
        self.start_index = index
        self.length_type = binary[index+6]
        self.subpackets = []

        bit_length_start_idx = index + 7
        if self.length_type == 0:
            subpacket_length = binary_to_decimal(binary[bit_length_start_idx: bit_length_start_idx + 15])
            subpacket_start_idx = bit_length_start_idx + 15
            subpacket_end_idx = subpacket_start_idx + subpacket_length - 1
            pointer = subpacket_start_idx

            while pointer <= subpacket_end_idx:
                sp = read_packet(pointer, binary)
                pointer = sp.get_end_index() + 1
                self.subpackets.append(sp)

            self.end_index = subpacket_end_idx

        else:
            subpacket_count = binary_to_decimal(binary[bit_length_start_idx: bit_length_start_idx + 11])
            pointer = bit_length_start_idx + 11
            for i in range(subpacket_count):
                sp = read_packet(pointer, binary)
                pointer = sp.get_end_index() + 1
                self.subpackets.append(sp)

            self.end_index = pointer - 1

    def evaluate(self) -> int:
        match self.type:
            case 0:
                return sum([sp.evaluate() for sp in self.get_subpackets()])
            case 1:
                res = 1
                for sp in self.get_subpackets():
                    res = res * sp.evaluate()
                return res
            case 2:
                return min([sp.evaluate() for sp in self.get_subpackets()])
            case 3:
                return max([sp.evaluate() for sp in self.get_subpackets()])
            case 5:
                return 1 if self.get_subpackets()[0].evaluate() > self.get_subpackets()[1].evaluate() else 0
            case 6:
                return 1 if self.get_subpackets()[0].evaluate() < self.get_subpackets()[1].evaluate() else 0
            case 7:
                return 1 if self.get_subpackets()[0].evaluate() == self.get_subpackets()[1].evaluate() else 0
            case _:
                raise Exception('unexpected type')
            
    def get_end_index(self) -> int:
        return self.end_index
    
    def get_subpackets(self):
        return self.subpackets
    
    def __repr__(self) -> str:
        return f'Operator {self.version}-{self.type} | {self.length_type}'

class LiteralPacket:
    def __init__(self, binary: List[int], index: int) -> None:
        self.version = binary_to_decimal(binary[index:index+3])
        self.type = get_type_id(binary, index)
        self.start_index = index

        buffer = []
        pointer = index+6
        while binary[pointer] == 1:
            buffer += binary[pointer+1:pointer+5]
            pointer += 5

        buffer += binary[pointer+1:pointer+5]
        self.literal = binary_to_decimal(buffer)
        self.end_index = pointer + 4

    def get_end_index(self) -> int:
        return self.end_index
    
    def evaluate(self) -> int:
        return self.literal
    
    def __repr__(self) -> str:
        return f'Literal {self.version}-{self.type} | {self.evaluate()}'

def read_packet(idx: int, binary: List[int]):
    type_id = get_type_id(binary, idx)
    if type_id == 4: # LiteralPacket
        return LiteralPacket(binary, idx)
    else:
        return OperatorPacket(binary, idx)
    

def func1(s):
    binary = hexa_to_binary(s)
    packet = read_packet(0, binary)
    
    total = 0
    inspect = [packet]
    while len(inspect) > 0:
        p = inspect.pop(0)
        total += p.version
        if p.type != 4:
            sp = p.get_subpackets()
            inspect += sp
        
    return total


# print(hexa_to_binary('620D79802F60098803B10E20C3C1007A2EC4C84136F0600BCB8AD0066E200CC7D89D0C4401F87104E094FEA82B0726613C6B692400E14A305802D112239802125FB69FF0015095B9D4ADCEE5B6782005301762200628012E006B80162007B01060A0051801E200528014002A118016802003801E2006100460400C1A001AB3DED1A00063D0E25771189394253A6B2671908020394359B6799529E69600A6A6EB5C2D4C4D764F7F8263805531AA5FE8D3AE33BEC6AB148968D7BFEF2FBD204CA3980250A3C01591EF94E5FF6A2698027A0094599AA471F299EA4FBC9E47277149C35C88E4E3B30043B315B675B6B9FBCCEC0017991D690A5A412E011CA8BC08979FD665298B6445402F97089792D48CF589E00A56FFFDA3EF12CBD24FA200C9002190AE3AC293007A0A41784A600C42485F0E6089805D0CE517E3C493DC900180213D1C5F1988D6802D346F33C840A0804CB9FE1CE006E6000844528570A40010E86B09A32200107321A20164F66BAB5244929AD0FCBC65AF3B4893C9D7C46401A64BA4E00437232D6774D6DEA51CE4DA88041DF0042467DCD28B133BE73C733D8CD703EE005CADF7D15200F32C0129EC4E7EB4605D28A52F2C762BEA010C8B94239AAF3C5523CB271802F3CB12EAC0002FC6B8F2600ACBD15780337939531EAD32B5272A63D5A657880353B005A73744F97D3F4AE277A7DA8803C4989DDBA802459D82BCF7E5CC5ED6242013427A167FC00D500010F8F119A1A8803F0C62DC7D200CAA7E1BC40C7401794C766BB3C58A00845691ADEF875894400C0CFA7CD86CF8F98027600ACA12495BF6FFEF20691ADE96692013E27A3DE197802E00085C6E8F30600010882B18A25880352D6D5712AE97E194E4F71D279803000084C688A71F440188FB0FA2A8803D0AE31C1D200DE25F3AAC7F1BA35802B3BE6D9DF369802F1CB401393F2249F918800829A1B40088A54F25330B134950E0'))
# print(read_packet(0, [int(i) for i in '11101110000000001101010000001100100000100011000001100000']).get_subpackets())
# print(len('00111000000000000110111101000101001010010001001000000000')-1)
# tcs = [
#     ('8A004A801A8002F478', 16),
#     ('C0015000016115A2E0802F182340', 23),
#     ('A0016C880162017C3686B18A3D4780', 31),
#     ('620080001611562C8802118E34', 12)
# ]

# for tc in tcs:
#     ans = func1(tc[0])
#     print(tc[0], ans, tc[1], ans == tc[1])

# ans1 = func1(s)
# submit(DAY, 1, ans1)

def func2(s):
    binary = hexa_to_binary(s)
    packet = read_packet(0, binary)
        
    return packet.evaluate()

# tcs = [
#     ('C200B40A82', 3),
#     ('04005AC33890', 54),
#     ('880086C3E88112', 7),
#     ('CE00C43D881120', 9),
#     ('F600BC2D8F', 1),
#     ('9C005AC2F8F0', 0),
#     ('9C0141080250320F1802104A08', 1)
# ]

# for tc in tcs:
#     ans = func2(tc[0])
#     print(tc[0], ans, tc[1], ans == tc[1])

ans2 = func2(s)
submit(DAY, 2, ans2)