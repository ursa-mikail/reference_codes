# Group Key and Certificate Creation
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import BestAvailableEncryption, NoEncryption
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding

from cryptography.hazmat.backends import default_backend
import datetime
import os
import base64


def create_key_pair():
    # Generate RSA key pair
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    return key

def create_certificate(key, subject_name, issuer_name):
    # Create a certificate with unique profiles
    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, issuer_name),
        x509.NameAttribute(NameOID.COMMON_NAME, subject_name),
    ])
    issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "CA Org"),
        x509.NameAttribute(NameOID.COMMON_NAME, "CA Common Name"),
    ])
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
        critical=False,
    ).sign(key, hashes.SHA256(), default_backend())
    return cert

def save_key_and_cert(key, cert, key_path, cert_path, password=None):
    # Save the private key
    with open(key_path, "wb") as key_file:
        if password:
            encryption_algorithm = BestAvailableEncryption(password)
        else:
            encryption_algorithm = NoEncryption()
        key_file.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=encryption_algorithm,
            )
        )

    # Save the certificate
    with open(cert_path, "wb") as cert_file:
        cert_file.write(
            cert.public_bytes(serialization.Encoding.PEM)
        )

def read_key_and_cert(key_path, cert_path, password=None):
    # Read the private key
    with open(key_path, "rb") as key_file:
        key_data = key_file.read()
        if password:
            key = serialization.load_pem_private_key(key_data, password=password, backend=default_backend())
        else:
            key = serialization.load_pem_private_key(key_data, password=None, backend=default_backend())
    
    # Read the certificate
    with open(cert_path, "rb") as cert_file:
        cert_data = cert_file.read()
        cert = x509.load_pem_x509_certificate(cert_data, backend=default_backend())
    
    return key, cert


def translate_certificate(cert_pem):
    # Remove the 'BEGIN CERTIFICATE' and 'END CERTIFICATE' lines
    cert_str = cert_pem.replace('-----BEGIN CERTIFICATE-----', '').replace('-----END CERTIFICATE-----', '').strip()
    
    # Decode the base64 encoded string
    cert_bytes = base64.b64decode(cert_str)
    
    # Load the certificate
    cert = x509.load_der_x509_certificate(cert_bytes, default_backend())
    
    # Extract certificate details
    cert_details = {
        'Subject': cert.subject,
        'Issuer': cert.issuer,
        'Serial Number': cert.serial_number,
        'Version': cert.version.name,
        'Not Before': cert.not_valid_before_utc,
        'Not After': cert.not_valid_after_utc,
        'Public Key': cert.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
    }

    # Print certificate details
    for key, value in cert_details.items():
        print(f"{key}: {value}")

# Usage
# Create directories if they don't exist
folder_certs = "certs"
folder_keys = "keys"

os.makedirs(folder_certs, exist_ok=True)
os.makedirs(folder_keys, exist_ok=True)

# Generate keys and certificates for 3 recipients and self
number_of_members = 4 # 1 to 3 for recipients, 4 for self

for i in range(1, (number_of_members+1)):   
    key = create_key_pair()
    cert = create_certificate(key, f"User {i}", f"User {i}")
    
    # Define file paths
    key_path = f"{folder_keys}/user{i}_private_key.pem"
    cert_path = f"{folder_certs}/user{i}_cert.pem"
    
    # Save the keys and certificates
    save_key_and_cert(key, cert, key_path, cert_path, password=b"your_password" if i == 4 else None)

    # Read and display the keys and certificates
    read_key, read_cert = read_key_and_cert(key_path, cert_path, password=b"your_password" if i == 4 else None)
    print(f"User {i} Private Key: {read_key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, NoEncryption()).decode('utf-8')}")
    print(f"User {i} Public Key: {read_key.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo).decode('utf-8')}")
    certificate_pem = read_cert.public_bytes(serialization.Encoding.PEM).decode('utf-8')
    print(f"User {i} Certificate: {certificate_pem}")
    print(f"User {i} Certificate: {translate_certificate(certificate_pem)}")

print("Certificates and keys generated, saved, and read successfully.")

""" N: 1 to 4, where 4:self
User N Private Key: -----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC5a4p6UOsLFuGw
:
wMspVbiaDi4/kaJb0GSc8yw=
-----END PRIVATE KEY-----

User N Public Key: -----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuWuKelDrCxbhsGRanUaC
:
OQIDAQAB
-----END PUBLIC KEY-----

User N Certificate: -----BEGIN CERTIFICATE-----
MIIDZjCCAk6gAwIBAgIUZfSJNTyJD7oDGfPSr5jBBkWmS0gwDQYJKoZIhvcNAQEL
:
ESEUbX0PNRpIIw==
-----END CERTIFICATE-----

Subject: <Name(C=US,ST=California,L=San Francisco,O=User 1,CN=User 1)>
Issuer: <Name(C=US,ST=California,L=San Francisco,O=CA Org,CN=CA Common Name)>
Serial Number: 582061402180252705347867733733247598510498794312
Version: v3
Not Before: 2024-10-03 17:19:48+00:00
Not After: 2025-10-03 17:19:48+00:00
Public Key: -----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuWuKelDrCxbhsGRanUaC
:
OQIDAQAB
-----END PUBLIC KEY-----

Certificates and keys generated, saved, and read successfully.
"""

