from z3 import *

def foo(x, y):
    if x - y > 5:
        print("foo")
        if x == y * 10 + 2:
            print("bar")
        else:
            print("zoo")

class SymBool:
    def __init__(self, s, c):
        self.symbolic = s
        self.concrete = c
    
    def __repr__(self) -> str:
        return f"{self.symbolic}({self.concrete})"
    
    def negate(self):
        return SymBool(f"Not({self.symbolic})", not self.concrete)

    def __bool__(self):
        # 이렇게 바꿈으로써 참, 거짓일때 어떤 조건에서 만족해서 들어간건지 확인을 해볼수가 있어요
        # print(self.symbolic)
        if self.concrete:
            constraints.append(self)
        else:
            constraints.append(self.negate())
        return self.concrete

class SymInt:
    def __init__(self, s, c):
        self.symbolic = s
        self.concrete = c

    # 지금 SymInt에 대한 연산자가 정의가 안되어서 에러가 나오니까
    # 오버라이트해줄꺼임
    # __ 붙는걸 파이썬에서 magic method라고 하나봐

    def __repr__(self) -> str:
        return f"{self.symbolic}({self.concrete})"

    def __sub__(self, other):
        if(type(other) == int):
            other = SymInt(str(other), other)
        return SymInt(f"({self.symbolic} - {other.symbolic})", self.concrete - other.concrete)

    # 이건 두번째 연산자 기준으로 작동하는거래 쥐리네..
    def __rsub__(self, other):
        if(type(other) == int):
            other = SymInt(str(other), other)
        return SymInt(f"({other.symbolic} - {self.symbolic})", other.concrete - self.concrete)

    def __add__(self, other):
        if(type(other) == int):
            other = SymInt(str(other), other)
        return SymInt(f"({self.symbolic} + {other.symbolic})", self.concrete + other.concrete)

    def __radd__(self, other):
        if(type(other) == int):
            other = SymInt(str(other), other)
        return SymInt(f"({self.symbolic} + {other.symbolic})", self.concrete + other.concrete)

    def __mul__(self, other):
        if(type(other) == int):
            other = SymInt(str(other), other)
        return SymInt(f"({self.symbolic} * {other.symbolic})", self.concrete * other.concrete)

    def __rmul__(self, other):
        if(type(other) == int):
            other = SymInt(str(other), other)
        return SymInt(f"({self.symbolic} * {other.symbolic})", self.concrete * other.concrete)

    def __div__(self, other):
        if(type(other) == int):
            other = SymInt(str(other), other)
        return SymInt(f"({self.symbolic} / {other.symbolic})", self.concrete / other.concrete)

    # 이건 두번째 연산자 기준으로 작동하는거래 쥐리네..
    def __rdiv__(self, other):
        if(type(other) == int):
            other = SymInt(str(other), other)
        return SymInt(f"({other.symbolic} / {self.symbolic})", other.concrete / self.concrete)

    def __lt__(self, other):
        if(type(other) == int):
            other = SymInt(str(other), other)
        return SymBool(f"({self.symbolic} < {other.symbolic})", self.concrete < other.concrete)

    def __gt__(self, other):
        if(type(other) == int):
            other = SymInt(str(other), other)
        return SymBool(f"({self.symbolic} > {other.symbolic})", self.concrete > other.concrete)

    def __le__(self, other):
        if(type(other) == int):
            other = SymInt(str(other), other)
        return SymBool(f"({self.symbolic} <= {other.symbolic})", self.concrete <= other.concrete)

    def __ge__(self, other):
        if(type(other) == int):
            other = SymInt(str(other), other)
        return SymBool(f"({self.symbolic} >= {other.symbolic})", self.concrete >= other.concrete)

    def __eq__(self, other):
        if(type(other) == int):
            other = SymInt(str(other), other)
        return SymBool(f"({self.symbolic} == {other.symbolic})", self.concrete == other.concrete)
    
    def __ne__(self, other):
        if(type(other) == int):
            other = SymInt(str(other), other)
        return SymBool(f"({self.symbolic} != {other.symbolic})", self.concrete != other.concrete)


# print(x - y)
# print(x - 2)
# print(2 - x)
# print(x * 2)
# # print(x / 2)
# print(x > y)
# print(x == y)
# print(x != y)
# print(x != 0)
# print(x != 4)
_x = SymInt("x", 0)
_y = SymInt("y", 0)

print("==========")
constraints = []
foo(_x, _y)
# print(constraints)

#인쟈 이걸 활용해서 뒤집는걸 해보고 싶은디유
x = Int("x")
y = Int("y")
s = Solver()
for c in constraints[:-1]:
    # s.add(c.symbolic)
    eval(f"s.add({c.symbolic})")
eval(f"s.add({constraints[-1].negate().symbolic})")

s.check()
m = s.model()
print("x = ", m[x].as_long(), type(m[x].as_long()))
print("y = ", m[y].as_long(), type(m[y].as_long()))

_x = SymInt("x", m[x].as_long())
_y = SymInt("y", m[y].as_long())

constraints.clear()
foo(_x, _y)
print(constraints)