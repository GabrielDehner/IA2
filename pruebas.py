"""def algo2():
    print ("algo2")
algo2
def algo3():
    print ("asdasd")
algo3
def algo():
    variable = 'mundo'
    print (variable)
    algo2()
    algo3()
algo()"""

import csv
def main():
    m = open("archivo.csv", "r")
    m_csv = csv.reader(m)
    for cab1, cab2 in m_csv:
        print ("c1-----> ", cab1, " \tc2----> ", cab2)
    m.close()

main()