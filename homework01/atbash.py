"""
Модуль для шифрования и расшифровки текста с помощью шифра Атбаш.
Функция encrypt_atbash(plaintext) выполняет подстановочное шифрование,
заменяя каждую букву на отражённую с противоположного конца алфавита.
"""

def encrypt_atbash(plaintext: str) -> str:
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    n = len(alphabet)
    ciphertext = []
    for char in plaintext:
        lower_char = char.lower()
        if lower_char in alphabet:
            i = alphabet.index(lower_char)
            reflected_char = alphabet[n - i - 1]
            if char.isupper():
                reflected_char = reflected_char.upper()
            ciphertext.append(reflected_char)
        else:
            ciphertext.append(char)
    return "".join(ciphertext)


print("Plaintext: ")
plaintext = input()
print(encrypt_atbash(plaintext))
