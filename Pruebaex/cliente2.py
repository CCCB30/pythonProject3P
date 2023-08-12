import socket
import threading

class ClienteSocket:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 8560))
        self.usuario = input("Ingresa tu nombre de usuario: ")
        self.client_socket.send(self.usuario.encode())

        mensaje = self.client_socket.recv(1024).decode()
        print(mensaje)

        threading.Thread(target=self.recibir_mensajes).start()

        while True:
            movimiento = input("Ingresa el movimiento en formato fila,columna (0, 1, 2): ")
            self.client_socket.send(movimiento.encode())

    def recibir_mensajes(self):
        while True:
            mensaje = self.client_socket.recv(1024).decode()
            print(mensaje)

if __name__ == "__main__":
    cliente = ClienteSocket()