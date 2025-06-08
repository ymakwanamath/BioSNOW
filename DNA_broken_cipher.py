#defining key for the cipher
import random
import copy
import math
from collections import Counter

SBOX_Amino={'0000': '0023', '0001': '2100', '0002': '3200', '0003': '0221', '0010': '1332', '0011': '1112', '0012': '0112', '0013': '3122', '0020': '1033', '0021': '3230', '0022': '1222', '0023': '1002', '0030': '3232', '0031': '2211', '0032': '0012', '0033': '0301', '0100': '3310', '0101': '1133', '0102': '3302', '0103': '1212', '0110': '2210', '0111': '3032', '0112': '2233', '0113': '2122', '0120': '0333', '0121': '2102', '0122': '0133', '0123': '2003', '0130': '0231', '0131': '2311', '0132': '2032', '0133': '1113', '0200': '1010', '0201': '2320', '0202': '3021', '0203': '0100', '0210': '3201', '0211': '0300', '0212': '3113', '0213': '1102', '0220': '0223', '0221': '0030', '0222': '2321', '0223': '1302', '0230': '1323', '0231': '1022', '0232': '2203', '0233': '0202', '0300': '2232', '0301': '3301', '0302': '1132', '0303': '2010', '0310': '1003', '0311': '3011', '0312': '0001', '0313': '2332', '0320': '0201', '0321': '2020', '0322': '0212', '0323': '1111', '0330': '3003', '0331': '2121', '0332': '3030', '0333': '1223', '1000': '3213', '1001': '0123', '1002': '3000', '1003': '3103', '1010': '0232', '1011': '1313', '1012': '2111', '1013': '1032', '1020': '2031', '1021': '1301', '1022': '1000', '1023': '2231', '1030': '0111', '1031': '3210', '1032': '0032', '1033': '1101', '1100': '1320', '1101': '3133', '1102': '0011', '1103': '2011', '1110': '1120', '1111': '0033', '1112': '1331', '1113': '0131', '1120': '1021', '1121': '0310', '1122': '1201', '1123': '0003', '1130': '0003' ,'1131': '3110', '1132': '0331', '1133': '2113', '1200': '0200', '1201': '2103', '1202': '2203', '1203': '1030', '1210': '2212', '1211': '2303', '1212': '3112', '1213': '2101', '1220': '3110', '1221': '0110', '1222': '2133', '1223': '1221', '1230': '0130', '1231': '2301', '1232': '1312', '1233': '0122', '1300': '3031', '1301': '1300', '1302': '3010', '1303': '0213', '1310': '2033', '1311': '0000', '1312': '1121', '1313': '0120', '1320': '1123', '1321': '2223', '1322': '2121', '1323': '3130', '1330': '2130', '1331': '3010', '1332': '1013', '1333': '0313', '2000': '2310', '2001': '0010', '2002': '1202', '2003': '1001', '2010': '1322', '2011': '0132', '2012': '3220', '2013': '2120', '2020': '3001', '2021': '1233', '2022': '0322', '2023': '3012', '2030': '0102', '2031': '3101', '2032': '2012', '2033': '3231', '2100': '0320', '2101': '3212', '2102': '2022', '2103': '1110', '2110': '1232', '2111': '1303', '2112': '2013', '2113': '0303', '2120': '0022', '2121': '2030', '2122': '2213', '2123': '0311', '2130': '1231', '2131': '3120', '2132': '1131', '2133': '0031', '2200': '2330', '2201': '3313', '2202': '0121', '2203': '3132', '2210': '0103', '2211': '3233', '2212': '1020', '2213': '2300', '2220': '2303', '2221': '3020', '2222': '2302', '2223': '2132', '2230': '1321', '2231': '0013', '2232': '3020', '2233': '2333', '2300': '1011', '2301': '3100', '2302': '1213', '2303': '1130', '2310': '1202', '2311': '0333', '2312': '2322', '2313': '1330', '2320': '2021', '2321': '0101', '2322': '1203', '2323': '1310', '2330': '0203', '2331': '2221', '2332': '1100', '2333': '1211', '3000': '0222', '3001': '2323', '3002': '2002', '3003': '3111', '3010': '0130', '3011': '3211', '3012': '2220', '3013': '0213', '3020': '3333', '3021': '3123', '3022': '3022', '3023': '3330', '3030': '3332', '3031': '0301', '3032': '3321', '3033': '3222', '3100': '3223', '3101': '0020', '3102': '0321', '3103': '2123', '3110': '1031', '3111': '3313', '3112': '1311', '3113': '3303', '3120': '2331', '3121': '0233', '3122': '2023', '3123': '3221', '3130': '2000', '3131': '0001', '3132': '2312', '3133': '0013', '3200': '2131', '3201': '3300', '3202': '2313', '3203': '3202', '3210': '0210', '3211': '3002', '3212': '2130', '3213': '3031', '3220': '1121', '3221': '3323', '3222': '3131', '3223': '0002', '3230': '3331', '3231': '3102', '3232': '1012', '3233': '0332', '3300': '0323', '3301': '1220', '3302': '3320', '3303': '2222', '3310': '3023', '3311': '1110', '3312': '3300', '3313': '0021', '3320': '3311', '3321': '3121', '3322': '3000', '3323': '2110', '3330': '3203', '3331': '1333', '3332': '0220', '3333': '2200'}


