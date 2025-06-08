# This program is for generating equations from SNOW cipher. 

# Firstly, we will develop a program for SNOW cipher and then put the values and variables, which will in turn give us the equations. 

#SNOW is basically divided into two parts LFSR and FSM. We first develop the LFSR part: 

#Define two LFSRs of size 16, where each cell has 16 bits. 
from PIL import Image
import numpy as np
from random import *

def genrandom16bits():
    random16bits=[]
    for i in range(16):
        random16bits.append(randint(0,1))
    return random16bits

A=[]
B=[]
for i in range(16):
    A.append(genrandom16bits())
    B.append(genrandom16bits())
print(A)
print(B)

Z=[]
#For once, we have defined it as all zero. But, when we will find equations, we shall replace them by actual key values.

#Each element is a word in F_{2^16}

#Generating Polynomial of LFSR-A is 

def LFSR_shift():
    #This defines the shifting of LFSRs
    for __ in range(8):
        LFSR_clock()

def F_n_times(F, n, u):
    #This function defines applying F n times to a value. 
    for __ in range(n): 
        u=F(u)
    return(u)

def Xor_list(list_of_lists): 
    #This function defines xoring of a list of lists 
    c=[]
    for i in range(len(list_of_lists[0])):
        x=list_of_lists[0][i]
        for j in range(1,len(list_of_lists)):
            x=x^list_of_lists[j][i]
        c.append(x)
    return(c)
    

def mul_alpha(u):
    v=[u[15], u[0]+u[15], u[1]+u[15], u[2]+u[15], u[3], u[4], u[5], u[6], u[7]+u[15], u[8], u[9], u[10]+u[15], u[11]+u[15], u[12], u[13], u[14]+u[15]]
    #This defines the multiplication by the root of g^A(x) polynomial
    return(v)

def mul_alpha_inv(u): 
   v=[0]*16
   v= Xor_list([u, mul_alpha(u), F_n_times(mul_alpha, 2, u), F_n_times(mul_alpha, 7,u), F_n_times(mul_alpha, 10, u), F_n_times(mul_alpha, 11, u), F_n_times(mul_alpha, 14, u), F_n_times(mul_alpha, 15, u)])
   return(v)
    #This defines the multiplication by alpha inverse
    

def mul_beta(u):
    v=[u[15], (u[0] + u[15])%2, u[1], u[2], u[3], (u[4]+u[15])%2, (u[5]+u[15])%2, u[6], (u[7]+u[15])%2, u[8], u[9], (u[5]+u[15])%2, u[11], u[12], u[13] + u[15], (u[14]+u[15])%2]
    return(v)
     #This defines the multiplication by the root of g^B(x) polynomial
    

def mul_beta_inv(u): 

    v=[0]*16
    v=Xor_list([u, mul_beta(u), F_n_times(mul_beta, 4, u), F_n_times(mul_beta, 5, u), F_n_times(mul_beta, 7, u), F_n_times(mul_beta, 10, u), F_n_times(mul_beta, 10, u), F_n_times(mul_beta, 13, u), F_n_times(mul_beta, 14, u), F_n_times(mul_beta, 15, u)])
    #this defines the multiplication of beta inverse. 
    return(v)
def bin_add(u,v):
    c=[]
    for i in range(len(u)):
        c.append((u[i]+v[i])%2)
    return(c)
def LFSR_clock():
    A15= bin_add(B[0],bin_add(mul_alpha(A[0]), bin_add(A[1], mul_alpha_inv(A[8]))))
    B15= bin_add(A[0],bin_add(mul_beta(B[0]),bin_add(B[3], mul_beta_inv(B[8]))))
    for i in range(16-1):
        
        A[i]=A[i+1]
        B[i]=B[i+1]

    B[15]=B15
    A[15]=A15

T1=[0]*128
T2=[0]*128

def Tap_update():
    global T1
    global T2
    LFSR_shift()
    T1_tap=[]
    T2_tap=[]
    T1=[B[8], B[9], B[10], B[11], B[12], B[13], B[14], B[15]]
    for i in range(8):
        T1_tap.extend(T1[i])
    
    T2=[A[0], A[1], A[2], A[3], A[4], A[5], A[6], A[7]]
    for i in range(8):
        T2_tap.extend(T2[i])
    T1=T1_tap
    T2=T2_tap


#Now, the below part defines the FSM Part and AES encryption part. 
#We define the three 128 bit registers: 

R1=[0]*128
R2=[0]*128
R3=[0]*128

