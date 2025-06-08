from PIL import Image
from random import *
import DNA_broken_cipher
#from DNA_Stream_Cipher2 import *


#Initial Definitions. 
A=0
C=1
G=2
T=3



def add(x, y):
    return((x+y)%4)

mul_table=[[0,0,0,0], [0,1,2,3], [0,2,0,2], [0,3,2,1]]

def mul(x, y):
    return(mul_table[x][y])


# LFSR and FSM declaration
#S=[0]*256
#LFSR_A=[0]*128
#LFSR_B=[0]*128
#R1=[0]*64
#R2=[0]*64
#R3=[0]*64

#defining LFSR update
def LFSR_update_function():
    #print(S)
    t1=add(S[100], S[127])
   
    t2=add(S[240], S[255])
    


    t1= add(add(t1, mul(S[126], S[125]) ), S[245])
    t2= add(add(t2, mul(S[253], S[254])), S[114])

    for i in range(127,0,-1):
        S[i]=S[i-1]
    S[0]=t2

    for i in range(255, 128,-1):
        S[i]=S[i-1]
    S[128]=t1
    #print(S)
def parallel_add(u,v):
    c=[]
    for j in range(4):
        carry_bit=0
        for i in range(16):
            bit_sum=(u[16*j+i]+v[16*j+i]+carry_bit)%4
            c.append(bit_sum)
            carry_bit=(u[16*j+i]+v[16*j+i]+carry_bit)//4
    return(c)

SBOX_Amino={'0000': '0023', '0001': '2100', '0002': '3200', '0003': '0221', '0010': '1332', '0011': '1112', '0012': '0112', '0013': '3122', '0020': '1033', '0021': '3230', '0022': '1222', '0023': '1002', '0030': '3232', '0031': '2211', '0032': '0012', '0033': '0301', '0100': '3310', '0101': '1133', '0102': '3302', '0103': '1212', '0110': '2210', '0111': '3032', '0112': '2233', '0113': '2122', '0120': '0333', '0121': '2102', '0122': '0133', '0123': '2003', '0130': '0231', '0131': '2311', '0132': '2032', '0133': '1113', '0200': '1010', '0201': '2320', '0202': '3021', '0203': '0100', '0210': '3201', '0211': '0300', '0212': '3113', '0213': '1102', '0220': '0223', '0221': '0030', '0222': '2321', '0223': '1302', '0230': '1323', '0231': '1022', '0232': '2203', '0233': '0202', '0300': '2232', '0301': '3301', '0302': '1132', '0303': '2010', '0310': '1003', '0311': '3011', '0312': '0001', '0313': '2332', '0320': '0201', '0321': '2020', '0322': '0212', '0323': '1111', '0330': '3003', '0331': '2121', '0332': '3030', '0333': '1223', '1000': '3213', '1001': '0123', '1002': '3000', '1003': '3103', '1010': '0232', '1011': '1313', '1012': '2111', '1013': '1032', '1020': '2031', '1021': '1301', '1022': '1000', '1023': '2231', '1030': '0111', '1031': '3210', '1032': '0032', '1033': '1101', '1100': '1320', '1101': '3133', '1102': '0011', '1103': '2011', '1110': '1120', '1111': '0033', '1112': '1331', '1113': '0131', '1120': '1021', '1121': '0310', '1122': '1201', '1123': '0003', '1130': '0003' ,'1131': '3110', '1132': '0331', '1133': '2113', '1200': '0200', '1201': '2103', '1202': '2203', '1203': '1030', '1210': '2212', '1211': '2303', '1212': '3112', '1213': '2101', '1220': '3110', '1221': '0110', '1222': '2133', '1223': '1221', '1230': '0130', '1231': '2301', '1232': '1312', '1233': '0122', '1300': '3031', '1301': '1300', '1302': '3010', '1303': '0213', '1310': '2033', '1311': '0000', '1312': '1121', '1313': '0120', '1320': '1123', '1321': '2223', '1322': '2121', '1323': '3130', '1330': '2130', '1331': '3010', '1332': '1013', '1333': '0313', '2000': '2310', '2001': '0010', '2002': '1202', '2003': '1001', '2010': '1322', '2011': '0132', '2012': '3220', '2013': '2120', '2020': '3001', '2021': '1233', '2022': '0322', '2023': '3012', '2030': '0102', '2031': '3101', '2032': '2012', '2033': '3231', '2100': '0320', '2101': '3212', '2102': '2022', '2103': '1110', '2110': '1232', '2111': '1303', '2112': '2013', '2113': '0303', '2120': '0022', '2121': '2030', '2122': '2213', '2123': '0311', '2130': '1231', '2131': '3120', '2132': '1131', '2133': '0031', '2200': '2330', '2201': '3313', '2202': '0121', '2203': '3132', '2210': '0103', '2211': '3233', '2212': '1020', '2213': '2300', '2220': '2303', '2221': '3020', '2222': '2302', '2223': '2132', '2230': '1321', '2231': '0013', '2232': '3020', '2233': '2333', '2300': '1011', '2301': '3100', '2302': '1213', '2303': '1130', '2310': '1202', '2311': '0333', '2312': '2322', '2313': '1330', '2320': '2021', '2321': '0101', '2322': '1203', '2323': '1310', '2330': '0203', '2331': '2221', '2332': '1100', '2333': '1211', '3000': '0222', '3001': '2323', '3002': '2002', '3003': '3111', '3010': '0130', '3011': '3211', '3012': '2220', '3013': '0213', '3020': '3333', '3021': '3123', '3022': '3022', '3023': '3330', '3030': '3332', '3031': '0301', '3032': '3321', '3033': '3222', '3100': '3223', '3101': '0020', '3102': '0321', '3103': '2123', '3110': '1031', '3111': '3313', '3112': '1311', '3113': '3303', '3120': '2331', '3121': '0233', '3122': '2023', '3123': '3221', '3130': '2000', '3131': '0001', '3132': '2312', '3133': '0013', '3200': '2131', '3201': '3300', '3202': '2313', '3203': '3202', '3210': '0210', '3211': '3002', '3212': '2130', '3213': '3031', '3220': '1121', '3221': '3323', '3222': '3131', '3223': '0002', '3230': '3331', '3231': '3102', '3232': '1012', '3233': '0332', '3300': '0323', '3301': '1220', '3302': '3320', '3303': '2222', '3310': '3023', '3311': '1110', '3312': '3300', '3313': '0021', '3320': '3311', '3321': '3121', '3322': '3000', '3323': '2110', '3330': '3203', '3331': '1333', '3332': '0220', '3333': '2200'}

            




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
        #print("R1")
        #print(R1)
        #print("R2")
        #print(R2)
        #print("R3")
        #print(R3)
        Z.append(parallel_add(R1,T1))
        #Z.append(add_list(R1, T1))
        #Z.append(add_list(parallel_add(R1,T1),R2))
        





