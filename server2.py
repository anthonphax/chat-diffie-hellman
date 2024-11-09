import threading
import socket

# Configurações do servidor
SERVER_HOST = 'localhost'
SERVER_PORT = 3000

# Lista para armazenar os sockets dos clientes
clients = []

def handle_client(client_socket):
    while True:
        try:
            # Recebe a mensagem do cliente
            message = client_socket.recv(1024)
            if not message:
                break
            
            # Envia a mensagem para todos os outros clientes
            broadcast(message, client_socket)
        except:
            break

    # Remove o cliente da lista e fecha a conexão
    clients.remove(client_socket)
    client_socket.close()

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:  # Não envia a mensagem de volta para o remetente
            try:
                print(message)
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen()

    print("Servidor ouvindo...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Nova conexão: {client_address}")
        clients.append(client_socket)

        # Inicia uma thread para lidar com o cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server()