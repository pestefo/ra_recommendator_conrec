#!/usr/bin/env python
# coding: utf-8

from con_rec import *


def main():
    conrec = ConRec()
    results = conrec.ranking_for_question(9061)
    print(results)


if __name__ == '__main__':
    main()
