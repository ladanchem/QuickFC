import math


e1=1
p1=1
r1=0.1
r2=0.6

x = -e1 / ((e1 + p1) * math.log(1 - r1))
u2 = -x * math.log(1 - r2)
if u2 <= 0.5:
    pentane_result2 = 1 / u2 - 1
    ea_result2 = 1
else:
    x = -p1 / ((e1 + p1) * math.exp(1 - r1))
    u2 = -x * math.exp(1 - r2)
    pentane_result2 = 1
    ea_result2 = 1 / u2 - 1

print(x)
print(u2)
print(pentane_result2)
print(ea_result2)



if ea_result2 <= 1:
    ea_result2 = 1
if pentane_result2 <= 1:
    pentane_result2 = 1