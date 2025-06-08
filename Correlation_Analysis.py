import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def calculate_correlation(image, direction):
    if direction == 'horizontal':
        x = image[:, :-1].flatten()
        y = image[:, 1:].flatten()
    elif direction == 'vertical':
        x = image[:-1, :].flatten()
        y = image[1:, :].flatten()
    elif direction == 'diagonal':
        x = image[:-1, :-1].flatten()
        y = image[1:, 1:].flatten()
    else:
        raise ValueError("Direction must be 'horizontal', 'vertical', or 'diagonal'")
    return x, y

def plot_correlation(x, y, title, output_file):
    plt.style.use('bmh')
    plt.figure(figsize=(6, 6))
    plt.scatter(x, y, alpha=0.6, s=0.5)
    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel('Pixel Value', fontsize=12)
    plt.ylabel('Adjacent Pixel Value', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig(output_file)
    plt.close()

# Load the original, encrypted, and decrypted images
original_image = cv2.imread('/home/yash/phd/Programs/DNA_Stream_Cipher_Image_crypt/input_image_colorful.jpg')
encrypted_image = cv2.imread('s/home/yash/phd/Programs/DNA_Stream_Cipher_Image_crypt/encrypted_image_new_DNA_cipher.png')
decrypted_image = cv2.imread('/home/yash/phd/Programs/DNA_Stream_Cipher_Image_crypt/decrypted_image_new_DNA_cipher.png')

# Split the images into their color channels
original_channels = cv2.split(original_image)
encrypted_channels = cv2.split(encrypted_image)
decrypted_channels = cv2.split(decrypted_image)
colors = ('Blue', 'Green', 'Red')

# Define output directory for correlation plots
output_dir = '/home/yash/phd/Programs/DNA_Stream_Cipher_Image_crypt/Image_Analysis/'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

directions = ['horizontal', 'vertical', 'diagonal']

# Perform correlation analysis for each channel and each direction
for i, (orig_channel, enc_channel, dec_channel, color) in enumerate(zip(original_channels, encrypted_channels, decrypted_channels, colors)):
    for direction in directions:
        # Original image correlation
        x_orig, y_orig = calculate_correlation(orig_channel, direction)
        plot_correlation(x_orig, y_orig, f'Original Image {color} {direction.capitalize()} Correlation', 
                         f'{output_dir}/Original_{color}_{direction}_correlation.png')
        
        # Encrypted image correlation
        x_enc, y_enc = calculate_correlation(enc_channel, direction)
        plot_correlation(x_enc, y_enc, f'Encrypted Image {color} {direction.capitalize()} Correlation', 
                         f'{output_dir}/Encrypted_{color}_{direction}_correlation.png')
        
        # Decrypted image correlation
        x_dec, y_dec = calculate_correlation(dec_channel, direction)
        plot_correlation(x_dec, y_dec, f'Decrypted Image {color} {direction.capitalize()} Correlation', 
                         f'{output_dir}/Decrypted_{color}_{direction}_correlation.png')

print("Correlation analysis plots saved successfully.")
