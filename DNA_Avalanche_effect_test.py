import DNA_broken_cipher
import random


def bit_changed(block1, block2):
    sum=0
    for i in range(len(block1)):
	    for j in range(8):
                for k in range(8):
                    sum=sum+abs(block1[i][j][k]-block2[i][j][k])
    return(sum)

def negate(x):
     if x==1:
        return(0)
     else:
        return(1)
rw1=[]
cw1=[]
mw1=[]

rw2=[]
cw2=[]
mw2=[]
for i in range(8): 
    rw1.append(random.randint(0,1))
    cw1.append(random.randint(0,1))
    mw1.append(random.randint(0,1))


#print("rw2 is ",rw2)

sum_perc=0
n=24
for num in range(n):
    rw2=list(rw1)
    cw2=list(cw1)
    mw2=list(mw1)
    
    vec_choice=random.randint(0,2)
    print(vec_choice)
    key_choice=random.randint(0,7)
    if vec_choice==0:
         rw2[key_choice]=negate(rw2[key_choice])
    elif vec_choice==1:
        cw2[key_choice]=negate(cw2[key_choice])
    else:
        mw2[key_choice]=negate(mw2[key_choice])
    
    #print(rw2)
    pt1 =[] # plaintext
    data_size=950878
    #print("data size is ", data_size)
    for __ in range(64*int(data_size/8)):
        pt1.append(random.randint(0,1))
        
    plainBlock=DNA_broken_cipher.createBlocks(pt1)

    cipher_block1=DNA_broken_cipher.encrypt_old(plainBlock,rw1, cw1, mw1)
    cipher_block2=DNA_broken_cipher.encrypt_old(plainBlock, rw2, cw2, mw2)
    print("bits changed are",bit_changed(cipher_block1, cipher_block2))
    #print("Total number of bits", 64*int(data_size/8))
    Avalanche_effect=(bit_changed(cipher_block1, cipher_block2)/(64*int(data_size/8)))*100
    print("Percentage of Avalanche effect is ", Avalanche_effect)

    sum_perc=sum_perc+Avalanche_effect

print("Average Avalanche effect is ", sum_perc/n)


