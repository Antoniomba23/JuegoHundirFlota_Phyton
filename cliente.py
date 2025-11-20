import socket as sk
import json
import sys
from Tablero import Tablero, pedir_coordenada, BattleshipError

def main():
    """
    Función principal del cliente.
    - Conecta al servidor.
    - Inicializa los tableros (propio y enemigo).
    - Coloca barcos.
    - Bucle principal: recibe mensajes JSON del servidor y actúa (disparar, esperar, recibir disparo).
    """
    HOST = '127.0.0.1'
    PORT = 65432

    # Usamos "sock" como en el ejemplo
    try:
        sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        sock.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("No se pudo conectar. Asegúrate de que el servidor esté 'escuchando'...")
        return

    print(f"Conectado con {HOST}:{PORT}")
    
    mi_tablero = Tablero("Jugador")
    tablero_enemigo = Tablero("Enemigo")

    print("Colocando barcos aleatoriamente...")
    mi_tablero.colocar_barcos_automaticamente()
    print("¡Barcos colocados!")

    salir = False
    while not salir:
        try:
            datos = sock.recv(1024)
            if not datos:
                print("Servidor desconectado.")
                salir = True
                break

            # Decodificar el diccionario JSON
            mensaje = json.loads(datos.decode())
            
            accion = mensaje.get("accion")

            if accion == "info":
                # Mensaje informativo del servidor
                print(f"Servidor dice: {mensaje['mensaje']}")

            elif accion == "turno":
                estado = mensaje.get("estado")
                if estado == "activo":
                    print("\n--- TU TURNO ---")
                    # Mostrar tableros
                    print("Tu tablero:".ljust(35) + "Tablero del oponente:")
                    for i in range(10):
                        print(f"{chr(65+i)} {mi_tablero.mostrar_fila(i)}   {chr(65+i)} {tablero_enemigo.mostrar_fila(i, ocultar_barcos=True)}")

                    # Pedir coordenadas
                    valido = False
                    while not valido:
                        try:
                            fila = pedir_coordenada("fila")
                            columna = pedir_coordenada("columna")
                            if tablero_enemigo.matriz[fila][columna] in ["💥", "❌"]:
                                print("Ya disparaste ahí.")
                                continue
                            valido = True
                        except ValueError:
                            pass
                    
                    # Enviar diccionario JSON con el disparo
                    disparo_dict = {
                        "accion": "disparo",
                        "fila": fila,
                        "columna": columna
                    }
                    sock.send(json.dumps(disparo_dict).encode())

                    # Recibir resultado del disparo
                    datos_res = sock.recv(1024)
                    res_dict = json.loads(datos_res.decode())
                    resultado = res_dict.get("resultado")
                    print(f"Resultado: {resultado}")

                    # Actualizar mapa enemigo según el resultado
                    if "Tocado" in resultado or "Hundido" in resultado or "Ganado" in resultado:
                        tablero_enemigo.matriz[fila][columna] = "💥"
                    elif "Agua" in resultado:
                        tablero_enemigo.matriz[fila][columna] = "❌"
                    
                    if "Ganado" in resultado:
                        print("¡HAS GANADO!")
                        salir = True

                elif estado == "espera":
                    print("\nEsperando al oponente...")

            elif accion == "disparo":
                # Recibimos ataque: {"accion": "disparo", "fila": 1, "columna": 2}
                fila = mensaje["fila"]
                columna = mensaje["columna"]
                print(f"\n¡Ataque en {chr(65+fila)}{columna}!")

                # Procesar disparo en nuestro tablero local
                res_local = mi_tablero.disparo(fila, columna)
                
                if res_local == "Tocado":
                    if mi_tablero.barco_hundido(fila, columna):
                        res_local = "Hundido"
                        print("¡Barco hundido!")
                    if mi_tablero.barcos_restantes() == 0:
                        res_local = "Ganado"
                        print("¡Has perdido!")
                        salir = True
                
                # Enviar resultado como JSON al servidor (para que se lo pase al otro)
                res_dict = {"accion": "resultado", "resultado": res_local}
                sock.send(json.dumps(res_dict).encode())

                print("Tu tablero tras el ataque:")
                for i in range(10):
                    print(f"{chr(65+i)} {mi_tablero.mostrar_fila(i)}")

        except Exception as e:
            print(f"Error: {e}")
            salir = True

    sock.close()

if __name__ == "__main__":
    main()
