import random
import threading
import socket

# Configurações do servidor
SERVER_HOST = 'localhost'
SERVER_PORT = 3000

def generate_keys(p, g):
    private_key = random.randint(1, p -1)
    public_key = (g ** private_key) % p

    return private_key, public_key

def calculate_shared_key(ther_public, my_private, p):
    shared_key = (ther_public ** my_private) % p
    return shared_key

def gera_chaves():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Gera chaves do Diffie-Hellman
    private_key, public_key = generate_keys()
    print(f"Chave Privada: {private_key}, Chave Pública: {public_key}")

    # Envia a chave pública para o servidor
    client_socket.send(str(public_key).encode())

    # Recebe a chave pública do servidor e calcula a chave compartilhada
    server_public_key = int(client_socket.recv(1024).decode())
    shared_key = calculate_shared_key(server_public_key, private_key, 23)
    print(f"Chave Compartilhada: {shared_key}")


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"\nMensagem recebida: {message.decode()}")
            
        except:
            print("Erro ao receber a mensagem.")
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Inicia uma thread para receber mensagens
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    while True:
        # p = input("digite p:")
        # q = input("digite q:")
        #garantir que q é raíz primitiva de p        
        
        private_key, public_key = generate_keys(23, 5)
        print(f"Cliente - Chave Privada: {private_key}, Chave Pública: {public_key}")

        # Envia a chave pública do cliente e recebe a chave pública do servidor
        client_socket.send(str(public_key).encode())
        server_public_key = int(client_socket.recv(1024).decode())

        # Calcula a chave compartilhada
        shared_key = calculate_shared_key(server_public_key, private_key, 23)
        print(f"Cliente - Chave Compartilhada: {shared_key}")   
            
        message = input("Digite sua mensagem: ")
        if message.lower() == 'sair':
            break
        
        client_socket.send(message.encode())

    client_socket.close()

if __name__ == "__main__":
    start_client()