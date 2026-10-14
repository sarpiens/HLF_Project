#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: main.py

Description:

HLF. Main. Programa principal para lanzar el juego Hundir La Flota (HLF).
Proyecto individual curso Data Science - The Bridge y Fundación Universia (2026-09).

Author: Samuel Piquer Esteban
Date: 14 Octubre 2026

Version: 1.0.0
"""
#Atributos del programa y constantes
PROGRAM_NAME = "Hundir La Flota"
__version__ = "1.0.0"
MACHINE_NAME = "WarMachine"
DIM_BARCOS = [2,2,2,3,3,4] #Las dimensiones de los 6 barcos a generar

#Importar librerias y clases de utils
from utils import Jugador, Partida
import os, subprocess

#Programa principal
def main():
    #Menú para elegir modo juego 
    while True:
        #Limpiamos pantalla AL PRINCIPIO de la vuelta al menú principal
        ##Windows: 'cls' if os.name == 'nt'
        ##Else(Linux y Mac): ['clear']
        subprocess.run('cls' if os.name == 'nt' else ['clear'], shell=os.name == 'nt')

        ##Mensaje nombre y version programa
        print(f"\n{PROGRAM_NAME} v {__version__}")

        #Mostrar mensaje de menú con opciones
        print("\n===================================")
        print("        ⚓ Menú de Juego ⚓       ")
        print("===================================")
        print("1. Modo de Juego contra Máquina")
        print("2. Modo de Juego para 2 Jugadores")
        print("3. Salir del Programa")
        print("===================================")
        #Preguntar valor al usuario
        try:
            #Intentar convertir a número float
            menu_input = input("Proporciona tu elección (1-3): ")
            menu_input_float = float(menu_input)
        except:
            print(f"\n{menu_input} no es un número!")
            print("Vuelve a intentarlo!")
            input("\nPresiona Enter para volver al menú principal...")
        else:
            #Validamos los inputs
            if menu_input_float not in range(1,4):
                print(f"\n{menu_input} no es un número entero positivo entre 1-3!")
                print("Vuelve a intentarlo!")
                input("\nPresiona Enter para volver al menú principal...")
            else:
                 #Modo de Juego contra Máquina
                 if menu_input_float == 1:
                    #1.1 Mensaje inicial
                    mesaje_inicial = f"\nBienvenido Jugador!\nPreparate para enfrentarte a la poderosa {MACHINE_NAME} en el clásico juego {PROGRAM_NAME}!"
                    print(mesaje_inicial)
                    #1.2. Solicitar su nombre al Jugador por pantalla
                    nombre_jugador = input("- Proporcione su nombre: ")
                    #1.3. Inicilizar jugadores
                    ##Mostrar mensaje
                    print("\nInicializando jugadores...")
                    ##Inicializar jugador
                    jugador_main = Jugador(nombre_jugador,DIM_BARCOS)
                    jugador_main.colocar_barcos()   
                    ##Inicializar warmachine
                    maquina = Jugador(MACHINE_NAME, DIM_BARCOS)
                    maquina.colocar_barcos()
                    #1.4. Inicializar partida con jugadores
                    ##Mostrar mensaje
                    print("\nInicializando partida...\n")
                    partida_maquina = Partida(jugador1 = jugador_main, jugador2 = maquina)
                    #1.5. Lanzar modo de juego
                    partida_maquina.modo_maquina()
                 #Modo de Juego para 2 Jugadores
                 elif menu_input_float == 2:
                    #2.1. Mensaje inicial
                    mesaje_inicial = f"\nBienvenidos Jugadores!\nPrepararos para enfrentaros en el clásico juego {PROGRAM_NAME}!"
                    print(mesaje_inicial)
                    #2.2. Pedir el nombre a los jugadores
                    nombre_jugador1 = input("- Proporcione su nombre (Jugador 1): ")
                    nombre_jugador2 = input("- Proporcione su nombre (Jugador 2): ")
                    #2.3. Inicilizar jugadores
                    ##Mostrar mensaje
                    print("\nInicializando jugadores...")
                    ##Inicializar jugador1
                    jugador1 = Jugador(nombre_jugador1,DIM_BARCOS)
                    jugador1.colocar_barcos()
                    ##Inicializar jugador2
                    jugador2 = Jugador(nombre_jugador2,DIM_BARCOS)
                    jugador2.colocar_barcos()  
                    #2.4. Inicializar partida con jugadores
                    ##Mostrar mensaje
                    print("\nInicializando partida...\n")
                    partida_2jugadores = Partida(jugador1 = jugador1, jugador2 = jugador2)
                    #2.5. Lanzar modo de juego
                    partida_2jugadores.modo_2_jugadores()
                 #Salida del programa (Solo opción 3 tiene break, al acabar la partida volverá al menú principal)
                 else:
                    print("\nSaliendo del Programa. Chao!")
                    print("Decidiste hacer el amor, no la guerra!\n")
                    break
                     
if __name__ == "__main__":
    main()