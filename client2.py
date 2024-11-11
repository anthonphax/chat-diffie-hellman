import random
import threading
import socket

# Configurações do servidor
SERVER_HOST = 'localhost'
SERVER_PORT = 3000

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def gcd(a, b):
    # máximo divisor comum
    while b:
        a, b = b, a % b
    return a

def find_primitive_root(p):
    """Calcula uma raiz primitiva qualquer do número primo"""
    if not is_prime(p):
        raise ValueError(f"{p} não é um número primo.")

    # Encontre φ(p) = p - 1
    phi = p - 1
    factors = []

    # Encontre os fatores primos de φ(p)
    n = phi
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            factors.append(i)
            while n % i == 0:
                n //= i
    if n > 1:
        factors.append(n)

    primitive = []

    # Teste cada número a partir de 2 até p-1
    for g in range(2, p):
        is_primitive_root = True
        for factor in factors:
            # Verifique se g^(phi/factor) mod p é 1
            if pow(g, phi // factor, p) == 1:
                is_primitive_root = False
                break
        if is_primitive_root:
            primitive.append(g)

    return random.choice(primitive)

def generate_keys(p, g):
    private_key = random.randint(1, p - 1)
    public_key = (g ** private_key) % p
    return private_key, public_key

def calculate_shared_key(ther_public, my_private, p):
    shared_key = (ther_public ** my_private) % p
    return shared_key

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"\nMensagem recebida: {message.decode()}")
        except Exception as e:
            print(f"Erro ao receber a mensagem: {e}")
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # thread para receber mensagens
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    # Diffie-Hellman
    p = input("digite número primo: ")
    p = int(p)
    g = find_primitive_root(p)
    print(f"A raiz primitiva de {p} é: {g}")

    private_key, public_key = generate_keys(p, g)
    print(f"Cliente - Chave Privada: {private_key}, Chave Pública: {public_key}")

    # Envia o número primo (necessário para calcular g pelo outro cliente)

    #criptografas p e pública para cesar (%26)

    client_socket.send(str(p).encode())

    # Envia a chave pública do cliente e recebe a chave pública do servidor
    client_socket.send(str(public_key).encode())
    
    try:
        server_public_key = int(client_socket.recv(1024).decode())
    except ValueError:
        print("Erro: A chave pública do servidor não é um número válido.")
        client_socket.close()
        return

    # Calcula a chave compartilhada
    shared_key = calculate_shared_key(server_public_key, private_key, p)
    print(f"Cliente - Chave Compartilhada: {shared_key}")   

    while True:
        message = input("Digite sua mensagem: ")
        if message.lower() == 'sair':
            break
        
        client_socket.send(message.encode())

    client_socket.close()

if __name__ == "__main__":
    start_client()