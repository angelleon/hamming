#!/usr/bin/env python3

from typing import Union
import struct

from .ui import Application
from .receptor import Receptor

def es_potencia_2(a):
    if a == 1:
        return True
    while True:
        if a % 2 == 0:
            a //= 2
        else:
            return False
        if a == 1:
            return True

def gen_mask(pwr, length):
    base = 1
    i = 1
    while i < pwr:
        base = (base << 1) | 1
        # print(bin(base))
        i += 1
    i = 1
    mask = base
    # print(f"base: {bin(base)}")
    times = length // pwr
    if times * pwr < length:
        times += 1
    while i < times:
        if i % 2 == 0:
            mask = (mask << (pwr * 2))
            mask |= base
        i += 1
    return mask

def hamming_algorithm(data: bytearray):
    #        12345678 12345678 12345678 12345678
    if len(data) % 4 != 0:
        diff = 4 - len(data) % 4
        data += bytes(diff)
    m = len(data) * 4
    r = 0
    while 2 ** r < m + r + 1:
        r += 1
    i = 0









class Hamming:
    def __init__(self):
        self.ui = Application()
        self.connection = Receptor

    def start(self):
        return self.ui.exec()