def Bio_Round(Blocks):
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

    for i in range(len(Blocks)):
        for j in range(8):
            after_sbox=SBOX_Amino[bin_to_quad_func(binary_to_string(Blocks[i][j]))]
            Blocks[i][j]=string_to_binary(quad_to_bin_func(after_sbox))

    return(Blocks)
  


def bit_logistic_map(x, r, iterations):
    result = []
    for _ in range(iterations):
        x = (r * x * (1 - x)) % 1  # Ensure result is between 0 and 1
        bit = 1 if x > 0.5 else 0
        result.append(bit)
    return result


def cross_over(vec1, vec2, vec3):
	temp_vec=[]
	l=len(vec1)
	for i in range(l):
		if i<(int(l/2)):
			bit_to_add=vec1[i]^vec2[int(l/2)+i]
		else:
			bit_to_add=vec1[i]^vec2[i-int(l/2)]
		temp_vec.append(bit_to_add^vec3[l-i-1])
	return(temp_vec)

def createBlocks(pt):
    Blocks=[]
    counter=0
    for k in range(int(len(pt)/64)):
        tempBlock=[]
        for j in range(8):
            tempRow=[]
            for i in range(8):
                tempRow.append(pt[counter])
                counter=counter+1
            tempBlock.append(tempRow)
			
        Blocks.append(tempBlock)
    return(Blocks)


def key_variation_chaotic(rw,cw,mw):
	x1=byte_to_number(rw)
	y1=byte_to_number(cw)
	r1=byte_to_number(mw)

	logistic_array=bit_logistic_map(x1+y1,r1,24)
	(rv,cv,mv)=(list(logistic_array[0:8]),list(logistic_array[8:16]),(list(logistic_array[16:24])))
	return(rv,cv,mv)

def key_variation_old(rw, cw,mw):	
	s=[]
	for i in range(len(rw)):
		s.append(rw[i]^cw[i])
	#rotating left
	ls=[]
	for i in range(len(s)-1):
		ls.append(s[i+1])
	ls.append(s[1])
	#rotating right
	rs=[]
	rs.append(s[len(s)-1])
	for i in range(len(s)-1):
		rs.append(s[i])
	
	for i in range(len(s)):
		ls[i]=ls[i]^mw[i]
		rs[i]=rs[i]^mw[i]
	return(ls, rs)

def key_variation_new(rw, cw,mw):	
	s=[]
	for i in range(len(rw)):
		s.append(rw[i]^cw[i])
	#rotating left
	ls=[]
	for i in range(len(s)-1):
		ls.append(s[i+1])
	ls.append(s[1])
	#rotating right
	rs=[]
	rs.append(s[len(s)-1])
	for i in range(len(s)-1):
		rs.append(s[i])
	
	for i in range(len(s)):
		ls[i]=ls[i]^mw[i]
		rs[i]=rs[i]^mw[i]
	#ms=cross_over(ls,rs,mw)
	return(ls, rs,mw)



def encrypt_old(Blocks,rw,cw, mw): 
	Blocks_old=copy.deepcopy(Blocks)
	for i in range(len(Blocks_old)): 
		if i==0:
			rv=list(rw)
			cv=list(cw)
		else:
			(rv,cv)=key_variation_old(rv,cv,mw)
		for j in range(8):
			for k in range(8):
				Blocks_old[i][j][k]=Blocks_old[i][j][k]^rv[j]^cv[k]
		
		for k in range(8):
			if(cv[k]==rv[k]): 
				for j in range(8):
					temp=Blocks_old[i][k][j]
					Blocks_old[i][k][j]=Blocks_old[i][j][k]
					Blocks_old[i][j][k]=temp
	return(Blocks_old)


def key_initialization(row,column, mutator,times):
	(rv, cv,mv)=key_variation_new(row, column,mutator)
	for __ in range(times-1):
		(rv,cv,mv)=key_variation_new(rv,cv,mv)
	return(rv,cv,mv)


