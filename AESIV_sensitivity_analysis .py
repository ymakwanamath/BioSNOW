from random import *



import secrets

def generate_integer_key(size):
    """
    Generates a cryptographically secure list of integers 
    containing only 0, 1, 2, or 3.
    """
    # The pool of integers to choose from
    alphabet = [0, 1, 2, 3]
    
    # Generate the list of a prescribed size
    key_array = [secrets.choice(alphabet) for _ in range(size)]
    
    return key_array



#Initial Definitions. 
A=0
C=1
G=2
T=3



def add(x, y):
    return((x+y)%4)

mul_table=[[0,0,0,0], [0,1,2,3], [0,2,3,1], [0,3,1,2]]

def mul(x, y):
    return(mul_table[x][y])


# LFSR and FSM declaration
S=[0]*256
LFSR_A=[0]*128
LFSR_B=[0]*128
R1=[0]*64
R2=[0]*64
R3=[0]*64

#defining LFSR update
def LFSR_update_function():
    t1= add(S[100], S[127])
    t2=add(S[240], S[255])

    t1= add(add(t1, mul(S[126], S[125]) ), S[245])
    t2= add(add(t2, mul(S[253], S[254])), S[114])

    for i in range(1,128):
        S[i]=S[i-1]
    S[0]=t2

    for i in range(129, 256):
        S[i]=S[i-1]
    S[128]=t1

def parallel_add(u,v):
    c=[]
    for j in range(4):
        carry_bit=0
        for i in range(16):
            bit_sum=(u[16*j+i]+v[16*j+i]+carry_bit)%4
            c.append(bit_sum)
            carry_bit=(u[16*j+i]+v[16*j+i]+carry_bit)//4
    return(c)


