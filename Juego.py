from Tablero import Tablero, pedir_coordenada, BattleshipError, DisparoRepetidoError, CoordenadaInvalidaError

def mostrar_tableros_lado_a_lado(tablero_jugador, tablero_oponente):
    """Muestra los dos tableros en pantalla."""
    print(f"\n--- Turno de {tablero_jugador.nombre} ---")
    espacio = " " * 5
    encabezado = "  " + " ".join(f"{i:^3}" for i in range(10))
    
    print("TU TABLERO".ljust(35) + espacio + "TABLERO RIVAL (Disparos)")
    print(encabezado.ljust(35) + espacio + encabezado)
    
    for idx in range(10):
        letra = chr(ord('A') + idx)
        # Tu tablero muestra tus barcos
        fila_jugador = tablero_jugador.mostrar_fila(idx, ocultar_barcos=False)
        # El tablero rival oculta los barcos, solo muestra agua/tocado/hundido
        fila_oponente = tablero_oponente.mostrar_fila(idx, ocultar_barcos=True)
        
        print(f"{letra} {fila_jugador}".ljust(35) + espacio + f"{letra} {fila_oponente}")

def main():
    print("=== BIENVENIDO A HUNDIR LA FLOTA (BATTLESHIP) ===")
    
    # 1. Creación de Objetos (Clases)
    jugador1 = Tablero("Jugador 1")
    jugador2 = Tablero("Jugador 2")

    # 2. Uso de Diccionarios y Métodos para colocar barcos
    print("\nColocando barcos para Jugador 1...")
    jugador1.colocar_barcos_automaticamente()
    print("Colocando barcos para Jugador 2...")
    jugador2.colocar_barcos_automaticamente()

    turno = 1
    juego_activo = True

    while juego_activo:
        # Definir quién ataca y quién defiende
        if turno == 1:
            atacante = jugador1
            defensor = jugador2
        else:
            atacante = jugador2
            defensor = jugador1

        mostrar_tableros_lado_a_lado(atacante, defensor)

        # 3. Manejo de Excepciones en el flujo del juego
        tiro_valido = False
        while not tiro_valido:
            try:
                print(f"\n{atacante.nombre}, elige coordenadas para disparar.")
                fila = pedir_coordenada("fila")
                columna = pedir_coordenada("columna")
                
                # Realizar disparo
                resultado = defensor.disparo(fila, columna)
                print(f"\n>>> RESULTADO: {resultado} <<<")
                
                # Si no salta excepción, el tiro fue válido
                tiro_valido = True
                
                # Verificar condiciones de victoria
                if resultado == "Tocado":
                    if defensor.barco_hundido(fila, columna):
                        print("¡BOOM! ¡Has hundido un barco enemigo!")
                    
                    if defensor.barcos_restantes() == 0:
                        print(f"\n¡¡¡FELICIDADES {atacante.nombre}!!! HAS GANADO LA PARTIDA.")
                        juego_activo = False
                
                # Cambio de turno: Si es Agua, pasa turno. Si es Tocado, repite.
                if resultado == "Agua":
                    input("\nDisparo al agua. Presiona ENTER para cambiar de turno...")
                    turno = 2 if turno == 1 else 1
                elif juego_activo:
                    print("¡Has tocado un barco! Vuelves a disparar.")
                    
            except DisparoRepetidoError as e:
                print(f"¡Error! {e} Intenta en otra casilla.")
            except CoordenadaInvalidaError as e:
                print(f"¡Error! {e}")
            except BattleshipError as e:
                print(f"Error genérico de Battleship: {e}")
            except Exception as e:
                print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
