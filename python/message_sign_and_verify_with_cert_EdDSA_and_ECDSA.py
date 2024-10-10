from cryptography import x509
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
import datetime

"""
EdDSA (Ed25519) Certificate Example
1. Generate Keys
2. Create a Certificate
3. Sign a Message
4. Verify the Signature
"""
# Generate private key
private_key = Ed25519PrivateKey.generate()

# Generate public key
public_key = private_key.public_key()

# Create a self-signed certificate
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Company"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"mysite.com"),
])

cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(public_key)
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.utcnow())
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=10))
    .sign(private_key, None, default_backend())  # Use None for Ed25519
)

# Sign a message
message = b"Hello, EdDSA!"
signature = private_key.sign(message)

# Verify the signature using the public key from the certificate
try:
    cert.public_key().verify(signature, message)
    # public_key.verify(signature, message)
    print("EdDSA signature is valid.")
except InvalidSignature:
    print("EdDSA signature is invalid.")

# Save the certificate
with open("eddsa_cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

# Save the private key
with open("eddsa_private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))


from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed
from cryptography.exceptions import InvalidSignature
import datetime

"""
ECDSA (secp256r1) Certificate Example
1. Generate Keys
2. Create a Certificate
3. Sign a Message
4. Verify the Signature
"""
# Generate private key
private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())

# Generate public key
public_key = private_key.public_key()

# Create a self-signed certificate
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Company"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"mysite.com"),
])

cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(public_key)
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.utcnow())
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=10))
    .sign(private_key, hashes.SHA256(), default_backend())
)

# Sign a message
message = b"Hello, ECDSA!"
hasher = hashes.Hash(hashes.SHA256())
hasher.update(message)
digest = hasher.finalize()
signature = private_key.sign(digest, ec.ECDSA(Prehashed(hashes.SHA256())))

# Verify the signature using the public key from the certificate
try:
    cert.public_key().verify(signature, digest, ec.ECDSA(Prehashed(hashes.SHA256())))
    # public_key.verify(signature, digest, ec.ECDSA(Prehashed(hashes.SHA256())))
    print("ECDSA signature is valid.")
except InvalidSignature:
    print("ECDSA signature is invalid.")

# Save the certificate
with open("ecdsa_cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

# Save the private key
with open("ecdsa_private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))