def sigma(u1): 
    # This defines the sigma permuatation
    # convert to bytes
    u=[]
    v=[]
    for i in range(16):
        temp=[]
        for j in range(8): 
            temp.append(u1[i*8+j])
        u.append(temp)

    v1=[u[0], u[4], u[8], u[12], u[1], u[5], u[9], u[13], u[2], u[6], u[10], u[14], u[3], u[7], u[11], u[15]]
    for i in range(16):
        v.extend(v1[i])
    return(v)


def Add_32_parallel(u,v):
    c=[]
    for j in range(4):
        carry_bit=0
        for i in range(32):
            bit_sum=(u[32*j+i]+v[32*j+i]+carry_bit)%2
            c.append(bit_sum)
            carry_bit=(u[32*j+i]+v[32*j+i]+carry_bit)//2
    return(c)

def Xor_simple(u,v):
    c=[]
    for i in range(len(u)):
        c.append(u[i]^v[i])
    return(c)





# here comes the AES round function: 
# Define S-box (Substitution box) for AES
S_BOX = [0x63,0x7C,0x77,0x7B,0xF2,0x6B,0x6F,0xC5,0x30,0x01,0x67,0x2B,0xFE,0xD7,0xAB,0x76, 0xCA,0x82,0xC9,0x7D,0xFA,0x59,0x47,0xF0,0xAD,0xD4,0xA2,0xAF,0x9C,0xA4,0x72,0xC0, 0xB7,0xFD,0x93,0x26,0x36,0x3F,0xF7,0xCC,0x34,0xA5,0xE5,0xF1,0x71,0xD8,0x31,0x15,0x04,0xC7,0x23,0xC3,0x18,0x96,0x05,0x9A,0x07,0x12,0x80,0xE2,0xEB,0x27,0xB2,0x75, 0x09,0x83,0x2C,0x1A,0x1B,0x6E,0x5A,0xA0,0x52,0x3B,0xD6,0xB3,0x29,0xE3,0x2F,0x84, 0x53,0xD1,0x00,0xED,0x20,0xFC,0xB1,0x5B,0x6A,0xCB,0xBE,0x39,0x4A,0x4C,0x58,0xCF, 0xD0,0xEF,0xAA,0xFB,0x43,0x4D,0x33,0x85,0x45,0xF9,0x02,0x7F, 0x50,0x3C,0x9F,0xA8, 0x51,0xA3,0x40,0x8F,0x92,0x9D,0x38,0xF5,0xBC,0xB6,0xDA,0x21,0x10,0xFF,0xF3,0xD2, 0xCD,0x0C, 0x13,0xEC,0x5F,0x97,0x44,0x17,0xC4,0xA7,0x7E,0x3D,0x64,0x5D,0x19,0x73, 0x60,0x81,0x4F,0xDC,0x22,0x2A,0x90,0x88, 0x46,0xEE,0xB8,0x14,0xDE,0x5E,0x0B,0xDB, 0xE0,0x32,0x3A,0x0A,0x49,0x06,0x24,0x5C,0xC2,0xD3,0xAC,0x62,0x91,0x95,0xE4,0x79, 0xE7,0xC8,0x37,0x6D,0x8D,0xD5,0x4E,0xA9,0x6C,0x56,0xF4,0xEA,0x65,0x7A,0xAE,0x08, 0xBA,0x78,0x25,0x2E, 0x1C,0xA6,0xB4,0xC6,0xE8,0xDD,0x74,0x1F,0x4B,0xBD,0x8B,0x8A, 0x70,0x3E,0xB5,0x66,0x48,0x03,0xF6,0x0E,0x61,0x35, 0x57,0xB9,0x86,0xC1,0x1D,0x9E, 0xE1,0xF8,0x98,0x11,0x69,0xD9,0x8E,0x94,0x9B,0x1E,0x87,0xE9,0xCE,0x55,0x28,0xDF, 0x8C,0xA1,0x89,0x0D,0xBF,0xE6,0x42,0x68,0x41,0x99,0x2D,0x0F,0xB0,0x54,0xBB,0x16]

# Now, we have to define the AES function. 
# AES has 4 steps namely, 1) SubBytes, 2) Shift Rows 3) Mix columns 4) AddRoundKey. But before operating these, we have to transform the sequence of bytes into a matrix. 

def seq_to_matrix(bit_array):
    bit_matrix=[]
    
    for i in range(4):
        
        temp2=[]
        for j in range(4):
            byte=[]
            for k in range(8):
                byte.append(bit_array[32*j+8*i+k])    
            temp2.append(byte)
        bit_matrix.append(temp2)
    return(bit_matrix)

