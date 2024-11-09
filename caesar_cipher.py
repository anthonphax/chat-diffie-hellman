def caesar_cipher(message, shift):
    encrypted_message = ""
    for char in message:
        if char.isalpha():
            shift_base = ord('a') if char.islower() else ord('A')
            encrypted_message += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            encrypted_message += char
    return encrypted_message

def caesar_decipher(message, shift):
    return caesar_cipher(message, -shift)
