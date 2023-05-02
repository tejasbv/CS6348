# define PY_SSIZE_T_CLEAN
import os
import cv2
import numpy as np
from PIL import Image
# from myProgram.AES.aes import myAES

from AES.aes import myAES
from YTHandler import YThandler
# from Google.YTHandler import YThandler


class Handler:

    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        self.ytHandler = YThandler()

    def file_to_binary(self, filename):
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

    def save(self, path, password, title, desc):
        in_filename = path
        display = ""
        # Encrypt the file
        aes = myAES(in_filename, in_filename+".enc", password)
        myAES.encrypt(aes)

        # Convert the encrypted file to a binary string
        encrypted_filename = in_filename + '.enc'
        encrypted_binary = self.file_to_binary(encrypted_filename)
        print(len(encrypted_binary))
        padding_length = 320*180 - (len(encrypted_binary) % (320*180))
        encrypted_binary += '0' * padding_length

        #metadata
        metadata = f"{in_filename.split('/')[-1]}?{padding_length}?"
        bin_str = ""
        for char in metadata:
            byte = char
            if not byte:
                break
            # Convert the byte to binary and append it to the binary string
            bin_str += bin(ord(byte))[2:].zfill(8)
        padding_length2 = 320*180 - (len(bin_str) % (320*180))
        bin_str += '0' * padding_length2
        encrypted_binary = bin_str+encrypted_binary
        # Create the metadata file

        print(len(encrypted_binary))
        binary_string = encrypted_binary

        # Pad the binary string with zeros at the beginning to make it a multiple of 4
        while len(binary_string) % 4 != 0:
            binary_string = '0' + binary_string

        # Calculate the number of images needed
        num_images = (len(binary_string) // (320 * 180))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(
            f'{in_filename}_{padding_length}.mp4', fourcc, 25, (1280, 720), isColor=False)

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
                if (chunk != ''):
                    for k in range(4):
                        # 0 -> white, 1 -> black
                        pixel_value = 255 - int(chunk[k])*255
                        image_data[current_row:current_row+4,
                                   current_col:current_col+4] = pixel_value
                        current_col += 4
                        if current_col == 1280:  # Move to the next row if we have reached the end of the current row
                            current_row += 4
                            current_col = 0
            # Save the final image
            final_image = Image.fromarray(image_data, mode='L')
            # final_image.save(f"binary_image_{i}.png")
            video_writer.write(np.array(image_data))
            print(f"generating frame {i}/{num_images}")
            # display+=f"generating frame {i}/{num_images}\n"
            
        print(f"created video {in_filename}_{padding_length}.mp4")
        video_writer.release()
        self.ytHandler.upload(f"{in_filename}_{padding_length}.mp4",title,desc)
        return f"created video {in_filename}_{padding_length}.mp4"
    
    def retreive(self, link, password):
        path = link
        fileName = path
        # out_file_name =  "out_"+fileName.split('_')[0]
        # padding = 17968  # int(fileName.split('_')[1].split('.')[0])
        video_reader = cv2.VideoCapture(fileName)

        # Set up counters to keep track of current row and column
        current_row = 0
        current_col = 0

        # Create an empty string to store the binary data
        binary_string = ''

        # Loop through the frames of the video
        f = 0

        out_file_name = ''
        padding  = 0
        metadata = ''
        while True:
            # Read a frame from the video
            ret, frame = video_reader.read()
            if not ret:  # If there are no more frames, break out of the loop
                md = ""
                for i in range(0, len(metadata), 8):
                    byte = int(metadata[i:i+8], 2)
                    md += chr(byte)
                arr = md.split('?')
                out_file_name = arr[0]
                padding = int(arr[1])
                    
                    
                binary_string = binary_string[:-padding]
                break

            # Convert the frame to grayscale
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Extract the pixels from the frame and append them to the binary string
            for i in range(0, 720, 4):
                for j in range(0, 1280, 4):
                    # Calculate the mean pixel value and normalize to 0-1
                    pixel_value = frame_gray[i:i+4, j:j+4].mean() / 255
                    if f==0:
                       metadata += '0' if pixel_value > 0.5 else '1'
                    else:
                        binary_string += '0' if pixel_value > 0.5 else '1'
            
            f += 1
            print(f"reading frame {f}")

        # Save the binary string to a file
        with open('binary_string.txt', 'w') as f:
            f.write(binary_string)

        # Print a message indicating the file was saved
        print("Binary string extracted from video, converting binary to ascii")

        with open(out_file_name+".enc", 'wb') as new_file:
            # Write the binary string to the new file
            for i in range(0, len(binary_string), 8):
                byte = int(binary_string[i:i+8], 2)
                new_file.write(bytes([byte]))

        print(f"output file name is {out_file_name}")
        aes = myAES(out_file_name+".enc", out_file_name, password)
        aes.decrypt()
        return out_file_name

if __name__ == "__main__":
    handler = Handler("")
    handler.retreive("data/temp.txt_38768.mp4", "1234")