# -*- coding:utf-8 -*-

import sys

def read_file(filename):
    f = open(filename)
    content = f.read()
    f.close()
    return content


def main():
    if len(sys.argv) <2:
        print("please specifiy input text filename")
    lines = read_file(sys.argv[1]).split("\n")
   
    # process data 
    data = {}
    indent = "   "
    for line in lines:
        try:
            items = line.split("\t")
            categoryName = items[0]
            subitems = items[1].split("、")
            if categoryName in data.keys():
                data[categoryName].extend(subitems)
            else:
                data[categoryName] = subitems
        except:
            pass

    for categoryName in data.keys():
        print(indent * 2 + categoryName)
        for i in range(len(data[categoryName])):
            subitemName = data[categoryName][i].replace("；", "")
            print(indent * 3 + subitemName)

if __name__ == "__main__":
    main()
