import sympy as sp
import random
from sympy import Xor, Not
N=16
mv= sp.symbols(f'mv0:{N}', boolean=True)

rv=[random.randint(0,1) for __ in range(N)]
cv=[random.randint(0,1) for __ in range(N)]



def key_update(rv1,cv1):
    rv1xorcv1=[rv1[i]^cv1[i] for i in range(N)]
    #right shift
    right_shifted= rv1xorcv1[-1:] + rv1xorcv1[:-1]
    
    #left shift
    left_shifted= rv1xorcv1[1:] + rv1xorcv1[:1]

    rv2=[Xor(right_shifted[i],mv[i]) for i in range(N)]
    cv2=[Xor(left_shifted[i], mv[i]) for i in range(N)]

    return (rv2,cv2)
print("Value of N is")
print(N)
print("rv^i and cv^i are: ")
print(rv)
print(cv)
rv,cv=key_update(rv,cv)
print("rv^(i+1) and cv^(i+1) are: ")
print(rv)
print(cv)
rv,cv=key_update(rv,cv)
print("rv^(i+2) and cv^(i+2) are: ")
print(rv)
print(cv)
rv,cv=key_update(rv,cv)
print("rv^(i+3) and cv^(i+3) are: ")
print(rv)
print(cv)