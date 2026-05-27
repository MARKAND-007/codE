# Caesar Cipher Encryption

text = input("Enter text: ")
shift = int(input("Enter shift value: "))

encrypted = ""

for char in text:
    if char.isalpha():
        if char.isupper():
            encrypted += chr((ord(char) - 65 + shift) % 26 + 65)
        else:
            encrypted += chr((ord(char) - 97 + shift) % 26 + 97)
    else:
        encrypted += char

print("Encrypted Text:", encrypted)
