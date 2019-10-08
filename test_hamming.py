#!/usr/bin/env python3

from struct import pack

from hamming.hamming import gen_mask, insert_redundant_bits, hamming_algorithm


def str_to_bytearray(s):
    arr = bytearray()
    for c in s:
        b = ord(c)
        arr += pack("B", b)
    return arr


"""gen_mask(2, 40)
gen_mask(4, 40)
gen_mask(8, 40)
gen_mask(16, 40)

insert_redundant_bits(0xff_ff_ff_ff)
# insert_redundant_bits(0x0f)
# insert_redundant_bits(0x08)
# insert_redundant_bits(0x04)"""

print(hamming_algorithm(b"\xfe\xff\xff\xff"))
