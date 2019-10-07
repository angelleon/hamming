#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_STREAM as TCP, SOCK_DGRAM as UDP
from threading import Thread, Event


class Emiter(Thread):
    def __init__(self):
        super().__init__()