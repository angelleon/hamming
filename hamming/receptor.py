#!/usr/bin/env python3


from threading import Event, Thread
from socket import socket, AF_INET, SOCK_DGRAM as UDP, SOCK_STREAM as TCP
from time import sleep


class Receptor(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        pass



