
def plus(array1, array2):
    res = list()
    for i in range(len(array1)):
        res.append(array1[i] + array2[i])
    return res

def minus(array1, array2):
    res = list()
    for i in range(len(array1)):
        res.append(array1[i] - array2[i])
    return res

def multiply(num, array1):
    print(array1)
    res = list()
    for i in range(len(array1)):
        res.append(array1[i] * num)
    return res


print(plus([8.218,-9.341], [-1.129,2.111]))
print(minus([7.119,8.215], [-8.223,0.878]))
print(multiply(7.41, [1,671, -1.012, -0.318]))