def encrypt_new(Blocks,rw,cw,mw):
	#rw,cw,mw=key_variation_chaotic(rw,cw,mw)
	#rw,cw,mw=key_initialization(rw,cw,mw,256)
	Blocks_new=copy.deepcopy(Blocks)
	#Blocks_new=Bio_Round(Blocks_new)
	for i in range(len(Blocks_new)): 
		if i==0:
			rv=list(rw)
			cv=list(cw)
		else:
			(rv, cv,mv)=key_variation_new(rv, cv,mw)
	
		for j in range(8):
			for k in range(8):
				Blocks_new[i][j][k]=Blocks_new[i][j][k]^rv[j]^cv[k]
	Blocks_new=Bio_Round(Blocks_new)
	for i in range(len(Blocks_new)):
		for k in range(8):
			if(cv[k]==rv[k]): 
				for j in range(8):
					temp=Blocks_new[i][k][j]
					Blocks_new[i][k][j]=Blocks_new[i][j][k]
					Blocks_new[i][j][k]=temp		
	#This is the improvement. 
	for i in range(len(Blocks_new)):
		for j in range(8):
			Blocks_new[i][j][j]=Blocks_new[i][j][j]^mv[j]
	#return(Bio_Round(Blocks_new))
	return(Blocks_new)





#Calculating PSNR ratio. 
#NMAE= \sum_{i=1}^{SSize}|S(k)-E(k)|/SSize *100 
#where Ssize is the size of bytes. 
def byte_to_number(bit_array):
	byte_number = int(''.join(map(str, bit_array)), 2)
	return(byte_number)

def byte_of_plaintext(pt, a, b):
	byte_of_pt=[]
	for i in range(8):
		byte_of_pt.append(pt[a*64+b*8+i])
	return(byte_of_pt)

def PSNR_calculate(Blocks_PSNR):
	sum=0

	maximum=0
	for i in range(len(Blocks_PSNR)):
		for j in range(8):
			plain_text_byte=byte_to_number(byte_of_plaintext(pt, i, j))
			if plain_text_byte>maximum:
				maximum=plain_text_byte
			sum=sum + abs(byte_to_number(Blocks_PSNR[i][j])-byte_to_number(byte_of_plaintext(pt,i,j)))
			
	no_of_bytes=len(pt)/8
	NMAE=(sum/no_of_bytes)*100
	PSNR= 10*math.log10((maximum*maximum)/NMAE)
	return(PSNR)





	


# now moving towards entropy
def find_entropy(Blocks_entropy):
	byte_data = b''
	for byte_arrays in Blocks_entropy:
		for byte in byte_arrays:
			byte_value = int(''.join(map(str, byte)), 2)
			byte_data += bytes([byte_value])

	# Calculate frequencies of each unique byte value
	byte_counts = Counter(byte_data)
	data_size = len(byte_data)

	# Calculate probabilities and entropy
	probabilities = [count / data_size for count in byte_counts.values()]
	entropy = -sum(p * math.log2(p) for p in probabilities if p != 0)

	return(entropy)


if __name__ == "__main__":
	sum_psnr_old=0
	sum_psnr_new=0
	sum_entropy_old=0
	sum_entropy_new=0
	for j in range(10):
		rw=[]
		cw=[]
		mw=[]
		for i in range(8): 
			rw.append(random.randint(0,1))
			cw.append(random.randint(0,1))
			mw.append(random.randint(0,1))

		#generating plaintext
		pt =[] # plaintext.
		datasize=950878
		print("data size is ", datasize)
		for __ in range(64*int(datasize/8)):
			pt.append(random.randint(0,1))

		#division into blocks
		Blocks_plaintext=createBlocks(pt)

		cipher_text_old=encrypt_old(Blocks_plaintext,rw,cw,mw)
		cipher_text_new=encrypt_new(Blocks_plaintext,rw, cw, mw)	
		
		PSNR_old=PSNR_calculate(cipher_text_old)
		
		print("Old PSNR is ")
		print(PSNR_old)

		PSNR_new=PSNR_calculate(cipher_text_new)
		print("New PSNR is")
		print(PSNR_new)

		entropy_plaintext=find_entropy(Blocks_plaintext)
		print("entropy of plaintext is ")
		print(entropy_plaintext)

		entropy_cipher_text_old=find_entropy(cipher_text_old)
		print("entropy of ciphertext by old cipher is")
		print(entropy_cipher_text_old)

		entropy_cipher_text_new=find_entropy(cipher_text_new)
		print("entropy of ciphertext by new cipher is ")
		print(entropy_cipher_text_new)

		sum_psnr_old+=PSNR_old
		sum_psnr_new+=PSNR_new
		sum_entropy_old+=entropy_cipher_text_old
		sum_entropy_new+=entropy_cipher_text_new
	
	avg_psnr_old=sum_psnr_old/10
	avg_psnr_new=sum_psnr_new/10
	avg_entropy_old=sum_entropy_old/10
	avg_entropy_new=sum_entropy_new/10

	print("average psnr old is ", avg_psnr_old)
	print(sum_psnr_old)
	print("average psnr new is ", avg_psnr_new)
	print("average entropy old is ", avg_entropy_old)
	print("average entropy new is ", avg_entropy_new)