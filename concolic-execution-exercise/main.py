from z3 import *
x = Int("x")
y = Int("y")

s = Solver()

# constraint를 더한다고 표현하시네
s.add(x + 45 < y)
s.add(x * 3 == y)
# 아 대충 보니까 위에 constraint를 걸어놓고
# 체크를 해주면 밑에서 이걸 만족하는 모델을 찾아주나보다
s.check()

# 그냥 s.model()[x]를 하게되면 wrapper class가 나오는걸
# 확인할 수 있음. as_long()을 걸어줘야 int 형식으로 나오게됨.
print("x =", s.model()[x].as_long())
print("y =", s.model()[y].as_long())