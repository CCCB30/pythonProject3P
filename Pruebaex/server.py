import socket

class ServidorSocket:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 8560
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)
        self.cliente1 = None
        self.cliente2 = None

    def imprimir_tablero(self, tablero):
        for fila in tablero:
            print(" | ".join(fila))
            print("-" * 9)

    def verificar_ganador(self, tablero, jugador):
        for fila in tablero:
            if all(cell == jugador for cell in fila):
                return True

        for columna in range(3):
            if all(tablero[row][columna] == jugador for row in range(3)):
                return True

        if all(tablero[i][i] == jugador for i in range(3)) or all(tablero[i][2 - i] == jugador for i in range(3)):
            return True

        return False

    def jugar(self):
        tablero = [[" " for _ in range(3)] for _ in range(3)]
        jugador_actual = "X"
        juego_terminado = False

        while not juego_terminado:
            self.imprimir_tablero(tablero)

            if jugador_actual == "X":
                cliente_actual = self.cliente1
                otro_cliente = self.cliente2
            else:
                cliente_actual = self.cliente2
                otro_cliente = self.cliente1

            mensaje = "Tu turno. Ingresa fila (0, 1, 2): "
            cliente_actual.send(mensaje.encode())
            fila = int(cliente_actual.recv(1024).decode())

            mensaje = "Tu turno. Ingresa columna (0, 1, 2): "
            cliente_actual.send(mensaje.encode())
            columna = int(cliente_actual.recv(1024).decode())

            if tablero[fila][columna] == " ":
                tablero[fila][columna] = jugador_actual
                if self.verificar_ganador(tablero, jugador_actual):
                    self.imprimir_tablero(tablero)
                    mensaje = f"¡Jugador {jugador_actual} ha ganado!"
                    cliente_actual.send(mensaje.encode())
                    otro_cliente.send(mensaje.encode())
                    print(mensaje)
                    juego_terminado = True
                elif all(tablero[row][col] != " " for row in range(3) for col in range(3)):
                    self.imprimir_tablero(tablero)
                    mensaje = "¡Es un empate!"
                    self.cliente1.send(mensaje.encode())
                    self.cliente2.send(mensaje.encode())
                    juego_terminado = True
                else:
                    jugador_actual = "O"
            else:
                mensaje = "Esa casilla ya está ocupada. Intenta de nuevo."
                cliente_actual.send(mensaje.encode())

        self.cliente1.send("El juego ha terminado.".encode())
        self.cliente1.close()
        self.cliente2.send("El juego ha terminado.".encode())
        self.cliente2.close()

    def main(self):
        print("Esperando al jugador 1...")
        self.cliente1, _ = self.server_socket.accept()
        nombre_cliente1 = self.cliente1.recv(1024).decode()  # Recibir el nombre de usuario del cliente
        print(f"¡Jugador {nombre_cliente1} se ha conectado!")

        self.cliente1.send("Esperando al jugador 2...".encode())

        print("Esperando al jugador 2...")
        self.cliente2, _ = self.server_socket.accept()
        nombre_cliente2 = self.cliente2.recv(1024).decode()  # Recibir el nombre de usuario del cliente
        print(f"¡Jugador {nombre_cliente2} se ha conectado!")

        self.cliente1.send("Comienza el juego. Eres el Jugador 1 (X).".encode())
        self.cliente2.send("Comienza el juego. Eres el Jugador 2 (O).".encode())

        self.jugar()
        self.server_socket.close()

if __name__ == "__main__":
    servidor = ServidorSocket()
    servidor.main()