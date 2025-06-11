import sympy
from math import gcd

def display_intro():
    print("Welcome to Andrews Lab 3 Attempt developed for CISC 6660")

def get_prime_input(prompt):
    while True:
        try:
            num = int(input(prompt))
            if not sympy.isprime(num):
                nearest_prime = sympy.nextprime(num - 1)
                print(f"Wrong prime number entered! The nearest prime number is: {nearest_prime}")
                accept = input("Do you want to accept it? Yes/No: ").strip().lower()
                if accept == 'yes':
                    return nearest_prime
                else:
                    continue
            return num
        except ValueError:
            print("Invalid! Please enter a proper digit.")

def generate_keys(p, q):
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = 65537 
    if gcd(e, phi_n) != 1:
        raise ValueError("e and phi(n) are not coprime. Choose different primes.")
    d = pow(e, -1, phi_n)
    return (e, n), (d, n)

def encrypt_message(message, public_key):
    e, n = public_key
    return [pow(ord(char), e, n) for char in message]

def decrypt_message(encrypted_message, private_key):
    d, n = private_key
    return ''.join([chr(pow(char, d, n)) for char in encrypted_message])

def rsa_program():
    display_intro()
    
    p = get_prime_input("Enter the first prime number: ")
    q = get_prime_input("Enter the second prime number: ")

    public_key, private_key = generate_keys(p, q)
    
    print("\nYour public key:", public_key)
    print("Your private key:", private_key)

    message = input("Enter the message that you want to send: ")

    encrypted_message = encrypt_message(message, public_key)
    print("Your Encrypted Message is:", encrypted_message)

    decrypted_message = decrypt_message(encrypted_message, private_key)
    print("Your Decrypted Message is:", decrypted_message)

rsa_program()