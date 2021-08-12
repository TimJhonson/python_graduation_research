a = 3

c = [2,3,4]

def test():
    global c
    a = 4
    c = [3,5,6]
test()
print(c)
