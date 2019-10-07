#!/usr/bin/env python3

from hamming.hamming import Hamming


def main():
    hamming = Hamming()
    hamming.start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nSaliendo...")
