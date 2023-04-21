import cv2
import numpy as np
from AES.aes import myAES

# Open the video file
fileName = 'temp.txt_17968.mp4'
out_file_name = "out_"+fileName.split('_')[0]
padding = int(fileName.split('_')[1].split('.')[0])
video_reader = cv2.VideoCapture(fileName)

# Set up counters to keep track of current row and column
current_row = 0
current_col = 0

# Create an empty string to store the binary data
binary_string = ''

# Loop through the frames of the video
f=0
while True:
    # Read a frame from the video
    ret, frame = video_reader.read()
    if not ret:  # If there are no more frames, break out of the loop
        binary_string = binary_string[:-padding]
        break

    # Convert the frame to grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Extract the pixels from the frame and append them to the binary string
    for i in range(0, 720, 4):
        for j in range(0, 1280, 4):
            pixel_value = frame_gray[i:i+4, j:j+4].mean() / 255  # Calculate the mean pixel value and normalize to 0-1
            binary_string += '0' if pixel_value > 0.5 else '1'
    f+=1
    print(f"reading frame {f}")
    

# # Trim any trailing zeros from the binary string
# while binary_string[-1] == '0':
#     binary_string = binary_string[:-1]

# Save the binary string to a file
with open('binary_string.txt', 'w') as f:
    f.write(binary_string)

# Print a message indicating the file was saved
print("Binary string extracted from video, converting binary to ascii")
# text = ''
# for i in range(0, len(binary_string), 8):
#     chunk = binary_string[i:i+8]  # take 8 characters at a time
#     decimal = int(chunk, 2)  # convert binary to decimal
#     text += chr(decimal)

# with open(out_file_name+".enc", 'wb') as f:
#     f.write(text.encode("utf-8"))

with open(out_file_name+".enc", 'wb') as new_file:
    # Write the binary string to the new file
    for i in range(0, len(binary_string), 8):
        byte = int(binary_string[i:i+8], 2)
        new_file.write(bytes([byte]))

print(f"output file name is {out_file_name}")
aes = myAES("temp.txt"+".enc", "out_file_name.txt","password" )
aes.decrypt()
