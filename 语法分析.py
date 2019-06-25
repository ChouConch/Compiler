vt = ['(',')','i','+','*']
vn = ['E','A','T','B','F']
p = ['E->TA','A->+TA|@','T->FB','B->*FB|@','F->(E)|i']
first = {}
follow = {}
M = {}
def init():#初始化first集合和follow集
    for i in vn:
        first[i] = []
        follow[i] = []
    for i in vt:
        first[i] = [i]
    first['@'] = ['@']
def creatNewp(p):#分解所有产生式，把A->B|C分解成A->B，A->C
    newP = []
    for i in p:  # 分解所有|
        s = i.split('->')
        right = s[1].split('|')
        left = s[0] + '->'
        for j in right:
            newP.append(left + j)
    return  newP

newP = creatNewp(p)

def getFirst(v):#获取v的first集合
    fir = []
    for i in newP:
        if(i[0] == v):#左部是v
            s = i.split('->')
            right = s[1]
            if(right[0] in vt or right[0] == '@'):#类似于A->aB或存在A->@则将其直接放入A的first集
                fir.append(right[0])
            else:
                for j in getFirst(right[0]):#类似于A->Ba则将B的first集放入A的first集，递归调用
                    fir.append(j)
    return fir

def checkEnd(m1,m2):#检测follow集是否扩大
    for i in m1:
        if(not m1[i] == m2[i]):
            return True
    return False
def getFollow():#生成所有follow集
    follow['E'].append('$')#将@符号放入E的follow集合
    oldsize = {}#记录重新扫描之前各个follow集的大小
    newsize = {}#记录重新扫描一遍后各个follow集的大小
    for i in vn:#初始化
        oldsize[i] = len(follow[i])
        newsize[i] = len(follow[i])
    start = True
    while(start):#循环
        for i in newP:
            V = i.split('->')
            left = V[0]
            right = V[1]
            if(right[-1] in vn):#存在A->αB
                follow[right[-1]].extend(follow[left])#将A的follow集放入B的follow集
            if(len(right) >= 2):
                if(right[-2] in vn):#存在A->αBβ
                    for j in first[right[-1]]:#将β的非空first集放入B的follow集
                        if(not j == '@'):
                            follow[right[-2]].append(j)
                        if(j == '@'):#如果空符存在于β的first集中，将A的follow集放入A的follow集
                            follow[right[-2]].extend(follow[left])
        for i in vn:#重新计算各个follow集的属性
            follow[i] = list(set(follow[i]))
            newsize[i] = len(follow[i])
        if(not checkEnd(oldsize,newsize)):#如果follow集不再扩大
            break
        else:
            for i in vn:
                oldsize[i] = newsize[i]
def First(a):#求aBC的first集合
    ans = []
    for i in a:
        ans.extend(first[i])
        if(not '@' in first[i]):#只有@存在于i的first集中时才进入下一个
            break
    return ans
def getTable():
    for i in newP:
        t = i.split('->')
        if('@' in First(t[1])):#如果空符存在于产生式右部的first集合中
            for j in follow[t[0]]:#对于左部follow集中的所有元素b，M[A,b] = i
                M[t[0] + j] = i
        else:
            for j in First(t[1]):#对于右部first集中的所有元素b，M[A,b] = i
                M[t[0] + j] = i

def printTable():#输出预测分析表
    t = ' '*8
    s = ''
    V = ['$']
    V.extend(vt.copy())
    for i in V:
        s = s + t + i
    print(s)
    for i in vn:
        p = i + '       '
        for j in V:
            if(i + j in list(M.keys())):
                p = p + M[i+j] + (' '*(9-len(M[i+j])))
            else:
                p = p + ' '*9
        print(p)
def analyze(l):#分析语句
    stack = ['E']#开始符号入栈
    flag = False
    for i in l:#对于每一个符号进行分析
        flag = False
        while(not flag):
            if (stack[-1] == i):#如果匹配成功
                stack.pop()
                flag = True
            else:
                t = M[stack[-1] + i]#查找预测分析表中的产生式
                print(t)
                p = t.split('->')[1]
                s = list(p)
                s.reverse()
                stack.pop()
                if(not p == '@'):
                    stack.extend(s)#产生式入栈（规约）
    stack.reverse()#对于栈中剩余符号推出空产生式
    for i in stack:
        print(i + '->@')

init()
for i in vn:
    first[i] = getFirst(i)
for i in first:
    print('first('+i+')',first[i])
getFollow()
getTable()
for i in follow:
    print('follow('+i+')',follow[i])
for i in M:
    print(i,M[i])
printTable()
analyze('i*i+i')