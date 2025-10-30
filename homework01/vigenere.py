def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""

    j = 0
    key_len = len(keyword)

    for letter in plaintext:
        if letter.isalpha():
            key_letter = keyword[j % key_len]
            if key_letter.isupper():
                shift = ord(key_letter) - ord("A")
            else:
                shift = ord(key_letter) - ord("a")
            if letter.isupper():
                new_code = (ord(letter) - ord("A") + shift) % 26 + ord("A")
                ciphertext += chr(new_code)
            else:
                new_code = (ord(letter) - ord("a") + shift) % 26 + ord("a")
                ciphertext += chr(new_code)
                j += 1
        else:
            ciphertext += letter
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""

    j = 0
    key_len = len(keyword)
    for letter in ciphertext:
        if letter.isalpha():
            key_letter = keyword[j % key_len]
            if key_letter.isupper():
                shift = ord(key_letter) - ord("A")
            else:
                shift = ord(key_letter) - ord("a")
            if letter.isupper():
                new_code = (ord(letter) - ord("A") - shift) % 26 + ord("A")
                plaintext += chr(new_code)
            else:
                new_code = (ord(letter) - ord("a") - shift) % 26 + ord("a")
                plaintext += chr(new_code)
                j += 1
        else:
            plaintext += letter
    return plaintext
