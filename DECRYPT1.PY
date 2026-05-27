# Caesar Cipher Decryption

text = input("Enter encrypted text: ")
shift = int(input("Enter shift value: "))

decrypted = ""

for char in text:
    if char.isalpha():
        if char.isupper():
            decrypted += chr((ord(char) - 65 - shift) % 26 + 65)
        else:
            decrypted += chr((ord(char) - 97 - shift) % 26 + 97)
    else:
        decrypted += char

print("Decrypted Text:", decrypted)
