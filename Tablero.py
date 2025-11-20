import random

# --- Excepciones Personalizadas ---
class BattleshipError(Exception):
    """Clase base para excepciones del juego Battleship."""
    pass

class CoordenadaInvalidaError(BattleshipError):
    """Se levanta cuando las coordenadas están fuera del tablero o formato incorrecto."""
    pass

class DisparoRepetidoError(BattleshipError):
    """Se levanta cuando se dispara a una casilla ya disparada."""
    pass

class BarcoNoCabeError(BattleshipError):
    """Se levanta cuando un barco no cabe en la posición indicada."""
    pass

# --- Clase Tablero ---
class Tablero:
    def __init__(self, nombre):
        """
        Constructor de la clase Tablero.
        Inicializa el nombre del jugador, la matriz de 10x10 con agua,
        y define la flota de barcos disponible.
        """
        self.nombre = nombre
        self.matriz = [["🌊"] * 10 for _ in range(10)]
        self.barcos_vivos = 0
        # Diccionario de barcos: Nombre -> Tamaño
        self.flota = {
            "Portaaviones": 4,
            "Submarino": 3,
            "Destructor": 2,
            "Lancha": 1
        }

    def mostrar_fila(self, fila_idx, ocultar_barcos=False):
        """
        Devuelve una representación en string de una fila específica del tablero.
        Si ocultar_barcos es True, los barcos ('🚢') se muestran como agua ('🌊').
        """
        fila = self.matriz[fila_idx]
        if ocultar_barcos:
            mostrar = ["🌊" if cel == "🚢" else cel for cel in fila]
        else:
            mostrar = fila
        # Cada celda con ancho fijo de 3 espacios para alinear bien
        return " ".join(f"{cel:^3}" for cel in mostrar)

    def validar_coordenada(self, fila, columna):
        """
        Verifica si las coordenadas (fila, columna) están dentro del rango 0-9.
        Levanta CoordenadaInvalidaError si no lo están.
        """
        if not (0 <= fila < 10 and 0 <= columna < 10):
            raise CoordenadaInvalidaError(f"Coordenadas ({fila}, {columna}) fuera de rango.")

    def cabe_barco(self, fila, columna, tamaño, orientacion):
        """
        Comprueba si un barco de cierto tamaño cabe en la posición y orientación dadas
        sin salirse del tablero ni chocar con otro barco.
        Retorna True si cabe, False si no.
        """
        self.validar_coordenada(fila, columna)
        if orientacion == "H":
            if columna + tamaño > 10:
                return False
            for c in range(columna, columna + tamaño):
                if self.matriz[fila][c] != "🌊":
                    return False
        elif orientacion == "V":
            if fila + tamaño > 10:
                return False
            for f in range(fila, fila + tamaño):
                if self.matriz[f][columna] != "🌊":
                    return False
        else:
            raise BattleshipError("Orientación desconocida. Use 'H' o 'V'.")
        return True

    def colocar_barcos_automaticamente(self):
        """
        Coloca todos los barcos definidos en self.flota en posiciones aleatorias.
        Intenta hasta 100 veces por barco para encontrar un hueco libre.
        """
        for nombre_barco, tamaño in self.flota.items():
            colocado = False
            intentos = 0
            while not colocado and intentos < 100:
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
                intentos += 1

    def disparo(self, fila, columna):
        """
        Procesa un disparo en las coordenadas dadas.
        - Si hay barco ('🚢') -> Marca como tocado ('💥') y retorna "Tocado".
        - Si hay agua ('🌊') -> Marca como fallado ('❌') y retorna "Agua".
        - Si ya se disparó ahí -> Levanta DisparoRepetidoError.
        """
        self.validar_coordenada(fila, columna)
        celda = self.matriz[fila][columna]
        
        if celda in ["💥", "❌"]:
            raise DisparoRepetidoError(f"Ya has disparado en ({fila}, {columna}).")
        
        if celda == "🚢":
            self.matriz[fila][columna] = "💥"
            return "Tocado"
        elif celda == "🌊":
            self.matriz[fila][columna] = "❌"
            return "Agua"
        
        return "Error desconocido"

    def barcos_restantes(self):
        """
        Cuenta cuántas celdas de barco ('🚢') quedan intactas en el tablero.
        Si devuelve 0, el jugador ha perdido.
        """
        return sum(fila.count("🚢") for fila in self.matriz)

    def barco_hundido(self, fila, columna):
        """
        Verifica si el barco que ocupa la posición (fila, columna) ha sido hundido completamente.
        Revisa horizontal y verticalmente si todas las partes del barco están tocadas ('💥').
        """
        # Si no es un impacto, no tiene sentido verificar
        if self.matriz[fila][columna] != "💥":
            return False

        posiciones = []

        # Verificar horizontalmente
        c = columna
        while c >= 0 and self.matriz[fila][c] in ["🚢", "💥"]:
            posiciones.append((fila, c))
            c -= 1
        c = columna + 1
        while c <= 9 and self.matriz[fila][c] in ["🚢", "💥"]:
            posiciones.append((fila, c))
            c += 1
        
        if len(posiciones) > 0:
             if all(self.matriz[f][c] == "💥" for f, c in posiciones):
                 if len(posiciones) > 1: 
                     return True
        
        # Verificar verticalmente
        posiciones_v = []
        f = fila
        while f >= 0 and self.matriz[f][columna] in ["🚢", "💥"]:
            posiciones_v.append((f, columna))
            f -= 1
        f = fila + 1
        while f <= 9 and self.matriz[f][columna] in ["🚢", "💥"]:
            posiciones_v.append((f, columna))
            f += 1
            
        if posiciones_v and all(self.matriz[f][c] == "💥" for f, c in posiciones_v):
             return True

        return False

# --- Funciones auxiliares ---
def pedir_coordenada(tipo):
    """
    Solicita al usuario una coordenada (Fila A-J o Columna 0-9).
    Valida la entrada y la convierte a índice numérico (0-9).
    """
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
