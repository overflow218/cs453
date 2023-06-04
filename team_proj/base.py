
# import 하는 방식 1
import a, b
import lib.lib2.d
# import 하는 방식 1-1
from lib import c
from lib.lib2 import d

# linting이 된 상태라서 unused import는 없는 상태라고 가정하자.
from lib.lib2.d import test, hello, haha

# import 하는 방식 2
from b import multiply, divide

# 외부 프레임워크 import하는 예시
# 애초에 이거는 뮤테이션 하는 의미가 없네. 내가 손쓸수있는 범위가 아니니깐 ㅇㅇ
import random 

def fun1(x):
    return x

def fun2(x):
    return x + 1

# print('add ', a.plus(1, 3))
a.plus(1, 3)

# print('minus', a.minus(1, 3))
a.minus(1, 3)

# print('multiply ', multiply(1, 3))
multiply(1, 3)

# print('divide ', divide(10, 3))
divide(10, 3)

c.hello(1)
d.test(5)
test(3)

haha.hoho()