def binary_to_string(binary_list):
    binary_string = ''.join(map(str, binary_list))
    return(binary_string)

def string_to_binary(binary_string):
    return [int(bit) for bit in binary_string]
binary_to_quad={'00':'0', '01': '1', '10': '2', '11': '3'}
quad_to_binary={'0':'00', '1':'01', '2':'10', '3':'11'}

def quad_to_bin_func(quad_string):
    empty=''
    for k in range(4):
        empty=empty+quad_to_binary[quad_string[k]]
    return(empty) 

def bin_to_quad_func(binary_string):
    empty=''
    for k in range(4):
        empty=empty+binary_to_quad[binary_string[2*k:2*k+2]]
    return(empty)



def encrypt_image(image_path, output_path, cp):
    # Open an image file
    img = Image.open(image_path)
    width, height = img.size

    # Calculate the number of pixels
    num_pixels = width * height
    
    # Separate the RGB channels
    r, g, b = img.split()



    counter=0
    # Perform encryption on each channel


    new_r = Image.new('L', (width, height))
    new_g = Image.new('L', (width, height))
    new_b = Image.new('L', (width, height))

# Iterate over each pixel in the channels and apply sequential increment
    for y in range(height):
        for x in range(width):
            # Get the pixel value from each channel
            pixel_r = r.getpixel((x, y))
            pixel_g = g.getpixel((x, y))
            pixel_b = b.getpixel((x, y))
            
            
            val_to_xor_r=cp[12*(x+y)] +4*cp[12*(x+y)+1] + 16*cp[12*(x+y)+2] +64*cp[12*(x+y)+3]
            #print("val to xor r")

            #print(val_to_xor_r)
            val_to_xor_g=cp[12*(x+y)+4] +4*cp[12*(x+y)+5] + 16*cp[12*(x+y)+6] +64*cp[12*(x+y)+7]
            #print("val to xor g")
            #print(val_to_xor_g)
            val_to_xor_b=cp[12*(x+y)+8] +4*cp[12*(x+y)+9] + 16*cp[12*(x+y)+10] +64*cp[12*(x+y)+11]
            #print("val to xor b ")
            #print(val_to_xor_b)
            # Modify pixel values (you can adjust this based on your specific logic)
            new_pixel_r = pixel_r^val_to_xor_r 
            #Ensure it does not exceed 255

            #print(new_pixel_r)
            new_pixel_g = pixel_g^val_to_xor_g
            #print(new_pixel_g)
            new_pixel_b = pixel_b^val_to_xor_b
            #print(new_pixel_b)
            
            # Update the pixels in the new images
            new_r.putpixel((x, y), new_pixel_r)
            new_g.putpixel((x, y), new_pixel_g)
            new_b.putpixel((x, y), new_pixel_b)



    # Merge the encrypted channels back
    encrypted_img = Image.merge('RGB', (new_r, new_g, new_b))
    
    # Save the encrypted image
    encrypted_img.save(output_path)




