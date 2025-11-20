# 🚢 Batalla Naval (Battleship) - Python Socket Project

Este proyecto es una implementación del clásico juego **Hundir la Flota (Battleship)** utilizando **Python** y **Sockets** para permitir partidas multijugador en red local.

## 📋 Descripción

El objetivo del proyecto es demostrar el uso de conceptos fundamentales de programación y redes en Python, incluyendo:

- **Programación Orientada a Objetos (POO)**: Clases, objetos y encapsulamiento.
- **Sockets (TCP/IP)**: Comunicación cliente-servidor.
- **Manejo de Excepciones**: Control de errores personalizados.
- **Estructuras de Datos**: Listas bidimensionales y diccionarios.

## 🚀 Características

- **Arquitectura Cliente-Servidor**: Un servidor central gestiona la partida entre dos clientes.
- **Tableros Dinámicos**: Generación aleatoria de la flota de barcos.
- **Sistema de Turnos**: Control estricto de turnos y validación de disparos.
- **Feedback en Tiempo Real**: Los jugadores reciben información inmediata sobre sus disparos (Agua, Tocado, Hundido).
- **Código Documentado**: Todas las funciones y clases cuentan con comentarios explicativos.

## 🛠️ Requisitos

- Python 3.x
- Conexión a red local (o localhost para pruebas en un solo equipo).

## 🎮 Cómo Jugar

Para iniciar una partida, necesitas abrir **3 terminales**:

1. **Iniciar el Servidor**:

   ```bash
   python servidor.py
   ```

   _El servidor esperará a que se conecten dos jugadores._

2. **Conectar Jugador 1**:

   ```bash
   python cliente.py
   ```

3. **Conectar Jugador 2**:
   ```bash
   python cliente.py
   ```

¡El juego comenzará automáticamente cuando ambos jugadores estén conectados!

## 📂 Estructura del Proyecto

- `servidor.py`: Script del servidor que gestiona la lógica de conexión y retransmisión de mensajes.
- `cliente.py`: Script del cliente que permite al usuario jugar e interactuar con el servidor.
- `Tablero.py`: Módulo que contiene la clase `Tablero`, la lógica del juego y las excepciones personalizadas.

## 📝 Autor

Proyecto desarrollado como práctica de programación en Python.
