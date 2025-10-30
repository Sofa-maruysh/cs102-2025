def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for letter in plaintext:
        if "A" <= letter <= "Z":
            code = ord(letter)
            new_code = (code - ord("A") + shift) % 26 + ord("A")
            ciphertext += chr(new_code)
        elif "a" <= letter <= "z":
            code = ord(letter)
            new_code = (code - ord("a") + shift) % 26 + ord("a")
            ciphertext += chr(new_code)
        else:
            ciphertext += letter
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.python -m unittest discover

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for letter in ciphertext:
        if "A" <= letter <= "Z":
            code = ord(letter)
            new_code = (code - ord("A") - shift) % 26 + ord("A")
            plaintext += chr(new_code)
        elif "a" <= letter <= "z":
            code = ord(letter)
            new_code = (code - ord("a") - shift) % 26 + ord("a")
            plaintext += chr(new_code)
        else:
            plaintext += letter
    return plaintext
