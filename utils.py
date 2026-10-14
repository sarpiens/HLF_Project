#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: utils.py

Description:

HLF. Utils. Programa con utilidades para lanzar el juego Hundir La Flota (HLF).
Proyecto individual curso Data Science - The Bridge y Fundación Universia (2026-09).

Author: Samuel Piquer Esteban
Date: 14 Octubre 2026

Version: 1.0.0
"""

#Importar librerias principales
import numpy as np
import random
import os, subprocess
from itertools import cycle

#Definir clases
class Partida():
    """
    Clase Partida. Representa las características y métodos asociados a una partida del juego
    Hundir La Flota (HLF).

    Attributes:
        jugador1 (Jugador) : El primer jugador que interactúa por terminal.
        jugador2 (Jugador) : El segundo jugador que actúa como contrincante. Dependiendo del modo de juego será máquina u otro jugador real.
    """
    def __init__(self, jugador1:"Jugador",jugador2:"Jugador"):
        """
        Método que inizializa una nueva Partida.
        
        Args:
            jugador1 (Jugador) : El jugador principal que interactúa por terminal.
            jugador2 (Jugador) : El jugador que actúa como contrincante.
        """
        #Validamos los inputs proporcionados
        if not isinstance(jugador1,Jugador):
            raise TypeError(f"jugador1 debe ser un objeto de la clase Jugador, pero se proporcionó {type(jugador1)}.")
        if not isinstance(jugador2,Jugador):
            raise TypeError(f"jugador2 debe ser un objeto de la clase Jugador, pero se proporcionó {type(jugador2)}.")
        #Si las validaciones pasan asignamos atributos
        self.jugador1 = jugador1
        self.jugador2 = jugador2

    def mostrar_tablas(self, espacio_entre_tablas:int = 10, ocultar_jugador:int = 2):
        """
        Método mostrar_tablas. Imprime por pantalla los dos tableros de los jugadores
        decorados con índices de filas (izquierda) y columnas (abajo), así como los 
        nombres de los jugadores (arriba) y la leyenda. Además, podemos indicarle para 
        que jugador se ocultan las posiciones de barcos en pantalla.

        Args:
            espacio_entre_tablas (int) : El espacio a mostrar entre las tablas de los dos jugadores. Por defecto, 10.
            ocultar_jugador (int) : Indicar para que jugador ocultar los barcos. Opciones 1(jugador1) y 2(jugador2). Por defecto, 2.
        """
        #0.Validaciones de parámetros
        if ocultar_jugador not in (1,2):
            raise ValueError("ocultar_jugador debe ser estrictamente 1 o 2.")
        if not isinstance(espacio_entre_tablas,int):
            raise TypeError(f"espacio_entre_tablas debe ser un int, pero se proporcionó {type(espacio_entre_tablas)}.")
        if espacio_entre_tablas < 3:
            raise ValueError("espacio_entre_tablas debe ser al menos de tamaño 3.")

        # 1. Convertimos los arrays a texto en función de ocultar_jugador
        ##Luego reemplazamos los corchetes y los caracteres_barco del jugador a ocultar
        if ocultar_jugador == 1:
            str_tabla1 = np.array2string(self.jugador1.tablero).replace('[', ' ').replace(']', ' ').replace(self.jugador1.caracter_barco,self.jugador1.caracter_agua)
            str_tabla2 = np.array2string(self.jugador2.tablero).replace('[', ' ').replace(']', ' ')
        else:
            str_tabla1 = np.array2string(self.jugador1.tablero).replace('[', ' ').replace(']', ' ')
            str_tabla2 = np.array2string(self.jugador2.tablero).replace('[', ' ').replace(']', ' ').replace(self.jugador2.caracter_barco,self.jugador2.caracter_agua)
        ##Preparamos las lineas de las tablas en listas ("if linea.strip()" elimina filas vacias)
        lineast1 = [linea.strip() for linea in str_tabla1.split('\n') if linea.strip()]
        lineast2 = [linea.strip() for linea in str_tabla2.split('\n') if linea.strip()]
    
        # 2. Definimos los componentes decorativos inferiores
        ##Como tendran el mismo tamaño usamos atributo tablero_tamaño para definir limite superior
        indices_columnas = " "*5 + "   ".join([str(i) for i in range(0,self.jugador1.tablero_tamaño)])
        linea_divisoria  = "  "*2 + " ".join("——" * self.jugador1.tablero_tamaño)
    
        #3. Imprimimos la decoración superior con nombres de los jugadores
        espacio_nombres = len(linea_divisoria) - (len(self.jugador1.nombre)+2) + espacio_entre_tablas
        print(f"{" "*2}[{self.jugador1.nombre}]{" " * espacio_nombres}[{self.jugador2.nombre}]")

        # 4. Imprimimos el cuerpo (tablas + Índices de filas a la izquierda)
        for i in range(self.jugador1.tablero_tamaño):       
            # Imprimimos ambas filas formateadas (indice filas + filat1 + espacio + filat2)
            print(f"{i} | {lineast1[i]}{' ' * espacio_entre_tablas}{i} | {lineast2[i]}")
        
        # 5. Imprimimos la decoración inferior (Línea y luego índices de columnas)
        print(f"{linea_divisoria}{' ' * espacio_entre_tablas}{linea_divisoria}")
        print(f"{indices_columnas}{' ' * espacio_entre_tablas} {indices_columnas}")

        # 6. Mostrar leyenda de caracteres
        print(f"\nLeyenda: Agua '{self.jugador1.caracter_agua}', Barco '{self.jugador1.caracter_barco}', Disparo Agua '{self.jugador1.caracter_disparo_agua}' y Disparo Barco '{self.jugador1.caracter_disparo_acierto}'")
   
    def modo_maquina(self):
        """
        Método modo_maquina. Este método gestiona los turnos y acciones de cada jugador
        para el modo de juego de 1 jugador contra la máquina.
        """
        # Definimos los jugadores y creamos el ciclo
        jugadores = cycle([self.jugador1, self.jugador2])

        # Generamos un bucle que se repita mientras ambos jugadores esten vivos
        while (self.jugador1.alive == True) and (self.jugador2.alive == True):
            #Inicilizamos turno del jugador actual
            ## next() obtiene automáticamente el siguiente jugador en la lista
            jugador_actual = next(jugadores)
            ##Mensaje de inicio de turno 
            print(f"Turno de: {jugador_actual.nombre}\n")
            ##Inicializamos variable turno_activo
            turno_activo = True
            ##Inicializamos bucle de turno_activo
            while turno_activo:
                #Mostrar las tablas (ocultando siempre los barcos de la maquina)
                self.mostrar_tablas(ocultar_jugador=2)
                #Si el jugador actual es jugador1
                if jugador_actual == self.jugador1:
                    #Pedir disparo
                    ##Mensaje disparo
                    print("\nProporciona coordenadas de disparo")
                    ##Pedir coordenadas en try/except
                    try:
                        disparo_rows = input(f"- Proporciona tu elección de fila (0-{jugador_actual.tablero_tamaño-1}): ")
                        disparo_rows_int = int(disparo_rows)
                        disparo_cols = input(f"- Proporciona tu elección de columna (0-{jugador_actual.tablero_tamaño-1}): ")
                        disparo_cols_int = int(disparo_cols)
                    except:
                        print("\nEl valor proporcionado no es un número entero!")
                        print("Vuelve a intentarlo!\n")
                    else:
                        ##Disparar al rival en try/except (la funcion disparar valida el disparo internamente)
                        try:
                            disparo = (disparo_rows_int,disparo_cols_int)
                            self.jugador2.disparar(disparo)
                        except Exception as e:
                            print(e) #Si no cumple condiciones queda recogido en esta excepción
                        else:
                            #Si falla el disparo perdemos el turno
                            if self.jugador2.tablero[disparo] == self.jugador2.caracter_disparo_agua:
                                print("\nDisparo fallido, le diste al agua!")
                                #Terminamos el turno
                                turno_activo = False
                            else:
                                print("\nDisparo certero, le diste a un barco del rival!")
                            #Comprobar barcos hundidos del rival y mostramos stats de barcos
                            self.jugador1.check_barcos_hundidos(self.jugador2)
                #Si el jugador actual es la maquina
                else:
                    #Generar disparo maquina y disparar
                    disparo = self.jugador1.crear_disparo_maquina() #Valida el disparo internamente
                    self.jugador1.disparar(disparo)
                    print(f"\n{self.jugador2.nombre} disparó en las coordenadas {disparo}")
                    #Si falla el disparo la maquina pierde el turno
                    if self.jugador1.tablero[disparo] == self.jugador1.caracter_disparo_agua:
                        print("Disparo fallido, la máquina le dio al agua!")
                        #Terminamos el turno
                        turno_activo = False
                    else:
                        print("Disparo certero, la máquina le dio a uno de tus barcos!")
                    #Comprobar barcos hundidos del rival y mostramos stats de barcos
                    self.jugador2.check_barcos_hundidos(self.jugador1)
                
                #Además comprobamos/actualizamos el estado de los dos jugadores (alive)
                self.jugador1.check_alive()
                self.jugador2.check_alive()
                #Si alguno de los dos muere turno_activo = False (terminar partida)
                if (self.jugador1.alive == False) or (self.jugador2.alive == False):
                    turno_activo = False
        
        #Mensaje final
        ##Mensaje (Enhorabuena o derrota)
        if self.jugador1.alive == True:
            print(f"Enhorabuena {self.jugador1.nombre}! Ganaste la partida a {self.jugador2.nombre}!")
        else:
            print(f"Lo sentimos {self.jugador1.nombre}! Pertiste la partida contra {self.jugador2.nombre}!")
        ##Mensaje de juego finalizado y vuelta al menú
        print("\nPartida finalizada.")
        input("Presiona Enter para pasar al menú principal...")

    def modo_2_jugadores(self):
        """
        Método modo_2_jugadores. Este método gestiona los turnos y acciones de cada jugador
        para el modo de juego de 2 jugadores.
        """
        # Definimos los jugadores y creamos el ciclo
        jugadores = cycle([self.jugador1, self.jugador2])
        
        # Generamos un bucle que se repita mientras ambos jugadores esten vivos
        while (self.jugador1.alive == True) and (self.jugador2.alive == True):         
            #Inicilizamos turno del jugador actual
            ## next() obtiene automáticamente el siguiente jugador en la lista
            jugador_actual = next(jugadores)
            ## Definimos al rival_actual
            if jugador_actual == self.jugador1:
                rival_actual = self.jugador2
            else:
                rival_actual = self.jugador1
            #Limpiamos pantalla AL PRINCIPIO de la vuelta para el nuevo turno
            ##Windows: 'cls' if os.name == 'nt' y shell=True
            ##Else(Linux y Mac): ['clear']
            subprocess.run('cls' if os.name == 'nt' else ['clear'], shell=os.name == 'nt')
            ##Mensaje de inicio de turno
            print(f"\nTurno de: {jugador_actual.nombre}\n")
            ##Sala de espera
            input("Presiona Enter para comenzar tu turno ...\n")
            ##Inicializamos variable turno_activo
            turno_activo = True
            ##Inicializamos bucle de turno_activo
            while turno_activo:
                ##Mostras tableros dependiendo del jugador actual(ocultando barcos del rival)
                if jugador_actual == self.jugador1:
                    self.mostrar_tablas(ocultar_jugador=2)
                else:
                    self.mostrar_tablas(ocultar_jugador=1)
                #Pedir disparo
                ##Mensaje disparo
                print("\nProporciona coordenadas de disparo")
                ##Pedir coordenadas en try/except
                try:
                    disparo_rows = input(f"- Proporciona tu elección de fila (0-{jugador_actual.tablero_tamaño-1}): ")
                    disparo_rows_int = int(disparo_rows)
                    disparo_cols = input(f"- Proporciona tu elección de columna (0-{jugador_actual.tablero_tamaño-1}): ")
                    disparo_cols_int = int(disparo_cols)
                except:
                    print("\nEl valor proporcionado no es un número entero!")
                    print("Vuelve a intentarlo!\n")
                else:
                    ##Disparar al rival en try/except (la funcion disparar valida el disparo internamente)
                    try:
                        disparo = (disparo_rows_int,disparo_cols_int)
                        rival_actual.disparar(disparo)
                    except Exception as e:
                        print(e) #Si no cumple condiciones queda recogido en esta excepción
                    else:
                        #Si falla el disparo perdemos el turno
                        if rival_actual.tablero[disparo] == rival_actual.caracter_disparo_agua:
                            print("\nDisparo fallido, le diste al agua!")
                            #Terminamos el turno
                            turno_activo = False
                        else:
                            print("\nDisparo certero, le diste a un barco del rival!")
                        
                        #Comprobar barcos hundidos del rival y mostramos stats de barcos
                        jugador_actual.check_barcos_hundidos(rival_actual)
                        #Además comprobamos/actualizamos el estado de los dos jugadores (alive)
                        self.jugador1.check_alive()
                        self.jugador2.check_alive()
                        #Si ha terminado el turno pausamos hasta que presione enter
                        if turno_activo == False:
                            print("Turno finalizado.")
                            input("Presiona Enter para pasar el turno al rival...")
                        #Si alguno de los dos muere turno_activo = False (terminar partida)
                        if (self.jugador1.alive == False) or (self.jugador2.alive == False):
                            turno_activo = False
        #Mensaje final
        ##Mensaje enhorabuena
        if self.jugador1.alive == True:
            print(f"Enhorabuena {self.jugador1.nombre}! Ganaste la partida a {self.jugador2.nombre}!")
        else:
            print(f"Enhorabuena {self.jugador2.nombre}! Ganaste la partida a {self.jugador1.nombre}!")
        ##Mensaje de juego finalizado y vuelta al menú
        print("\nPartida finalizada.")
        input("Presiona Enter para pasar al menú principal...")

class Jugador():
    """
    Clase Jugador. Representa las características y métodos asociados a los jugadores del juego
    Hundir La Flota (HLF).

    Attributes:
        nombre (str) : Nombre del jugador.
        tablero (np.array) : El tablero de juego asignado al jugador.
        dim_barcos (list) : Lista con las dimensiones de los barcos del jugador.
        alive (bool) : Indica si el jugador sigue vivo o no.
        caracter_agua (str) : Carácter que representa agua en tablero. Por defecto, "_".
        caracter_barco (str) : Carácter que representa barco en tablero. Por defecto, "O".
        caracter_disparo_acierto (str) : Carácter que representa disparo sobre barco en tablero. Por defecto, "X".
        caracter_disparo_agua (str) : Carácter que representa disparo sobre agua en tablero. Por defecto, "A".
        tablero_tamaño (int): Tamaño del tablero del cuadrado tamaño x tamaño. Por defecto, 10.
        lista_barcos (list) : Lista de listas con las coordenadas (fila, columna) de cada barco del jugador.
        casillas_barcos (int) : Número total de casillas ocupadas por barcos.
        n_barcos_hundidos (int) : Indica el número de barcos hundidos del jugador.
    """
    #Definir atributos comunes de la clase
    alive:bool = True
    caracter_agua:str = "_"
    caracter_barco:str = "O"
    caracter_disparo_acierto:str = "X"
    caracter_disparo_agua:str = "A"
    tablero_tamaño:int = 10
    lista_barcos:list = []
    n_barcos_hundidos:int = 0

    #Iniciar constructor
    def __init__(self, nombre:str, dim_barcos:list):
        """
        Método que inizializa un nuevo Jugador.

        Args:
            nombre (str) : Nombre del jugador.
            dim_barcos (list) : Lista con las dimensiones de los barcos del jugador.
        """
        #Validamos los inputs proporcionados
        ##Comprobar que nombre sea str
        if not isinstance(nombre,str):
            raise TypeError(f"nombre debe ser un str, pero se proporcionó {type(nombre)}.")
        ##Comprobar que dim_barcos sea lista
        if not isinstance(dim_barcos, list):
            raise TypeError(f"dim_barcos debe ser una lista, pero se proporcionó {type(dim_barcos)}.")
        ##Comprobar que la lista no este vacia
        if len(dim_barcos) < 1:
            raise ValueError(f"dim_barcos no puede ser una lista vacía.")
        ##Comprobar que sus elementos sean numeros enteros no booleanos y positivos
        if not all(isinstance(x, int) and x > 0 and not isinstance(x, bool) for x in dim_barcos):
            raise TypeError(f"Todos los valores dentro de la lista dim_barcos deben ser números enteros positivos mayores que cero.")
        #Si las validaciones pasan asignamos atributos
        self.nombre = nombre
        self.tablero = self.crear_tablero(self.tablero_tamaño) #Crearemos el tablero al inicializar al jugador
        self.dim_barcos = dim_barcos
        self.casillas_barcos = sum(dim_barcos) #Calculamos el total de casillas ocupadas por barcos

    def crear_tablero(self, tamaño:int = 10):
        """
        Método crear_tablero. Genera el tablero del juego, un numpy array cuadrado del tamaño proporcionado (tamaño x tamaño).
        Por defecto, se generará un array cuadrado de tamaño 10 rellenado con el atributo caracter_agua.

        Args:
            tamaño (int) : Indicar el tamaño del tablero para generar un array cuadrado (tamaño x tamaño).
                           Por defecto, tamaño = 10.        
        Returns:
            numpy array : El tablero inicial rellenado con caracter_agua.
        """
        #Validamos los inputs proporcionados
        ##Comprobar que tamaño sea int
        if not isinstance(tamaño,int) or isinstance(tamaño, bool):
            raise TypeError(f"tamaño debe ser un int, pero se proporcionó {type(tamaño)}.")
        #Si pasa los checks creamos la tabla cuadrada
        return np.full((tamaño,tamaño),self.caracter_agua)

    def crear_disparo_maquina(self):
        """
        Método crear_disparo_maquina. Genera un disparo para el jugador máquina. De forma aleatoria en bucle hasta conseguir una coordenada
        adecuada. Internamente valida que el disparo este dentro del rango de posiciones del tablero y que la posición del disparo
        no coincida con un disparo previo (que no sean ni caracter_disparo_acierto ni caracter_disparo_agua).

        Returns:
            tuple : Las coordenadas validadas del disparo aleatorio (fila, columna).
        """
        while True:
            #Generamos disparo aleatoria entre (0,0) y (9,9) (0 a tablero_tamaño - 1, 0 a tablero_tamaño - 1)
            disparo = (random.randint(0,self.tablero_tamaño-1), random.randint(0,self.tablero_tamaño-1))
            #Comprobar condiciones
            ##Que este dentro de los limites del tablero
            condicion1 = (0 <= disparo[0] <= (self.tablero_tamaño-1) and 0 <= disparo[1] <= (self.tablero_tamaño-1))
            ##Que no sea un disparo previo
            condicion2 = not (self.tablero[disparo] == self.caracter_disparo_agua or self.tablero[disparo] == self.caracter_disparo_acierto)
            if condicion1 and condicion2:
                return disparo

    def disparar(self, casilla:tuple):
        """
        Método disparar. Actualiza el tablero en función de la casilla proporcionada para disparar.
        Comprobará si el disparo acertó a un barco o disparó al agua.

        Args:
            casilla (tuple) : Coordenadas validadas sobre las que se quiere disparar (fila, columna).
        """
        #Validamos los inputs proporcionados
        ##Comprobar que casilla sea tuple
        if not isinstance(casilla,tuple):
            raise TypeError(f"casilla debe ser una tupla, pero se proporcionó {type(casilla)}.")
        if len(casilla) != 2:
            raise ValueError("casilla debe ser una tupla de tamaño 2, representando coordenadas(fila, columna).")
        #Comprobar que este dentro de los limites del tablero
        rango_tablero = (0 <= casilla[0] <= (self.tablero_tamaño-1) and 0 <= casilla[1] <= (self.tablero_tamaño-1))
        if not rango_tablero:
            raise ValueError(f"\nLas coordenadas proporcionadas para disparar deben estar dentro del tablero en un rango (0-{self.tablero_tamaño-1},0-{self.tablero_tamaño-1})!\nVuelve a intentarlo!\n")
        ##Comprobar que no sea un disparo previo
        if self.tablero[casilla] == self.caracter_disparo_agua or self.tablero[casilla] == self.caracter_disparo_acierto:
            raise ValueError(f"\nLas coordenadas proporcionadas corresponden a un disparo previo!\nVuelve a intentarlo!\n")
        #Después de las comprobaciones realizamos el disparo
        if self.tablero[casilla] == self.caracter_barco:
            self.tablero[casilla] = self.caracter_disparo_acierto
        elif self.tablero[casilla] == self.caracter_agua:
            self.tablero[casilla] = self.caracter_disparo_agua

    def devolver_celdas_vecinas(self, posiciones_barco:list):
        """
        Método devolver_celdas_vecinas. Este método calcula las celdas vecinas dentro de las
        dimensiones del tablero para el barco proporcionado.
        
        Args:
            posiciones_barco (list): Lista de tuplas con las posiciones (fila,columna) del barco.
        
        Returns:
            celdas_vecinas (list) : Lista de tuplas con las posiciones vecinas (fila,columna) al barco.
        """
        #Inicializar resultado
        celdas_vecinas_raw = []

        #Calcular posiciones vecinas
        for f,c in posiciones_barco:
            #Calcular posiciones up (- 1 fila)
            celdas_vecinas_raw.append((f-1,c))
            #Calcular posiciones down (+ 1 fila)
            celdas_vecinas_raw.append((f+1,c))
            #Calcular posiciones izquierda (-1 columna)
            celdas_vecinas_raw.append((f,c-1))
            #Calcular posiciones derecha (+ 1 columna))
            celdas_vecinas_raw.append((f,c+1))
        #Filtrar aquellas que se salgan del tablero
        celdas_vecinas_ftablero = [(f,c) for f,c in celdas_vecinas_raw if 0 <= f <= (self.tablero_tamaño-1) and 0 <= c <= (self.tablero_tamaño-1)]
        #Filtrar aquellas que esten en posiciones_barco
        celdas_vecinas = [celda for celda in celdas_vecinas_ftablero if celda not in posiciones_barco]
        return celdas_vecinas

    def crear_barco(self, eslora:int):
        """
        Método crear_barco. Crea una lista de casillas de un barco en función de la eslora (tamaño barco).
        De forma aleatoria en bucle hasta conseguir una configuración adecuada. Internamente valida que
        el barco este dentro del rango de posiciones del tablero y que todas las posiciones esten vacias
        (posiciones caracter_agua) en el barco y sus celdas vecinas.

        Args:
            eslora (int) : El tamaño del barco a crear.

        Returns:
            list : Lista con las posiciones validadas del barco (fila, columna). Una lista de tuplas.
        """
        #Validamos el input
        #Comprobar que eslora sea int
        if not isinstance(eslora,int) or isinstance(eslora, bool):
            raise TypeError(f"el tamaño de eslora debe ser un int, pero se proporcionó {type(eslora)}.")
        #Comprobamos tamaños de eslora
        if eslora > self.tablero_tamaño:
            raise ValueError(f"el tamaño de eslora no puede ser mayor que el tamaño del tablero.")
        if eslora < 1:
            raise ValueError(f"el tamaño de eslora debe ser al menos de tamaño 1.")
        #Comenzar bucle para generar barco de forma aleatoria
        while True:
            #Inicializamos lista resultado
            boat_positions = []
            #Generamos la posición inicial aleatoria entre (0,0) y (9,9) (0 a tablero_tamaño-1,0 a tablero_tamaño-1)
            init_position = (random.randint(0,self.tablero_tamaño-1), random.randint(0,self.tablero_tamaño-1))
            boat_positions.append(init_position)
            ## Get random orientation
            orientacion = random.choice(["N","S","E","O"])
            ##Set signo e index dependiendo de orientación, ojo! array(filas, columnas)
            if orientacion == "N": #Filas; signo - (va hacia arriba)
                for n in range(1,eslora):
                    boat_positions.append((init_position[0]-n,init_position[1]))
            elif orientacion == "S": #Filas; signo + (va hacia abajo)
                for n in range(1,eslora):
                    boat_positions.append((init_position[0]+n,init_position[1]))
            elif orientacion == "E": #Columnas; signo + (va hacia la derecha)
                for n in range(1,eslora):
                    boat_positions.append((init_position[0],init_position[1]+n))
            else: # por descarte "O" Columnas; signo - (va hacia la izquierda)
                for n in range(1,eslora):
                    boat_positions.append((init_position[0],init_position[1]-n))
            #Comprobaciones
            ##Si todas las posiciones entran en el tablero
            if all(0<= fila <= (self.tablero_tamaño-1) and 0 <= columna <= (self.tablero_tamaño-1) for fila,columna in boat_positions):
                ###Si todas las posiciones son caracter_agua
                if all(self.tablero[posicion] == self.caracter_agua for posicion in boat_positions):
                    ###Y que sean caracter_agua también en las posiciones vecinas
                    if all(self.tablero[posicion] == self.caracter_agua for posicion in self.devolver_celdas_vecinas(boat_positions)):
                        return boat_positions

    def colocar_barco(self, barco:list):
        """
        Método colocar_barco. Coloca un barco proporcionado en el tablero.

        Args:
            barco (list) : Lista de tuplas con las posiciones del barco proporcionado (fila, columna).
        """
        for coordenada in barco:
            self.tablero[coordenada] = self.caracter_barco

    def colocar_barcos(self):
        """
        Método colocar_barcos. Este método usa el atributo dim_barcos junto con los métodos
        crear_barco y colocar_barco, para generar y colocar todos los barcos en el tablero del
        jugador. Además, actualiza el atributo lista_barcos para el jugador con los resultados.  
        """
        lista_barcos = []

        for eslora in self.dim_barcos:
            #Creamos el barco actual
            tmp_barco = self.crear_barco(eslora)
            #Lo añadimos al tablero
            self.colocar_barco(tmp_barco)
            #Guardamos el resultado en lista_barcos
            lista_barcos.append(tmp_barco)

        #Asignamos atributo con el resultado
        self.lista_barcos = lista_barcos

    def check_alive(self):
        """
        Método check_alive. Este método comprueba si el jugador está vivo. Para ello,
        cuenta el total de aciertos y mira si coincide con el total de casillas de los
        barcos del Jugador. En cuyo caso, se actualiza el atributo alive a False.
        """
        #Comprobamos si el total de aciertos (X) coincide con total casillas de barcos del jugador
        if np.sum(self.tablero==self.caracter_disparo_acierto) == self.casillas_barcos:
            self.alive = False

    def contar_barcos_hundidos(self):
        """
        Método contar_barcos_hundidos. Este método comprueba la lista de barcos y obtiene
        el total de barcos hundidos del Jugador.
        
        Returns:
            actual_n_barcos_hundidos (int) : Total de barcos hundidos del Jugador.
        """
        #Creamos un contador para ver los barcos hundidos actuales
        actual_n_barcos_hundidos = 0
        for barco in self.lista_barcos:
            if all(self.tablero[posicion] == self.caracter_disparo_acierto for posicion in barco):
                actual_n_barcos_hundidos += 1
        return actual_n_barcos_hundidos

    def check_barcos_hundidos(self, otro_jugador:"Jugador"):
        """
        Método check_barcos_hundidos. Comprueba los barcos hundidos del rival. Si el jugador ha conseguido
        hundir un nuevo barco, se actualiza el atributo n_barcos_hundidos del rival (otro_jugador). También
        se muestran mensajes y stats sobre la partida.

        Args:
            otro_jugador (Jugador): El objeto de la clase Jugador del rival.
        """
        #Validar input
        if not isinstance(otro_jugador,Jugador):
            raise TypeError(f"otro_jugador debe ser un objeto de la clase Jugador, pero se proporcionó {type(otro_jugador)}.")
        #Contar barcos hundidos del otro jugador
        n_barcos_hundidos_otro = otro_jugador.contar_barcos_hundidos()
        #Comprobar si he hundido barco del rival
        if n_barcos_hundidos_otro > otro_jugador.n_barcos_hundidos:
            #Actualizar variable del otro jugador
            otro_jugador.n_barcos_hundidos = n_barcos_hundidos_otro
            #Mensaje de barco hundido
            print(f"{self.nombre} hundió un barco de {otro_jugador.nombre}!")
        #Mensajes con stats del contrincante y propios
        print(f"- {self.nombre} ha hundido {otro_jugador.n_barcos_hundidos} barco(s) de {otro_jugador.nombre}!")
        print(f"- {otro_jugador.nombre} ha hundido {self.n_barcos_hundidos} barco(s) de {self.nombre}!\n")