# Create Secure Data Sharing
"""
Group Data Sharing
A file is created and ciphered with symmetric key. the file is ciphered with the symmetric key. This symmetric key is ciphered under each certificate of the 3 users with their public keys (public certificate) so that the authorized users can retrieve the data by deciphering the ciphered symmetric key under their individual public keys.

The data is signed with the sender’s certificate (i.e. sender’s private key). Each recipient checks the signature.
"""
def encrypt_file(file_path, symmetric_key):
    # Generate a random IV
    iv = os.urandom(16)
    
    # Create a cipher object
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Read the file and encrypt it
    with open(file_path, 'rb') as f:
        plaintext = f.read()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return iv + ciphertext  # Prepend IV to the ciphertext

def decrypt_file(ciphertext, symmetric_key):
    # Extract the IV from the beginning
    iv = ciphertext[:16]
    actual_ciphertext = ciphertext[16:]

    # Create a cipher object
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the ciphertext
    plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
    return plaintext

def encrypt_symmetric_key(symmetric_key, public_key):
    ciphered_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphered_key

def sign_file(file_path, private_key):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    signature = private_key.sign(
        file_data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return signature

def verify_signature(file_path, signature, public_key): # sender's public_key
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    try:
        public_key.verify(
            signature,
            file_data,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False


# Usage
keys = {}
certs = {}
ciphered_keys = {}

for i in range(1, number_of_members + 1):  
    key = create_key_pair()
    cert = create_certificate(key, f"User {i}", f"User {i}")
    
    # Define file paths
    key_path = f"keys/user{i}_private_key.pem"
    cert_path = f"certs/user{i}_cert.pem"
    
    # Save the keys and certificates
    save_key_and_cert(key, cert, key_path, cert_path, password=b"your_password" if i == 4 else None)

    # Read and store the keys and certificates
    keys[i], certs[i] = read_key_and_cert(key_path, cert_path, password=b"your_password" if i == 4 else None)

# Create a symmetric key
symmetric_key = os.urandom(32)  # AES-256 key
file_path = "test_file.txt"

# Write some data to the file
with open(file_path, 'w') as f:
    f.write("This is a secret message.")

# Encrypt the file
ciphered_file = encrypt_file(file_path, symmetric_key)

# Encrypt the symmetric key for each user
for i in range(1, number_of_members + 1):
    ciphered_keys[f"user{i}"] = encrypt_symmetric_key(symmetric_key, certs[i].public_key())

signer_id = 4
# Sign the file with the self certificate
signature = sign_file(file_path, keys[signer_id])  # Self certificate (User 4)

# Verify the signature for each user
for i in range(1, number_of_members + 1):
    if verify_signature(file_path, signature, certs[signer_id].public_key()):
        print(f"User {i} verified the signature successfully.")
    else:
        print(f"User {i} failed to verify the signature.")

# Decrypt the symmetric key and file for each user
for i in range(1, number_of_members + 1):
    decrypted_symmetric_key = keys[i].decrypt(ciphered_keys[f"user{i}"],
                                               padding.OAEP(
                                                   mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                   algorithm=hashes.SHA256(),
                                                   label=None
                                               ))

    decrypted_file = decrypt_file(ciphered_file, decrypted_symmetric_key)
    print(f"User {i} decrypted the file: {decrypted_file.decode('utf-8')}")

print("All operations completed successfully.")

"""
User 1 verified the signature successfully.
User 2 verified the signature successfully.
User 3 verified the signature successfully.
User 4 verified the signature successfully.

User 1 decrypted the file: This is a secret message.
User 2 decrypted the file: This is a secret message.
User 3 decrypted the file: This is a secret message.
User 4 decrypted the file: This is a secret message.

All operations completed successfully.
"""

def create_json_structure(signers, senders, recipients, access_for_recipients, file_data, signature, timestamp):
    # Convert ciphered keys to hex strings for JSON serialization
    access_for_recipients_hex = {user: key.hex() for user, key in access_for_recipients.items()}

    json_structure = {
        "signers": signers,
        "senders": senders,
        "recipients": recipients,
        "access_for_recipients": access_for_recipients_hex,  # Use hex converted keys
        "file": {
            "data": file_data,
            "signature": signature,  # Already in hex format
            "timestamp": timestamp
        }
    }
    return json_structure

def print_access_for_recipients(access_dict):
    for user, key in access_dict.items():
        print(f"User: {user}, Ciphered Key (hex): {key.hex()}")

# Usage
# Verify the signature for each user using the self certificate's public key
verification_results = {}
for i in range(1, number_of_members + 1):
    verification_results[f"user{i}"] = verify_signature(file_path, signature, certs[4].public_key())

# Create JSON structure
json_data = create_json_structure(
    signers=["User 4"],  # Self signer
    # senders=["User 1", "User 2", "User 3"],
    senders=["User 4"],  # Self signer
    recipients=["User 1", "User 2", "User 3"],
    access_for_recipients=ciphered_keys,
    file_data={"state": "ciphered"},
    signature=signature.hex(),  # Convert to hex for JSON serialization
    timestamp=datetime.datetime.utcnow().isoformat()
)

# Print the access dictionary
print_access_for_recipients(ciphered_keys)

# Output the JSON structure
print(json.dumps(json_data, indent=4))

# Decrypt the symmetric key and file for each user
for i in range(1, number_of_members + 1):
    decrypted_symmetric_key = keys[i].decrypt(ciphered_keys[f"user{i}"],
                                               padding.OAEP(
                                                   mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                   algorithm=hashes.SHA256(),
                                                   label=None
                                               ))

    decrypted_file = decrypt_file(ciphered_file, decrypted_symmetric_key)
    print(f"User {i} decrypted the file: {decrypted_file.decode('utf-8')}")

print("All operations completed successfully.")

"""

User: user1, Ciphered Key (hex): 4c3948b6a6f40285c401f295c45fe60c615b1893f60df4025686e682a031b1bf9b64e032d9730e400880ed84f6f959e18bb120bee5ab392e63f6e25865d4dddab103fcfe0f32b4bf7efa573b36438b8cd076504f60f0711715d88fb06f23bf0f6dff3db71819c09a29b496b6c1573898224dc1c13be259cb06ca0f3cfafd81b261bc71948d795262391813004acbe0ec2bd5e2497b23fc03c102030658c2da00b55a157e9aadec41e4940b25ae7ccf1d1af4747e2afcb47c1d2026ad83020496a90dc09c866a96ba2f42db933235c2221d437a360605c05c30875e9a10f3b6bacdf621c11b45b38ecc9c1f4803ea9dbc77e60807c39ada66636dc4ff541ea6d3
User: user2, Ciphered Key (hex): 1443647f1bad91a34c3bd9daf409661ad8566a510e5c29dbc7c33ec18e56934789184b1dd7c2785d402bd7a953dea07875ed39dd03cec92b19bb9561d9e0b6623c74d2c77672ca4c39723993b42d6fb041b050d0d30558dfedaae7d66aaf5553e8f2c27f5682c0d0086b1f18cfda3120930a8b0134680534da3c3d68aa3009882186a579d8af129bd692582db73a8f744167dbff236f7ee70d394cf6600634caf1381e5ce32e6d536290ec474520271237c92177275cfdd9c7b1161b95781d800872b4b5588365269842a1b0b7434884abf39385315f5ade2c09927d461b0c9b3cf4706b81c9925de7feaaae3f7aaa4f7216de3cf77b1f3c7edd932440089d89
User: user3, Ciphered Key (hex): 31946d7807b5472755a37711ea0b980563350a2aa7b42c3dffa56bbc39894b6e408eedd14e21e9add4ddddb94bb776da81e7f4b8b458f049342d7de72198466127be9da0fdbbe7c64d0c4d850e3ebe5356dd7005dbec54cf99e0c53727f61f2a59b96b8bdb486d05d9884eb3a4ad988e521c1c81fad49d0a2ecb9ba60875cb134208051dcd7eb342430a59651ecd720e035cfe33f6b7f8e3ae95d831ae9e3279890ef7f62d92c4f5802f47fc23bb0ef37689b8edc9e55646d23046bf199b2927bdcf9511cd7d45d1736b4421312df0da0d35251e903806c9b119c5290f8a64b6863b765cad5b60c38d5cb5778aa105a2369c92fe1b6a7451475dacab71efce9d
User: user4, Ciphered Key (hex): 8f8fade2f375df166e5eea3818093c006508d441ae30227fd26d352bc3e13dd32b2863010fab28ec23c05930c040cc8de5f27cae20390e67dfec70d47c08ee360b95ffc3682a971f034e2b64708d7cabbcdfdf1a995e15d6a30396d2063a3cf71e44f319307775f7fa7a478a3408a04faca64d88df4371a79ff341e14733c4cc2fd84efa57f99c1f0ed0ee67b5cede3339ea9f63ac0f0223a437722c29ffb8d884af34d00b9ef0bd686f49ec3ac51119f168d041387f223b7844e0e04c7317950d7ac48c8290279fdf8ff6bd9ff2ed1713c932cc072db1db3e53c8d5bfe7ab1b68b4e366db2024bf384075472e8f45f72b2b10703c0be60292f8832f614579eb
{
    "signers": [
        "User 4"
    ],
    "senders": [
        "User 4"
    ],
    "recipients": [
        "User 1",
        "User 2",
        "User 3"
    ],
    "access_for_recipients": {
        "user1": "4c3948b6a6f40285c401f295c45fe60c615b1893f60df4025686e682a031b1bf9b64e032d9730e400880ed84f6f959e18bb120bee5ab392e63f6e25865d4dddab103fcfe0f32b4bf7efa573b36438b8cd076504f60f0711715d88fb06f23bf0f6dff3db71819c09a29b496b6c1573898224dc1c13be259cb06ca0f3cfafd81b261bc71948d795262391813004acbe0ec2bd5e2497b23fc03c102030658c2da00b55a157e9aadec41e4940b25ae7ccf1d1af4747e2afcb47c1d2026ad83020496a90dc09c866a96ba2f42db933235c2221d437a360605c05c30875e9a10f3b6bacdf621c11b45b38ecc9c1f4803ea9dbc77e60807c39ada66636dc4ff541ea6d3",
        "user2": "1443647f1bad91a34c3bd9daf409661ad8566a510e5c29dbc7c33ec18e56934789184b1dd7c2785d402bd7a953dea07875ed39dd03cec92b19bb9561d9e0b6623c74d2c77672ca4c39723993b42d6fb041b050d0d30558dfedaae7d66aaf5553e8f2c27f5682c0d0086b1f18cfda3120930a8b0134680534da3c3d68aa3009882186a579d8af129bd692582db73a8f744167dbff236f7ee70d394cf6600634caf1381e5ce32e6d536290ec474520271237c92177275cfdd9c7b1161b95781d800872b4b5588365269842a1b0b7434884abf39385315f5ade2c09927d461b0c9b3cf4706b81c9925de7feaaae3f7aaa4f7216de3cf77b1f3c7edd932440089d89",
        "user3": "31946d7807b5472755a37711ea0b980563350a2aa7b42c3dffa56bbc39894b6e408eedd14e21e9add4ddddb94bb776da81e7f4b8b458f049342d7de72198466127be9da0fdbbe7c64d0c4d850e3ebe5356dd7005dbec54cf99e0c53727f61f2a59b96b8bdb486d05d9884eb3a4ad988e521c1c81fad49d0a2ecb9ba60875cb134208051dcd7eb342430a59651ecd720e035cfe33f6b7f8e3ae95d831ae9e3279890ef7f62d92c4f5802f47fc23bb0ef37689b8edc9e55646d23046bf199b2927bdcf9511cd7d45d1736b4421312df0da0d35251e903806c9b119c5290f8a64b6863b765cad5b60c38d5cb5778aa105a2369c92fe1b6a7451475dacab71efce9d",
        "user4": "8f8fade2f375df166e5eea3818093c006508d441ae30227fd26d352bc3e13dd32b2863010fab28ec23c05930c040cc8de5f27cae20390e67dfec70d47c08ee360b95ffc3682a971f034e2b64708d7cabbcdfdf1a995e15d6a30396d2063a3cf71e44f319307775f7fa7a478a3408a04faca64d88df4371a79ff341e14733c4cc2fd84efa57f99c1f0ed0ee67b5cede3339ea9f63ac0f0223a437722c29ffb8d884af34d00b9ef0bd686f49ec3ac51119f168d041387f223b7844e0e04c7317950d7ac48c8290279fdf8ff6bd9ff2ed1713c932cc072db1db3e53c8d5bfe7ab1b68b4e366db2024bf384075472e8f45f72b2b10703c0be60292f8832f614579eb"
    },
    "file": {
        "data": {
            "state": "ciphered"
        },
        "signature": "020a4977d9a0b378e8a2967f58746f32d196b1e274927d86c822fe7eb2f9750a1cdce39cd69a300e7cf92c2fad6b9e34d837be21bf4fc629a38f8ea41667465cf78c9372145510ade73c65f4b4d3f0e9d89c9bc7be943f1e96d61c617c91eaf7b44e1b946cf4e8baa0264fcf18014d4657c9fb9e1ecc55193a93c037696701c6600f40fbd355816af7eecb429d28a84036f72a686d4ca86e2fe75c9c412a6744508528cdf124d46ad2c2e32dcfb950b7739a1d40bdeaa8ef4819e3bc87574173033b92ff3b8762c17bcc67b9122101b7ed023b4a270854aa82734046be5195297a119514e76526afa05c617d47a9ce2d0fe5fd18c278bcd266f427201300bc06",
        "timestamp": "2024-08-03T17:59:06.986620"
    }
}
"""