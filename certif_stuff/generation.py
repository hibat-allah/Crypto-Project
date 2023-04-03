from cryptography import x509
from cryptography.x509.oid import NameOID
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

# Generate a CSR
csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
    # Provide various details about who we are

    x509.NameAttribute(NameOID.COUNTRY_NAME, u"AG"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"ALGIERS"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"El Mouradia"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"CFAO"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"CFAO_TECH.com"),

])).add_extension(
    x509.SubjectAlternativeName([
        # Describe what sites we want this certificate for.
        x509.DNSName(u"CFAO_TECH.com"),
        x509.DNSName(u"www.CFAO_TECH.com"),
    ]),
    critical=False,
# Sign the CSR with our private key.
).sign(key, hashes.SHA256())
# Write our CSR out to disk.
with open("D:/Cours/S2/Crypto/TPs/certif_stuff/csr.pem", "wb") as f:
    f.write(csr.public_bytes(serialization.Encoding.PEM))


# Various details about who we are. For a self-signed certificate the
# subject and issuer are always the same.
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"AG"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"ALGIERS"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"El Mouradia"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"CFAO"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"CFAO_TECH.com"),
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
    # Our certificate will be valid for 30 days
    datetime.datetime.utcnow() + datetime.timedelta(days=30)
).add_extension(
    x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
    critical=False,
# Sign our certificate with our private key
).sign(key, hashes.SHA256())
# Write our certificate out to disk.
with open("D:/Cours/S2/Crypto/TPs/certif_stuff/certificate.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))