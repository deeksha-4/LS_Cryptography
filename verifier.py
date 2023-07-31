import hashlib

def verify_signature(file_name, N, e, signature_hex):
    with open(file_name, 'rb') as file:
        file_hash = hashlib.sha256(file.read()).digest()

    signature = int(signature_hex, 16)

    decrypted_signature = pow(signature, e, N)

    expected_hash = int.from_bytes(file_hash, 'big')

    if decrypted_signature == expected_hash:
        return "accept"
    else:
        return "reject"

if _name_ == "_main_":
    import sys
    else:
        file_name = sys.argv[1]
        N = int(sys.argv[2], 16)
        e = int(sys.argv[3], 16)
        signature_hex = sys.argv[4]

        result = verify_signature(file_name, N, e, signature_hex)
        print(result)
