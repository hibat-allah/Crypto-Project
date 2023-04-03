from cryptography import x509
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Load the client certificate
with open("path/to/client_certificate.pem", "rb") as f:
    client_cert = x509.load_pem_x509_certificate(f.read())

# Load the CA certificate (which was used to sign the client certificate)
with open("path/to/ca_certificate.pem", "rb") as f:
    ca_cert = x509.load_pem_x509_certificate(f.read())

# Verify the client certificate's digital signature using the CA certificate's public key
try:
    ca_public_key = ca_cert.public_key()
    client_cert.public_key().verify(
        client_cert.signature,
        client_cert.tbs_certificate_bytes,
        padding.PKCS1v15(),
        client_cert.signature_hash_algorithm
    )
    print("Client certificate signature verified successfully")
except:
    print("Failed to verify client certificate signature")

# Check the client certificate's expiration date
if client_cert.not_valid_after < datetime.datetime.utcnow():
    print("Client certificate has expired")
else:
    print("Client certificate is valid")
