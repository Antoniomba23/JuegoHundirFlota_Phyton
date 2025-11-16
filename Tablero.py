import random

# --- Clase Tablero ---
class Tablero:
    def __init__(self, nombre):
        self.nombre = nombre
        self.matriz = [["🌊"] * 10 for _ in range(10)]

    def mostrar_fila(self, fila_idx, ocultar_barcos=False):
        fila = self.matriz[fila_idx]
        if ocultar_barcos:
            mostrar = ["🌊" if cel == "🚢" else cel for cel in fila]
        else:
            mostrar = fila
        # Cada celda con ancho fijo de 3 espacios
        return " ".join(f"{cel:^3}" for cel in mostrar)

    def cabe_barco(self, fila, columna, tamaño, orientacion):
        if orientacion == "H":
            if columna + tamaño - 1 > 9:
                return False
            for c in range(columna, columna + tamaño):
                if self.matriz[fila][c] != "🌊":
                    return False
        elif orientacion == "V":
            if fila + tamaño - 1 > 9:
                return False
            for f in range(fila, fila + tamaño):
                if self.matriz[f][columna] != "🌊":
                    return False
        return True

    def colocar_barco(self, tamaño):
        colocado = False
        while not colocado:
            orientacion = random.choice(["H", "V"])
            fila = random.randint(0, 9)
            columna = random.randint(0, 9)
            if self.cabe_barco(fila, columna, tamaño, orientacion):
                if orientacion == "H":
                    for c in range(columna, columna + tamaño):
                        self.matriz[fila][c] = "🚢"
                else:
                    for f in range(fila, fila + tamaño):
                        self.matriz[f][columna] = "🚢"
                colocado = True

    def disparo(self, fila, columna):
        if self.matriz[fila][columna] == "🚢":
            self.matriz[fila][columna] = "💥"
            return "Tocado"
        elif self.matriz[fila][columna] == "🌊":
            self.matriz[fila][columna] = "❌"
            return "Agua"
        else:
            return "Capitán, esas coordenadas ya fueron disparadas"

    def barcos_restantes(self):
        return sum(fila.count("🚢") for fila in self.matriz)

    def barco_hundido(self, fila, columna):
        posiciones = []

        # Verificar horizontal
        c = columna
        while c >= 0 and self.matriz[fila][c] in ["🚢", "💥"]:
            posiciones.append((fila, c))
            c -= 1
        c = columna + 1
        while c <= 9 and self.matriz[fila][c] in ["🚢", "💥"]:
            posiciones.append((fila, c))
            c += 1
        if posiciones and all(self.matriz[f][c] == "💥" for f, c in posiciones):
            return True

        # Verificar vertical
        posiciones = []
        f = fila
        while f >= 0 and self.matriz[f][columna] in ["🚢", "💥"]:
            posiciones.append((f, columna))
            f -= 1
        f = fila + 1
        while f <= 9 and self.matriz[f][columna] in ["🚢", "💥"]:
            posiciones.append((f, columna))
            f += 1
        if posiciones and all(self.matriz[f][c] == "💥" for f, c in posiciones):
            return True

        return False

# --- Funciones auxiliares ---
def pedir_coordenada(tipo):
    while True:
        valor = input(f"Ingrese {tipo} (A-J para filas, 0-9 para columnas): ").strip().upper()
        if tipo == "fila":
            if valor in "ABCDEFGHIJ":
                return ord(valor) - ord('A')
            else:
                print("¡Error! Debe ingresar una letra entre A y J.")
        else:
            if valor.isdigit() and 0 <= int(valor) <= 9:
                return int(valor)
            else:
                print("¡Error! Debe ingresar un número entre 0 y 9.")

def pedir_disparo(tablero):
    while True:
        fila = pedir_coordenada("fila")
        columna = pedir_coordenada("columna")
        if tablero.matriz[fila][columna] in ["💥", "❌"]:
            print("Capitán, esas coordenadas ya fueron disparadas. Intente otra.")
        else:
            return fila, columna

# Mostrar tableros lado a lado con alineación perfecta
def mostrar_tableros_lado_a_lado(tablero_jugador, tablero_oponente):
    espacio = " " * 8  # separación mayor entre tableros
    encabezado = "  " + " ".join(f"{i:^3}" for i in range(10))
    print("Tu tablero:".ljust(35) + espacio + "Tablero del oponente:")
    print(encabezado.ljust(35) + espacio + encabezado)
    for idx in range(10):
        letra = chr(ord('A') + idx)
        fila_jugador = tablero_jugador.mostrar_fila(idx)
        fila_oponente = tablero_oponente.mostrar_fila(idx, ocultar_barcos=True)
        print(f"{letra} {fila_jugador}".ljust(35) + espacio + f"{letra} {fila_oponente}")

# --- Inicialización ---
tablero1 = Tablero("Jugador 1")
tablero2 = Tablero("Jugador 2")

for t in [1, 2, 3, 4]:
    tablero1.colocar_barco(t)
    tablero2.colocar_barco(t)

turno = 1

# --- Bucle principal ---
while True:
    print(f"\nTurno del jugador {turno}")
    tablero_jugador = tablero1 if turno == 1 else tablero2
    tablero_oponente = tablero2 if turno == 1 else tablero1

    mostrar_tableros_lado_a_lado(tablero_jugador, tablero_oponente)

    fila, columna = pedir_disparo(tablero_oponente)

    resultado = tablero_oponente.disparo(fila, columna)
    print(resultado)

    if resultado == "Tocado" and tablero_oponente.barco_hundido(fila, columna):
        print("¡Hundiste un barco enemigo!")

    if tablero_oponente.barcos_restantes() == 0:
        print(f"¡Jugador {turno} ha ganado!")
        break

    if resultado == "Agua":
        turno = 2 if turno == 1 else 1
