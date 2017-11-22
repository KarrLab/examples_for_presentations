from instrumental_example.lib import func
def test1():
    assert func(True, False) == 1

def test2():
    assert func(False, False) == 0

def test3():
    assert func(False, True) == 1

'''
test1()
test2()
# test3()
'''
