# -*- coding: UTF-8 -*-

import sys
from collections import Counter


def getFile(argv):
    filename = ''
    if not argv:
        filename = input("输入文件名:\n")
        if "traffic" not in filename:
            filename = filename + ".traffic"
    else:
        filename = argv[0]
        if "traffic" not in filename:
            filename = filename + ".traffic"
    # print(filename)
    f = open(filename, 'r')
    txt = f.read()
    f.close()
    return txt, filename


def options():
    print("1:文件对半分\n"
          "2:查询n条相同的data数据")
    while True:
        opt = input("输入选项：\n")
        if opt not in "12":
            continue
        return opt


def iter_count(file_name):
    from itertools import (takewhile, repeat)
    buffer = 1024 * 1024
    with open(file_name) as f:
        buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
        return sum(buf.count('\n') for buf in buf_gen)


def killfile(rawdata, filename):
    lines = iter_count(filename)
    count = 0
    print(f"****************************\n"
          f"文件总共{lines}行")
    line1 = lines // 2
    line2 = lines - line1
    data = rawdata.splitlines()
    # print(data)
    # print(len(data))
    file1 = open(filename.replace(".traffic", "") + "_1.traffic", 'w')
    for i in range(line1):
        file1.write(data[i] + "\n")
    file1.close()
    file2 = open(filename.replace(".traffic", "") + "_2.traffic", 'w')
    for i in range(line2):
        file2.write(data[line1 + i] + "\n")
    file2.close()
    print("已生成文件" + filename.replace(".traffic", "") + "_1.traffic")
    print("已生成文件" + filename.replace(".traffic", "") + "_2.traffic")


def find(rawdata):
    count = 0
    while True:
        tmp = input("输入data相同的个数：\n")
        if str.isdigit(tmp):
            count = int(tmp)
            break
    data = rawdata.splitlines()
    list = []
    for item in data:
        _dic = eval(item)
        list.append(str(_dic['data']))

    # print(list)
    cot = dict(Counter(list))
    # print(cot)
    targelist = []
    for k, v in cot.items():
        if v == count:
            targelist.append(k)
    print(f"查询到{len(targelist)}组数据，是否输出？(y/n)")
    if input() == 'n':
        targelist = []
    ttt = 1
    for itemm in targelist:
        print(f"..................正在输出第{ttt}组数据...........................")
        file = open(filename.replace(".traffic", "") + f"_count{count}_{ttt}" + ".traffic", 'w')
        for item in data:
            tmp2 = eval(item)
            # print(str(tmp2))
            if itemm in str(tmp2):
                file.write(str(item) + "\n")
        file.close()
        ttt += 1
    if len(targelist) == 0:
        print("ERROR: 未查询到数量的信息\n*************************************")
        find(rawdata)
    else:
        print("SUCCESS: 文件输出完成")


if __name__ == "__main__":
    rawdata, filename = getFile(sys.argv[1:])
    opt = options()
    if opt == '1':
        killfile(rawdata, filename)
    if opt == '2':
        find(rawdata)
