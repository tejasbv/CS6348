import os
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt


class myAES:
    def __init__(self, in_fileName, out_fileName, password):
        self.password = password
        self.in_fileName = in_fileName
        self.out_fileName = out_fileName

    def encrypt(self):
        password = self.password

        input_filename = self.in_fileName
        output_filename = self.out_fileName

        # Open files
        file_in = open(input_filename, 'rb')
        file_out = open(output_filename, 'wb')

        salt = get_random_bytes(32) 
        key = scrypt(password, salt, key_len=32, N=2**17, r=8, p=1)
        file_out.write(salt)  
        cipher = AES.new(key, AES.MODE_GCM)
        file_out.write(cipher.nonce)

        BUFFER_SIZE = 1024 * 1024
        data = file_in.read(BUFFER_SIZE)  # Read in some of the file
        while len(data) != 0:  # Check if we need to encrypt anymore data
            encrypted_data = cipher.encrypt(data)  # Encrypt the data we read
            file_out.write(encrypted_data)
            data = file_in.read(BUFFER_SIZE)

        tag = cipher.digest()  # Signal to the cipher that we are done and get the tag
        file_out.write(tag)

        # Close both files
        file_in.close()
        file_out.close()
        print("encrypted file")

    def decrypt(self):
        password = self.password

        input_filename = self.in_fileName
        output_filename = self.out_fileName
        file_in = open(input_filename, 'rb')
        file_out = open(output_filename, 'wb')

        salt = file_in.read(32)  # The salt we generated was 32 bits long
        key = scrypt(password, salt, key_len=32, N=2**17, r=8, p=1)

        nonce = file_in.read(16)  # The nonce is 16 bytes long
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

       
        file_in_size = os.path.getsize(input_filename)
        encrypted_data_size = file_in_size - 32 - 16 - 16

        BUFFER_SIZE = 1024 * 1024

        for _ in range(int(encrypted_data_size / BUFFER_SIZE)):
            data = file_in.read(BUFFER_SIZE)
            decrypted_data = cipher.decrypt(data)  # Decrypt the data
            file_out.write(decrypted_data)
        data = file_in.read(int(encrypted_data_size % BUFFER_SIZE))
        decrypted_data = cipher.decrypt(data)  # Decrypt the data
        file_out.write(decrypted_data)

        tag = file_in.read(16)
        #
        file_in.close()
        file_out.close()


# if __name__ == "__main__":
#     # aes = myAES('temp.txt', 'enc_temp.txt', "securePassword1")
#     # aes.encrypt()

#     aes = myAES('enc_temp.txt', 'out.txt', 'securePassword1')
#     aes.decrypt()
