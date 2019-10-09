#!/usr/bin/env python3

from typing import Union
from struct import Struct
from ipaddress import IPv4Address, AddressValueError
from random import random, randrange

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QPlainTextEdit

from .ui import Application
from .receptor import Receptor

struct = Struct("B")
converter = Struct("I")


def str_4_by_4(s):
    ret = ""
    if len(s) < 4:
        return s
    if len(s) % 4 != 0:
        s += " " * (4 - len(s) // 4)
    i = 0
    while i < len(s) // 4:
        if i % 4 == 0 and i != 0:
            ret += "\n"
        ret += s[i * 4: i * 4 + 4] + " "
        i += 1
    return ret

def str_to_bytearray(s):
    arr = bytearray()
    for c in s:
        b = ord(c)
        arr += struct.pack(b)
    return arr


def is_2_pow(a):
    if a == 1:
        return True
    while True:
        if a % 2 == 0:
            a //= 2
            if a == 1:
                return True
        else:
            return False


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


def insert_redundant_bits(data):
    print(f"data: {bin(data)[2:]}")
    if data == 0:
        return bytearray(5), "0" * 32
    #                      5        4        3        2        1
    #               87654321 87654321 87654321 87654321 87654321
    parity_bits = 0b00000000_00000000_00000000_00000000_00000000
    for i in range(6):
        ones = 0
        mask = gen_mask(2**i, 32)
        masked = data & mask
        print(f"data:  {bin(data)[2:]}")
        print(f"mask:  {bin(mask)[2:]}")
        print(f"masked:{bin(masked)[2:]}")
        while masked != 0:
            if masked & 1 == 1:
                ones += 1
            masked >>= 1
        print(f"ones: {ones}")
        print(f"parity_bits: {bin(parity_bits)}")
        if ones % 2 == 0:
            parity_bits |= 1 << (2**i - 1)
        else:
            parity_bits |= abs(~(1 << (2**i - 1)))
        print(f"parity_bits: {bin(parity_bits)}")
    i = 1
    ret_data = parity_bits

    while data != 0:
        if not is_2_pow(i):
            ret_data |= (data & 1) << i
            data >>= 1
        i += 1
        print(f"ret_data: {bin(ret_data)}")
    data = ret_data
    data_str = bin(data)[2:]
    ret_data = bytearray()
    for i in range(5):
        ret_data += struct.pack(data & 0xff)
        data >>= 8
        print(f"ret_data: {repr(ret_data)}")
    return ret_data, data_str


def hamming_algorithm(data: bytearray):
    """Funcion que agrega los bits de comprobacion antes de enviarse en mensaje"""
    print(f"data: {data}")
    #        12345678 12345678 12345678 12345678
    if len(data) % 4 != 0:
        diff = 4 - len(data) % 4
        data += bytes(diff)
    m = len(data)
    r = 0
    chunck = 0
    i = 0
    ret_data = bytearray()
    ret_str = ""
    while i < m // 4:
        chunck = converter.unpack(data[i * 4: i * 4 + 4])[0]
        chunck, chunck_str = insert_redundant_bits(chunck)
        print(f"chunck: {chunck} chunck_str:{chunck_str}")
        ret_data += chunck
        ret_str += chunck_str
        i += 1
    return ret_data, ret_str


def chk_hamming(data):
    """Funcion quer comprueba el mensaje que se recibe"""
    pass


class Hamming(Application):
    CSS_ERR_QLINE_EDIT = "QLineEdit{background: DarkRed; color: LightGray}"
    CSS_DEFAULT_QLINE_EDIT = "QLineEdit{}"

    def __init__(self):
        super().__init__()
        self.connection = Receptor
        # self.connection = Emisor()
        self.w.btn_action.clicked.connect(self.slt_process_msg)
        self.w.rdio_send.toggled.connect(self.slt_rdio_toggle_mode)
        self.is_client = True
        # self.w.txt_ip.setStyleSheet("QLineEdit{background: DarkRed; color: LightGray}")

    @pyqtSlot(bool)
    def slt_rdio_toggle_mode(self, checked):
        if checked:
            self.is_client = True
            self.w.txt_editor.setEnabled(True)
            self.w.txt_ip.setEnabled(True)
        else:
            self.is_client = False
            self.w.txt_editor.setEnabled(False)
            self.w.txt_ip.setEnabled(False)

    @pyqtSlot(bool)
    def slt_process_msg(self):
        if self.is_client:
            if not (self.chk_ip() and self.chk_port()):
                return
            msg = self.w.txt_editor.toPlainText()
            if len(msg) == 0:
                return
            msg = str_to_bytearray(msg)
            msg, msg_str = hamming_algorithm(msg)
            self.w.txt_show.setPlainText(str_4_by_4(msg_str))
        else:
            pass

    @pyqtSlot(bytes)
    def slt_recv_msg(self, msg):
        pass

    def chk_ip(self):
        self.w.txt_ip.setStyleSheet(self.CSS_DEFAULT_QLINE_EDIT)
        ip = self.w.txt_ip.text()
        print(ip)
        try:
            IPv4Address(ip)
        except AddressValueError:
            self.w.txt_ip.setStyleSheet(self.CSS_ERR_QLINE_EDIT)
            return False
        return True

    def chk_port(self):
        self.w.txt_port.setStyleSheet(self.CSS_DEFAULT_QLINE_EDIT)
        port = self.w.txt_port.text()
        try:
            port = int(port)
            assert 0 <= port < 65536
        except (ValueError, AssertionError):
            self.w.txt_port.setStyleSheet(self.CSS_ERR_QLINE_EDIT)
            return False
        return True

    def send(self):
        pass

    def start(self):
        return self.exec()

