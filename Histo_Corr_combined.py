import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# Define the directory where you want to save the output images
output_dir = '/home/yash/phd/Programs/DNA_Stream_Cipher_Image_crypt/Image_Analysis/'

# Create the directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load the original, encrypted, and decrypted images
original_image = cv2.imread('/home/yash/phd/Programs/DNA_Stream_Cipher_Image_crypt/input_image_colorful.jpg')
encrypted_image = cv2.imread('/home/yash/phd/Programs/DNA_Stream_Cipher_Image_crypt/encrypted_image_new_DNA_cipher.png')
decrypted_image = cv2.imread('/home/yash/phd/Programs/DNA_Stream_Cipher_Image_crypt/decrypted_image_new_DNA_cipher.png')

# Function to plot and save histograms in a 3x3 grid
def plot_histograms_in_grid(original, encrypted, decrypted, output_file):
    channels = cv2.split(original)
    encrypted_channels = cv2.split(encrypted)
    decrypted_channels = cv2.split(decrypted)
    colors = ('b', 'g', 'r')
    titles = ('Original', 'Encrypted', 'Decrypted')
    channel_names = ('Blue', 'Green', 'Red')
    
    # Set up the figure for 3x3 grid
    fig, axes = plt.subplots(3, 3, figsize=(15, 15))
    
    for i, (orig_channel, enc_channel, dec_channel, color, name) in enumerate(zip(channels, encrypted_channels, decrypted_channels, colors, channel_names)):
        hist_orig = cv2.calcHist([orig_channel], [0], None, [256], [0, 256]).flatten()
        hist_enc = cv2.calcHist([enc_channel], [0], None, [256], [0, 256]).flatten()
        hist_dec = cv2.calcHist([dec_channel], [0], None, [256], [0, 256]).flatten()

        for j, (hist, title) in enumerate(zip([hist_orig, hist_enc, hist_dec], titles)):
            axes[j, i].plot(hist, color=color)
            axes[j, i].set_xlim([0, 256])
            axes[j, i].set_ylim([0, 4500])  # Adjust the y-axis limit as needed
            axes[j, i].set_title(f'{title} {name} Histogram', fontsize=14, fontweight='bold')
            axes[j, i].set_xlabel('Bins', fontsize=12)
            axes[j, i].set_ylabel('# of Pixels', fontsize=12)
            axes[j, i].grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    print(f"Histogram comparison grid saved as {output_file}")

# Function to calculate correlation
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

# Function to plot correlation analysis for each color channel
def plot_color_correlation_in_grid(original, encrypted, decrypted, output_file_prefix):
    directions = ['horizontal', 'vertical', 'diagonal']
    titles = ['Original', 'Encrypted', 'Decrypted']
    images = [original, encrypted, decrypted]
    color_channels = ['Blue', 'Green', 'Red']
    channel_colors = ['b', 'g', 'r']
    
    # Split images into color channels
    orig_channels = cv2.split(original)
    enc_channels = cv2.split(encrypted)
    dec_channels = cv2.split(decrypted)
    
    for channel_index, channel_color in enumerate(color_channels):
        # Set up the figure for 3x3 grid
        fig, axes = plt.subplots(3, 3, figsize=(15, 15))
        
        for i, image_channels in enumerate([orig_channels, enc_channels, dec_channels]):
            for j, direction in enumerate(directions):
                x, y = calculate_correlation(image_channels[channel_index], direction)
                axes[i, j].scatter(x, y, alpha=0.6, s=0.5, color=channel_colors[channel_index])
                axes[i, j].set_title(f'{titles[i]} {direction.capitalize()} {channel_color} Correlation', fontsize=14, fontweight='bold')
                axes[i, j].set_xlabel('Pixel Value', fontsize=12)
                axes[i, j].set_ylabel('Adjacent Pixel Value', fontsize=12)
                axes[i, j].grid(True, linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        output_file = f"{output_file_prefix}_{channel_color}_Correlation_Grid.png"
        plt.savefig(output_file)
        plt.close()
        print(f"{channel_color} correlation analysis grid saved as {output_file}")

# Define the output file paths
histogram_output_file = os.path.join(output_dir, 'Histogram_Comparison_Grid.png')
correlation_output_file_prefix = os.path.join(output_dir, 'Correlation_Analysis_Grid')

# Plot and save histograms in a 3x3 grid
plot_histograms_in_grid(original_image, encrypted_image, decrypted_image, histogram_output_file)

# Plot and save correlation analysis for each color channel in a 3x3 grid
plot_color_correlation_in_grid(original_image, encrypted_image, decrypted_image, correlation_output_file_prefix)
