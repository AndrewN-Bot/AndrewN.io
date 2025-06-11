from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.x509 import NameOID
from cryptography import x509
import datetime

def display_info():
    print("Welcome to Andrew’s Program (Lab L5) developed for CISC 6660")
def generate_key_and_certificate():
    print("Generating private key...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    with open("private_key.pem", "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )
    print("Private key generated and saved to 'private_key.pem'.")

    print("Generating self-signed certificate...")
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "New York"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Brooklyn"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "CISC Lab"),
        x509.NameAttribute(NameOID.COMMON_NAME, "cisc6660.example.com"),
    ])

    certificate = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
        .sign(private_key, hashes.SHA256())
    )
    with open("certificate.pem", "wb") as f:
        f.write(certificate.public_bytes(serialization.Encoding.PEM))
    print("Certificate generated and saved to 'certificate.pem'.")

    return private_key

def hash_message(message):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(message)
    return digest.finalize()

def sign_hash(private_key, message_hash):
    signature = private_key.sign(
        message_hash,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify_signature(signature, message_hash):

    with open("certificate.pem", "rb") as f:
        certificate = x509.load_pem_x509_certificate(f.read())
    public_key = certificate.public_key()

    try:
        public_key.verify(
            signature,
            message_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False

def main():
    display_info()

    
    private_key = generate_key_and_certificate()

    
    sample_message = input("Enter a sample message to be signed: ").encode()

    
    message_hash = hash_message(sample_message)
    print("Generated Hash of the Message:")
    print(message_hash.hex())

    
    signature = sign_hash(private_key, message_hash)
    print("Signature of the Hash:")
    print(signature.hex())

    
    if verify_signature(signature, message_hash):
        print("Verification: The signature is valid.")
    else:
        print("Verification: The signature is invalid.")

if __name__ == "__main__":
    main()

