from typing import List

def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenère cipher.
    Keeps non-alphabetic characters unchanged.
    Preserves the case of letters.
    Advances the key over ALL characters (including spaces/punct).
    """
    if not keyword:
        raise ValueError("Keyword must be non-empty")
    if not keyword.isalpha():
        raise ValueError("Keyword must only contain letters (A-Z/a-z)")

    result = []
    j = 0
    key_len = len(keyword)
    key_upper = keyword.upper()

    for ch in plaintext:
        shift = ord(key_upper[j % key_len]) - ord('A')
        if ch.isalpha():
            if ch.isupper():
                result.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
        else:
            result.append(ch)
        j += 1  # advance key regardless of ch type

    return ''.join(result)


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts ciphertext using a Vigenère cipher.
    Keeps non-alphabetic characters unchanged.
    Preserves the case of letters.
    Advances the key over ALL characters (including spaces/punct).
    """
    if not keyword:
        raise ValueError("Keyword must be non-empty")
    if not keyword.isalpha():
        raise ValueError("Keyword must only contain letters (A-Z/a-z)")

    result = []
    j = 0
    key_len = len(keyword)
    key_upper = keyword.upper()

    for ch in ciphertext:
        shift = ord(key_upper[j % key_len]) - ord('A')
        if ch.isalpha():
            if ch.isupper():
                result.append(chr((ord(ch) - ord('A') - shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(ch) - ord('a') - shift) % 26 + ord('a')))
        else:
            result.append(ch)
        j += 1  # advance key regardless of ch type

    return ''.join(result)