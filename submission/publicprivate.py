from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

class PublicPrivate:
    def generateKeys(self):
        # Generate a public-private key pair
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Write the keys to separate files
        with open('private_key.pem', 'wb') as f:
            f.write(private_key_pem)

        with open('public_key.pem', 'wb') as f:
            f.write(public_key_pem)

    def encrypt(self,pathtoKey ,password):
        
        with open(pathtoKey, 'rb') as f:
            public_key = serialization.load_pem_public_key(
                f.read()
            )
        
        # Encrypt a message using the public key
        message =  password.encode('utf-8')
        encrypted = public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        with open('encrypted_password.key', 'wb') as f:
            f.write(encrypted)

    def decrypt(self, pathToPrivateKey, encrypted_password):
        
        
        with open(encrypted_password, 'rb') as f:
            encrypted = f.read()
        # Load the keys from the files
        with open(pathToPrivateKey, 'rb') as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None
            )


        # Decrypt the message using the private key
        decrypted = private_key.decrypt(
            encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print(f"Decrypted message: {decrypted.decode('utf-8')}")

    
    
if __name__ == "__main__":
    handler = PublicPrivate()
    # handler.generateKeys()
    handler.decrypt("private_key.pem", "encrypted_password.key")
    

