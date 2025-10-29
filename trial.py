import random

def left_shift_array(arr, shift):
    """
    Circular left shift (rotation) of an array by 'shift' positions.
    """
    n = len(arr)
    shift %= n  # ensure shift < n
    return arr[shift:] + arr[:shift]


def right_shift_array(arr, shift):
    """
    Circular right shift (rotation) of an array by 'shift' positions.
    """
    n = len(arr)
    shift %= n
    return arr[-shift:] + arr[:-shift]



def UpdateRVCV(rv, cv, mv):
    print("mutator vector is")
    print(mv)
    rvxorcv=[rv[i]^cv[i] for i in range(N)]
    print("rvxorcv in update is")
    print(rvxorcv)    
    leftshifted=left_shift_array(rvxorcv,1 )
    print("left shifted is ")
    print(leftshifted)    
    rightshifted=right_shift_array(rvxorcv,1 )
    print("right shifted is")
    print(rightshifted)    
    rv1=[leftshifted[i]^mv[i] for i in range(N)]
    cv1=[rightshifted[i]^mv[i] for i in range(N)]
    print("Rv and cv after update are")
    print(rv1)
    print(cv1)
    return rv1, cv1
    

N=16
RV=[random.randint(0,1) for __ in range(N)]
CV=[random.randint(0,1) for __ in range(N)]
MV=[random.randint(0,1) for __ in range(N)]

print("original rv, cv are")
print(RV)
print(CV)
index=0
for __ in range(50):
    print("iteration no. is")
    print(__)
    RV, CV=UpdateRVCV(RV, CV, MV)
    rvxorcv=[RV[i]^CV[i] for i in range(len(RV))]
    print("rvxorcv is ")
    if rvxorcv==[0]*N:
        index=__
        break
print("Index where rvxorcv=0, is ")
print(index)
    

