p = "a=((b+c)*d-e/f)*2"

def middle2behind(expression):
    result = []             # 结果列表
    stack = []              # 栈
    for item in expression:
        if item.isalnum():      # 如果当前字符为数字那么直接放入结果列表
            result.append(item)
        else:                     # 如果当前字符为一切其他操作符
            if len(stack) == 0:   # 如果栈空，直接入栈
                stack.append(item)
            elif item in '*/(':   # 如果当前字符为*/（，直接入栈
                stack.append(item)
            elif item == ')':     # 如果右括号则全部弹出（碰到左括号停止）
                t = stack.pop()
                while t != '(':
                    result.append(t)
                    t = stack.pop()
            # 如果当前字符为加减且栈顶为乘除，则开始弹出
            elif item in '+-' and stack[len(stack)-1] in '*/':
                if stack.count('(') == 0:           # 如果有左括号，弹到左括号为止
                    while stack:
                        result.append(stack.pop())
                else:                               # 如果没有左括号，弹出所有
                    t = stack.pop()
                    while t != '(':
                        result.append(t)
                        t = stack.pop()
                    stack.append('(')
                stack.append(item)  # 弹出操作完成后将‘+-’入栈
            else:
                stack.append(item)# 其余情况直接入栈（如当前字符为+，栈顶为+-）

    # 表达式遍历完了，但是栈中还有操作符不满足弹出条件，把栈中的东西全部弹出
    while stack:
        result.append(stack.pop())
    # 返回字符串
    return "".join(result)
def printfour(expression):
    temp = 1
    k = ['+','-','*','/']
    l = []
    for index in range(2,len(expression)):
        i = expression[index]
        if(not i in k):
            l.append(i)
        else:
            if(len(l) >=2):
                s = '(' + i + ' ' + l[-2] + ' ' + l[-1] + ' t' + str(temp) + ')'
                print(s)
                l.pop()
                l.pop()
                l.append('t' + str(temp))
                temp = temp + 1
    s = '(' + '=' + ' ' + l[-1] + '  ' +  '  ' + expression[0] + ')'
    print(s)
    print('成功！')
def check(p):
    k = ['+', '-', '*', '/']
    if(not '=' in p):
        return False
    expression = p[2:]
    stack = []
    if(expression[0] in k):
        return False
    if(expression[-1] in k):
        return False
    for index in range(len(expression)):
        i = expression[index]
        if(i == '('):
            stack.append(i)
        elif(i == ')'):
            if(not '(' == stack.pop()):
                return False
        elif(expression[index] in k and expression[index-1] in k):
            return False
        elif(expression[index].isalnum() and expression[index-1].isalnum()):
            return False
    if(not len(stack) == 0):
        return False
    return True
if(__name__ == '__main__'):
    print(p)
    expression = p[2:]
    if(check(p)):
        expression = middle2behind(expression)
        expression = p[0:2] + expression
        printfour(expression)
    else:
        print('所输入的语句不是合法的中缀表达式赋值语句！')