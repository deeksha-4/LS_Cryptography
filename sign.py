import random
import hashlib

def check_prime(n):
    if n < 2:
        return False
    lim= int(n/2) + 1
    for i in range(2, lim):
        if n % i == 0:
            return False
    return True

def semiprime_nos(num_bits):
    while True:
        p = random.getrandbits(num_bits)
        if check_prime(p):
            q = p + 2
            if check_prime(q):
                return p * q
            
def rsa_keys():
    e = 65537
    num_bits = 512
    N = semiprime_nos(num_bits)
    return N, e

def sign_file(file_name, N, e):
    with open(file_name, 'rb') as file:
        file_hash = hashlib.sha256(file.read()).digest()

    signature = pow(int.from_bytes(file_hash, 'big'), e, N)
    return N, e, signature

if _name_ == "_main_":
    import sys
    else:
        file_name = sys.argv[1]
        N, e = rsa_keys()
        N_str = hex(N)[2:].upper()
        N_str = '0' * (len(N_str) % 2) + N_str  # Ensure even length of N_str
        e_str = hex(e)[2:].upper()
        e_str = '0' * (len(e_str) % 2) + e_str  # Ensure even length of e_str

        N, e, signature = sign_file(file_name, N, e)

        signature_str = hex(signature)[2:].upper()
        signature_str = '0' * (len(signature_str) % 2) + signature_str  # Ensure even length of signature_str

        print("Public Key (N, e):")
        print(f"N: 0x{N_str}")
        print(f"e: 0x{e_str}")
        print("\nDigital Signature (in hex):")
        print(f"Signature: 0x{signature_str}")
