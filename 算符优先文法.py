p = ['E->E+T|T','T->T*F|F','F->(E)|i']
vn = []
vt = []
newP = []
firstVt = {}
lastVt = {}
table = {}
def init():
    global firstVt,lastVt
    for i in vn:
        firstVt[i] = []
        lastVt[i] = []
def creatNewp():#分解所有产生式，把A->B|C分解成A->B，A->C
    global newP,p
    for i in p:  # 分解所有|
        s = i.split('->')
        right = s[1].split('|')
        left = s[0] + '->'
        for j in right:
            newP.append(left + j)

def getVn():
    global vn
    for i in newP:
        for j in i:
            if(j.isupper()):
                vn.append(j)
    vn = list(set(vn))

def getVt():
    global vt,vn
    for i in newP:
        for j in range(len(i)):
            if(j>2 and (not i[j] in vn)):
                vt.append(i[j])
    vt = list(set(vt))
def checkEnd(m1,m2):#检测firstVt集是否扩大
    for i in m1:
        if(not m1[i] == m2[i]):
            return True
    return False
def isAll(a):
    for i in a:
        if(not i in vn):
            return False
    return True
def change(newp):
    x = []
    for i in newP:
        t = i
        for j in vn:
            t = t.replace(j,'E')
        x.append(t)
    return x

def getFirstVt():
    oldsize = {}
    newsize = {}
    for i in vn:
        oldsize[i] = len(firstVt[i])
        newsize[i] = len(firstVt[i])
    while(True):
        for i in newP:
            t = i.split('->')
            left = t[0]
            right = t[1]
            if(isAll(right) and right[0] in vn):
                firstVt[left].extend(firstVt[right[0]])
            for j in right:
                if(j in vt):
                    firstVt[left].append(j)
                    break
        for i in vn:#重新计算各个firstVt的属性
            firstVt[i] = list(set(firstVt[i]))
            newsize[i] = len(firstVt[i])
        if(not checkEnd(oldsize,newsize)):#如果不再扩大
            break
        else:
            for i in vn:
                oldsize[i] = newsize[i]
def getLastVt():
    oldsize = {}
    newsize = {}
    for i in vn:
        oldsize[i] = len(lastVt[i])
        newsize[i] = len(lastVt[i])
    while (True):
        for i in newP:
            t = i.split('->')
            left = t[0]
            right = t[1]
            r = list(right)
            r.reverse()
            right = ''.join(r)
            if (isAll(right) and right[-1] in vn):
                lastVt[left].extend(lastVt[right[-1]])
            for j in right:
                if (j in vt):
                    lastVt[left].append(j)
                    break
        for i in vn:  # 重新计算各个LastVt集的属性
            lastVt[i] = list(set(lastVt[i]))
            newsize[i] = len(lastVt[i])
        if (not checkEnd(oldsize, newsize)):  # 如果不再扩大
            break
        else:
            for i in vn:
                oldsize[i] = newsize[i]

def getTable():
    Vt = vt.copy()
    Vt.append('#')
    y = newP.copy()
    y.append('E->#E#')
    for i in y:
        t = i.split('->')
        left = t[0]
        right = t[1]
        if(len(right) >= 3):
            for j in range(len(right)-2):
                if(right[j] in Vt and right[j+1] in vn and right[j+2] in Vt):
                    table[right[j] + right[j+2]] = '='
        if(len(right) >= 2):
            for j in range(len(right)-1):
                if(right[j] in Vt and right[j+1] in vn):
                    for k in firstVt[right[j+1]]:
                        table[right[j] + k] = '<'
                if(right[j] in vn and right[j+1] in Vt):
                    for k in lastVt[right[j]]:
                        table[k + right[j+1]] = '>'
    Vt = vt.copy()
    Vt.append('#')
    for i in Vt:
        for j in Vt:
            if(not (i+j) in list(table.keys())):
                table[i+j] = '0'

def printTable():
    print('算符优先分析表如下')
    s = ' '*4
    t = ' '*4
    Vt = vt.copy()
    Vt.append('#')
    for i in Vt:
        s = s + i + t
    print(s)
    for i in Vt:
        st = i + ' ' * 3
        for j in Vt:
            if(i+j in list(table.keys())):
                st = st + table[i+j] + ' '*4
        print(st)
def findLeft(l):
    x = change(newP)
    for i in range(len(l)):
        t = l[i:]
        s = ''.join(t)
        for j in x:
            k = j.split('->')
            if(k[1] == s):
                return k[0],k[1]
def findVt(l):
    Vt = vt.copy()
    Vt.append('#')
    for i in range(len(l)-1,-1,-1):
        if(l[i] in Vt):
            return i
    return -1
def analyze(s):
    s = s + '#'
    index = 0
    symbolstack = ['#']
    print('步骤' + '  ' + '符号栈' + ' '*4 + '输入符号串' + ' '*3 + '优先关系  ' + '动作')
    num = 1
    try:
        while (True):
            #print(symbolstack)
            flag = findVt(symbolstack)
            st = str(num)
            stack = ''.join(symbolstack)
            ss = s[index:]
            st = st + '  ' * 2 + stack + ' ' * (9 - len(stack)) + ss + ' ' * (12 - len(ss))
            if (ss[0] == '#' and symbolstack[-1] == 'E' and len(symbolstack) == 2):
                st = st + ss[0] + '       接受'
                print(st)
                break
            elif (table[symbolstack[flag] + ss[0]] == '>'):
                st = st + symbolstack[flag] + table[symbolstack[flag] + ss[0]] + ss[0] + '      规约'
                s1, s2 = findLeft(symbolstack)
                S1 = list(s1)
                S2 = list(s2)
                for k in range(len(S2)):
                    symbolstack.pop()
                symbolstack.extend(S1)
                print(st)
            elif (table[symbolstack[flag] + ss[0]] in '<='):
                st = st + symbolstack[flag] + table[symbolstack[flag] + ss[0]] + ss[0] + '      移进'
                symbolstack.append(ss[0])
                index = index + 1
                print(st)
            elif (table[symbolstack[flag] + ss[0]] == '0'):
                print(st)
                print('出错！')
                break
            num = num + 1
    except (BaseException):
        print("非本文法句子")

creatNewp()
print('产生式集合为:',newP)
getVn()
print('非终结符集合:',vn)
getVt()
print('终结符集合:',vt)
init()
getFirstVt()
for i in firstVt:
    print('fitstVt('+i+')',firstVt[i])
getLastVt()
for i in lastVt:
    print('lastVt('+i+')',lastVt[i])
getTable()
#for i in table:
#    print(i,table[i])
printTable()
x = change(newP)
#print(x)
analyze('(i+i)*i')
analyze('i-i*i')