SBOX_Amino = {
'0000': '1203',
'0001': '1330',
'0002': '1313',
'0003': '1323',
'0010': '3302',
'0011': '1223',
'0012': '1233',
'0013': '3011',
'0020': '0300',
'0021': '0001',
'0022': '1213',
'0023': '0223',
'0030': '3332',
'0031': '3113',
'0032': '2223',
'0033': '1312',
'0100': '3022',
'0101': '2002',
'0102': '3021',
'0103': '1331',
'0110': '3322',
'0111': '1121',
'0112': '1013',
'0113': '3300',
'0120': '2231',
'0121': '3110',
'0122': '2202',
'0123': '2233',
'0130': '2130',
'0131': '2210',
'0132': '1302',
'0133': '3000',
'0200': '2313',
'0201': '3331',
'0202': '2103',
'0203': '0212',
'0210': '0312',
'0211': '0333',
'0212': '3313',
'0213': '3030',
'0220': '0310',
'0221': '2211',
'0222': '3211',
'0223': '3301',
'0230': '1301',
'0231': '3120',
'0232': '0301',
'0233': '0111',
'0300': '0010',
'0301': '3013',
'0302': '0203',
'0303': '3003',
'0310': '0120',
'0311': '2112',
'0312': '0011',
'0313': '2122',
'0320': '0013',
'0321': '0102',
'0322': '2000',
'0323': '3202',
'0330': '3223',
'0331': '0213',
'0332': '2302',
'0333': '1311',
'1000': '0021',
'1001': '2003',
'1002': '0230',
'1003': '0122',
'1010': '0123',
'1011': '1232',
'1012': '1122',
'1013': '2200',
'1020': '1102',
'1021': '0323',
'1022': '3112',
'1023': '2303',
'1030': '0221',
'1031': '3203',
'1032': '0233',
'1033': '2010',
'1100': '1103',
'1101': '3101',
'1102': '0000',
'1103': '3231',
'1110': '0200',
'1111': '3330',
'1112': '2301',
'1113': '1123',
'1120': '1222',
'1121': '3023',
'1122': '2332',
'1123': '0321',
'1130': '1022',
'1131': '1030',
'1132': '1120',
'1133': '3033',
'1200': '3100',
'1201': '3233',
'1202': '2222',
'1203': '3323',
'1210': '1003',
'1211': '1031',
'1212': '0303',
'1213': '2011',
'1220': '1011',
'1221': '3321',
'1222': '0002',
'1223': '1333',
'1230': '1100',
'1231': '0330',
'1232': '2133',
'1233': '2220',
'1300': '1101',
'1301': '2203',
'1302': '1000',
'1303': '2033',
'1310': '2102',
'1311': '2131',
'1312': '0320',
'1313': '3311',
'1320': '2330',
'1321': '2312',
'1322': '3122',
'1323': '0201',
'1330': '0100',
'1331': '3333',
'1332': '3303',
'1333': '3102',
'2000': '3031',
'2001': '0030',
'2002': '0103',
'2003': '3230',
'2010': '1133',
'2011': '2113',
'2012': '1010',
'2013': '0113',
'2020': '3010',
'2021': '2213',
'2022': '1332',
'2023': '0331',
'2030': '1210',
'2031': '1131',
'2032': '0121',
'2033': '1303',
'2100': '1200',
'2101': '2001',
'2102': '1033',
'2103': '3130',
'2110': '0202',
'2111': '0222',
'2112': '2100',
'2113': '2020',
'2120': '1012',
'2121': '3232',
'2122': '2320',
'2123': '0110',
'2130': '3132',
'2131': '1132',
'2132': '0023',
'2133': '3123',
'2200': '3200',
'2201': '0302',
'2202': '0322',
'2203': '0022',
'2210': '1021',
'2211': '0012',
'2212': '0210',
'2213': '1130',
'2220': '3002',
'2221': '3103',
'2222': '2230',
'2223': '1202',
'2230': '2101',
'2231': '2111',
'2232': '3210',
'2233': '1321',
'2300': '3213',
'2301': '3020',
'2302': '0313',
'2303': '1231',
'2310': '2031',
'2311': '3111',
'2312': '1032',
'2313': '2221',
'2320': '1230',
'2321': '1112',
'2322': '3310',
'2323': '3222',
'2330': '1211',
'2331': '1322',
'2332': '2232',
'2333': '0020',
'3000': '2322',
'3001': '1320',
'3002': '0211',
'3003': '0232',
'3010': '0130',
'3011': '2212',
'3012': '2310',
'3013': '3012',
'3020': '3220',
'3021': '3131',
'3022': '1310',
'3023': '0133',
'3030': '1023',
'3031': '2331',
'3032': '2023',
'3033': '2022',
'3100': '1300',
'3101': '0332',
'3102': '2311',
'3103': '1212',
'3110': '1020',
'3111': '0003',
'3112': '3312',
'3113': '0032',
'3120': '1201',
'3121': '0311',
'3122': '1113',
'3123': '2321',
'3130': '2012',
'3131': '3001',
'3132': '0131',
'3133': '2132',
'3200': '3201',
'3201': '3320',
'3202': '2120',
'3203': '0101',
'3210': '1221',
'3211': '3121',
'3212': '2032',
'3213': '2110',
'3220': '2123',
'3221': '0132',
'3222': '2013',
'3223': '3221',
'3230': '3032',
'3231': '1111',
'3232': '0220',
'3233': '3133',
'3300': '2030',
'3301': '2201',
'3302': '2021',
'3303': '0031',
'3310': '2333',
'3311': '3212',
'3312': '1002',
'3313': '1220',
'3320': '1001',
'3321': '2121',
'3322': '0231',
'3323': '0033',
'3330': '2300',
'3331': '1110',
'3332': '2323',
'3333': '0112'
}




def add_list(u, v):
    c=[]
    for i in range(len(u)):
        c.append(add(u[i], v[i]))
    return(c)


def Bio_Round(R):
    def quad_to_string(quad_list):
        quad_string = ''.join(map(str, quad_list))
        return(quad_string)
    def string_to_quad(quad_string):
        return [int(quad) for quad in quad_string]



    for i in range(len(R)): 
        match R[i]:
            case 0 :
                R[i]=3
            case 1 : 
                R[i]=2
            case 2 : 
                R[i]=1
            case 3 : 
                R[i]=0

    for j in range(16): 
        
        after_sbox=SBOX_Amino[quad_to_string(R[4*j: 4*(j+1)])]
        R[4*j:4*(j+1)]=string_to_quad(after_sbox)
    return(R)
        
    
def FSM_update():
    global R1, R2, R3, T2,T1
    R1=add_list(parallel_add(R2, R3), T2)
    R2=Bio_Round(R1)
    R3=Bio_Round(R2)

def keystream_generate(n):
    global Z
    for __ in range(n):
        global T1, T2
        T1=S[192:256]
        T2=S[0:64]
        FSM_update()
        for i in range(128):
            LFSR_update_function()
        print("R1")
        print(R1)
        print("R2")
        print(R2)
        print("R3")
        print(R3)
        Z.append(parallel_add(R1,T1))
        #Z.append(add_list(R1, T1))
        #Z.append(add_list(parallel_add(R1,T1),R2))
        

