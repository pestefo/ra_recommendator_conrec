#!/usr/bin/env python
# coding: utf-8

from con_rec import *


def main():
    t = TBMAAlgorithm()
    w = WCFAlgorithm()
    # results = conrec.ranking_for_question(9061)
    # print(results)

    print(t.tags_for_question(9061))
    print(list(w.participants_of_question(9061)))


if __name__ == '__main__':
    main()
