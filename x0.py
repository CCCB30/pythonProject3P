def imprimir_tablero(tablero):
    for fila in tablero:
        print(" | ".join(fila))
        print("-" * 9)


def verificar_ganador(tablero, jugador):
    for fila in tablero:
        if all(cell == jugador for cell in fila):
            return True

    for columna in range(3):
        if all(tablero[row][columna] == jugador for row in range(3)):
            return True

    if all(tablero[i][i] == jugador for i in range(3)) or all(tablero[i][2 - i] == jugador for i in range(3)):
        return True

    return False


def jugar():
    tablero = [[" " for _ in range(3)] for _ in range(3)]
    jugador_actual = "X"
    juego_terminado = False

    while not juego_terminado:
        imprimir_tablero(tablero)
        fila = int(input(f"Jugador {jugador_actual}, elige una fila (0, 1, 2): "))
        columna = int(input(f"Jugador {jugador_actual}, elige una columna (0, 1, 2): "))

        if tablero[fila][columna] == " ":
            tablero[fila][columna] = jugador_actual
            if verificar_ganador(tablero, jugador_actual):
                imprimir_tablero(tablero)
                print(f"¡Jugador {jugador_actual} ha ganado!")
                juego_terminado = True
            elif all(tablero[row][col] != " " for row in range(3) for col in range(3)):
                imprimir_tablero(tablero)
                print("¡Es un empate!")
                juego_terminado = True
            else:
                jugador_actual = "X" if jugador_actual == "O" else "O"
        else:
            print("Esa casilla ya está ocupada. Intenta de nuevo.")


if __name__ == "__main__":
    jugar()
