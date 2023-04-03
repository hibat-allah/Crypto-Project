from cryptography import x509
from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime


# Generate our key
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
# Write our key to disk for safe keeping
with open("D:/Cours/S2/Crypto/TPs/certif_stuff/key.pm", "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(b"ssi2023"),
    ))

# Create subject and issuer names
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"AG"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"ALGIERS"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"El Mouradia"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"CFAO"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"CFAO_TECH.com"),
])

# Create certificate builder object
builder = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer)

# Add extendedKeyUsage extension for client authentication only
extended_key_usage = x509.ExtendedKeyUsage([ExtendedKeyUsageOID.CLIENT_AUTH])
builder = builder.add_extension(extended_key_usage, critical=True)

# Set the public key, serial number, and validity period
builder = builder.public_key(key.public_key()).serial_number(x509.random_serial_number())
builder = builder.not_valid_before(datetime.datetime.utcnow()).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=10)
)

# Sign the certificate with the private key
certificate = builder.sign(key, hashes.SHA256())

# Write the certificate to disk
with open("D:/Cours/S2/Crypto/TPs/certif_stuff/certificateauth.pem", "wb") as f:
    f.write(certificate.public_bytes(serialization.Encoding.PEM))
