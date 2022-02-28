#! /usr/bin/env python
import sys
import argparse


def main():
    p = argparse.ArgumentParser()
    p.add_argument('gather_out')
    p.add_argument('gather_csv')
    p.add_argument('-o', '--output', required=True)
    args = p.parse_args()


if __name__ == '__main__':
    sys.exit(main())