def find_repeating_period(arr):
    n = len(arr)
    
    # Check all possible lengths for the repeating period
    for period in range(1, n // 2 + 1):
        if n % period == 0:  # The period must evenly divide the length of the array
            # Construct the repeating pattern
            pattern = arr[:period]
            repeated = pattern * (n // period)
            
            # Check if the reconstructed array matches the original array
            if repeated == arr:
                return period
    
    # If no repeating pattern is found
    return None


    # Example array consisting of 0s and 1s
    

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
        K.append(randint(0,3))
        IV.append(randint(0,3))

print("size of SBOX", len(SBOX_Amino))
#Initialization

S[0:64]= K[64:128]
S[64:128]=IV[0:64]
S[128:192]=IV[64:128]
S[192:256]=K[0:64]
print(S)
"""
print(S)
print(R1)
print(R2)
print(R3)
print(len(R3))
"""
for __ in range(128):
    print(S)
    LFSR_update_function()
    print("after 1 iterations")
    print(S)
for __ in range(16):
    T1=S[192:256]
    T2=S[0:64]
    FSM_update()
    for i in range(64):
        LFSR_update_function()
print(S)


    
#Keystream generation
    
keystream_generate(3000)
#print(Z)
cp = [item for sublist in Z for item in sublist]
#print(cp)
period = find_repeating_period(Z)

if period is not None:
    print(f"The array repeats every {period} elements.")
else:
    print("The array does not repeat with any period.")









# Replace 'input_image.jpg' with your input image file path
input_image = '/home/yash/phd/Programs/DNA_Stream_Cipher_Image_crypt/input_image.jpg'

# Replace 'output_image_encrypted.jpg' with your desired output image file path
output_image = '/home/yash/phd/Programs/DNA_Stream_Cipher_Image_crypt/output_image_encrypted_dna.png'

# Encryption value - you can change this value as per your encryption method
#encryption_value = 200

# Encrypt the image
encrypt_image(input_image, output_image, cp)
print(f'Image encrypted and saved to {output_image}')







# Example usage:
if __name__ == '__main__':
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
        K.append(randint(0,3))
        IV.append(randint(0,3))
    print("size of SBOX", len(SBOX_Amino))
    #Initialization

    S[0:64]= K[64:128]
    S[64:128]=IV[0:64]
    S[128:192]=IV[64:128]
    S[192:256]=K[0:64]
    print(S)
    """
    print(S)
    print(R1)
    print(R2)
    print(R3)
    print(len(R3))
    """
    for __ in range(1024):
        LFSR_update_function()
    print("after 1024 iterations")
    
    
    print(S)
    for __ in range(16):
        T1=S[192:256]
        T2=S[0:64]
        FSM_update()
        for i in range(64):
            LFSR_update_function()
    print(S)
    

       
    #Keystream generation
      
    keystream_generate(3000)
    #print(Z)
    cp = [item for sublist in Z for item in sublist]
    #print(cp)
    period = find_repeating_period(Z)
    
    if period is not None:
        print(f"The array repeats every {period} elements.")
    else:
        print("The array does not repeat with any period.")









    # Replace 'input_image.jpg' with your input image file path
    input_image = '/home/yash/phd/Programs/DNA_Stream_Cipher_Image_crypt/input_image.jpg'
    
    # Replace 'output_image_encrypted.jpg' with your desired output image file path
    output_image = '/home/yash/phd/Programs/DNA_Stream_Cipher_Image_crypt/output_image_encrypted_dna.png'
    
    # Encryption value - you can change this value as per your encryption method
    #encryption_value = 200
    
    # Encrypt the image
    encrypt_image(input_image, output_image, cp)
    print(f'Image encrypted and saved to {output_image}')