def flip_one_bit(arr):
    """
    Changes one bit at a random position in a list of bits.

    Args:
        arr: A list of integers (0s or 1s).

    Returns:
        The modified list with one bit flipped.
    """
    # Ensure the array is not empty
    if not arr:
        print("Error: The input array is empty.")
        return arr

    # Choose a random index to flip
    random_index = randint(0, len(arr) - 1)

    # Flip the bit at the chosen index (0 -> 1, 1 -> 0)
    arr[random_index] = 1 - arr[random_index]

    return arr
    
def change_random_element(arr):
    """
    Changes one element at a random position in an array of {0, 1, 2, 3}
    to a different value from the same set.

    Args:
        arr: A list of integers (from 0 to 3).

    Returns:
        The modified list with one element changed.
    """
    # Ensure the array is not empty
    if not arr:
        print("Error: The input array is empty.")
        return arr

    # Possible values for the elements
    possible_values = [0, 1, 2, 3]

    # Choose a random index to change
    random_index = random.randint(0, len(arr) - 1)
    
    # Get the current value at the chosen index
    current_value = arr[random_index]

    # Create a list of new possible values, excluding the current one
    new_options = [val for val in possible_values if val != current_value]
    
    # Randomly select a new value from the options
    new_value = random.choice(new_options)

    # Update the array with the new value
    arr[random_index] = new_value

    return arr

def convert_to_binary_array(arr):
    binary_arr = []
    for num in arr:
        # Convert each number to 2-bit binary representation
        bits = [(num >> 1) & 1, num & 1]
        binary_arr.extend(bits)
    return binary_arr

def convert_to_original_array(binary_arr):
    original_arr = []
    for i in range(0, len(binary_arr), 2):
        # Reconstruct number from two bits
        num = (binary_arr[i] << 1) | binary_arr[i+1]
        original_arr.append(num)
    return original_arr
def hamming_distance(arr1, arr2):
    if len(arr1) != len(arr2):
        raise ValueError("Arrays must be of the same length")
    distance = 0
    for bit1, bit2 in zip(arr1, arr2):
        if bit1 != bit2:
            distance += 1
    return distance



def flatten_list(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]

if __name__== "__main__":
    K=[]
    IV=[]
    S=[0]*256
    LFSR_A=[0]*128
    LFSR_B=[0]*128
    R1=[0]*64
    R2=[0]*64
    R3=[0]*64
    Z=[]



    for __ in range(128):
        K.append(secrets.randbelow(4))
        IV.append(secrets.randbelow(4))
    print("size of SBOX", len(SBOX_Amino))
    #Initialization

    S[0:64]= K[64:128]
    S[64:128]=IV[0:64]
    S[128:192]=IV[64:128]
    S[192:256]=K[0:64]
    """
    print(S)
    print(R1)
    print(R2)
    print(R3)
    print(len(R3))
    """
    for __ in range(1024):
        LFSR_update_function()

    for __ in range(16):
        T1=S[192:256]
        T2=S[0:64]
        FSM_update()
        for i in range(64):
            LFSR_update_function()
        
    #Keystream generation
      
    keystream_generate(5000)
    for i in range(len(Z)):
        print(Z[i])
    streamA=Z.copy()

    #Keysensitivity analysis begins here. 
    IV1=IV.copy()
    IV1=convert_to_original_array(flip_one_bit(convert_to_binary_array(IV1)))
    IV=IV1.copy()    

    S[0:64]= K[64:128]
    S[64:128]=IV[0:64]
    S[128:192]=IV[64:128]
    S[192:256]=K[0:64]
    Z=[]
    """
    print(S)
    print(R1)
    print(R2)
    print(R3)
    print(len(R3))
    """
    for __ in range(1024):
        LFSR_update_function()

    for __ in range(16):
        T1=S[192:256]
        T2=S[0:64]
        FSM_update()
        for i in range(64):
            LFSR_update_function()
        
    #Keystream generation
      
    keystream_generate(5000)
    for i in range(len(Z)):
        print(Z[i])
    streamB=Z.copy()

    arr1=convert_to_binary_array(flatten_list(streamA))
    arr2=convert_to_binary_array(flatten_list(streamB))
    print(arr1)    
    print("Hamming distance between two keystream is ")
    hd=hamming_distance(arr1, arr2)
    lenarr1=len(arr1)
    print(hamming_distance(arr1, arr2))
    print("length is")
    print(len(arr1))
    print("Avalanche effect is ")
    print(hd/lenarr1)
    
    