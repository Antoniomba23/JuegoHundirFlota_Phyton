import socket as sk
import json
import time

def main():
    """
    Función principal del servidor.
    - Crea el socket.
    - Acepta dos jugadores.
    - Gestiona el bucle de turnos.
    - Intercambia mensajes JSON entre clientes.
    """
    HOST = '127.0.0.1'
    PORT = 65432

    # Usamos "sock" como en el ejemplo
    sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(2)
    print(f"El servidor está esperando en {HOST}:{PORT}...")

    clientes = []
    
    # Aceptar Jugador 1
    conn1, addr1 = sock.accept()
    print(f"Conectado con {addr1} (Jugador 1)")
    mensaje_bienvenida = {"accion": "info", "mensaje": "Bienvenido Jugador 1. Esperando oponente..."}
    conn1.sendall(json.dumps(mensaje_bienvenida).encode())
    clientes.append(conn1)

    # Aceptar Jugador 2
    conn2, addr2 = sock.accept()
    print(f"Conectado con {addr2} (Jugador 2)")
    mensaje_bienvenida_2 = {"accion": "info", "mensaje": "Bienvenido Jugador 2. ¡Juego iniciado!"}
    conn2.sendall(json.dumps(mensaje_bienvenida_2).encode())
    clientes.append(conn2)

    # Avisar a J1
    conn1.sendall(json.dumps({"accion": "info", "mensaje": "¡Juego iniciado! Tu turno comienza."}).encode())

    turno = 1
    salir = False

    while not salir:
        # Definir roles: quién juega y quién espera
        if turno == 1:
            jugador_actual = clientes[0]
            jugador_espera = clientes[1]
        else:
            jugador_actual = clientes[1]
            jugador_espera = clientes[0]

        try:
            # 1. Enviar turno (Diccionario JSON)
            # Avisamos al jugador actual que es su turno y al otro que espere
            jugador_actual.sendall(json.dumps({"accion": "turno", "estado": "activo"}).encode())
            jugador_espera.sendall(json.dumps({"accion": "turno", "estado": "espera"}).encode())

            # 2. Recibir disparo (Diccionario JSON)
            datos = jugador_actual.recv(1024)
            if not datos:
                print(f"Jugador {turno} se desconectó.")
                salir = True
                break
            
            # Decodificar JSON
            mensaje_recibido = json.loads(datos.decode())
            print(f"Llega la siguiente información del Jugador {turno}:\n {mensaje_recibido}")
            
            # mensaje_recibido debería ser algo como {"accion": "disparo", "fila": 1, "columna": 2}

            # 3. Reenviar al oponente para que verifique el impacto
            jugador_espera.sendall(json.dumps(mensaje_recibido).encode())

            # 4. Recibir resultado del oponente (Tocado, Agua, Hundido...)
            datos_res = jugador_espera.recv(1024)
            if not datos_res:
                break
            resultado_dict = json.loads(datos_res.decode())
            print(f"Resultado recibido: {resultado_dict}")

            # 5. Reenviar resultado al atacante para que actualice su mapa
            jugador_actual.sendall(json.dumps(resultado_dict).encode())

            # Verificar fin de juego
            texto_resultado = resultado_dict.get("resultado", "")
            if "Ganado" in texto_resultado:
                print(f"¡Jugador {turno} ha ganado!")
                salir = True
                break

            # Cambio de turno
            # Si es agua, cambia el turno. Si acierta, repite.
            if "Agua" in texto_resultado:
                turno = 2 if turno == 1 else 1
            else:
                print(f"Jugador {turno} repite turno.")

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            salir = True

    print("Cerrando conexiones...")
    for c in clientes:
        c.close()
    sock.close()

if __name__ == "__main__":
    main()
