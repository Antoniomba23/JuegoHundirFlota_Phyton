import random


# --------------------------------------
# Función para comprobar si un barco cabe
# --------------------------------------
def cabe_barco(tablero, fila, columna, tamaño, orientacion):
    if orientacion == "H":
        if columna + tamaño - 1 > 9:
            return False
        for c in range(columna, columna + tamaño):
            if tablero[fila][c] != "🌊":
                return False
    elif orientacion == "V":
        if fila + tamaño - 1 > 9:
            return False
        for f in range(fila, fila + tamaño):
            if tablero[f][columna] != "🌊":
                return False
    return True


# --------------------------------------
# Función para colocar un barco automáticamente
# --------------------------------------
def colocar_barco(tablero, tamaño):
    colocado = False
    while not colocado:
        orientacion = random.choice(["H", "V"])
        fila = random.randint(0, 9)
        columna = random.randint(0, 9)
        if cabe_barco(tablero, fila, columna, tamaño, orientacion):
            if orientacion == "H":
                for c in range(columna, columna + tamaño):
                    tablero[fila][c] = "🚢"
            else:
                for f in range(fila, fila + tamaño):
                    tablero[f][columna] = "🚢"
            colocado = True


# --------------------------------------
# Función para disparar
# --------------------------------------
def disparo(tablero, fila, columna):
    if tablero[fila][columna] == "🚢":
        tablero[fila][columna] = "💥"
        return "Tocado"
    elif tablero[fila][columna] == "🌊":
        tablero[fila][columna] = "❌"
        return "Capitan el disparo ha fallado"
    else:
        return "Capitan esas coordenadas ya fueron disparadas"


# --------------------------------------
# Crear tableros para los dos jugadores
# --------------------------------------
tablero1 = [["🌊"] * 10 for _ in range(10)]
tablero2 = [["🌊"] * 10 for _ in range(10)]

# Colocar barcos automáticamente
for t in [1, 2, 3, 4]:
    colocar_barco(tablero1, t)
    colocar_barco(tablero2, t)


# --------------------------------------
# Función para mostrar tablero del oponente (ocultar barcos)
# --------------------------------------
def mostrar_tablero(tablero):
    for fila in tablero:
        mostrar = ["🌊" if cel == "🚢" else cel for cel in fila]
        print(" ".join(mostrar))


# --------------------------------------
# Función para contar barcos restantes
# --------------------------------------
def barcos_restantes(tablero):
    return sum(fila.count("🚢") for fila in tablero)


# --------------------------------------
# Bucle principal de juego con turnos
# --------------------------------------
def pedir_coordenada(tipo):
    while True:
        try:
            valor = int(input(f"Ingrese {tipo} (0-9): "))
            if 0 <= valor <= 9:
                return valor
            else:
                print("¡Error! el rango de batalla es un número entre 0 y 9.")
        except ValueError:
            print("¡Error! Debe ser un número entero.")

def pedir_disparo(tablero):
    while True:
        fila = pedir_coordenada("fila")
        columna = pedir_coordenada("columna")
        if tablero[fila][columna] in ["💥", "❌"]:
            print("capitan estas coordenadas ya fueron disparadas, Intenta otra posición.")
        else:
            return fila, columna


def mostrar_tableros(tablero_jugador, tablero_oponente):
    print("\nMi tablero:")
    for fila in tablero_jugador:
        print(" ".join(fila))

    print("\nTablero del oponente:")
    for fila in tablero_oponente:
        mostrar = ["🌊" if cel == "🚢" else cel for cel in fila]
        print(" ".join(mostrar))

def barco_hundido(tablero, fila, columna):
    # Encontrar el barco tocado en esta posición
    # Buscamos hacia arriba, abajo, izquierda, derecha
    # hasta encontrar agua o borde del tablero
    tamaño = 0
    posiciones = []

    # Verificar horizontal
    c = columna
    while c >= 0 and tablero[fila][c] in ["🚢", "💥"]:
        posiciones.append((fila, c))
        c -= 1
    c = columna + 1
    while c <= 9 and tablero[fila][c] in ["🚢", "💥"]:
        posiciones.append((fila, c))
        c += 1
    if posiciones:
        # Comprobar si todos los segmentos están tocados
        if all(tablero[f][c] == "💥" for f, c in posiciones):
            return True
    posiciones = []

    # Verificar vertical
    f = fila
    while f >= 0 and tablero[f][columna] in ["🚢", "💥"]:
        posiciones.append((f, columna))
        f -= 1
    f = fila + 1
    while f <= 9 and tablero[f][columna] in ["🚢", "💥"]:
        posiciones.append((f, columna))
        f += 1
    if posiciones:
        if all(tablero[f][c] == "💥" for f, c in posiciones):
            return True

    return False



turno = 1  # jugador 1 empieza

while True:
    print(f"\nTurno del jugador {turno}")

    # Elegir el tablero del oponente
    tablero_oponente = tablero2 if turno == 1 else tablero1

    # Mostrar ambos tableros
    if turno == 1:
        mostrar_tableros(tablero1, tablero2)
    else:
        mostrar_tableros(tablero2, tablero1)

    # Pedir coordenadas de disparo válidas
    fila, columna = pedir_disparo(tablero_oponente)

    # Realizar disparo
    resultado = disparo(tablero_oponente, fila, columna)
    print(resultado)

    # Comprobar si se terminó el juego
    if barcos_restantes(tablero_oponente) == 0:
        print(f"¡Jugador {turno} ha ganado!")
        break

    # Cambiar turno solo si disparó al agua
    if resultado == "Capitan el disparo ha fallado":
        turno = 2 if turno == 1 else 1


    # Verificar si hundiste un barco
    if resultado == "Tocado" and barco_hundido(tablero_oponente, fila, columna):
        print("¡Hundiste un barco enemigo!")
