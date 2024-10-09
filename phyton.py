from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import base64

def encrypt_aes(key, plaintext):
    # Garante que a chave tenha 16, 24 ou 32 bytes (128, 192 ou 256 bits)
    key = key.ljust(32)[:32].encode('utf-8')  # Pad ou trunque a chave
    cipher = AES.new(key, AES.MODE_CBC)  # Modo CBC
    iv = cipher.iv  # Vetor de inicialização
    ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    return base64.b64encode(iv + ciphertext).decode('utf-8')

def decrypt_aes(key, encrypted):
    key = key.ljust(32)[:32].encode('utf-8')  # Pad ou trunque a chave
    encrypted = base64.b64decode(encrypted.encode('utf-8'))
    iv = encrypted[:16]  # Extrai o IV
    ciphertext = encrypted[16:]  # O restante é o texto cifrado
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode('utf-8')

# Exemplo de uso
if __name__ == "__main__":
    chave = "a3123"
    mensagem = "mensagem criptografada"

    # Criptografar
    mensagem_cifrada = encrypt_aes(chave, mensagem)
    print(f"Mensagem Cifrada: {mensagem_cifrada}")

    # Descriptografar
    mensagem_decifrada = decrypt_aes(chave, mensagem_cifrada)
    print(f"Mensagem Decifrada: {mensagem_decifrada}")