def matrix_to_seq(bit_matrix):
    bit_array=[]

    for j in range(4):
        for i in range(4): 
            for k in range(8):
                bit_array.append(bit_matrix[i][j][k])
    return(bit_array)




def SBox_Apply(bit_array):
    bit_array.reverse()
    byte_value = 0
    
    for bit in bit_array:
        byte_value = (byte_value << 1) | bit
    #print(byte_value)  # This will give you the integer value of the byte
    #print(hex(byte_value))  # This will give you the hexadecimal representation of the byte
   
    output=S_BOX[byte_value]
    #print(output)
    hex_value = output  # Replace this with the hexadecimal value you want to convert

    byte_value2 = int(str(hex_value), 16)
    #print(byte_value)
    bit_array = []

    for i in range(7, -1, -1):
        bit = (byte_value2 >> i) & 1
        bit_array.append(bit)
    bit_array.reverse()


#Now, we proceed towards first operation of AES encryption round that is #Subbytes 
def SubBytes(bit_matrix):
    for i in range(4):
        for j in range(4):
            SBox_Apply(bit_matrix[i][j])
    return(bit_matrix)

# Now we apply second operation that is shiftrows

def shiftRows(bit_matrix):
    bit_matrix_new=[]
    bit_matrix_new.append(bit_matrix[0])
    
    for r in range(1,4):
        temp=[]
        for i in range(4):
            temp.append(bit_matrix[r][(i+r)%4])
        bit_matrix_new.append(temp)
    
    bit_matrix=bit_matrix_new
    return(bit_matrix_new)

def mul_byte_sc(alpha, byte_val):
    return((alpha*byte_val)%256)

def sc_mul(alpha, X):
    for i in range(len(X)):
        Y[i]=X[i]*alpha
    return(Y)

def bit_to_byte(bit_array):
    bit_array.reverse()
    byte_value = 0
    for bit in bit_array:
        byte_value = (byte_value << 1) | bit
    #print(byte_value)  # This will give you the integer value of the byte
    return(byte_value)  # This will give you the hexadecimal representation of the byte


def byte_to_bit(byte_val):
    byte_value = int(str(byte_val), 16)
    #print(byte_value)
    bit_array = []

    for i in range(7, -1, -1):
        bit = (byte_value >> i) & 1
        bit_array.append(bit)
    bit_array.reverse()
    return(bit_array)


def Mix_Columns(bit_matrix):
    zero1=[0]*8
    zero2=[zero1]*4
    S=[zero2]*4

    for i in range(4):
        for j in range(4):
            bit_matrix[i][j]= bit_to_byte(bit_matrix[i][j])
    
    for c in range(0, 4):
        S[0][c]=byte_to_bit(mul_byte_sc(2,bit_matrix[0][c]) ^ mul_byte_sc(3, bit_matrix[1][c]) ^ bit_matrix[2][c] ^ bit_matrix[3][c])

        S[1][c]= byte_to_bit(bit_matrix[0][c] ^ mul_byte_sc(2, bit_matrix[1][c]) ^ mul_byte_sc(3, bit_matrix[2][c]) ^ bit_matrix[3][c])

        S[2][c]= byte_to_bit(bit_matrix[0][c] ^ bit_matrix[1][c]^ mul_byte_sc(2, bit_matrix[2][c])^ mul_byte_sc(3,bit_matrix[3][c]))

        S[3][c]= byte_to_bit(mul_byte_sc(3, bit_matrix[0][c])^ bit_matrix[1][c]^ bit_matrix[2][c]^ mul_byte_sc(2, bit_matrix[3][c]))
    bit_matrix= S
    return(bit_matrix)

def AES_Enc_Round(bit_array):
    after_aes_enc= matrix_to_seq(Mix_Columns(shiftRows(SubBytes(seq_to_matrix(bit_array)))) )    
    return(after_aes_enc)

def update_FSM():
    global R3
    global R2
    R1=Xor_simple(R3,T2)
    R1= sigma(Add_32_parallel(Xor_simple(R3, T2), R2))
    R2= AES_Enc_Round(R1)
    R3=AES_Enc_Round(R2)

def output_SNOW(n):
    global Z
    for i in range(n):
        output= Xor_simple(Add_32_parallel(R1,T1), R2)
        Z.append(output)
        

        #print("The {} output is {}".format(i, output))
        Tap_update()
        update_FSM()

