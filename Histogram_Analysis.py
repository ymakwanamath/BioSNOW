import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# Define the directory where you want to save the histograms
output_dir = '/home/yash/phd/Programs/DNA_Stream_Cipher_Image_crypt/Image_Analysis/'

# Create the directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load the original, encrypted, and decrypted images
original_image = cv2.imread('/home/yash/phd/Programs/DNA_Stream_Cipher_Image_crypt/input_image_colorful.jpg')
encrypted_image = cv2.imread('/home/yash/phd/Programs/DNA_Stream_Cipher_Image_crypt/encrypted_image_new_DNA_cipher.png')
decrypted_image = cv2.imread('/home/yash/phd/Programs/DNA_Stream_Cipher_Image_crypt/decrypted_image_new_DNA_cipher.png')

# Function to plot and save histograms with enhanced aesthetics
def plot_and_save_histograms(original, encrypted, decrypted, output_dir):
    channels = cv2.split(original)
    encrypted_channels = cv2.split(encrypted)
    decrypted_channels = cv2.split(decrypted)
    colors = ('b', 'g', 'r')
    channel_names = ('Blue', 'Green', 'Red')
    
    # Set a style
    plt.style.use('bmh')
    
    for i, (orig_channel, enc_channel, dec_channel, color, name) in enumerate(zip(channels, encrypted_channels, decrypted_channels, colors, channel_names)):
        hist_orig = cv2.calcHist([orig_channel], [0], None, [256], [0, 256]).flatten()
        hist_enc = cv2.calcHist([enc_channel], [0], None, [256], [0, 256]).flatten()
        hist_dec = cv2.calcHist([dec_channel], [0], None, [256], [0, 256]).flatten()

        # Plot the histogram
        plt.figure(figsize=(10, 6))
        plt.title(f"Histogram Comparison for {name} Channel", fontsize=18, fontweight='bold')
        plt.xlabel("Bins", fontsize=14, fontweight='bold')
        plt.ylabel("# of Pixels", fontsize=14, fontweight='bold')
        plt.plot(hist_orig, color=color, linestyle='-', linewidth=2, alpha=0.75, label='Original')
        plt.plot(hist_enc, color=color, linestyle='--', linewidth=2, alpha=0.75, label='Encrypted')
        plt.plot(hist_dec, color=color, linestyle='-.', linewidth=2, alpha=0.75, label='Decrypted')
        plt.xlim([0, 256])
        plt.ylim([0, 2200])  # Adjust the y-axis limit as needed
        plt.grid(True, linestyle='--', alpha=0.5)
        
        # Adding legend
        plt.legend(loc='upper right', fontsize=12)
        
        # Save the histogram as an image file in the specified directory
        output_file = os.path.join(output_dir, f"Histogram_Comparison_{name}.png")
        plt.savefig(output_file, bbox_inches='tight', pad_inches=0.1)
        print(f"Histogram comparison for {name} channel saved as {output_file}")

        # Close the plot to free memory
        plt.close()

# Plot and save histograms for comparison
plot_and_save_histograms(original_image, encrypted_image, decrypted_image, output_dir)
