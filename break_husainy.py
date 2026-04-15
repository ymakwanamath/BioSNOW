import random
import time
import copy

import sympy as sp

from sympy import Xor, Not

n=2
N=8*n

rv=[random.randint(0,1) for __ in range(N)]
print("Secret Row Vector is ")
print(rv)
initial_rv=rv.copy()
cv=[random.randint(0,1) for __ in range(N)]
initial_cv=cv.copy()
print("Secret Column Vector is")
print(cv)
mv=[random.randint(0,1) for __ in range(N)]
print("Secret Mutator Vector is")
print(mv)
rvxorcv=[rv[i]^cv[i] for i in range(N)]

num_Blocks=2
plaintext1= [[random.randint(0, 1) for _ in range(N)] for _ in range(N)]
print("plaintext Block 1 is ")
print(plaintext1)
plaintext2= [[random.randint(0, 1) for _ in range(N)] for _ in range(N)]
print("plaintext Block 2 is ")
print(plaintext2)

cipher1=copy.deepcopy(plaintext1)
cipher2=copy.deepcopy(plaintext2)

#XOR with rv and cv

def encryption(cipher):
    for i in range(N):
        for j in range(N):
            cipher[i][j]=cipher[i][j]^rv[j]^cv[i]

    #Selective Transpose
    for i in range(N):
        if rvxorcv[i]==1:
            # Swap the symmetric elements around the diagonal for the chosen position
            for pos in range(N):
                cipher[i][pos], cipher[pos][i] = cipher[pos][i], cipher[i][pos]
    return cipher

def key_update(rv1,cv1):
    rv1xorcv1=[rv1[i]^cv1[i] for i in range(N)]
    #right shift
    right_shifted= rv1xorcv1[-1:] + rv1xorcv1[:-1]
    
    #left shift
    left_shifted= rv1xorcv1[1:] + rv1xorcv1[:1]

    rv2=[right_shifted[i]^mv[i] for i in range(N)]
    cv2=[left_shifted[i]^mv[i] for i in range(N)]

    return rv2,cv2


cipher1=encryption(cipher1)


