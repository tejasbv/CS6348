# define PY_SSIZE_T_CLEAN
import os
import cv2
import numpy as np
from Crypto.Cipher import AES
import secrets
from PIL import Image


# Define the encryption function


def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """Encrypts a file using AES (CBC mode) with the given key."""
    if not out_filename:
        out_filename = in_filename + '.enc'

    # Generate a random IV (initialization vector)
    iv = os.urandom(AES.block_size)

    # Create the AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Open the input and output files
    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            # Write the IV to the output file
            outfile.write(iv)

            # Encrypt the file in chunks
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % AES.block_size != 0:
                    # Pad the last chunk if it's not a multiple of the block size
                    chunk += b' ' * (AES.block_size - len(chunk) %
                                     AES.block_size)

                # Encrypt the chunk and write it to the output file
                outfile.write(cipher.encrypt(chunk))

# Define the function to convert a file to a binary string


def file_to_binary(filename):
    """Reads a file and returns its contents as a binary string."""
    with open(filename, 'rb') as file:
        binary_string = ''
        while True:
            byte = file.read(1)
            if not byte:
                break
            # Convert the byte to binary and append it to the binary string
            binary_string += bin(ord(byte))[2:].zfill(8)
        file = open("binarystring.txt", "w")
        file.write(binary_string)
        file.close()
        return binary_string


# Define the video dimensions
width = 640
height = 480

# Generate a strong random key
key = secrets.token_bytes(32)

# Save the key to a file
with open('key.txt', 'wb') as key_file:
    key_file.write(key)

# Define the input file
in_filename = 'temp.txt'

# Encrypt the file
encrypt_file(key, in_filename)

# Convert the encrypted file to a binary string
encrypted_filename = in_filename + '.enc'
encrypted_binary = file_to_binary(in_filename)
print(len(encrypted_binary))
padding_length = width*height - (len(encrypted_binary) % (width*height))
encrypted_binary += '0' * padding_length
print(len(encrypted_binary))
binary_string = encrypted_binary


# Pad the binary string with zeros at the beginning to make it a multiple of 4
while len(binary_string) % 4 != 0:
    binary_string = '0' + binary_string

# Calculate the number of images needed
num_images = (len(binary_string) // (320 * 180)) + 1


fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter('binary_video.mp4', fourcc, 25, (1280, 720), isColor=False)

# Loop through the binary string and generate images
for i in range(num_images):
    # Create a 1280x720 image with all white pixels
    image_data = np.zeros((720, 1280), dtype=np.uint8) + 255

    # Set up counters to keep track of current row and column
    current_row = 0
    current_col = 0

    # Loop through the binary string and update the pixels of the image
    for j in range(i*320*180, (i+1)*320*180, 4):
        chunk = binary_string[j:j+4]
        if(chunk != ''):
            for k in range(4):
                pixel_value = 255 - int(chunk[k])*255  # 0 -> white, 1 -> black
                image_data[current_row:current_row+4, current_col:current_col+4] = pixel_value
                current_col += 4
                if current_col == 1280:  # Move to the next row if we have reached the end of the current row
                    current_row += 4
                    current_col = 0
    # Save the final image
    final_image = Image.fromarray(image_data, mode='L')
    # final_image.save(f"binary_image_{i}.png")
    video_writer.write(np.array(image_data))
    print(f"{i}/{num_images}")

video_writer.release()
