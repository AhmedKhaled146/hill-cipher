import numpy as np
from math import sqrt
from sympy import Matrix

# helper mappers, from letters to ints and the inverse instead of using char() and ord() 
LETTERS_INTEGERS = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", [*range(26)] + [*range(26)]))
INTEGERS_UPPERLETTERS = dict(zip([*range(26)], "ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
INTEGERS_LOWERLETTERS = dict(zip([*range(26)], "abcdefghijklmnopqrstuvwxyz"))

#return array of strings each string in element
#list comprehinsion (if in for)
#string format 
def split_evey_n(text, n):
    return ['{message:{fill}{align}{width}}'.format(message=text[i:i+n], fill='X', align='<', width=n) for i in range(0, len(text), n)]

# Generates the key matrix for the key string
def convert_string_to_matrix(text, n):
    keyMatrix = [[0] * n for i in range(n)]
    k = 0
    for i in range(n):
        for j in range(n):
            keyMatrix[i][j] = LETTERS_INTEGERS[text[k]] % 65
            k += 1
    return keyMatrix

# key: array
def encrypt(text, key, n, encrypt=True):
    result = ""
     #convert key from array to matrix
    key = np.matrix(key)
    key = Matrix(key)
    if (not encrypt): # Inverse Matrix (Decryption Key)
        try:
            key = key.inv_mod(26)
        except:
            print("Cannot decrypt, uninvertible key")
            return None

    parts = split_evey_n(text, n)
    for part in parts:
        # Generate vector for the text part
        vector = [[LETTERS_INTEGERS[part[i]]] for i in range(n)]
        vector = np.matrix(vector)
        vector = key * vector
        vector %= 26

        for i in range(0, n):
            result += INTEGERS_UPPERLETTERS[vector[i]] if part[i].isupper() else INTEGERS_LOWERLETTERS[vector[i]]
        
    return result


def main():
 
    text = input("Enter the text to cipher:\n")

    if (not text.isalpha()):
        print("Text can only contain letters.")
        exit()

    key = input("Enter the key (2x2=4 or 3x3=9):\n")
    
    key_size = len(key)
    key_matrix_float_size = sqrt(key_size)
    key_matrix_size = int(key_matrix_float_size)

    if (key_size != 4 and key_size != 9) or not key_matrix_float_size.is_integer():
        print("Key must be 4 or 9 characters")
        exit()

    key_matrix = convert_string_to_matrix(key, key_matrix_size)

    encrypted = encrypt(text, key_matrix, key_matrix_size)

    print("Text:", text)
    print("Key:", key, "-> Matrix:", key_matrix)
    print("Encrypted: ", encrypted)
    print("Decrypted: ", encrypt(encrypted, key_matrix, key_matrix_size, False))


if __name__ == "__main__":
    main()