def recover_rv_cv(plaintext1, cipher1, initial_rv, initial_cv):
    rvfind= sp.symbols(f'rvfind0:{N}', boolean=True)
    cvfind= sp.symbols(f'cvfind0:{N}', boolean=True)

    #From here the attack starts. 

    #Let us say we know diagonal bits of cipher1 and plaintext1.

    diag1=[plaintext1[i][i]^ cipher1[i][i] for i in range(N)]

    #print("Check if diagonal is equal to rvxorcv")
    #verify if we are correct
    #print(diag1==rvxorcv)


    #Now we suppose the first row elements are also known. 
    #first_row=[plaintext1[0][i]^ cipher1[0][i] for i in range(N)]


    element_p10=plaintext1[1][0]^cipher1[1][0]

    if diag1[0]^diag1[1]==0:
        expr1=Xor(rvfind[1],cvfind[0],plaintext1[0][1],cipher1[0][1])
    else:
        expr1=Xor(rvfind[1],cvfind[0],plaintext1[0][1],cipher1[1][0])


    #Now from the knowledge of element_p10, we get


    if diag1[0]^diag1[1]==0:
        expr2=Xor(rvfind[1],diag1[0],cvfind[0],diag1[1],plaintext1[1][0],cipher1[1][0])
    else:
        expr2=Xor(rvfind[1],diag1[0],cvfind[0],diag1[1],plaintext1[1][0],cipher1[0][1])


    print("Equations generated from the pair p_10 are:")
    print(expr1)
    print(expr2)

    if expr1==expr2:
        print("Two solutions present")

    #case 1: 
    print("The first set of solutions are")
    print("Both of the expressions must result to 0")

    print(expr1==Xor(cvfind[0],rvfind[1]))
    print(Xor(cvfind[0], rvfind[1]))
    if expr1==Xor(cvfind[0],rvfind[1]):

        rvfindval=[1^diag1[0],1]


        for j in range(2,N):
            if diag1[0]^diag1[j]==0:
                rvfindval.append(1^plaintext1[0][j]^cipher1[0][j])
            else:
                rvfindval.append(1^plaintext1[0][j]^cipher1[j][0])
        print("Recovered Row Vector is ")
        print(rvfindval)
        #print("Initial Row Vector is ")
        #print(initial_rv)
        #print("Compare Recovered Row Vector and Initial Row Vector.")

        cvfindval=[rvfindval[i]^diag1[i] for i in range(N)]
        print("Recoverd Column Vector is ")
        print(cvfindval)
        #print("Initial Column Vector is")
        #print(initial_cv)
        #print("Compare Recovered Column Vector and Initial Row Vector")
        print("Second Set of solutions is ")

        rvfindval=[0^diag1[0],0]
        for j in range(2,N):
            if diag1[0]^diag1[j]==0:
                rvfindval.append(1^plaintext1[0][j]^cipher1[0][j])
            else:
                rvfindval.append(1^plaintext1[0][j]^cipher1[j][0])
        print("Recovered Row Vector is ")
        print(rvfindval)
        #print("Initial Row Vector is ")
        #print(initial_rv)
        #print("Compare Recovered and Initial Row Vector")
        cvfindval=[rvfindval[i]^diag1[i] for i in range(N)]
        print("Recoverd Column Vector is ")
        print(cvfindval)
        #print("Initial Column Vector is")
        #print(initial_cv)  
        #print("Compare Recovered and Initial Column Vector")  

    else:
        rvfindval=[0^diag1[0],1]
        print("First set is ")

        for j in range(2,N):
            if diag1[0]^diag1[j]==0:
                rvfindval.append(0^plaintext1[0][j]^cipher1[0][j])
            else:
                rvfindval.append(0^plaintext1[0][j]^cipher1[j][0])
        print("Recovered Row Vector is")
        print(rvfindval)
        #print("Intial Row Vector is ")
        #print(initial_rv)
        #print("Compare Recovered and Initial Row Vector")
        cvfindval=[rvfindval[i]^diag1[i] for i in range(N)]
        print("Recoverd Column Vector is ")
        print(cvfindval)
        #print("Initial Column Vector is")
        #print(initial_cv)
        #print("Compare Recovered and Initial Column Vector") 

        print("Second Set of solutions is ")
        

        rvfindval=[1^diag1[0],0]


        for j in range(2,N):
            if diag1[0]^diag1[j]==0:
                rvfindval.append(1^plaintext1[0][j]^cipher1[0][j])
            else:
                rvfindval.append(1^plaintext1[0][j]^cipher1[j][0])
        print("Recovered Row Vector is ")
        print(rvfindval)
        #print("Initial Row Vector is")
        #print(initial_rv)
        #print("Compare Recovered and Initial Row Vector")
        cvfindval=[rvfindval[i]^diag1[i] for i in range(N)]
        print("Recoverd Column Vector is ")
        print(cvfindval)
        #print("Initial Column Vector is")
        #print(initial_cv)
        #print("Compare Recovered and Initial Column Vector") 



def mv_recover(rv1,cv1, rv2, cv2):
    rv1xorcv1=[rv1[i]^cv1[i] for i in range(N)]
    #right shift
    right_shifted= rv1xorcv1[-1:] + rv1xorcv1[:-1]
    
    #left shift
    left_shifted= rv1xorcv1[1:] + rv1xorcv1[:1]

    mv=[right_shifted[i]^rv2[i] for i in range(N)]
    
    return mv


start=time.time()
recover_rv_cv(plaintext1, cipher1, initial_rv, initial_cv)

rv,cv=key_update(rv,cv)
initial_cv2=cv.copy()
initial_rv2=rv.copy()

print("Now let us assume that we have got row and column vectors from two plaintext-ciphertext blocks")
print("The recovered mutator vector is ")
print(mv_recover(initial_rv, initial_cv, initial_rv2, initial_cv2))
print("The Initial mutator vector is ")
print(mv)
end=time.time()

print("time taken is")
print(end-start)