output_SNOW(90000)
def concatenate_sublists(Z):
            return [item for sublist in Z for item in sublist]

        # Example usage

Z = concatenate_sublists(Z)
#print(Z)


def binary_list_to_bytes(binary_list):
    """Convert a list of 0s and 1s into a list of bytes."""
    length = len(binary_list)
    
    # Calculate padding length to make the length a multiple of 8
    if length % 8 != 0:
        padding_length = 8 - (length % 8)
        binary_list += [0] * padding_length

    # Convert the list to bytes
    byte_list = []
    for i in range(0, len(binary_list), 8):
        byte_chunk = binary_list[i:i+8]
        # Convert the 8-bit list chunk to a byte
        byte_value = int(''.join(map(str, byte_chunk)), 2)
        byte_list.append(byte_value)
    
    return byte_list

# Example binary sequence as a list
#binary_list = [0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1]  # Example sequence

# Convert the binary list to a list of bytes
Z = binary_list_to_bytes(Z)
#print(Z)
#print(len(Z))











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
    
period = find_repeating_period(Z)
    
if period is not None:
    print(f"The array repeats every {period} elements.")
else:
    print("The array does not repeat with any period.")






# Function to XOR encrypt a channel with the sequence
def xor_encrypt_channel(channel, sequence):
    height, width = channel.shape
    num_pixels = height * width
    encrypted_channel = np.zeros_like(channel)

    # Apply XOR operation with the sequence
    for i in range(height):
        for j in range(width):
            pixel_index = i * width + j
            encrypted_channel[i, j] = channel[i, j] ^ sequence[pixel_index]

    return encrypted_channel

# Path to your input image
input_image_path = '/home/yash/phd/Programs/DNA_Stream_Cipher_Image_crypt/input_image33.jpg'  # Replace with the path to your input image
# Path to save the encrypted image
output_image_path = '/home/yash/phd/Programs/DNA_Stream_Cipher_Image_crypt/encrypted_image_snow_yash_different_Z33.png'  # Replace with the desired output file name
# path to decrypted image. 
decrypted_image_path='/home/yash/phd/Programs/DNA_Stream_Cipher_Image_crypt/decrypted_image_snow_yash_different_Z33.png' 
# Your provided sequence of 0s and 1s
#sequence = [0, 1] * (100 * 100)  # Example sequence; replace with your actual sequence

# Load the image
image = Image.open(input_image_path)
image_array = np.array(image)

# Check if image is in RGB format
if image_array.ndim != 3 or image_array.shape[2] != 3:
    raise ValueError("The input image must be an RGB image.")

height, width, _ = image_array.shape
num_pixels = height * width
print(num_pixels)
# Ensure the sequence length is sufficient
if len(Z) < num_pixels:
    raise ValueError("The length of the sequence must be at least as long as the number of pixels in the image.")

# Extract RGB channels
r_channel = image_array[:, :, 0]
g_channel = image_array[:, :, 1]
b_channel = image_array[:, :, 2]
print(r_channel)
# Encrypt each channel using the sequence
encrypted_r = xor_encrypt_channel(r_channel, Z[0:num_pixels])
encrypted_g = xor_encrypt_channel(g_channel, Z[num_pixels:2*num_pixels])
encrypted_b = xor_encrypt_channel(b_channel, Z[2*num_pixels:3*num_pixels])

# Combine the encrypted channels
encrypted_image_array = np.stack([encrypted_r, encrypted_g, encrypted_b], axis=-1)

# Convert the encrypted array back to an image
encrypted_image = Image.fromarray(encrypted_image_array.astype(np.uint8))

# Save the encrypted image
encrypted_image.save(output_image_path)

print(f"Encrypted image saved to {output_image_path}")




##decryption
image = Image.open(output_image_path)
image_array = np.array(image)
r_channel = image_array[:, :, 0]
g_channel = image_array[:, :, 1]
b_channel = image_array[:, :, 2]
print(r_channel)
# Encrypt each channel using the sequence
encrypted_r = xor_encrypt_channel(r_channel, Z)
encrypted_g = xor_encrypt_channel(g_channel, Z)
encrypted_b = xor_encrypt_channel(b_channel, Z)

# Combine the encrypted channels
encrypted_image_array = np.stack([encrypted_r, encrypted_g, encrypted_b], axis=-1)

# Convert the encrypted array back to an image
encrypted_image = Image.fromarray(encrypted_image_array.astype(np.uint8))

# Save the encrypted image
encrypted_image.save(decrypted_image_path)

print(f"Encrypted image saved to {decrypted_image_path}")

