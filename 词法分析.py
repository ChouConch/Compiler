import re
keyword = ['do','if','return','typedef','auto','double','short'
           ,'bool','int','break','else','long','sizeof','case','enum','static','unsigned',
           'catch','namespace','using','char','new','struct','class','operator','switch','void'
           ,'const','false','private','template','float','pretected','this','continue','for',
           'public','throw','while','default','friend','true','delete','try','String','main']

operator = ['+','-','*','/','&','|','%','=','<','>','.','++','--','==']

special = ['{','}','(',')',';','\"','()']
def analyse(string,line):
    string = string.strip('\n')
    litter = re.findall('\".*\"|[a-zA-Z0-9]{1,}',string)#匹配单词或者字符串常量
    #print(litter)
    sp = re.findall("[^\w' '\"\;\(]{1,}|[;]|[(]",string) #匹配所有非空格非字母数字
    #print(sp)
    i,j = 0,0
    all = []
    index = {}
    for m in litter:
        index[m] = 0
    for m in sp:
        index[m] = 0
    while(i<len(litter) or j<len(sp)):
        if(i==len(litter)):
            all.append(sp[j])
            j = j + 1
        elif(j==len(sp)):
            all.append(litter[i])
            i = i + 1
        elif(string.index(litter[i],index[litter[i]])<string.index(sp[j],index[sp[j]])):
            index[litter[i]] = string.index(litter[i],index[litter[i]]) + 1
            all.append(litter[i])
            i = i + 1
        else:
            index[sp[j]] = string.index(sp[j], index[sp[j]]) + 1
            all.append(sp[j])
            j = j + 1
    ans = []
    for i in all:
        if(i in keyword):
            ans.append('第' + str(line)+ '行保留字:' + i)
        elif(i in operator):
            ans.append('第' + str(line)+ '行运算符:' + i)
        elif(i in special):
            ans.append('第' + str(line)+ '行分隔符:' + i)
        elif(i.isdigit()):
            ans.append('第' + str(line)+ '行数字:' + i)
        elif(i[0] == '\"' and len(i)>1):
            ans.append('第' + str(line)+ '行字符串常量:' + i)
        else:
            ans.append('第' + str(line)+ '行标识符:' + i)
    return ans

f = open("C:\\Users\\36964\\Desktop\\1.txt")
num = 1
for line in f:
    lineans = analyse(line,num)
    num = num + 1
    for i in lineans:
        print(i)