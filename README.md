# 🎮 Juego Hundir La Flota / Proyecto HLF

## 📋 Índice

- [**Descripción**](#ℹ️-descripción)
- [**Características**](#-características)
- [**Tecnologías y Prerrequisitos**](#️-tecnologías-y-prerrequisitos)
- [**Instalación y Ejecución**](#-instalación-y-ejecución)

## ℹ️ Descripción

Proyecto individual HLF para el Curso de Data Science - The Bridge y Fundación Universia (2026-09). En este proyecto hemos creado nuestra propia versión del clásico juego **Hundir La Flota** en Python.

## 🚀 Características

El programa presenta dos modos de juego:

- **Modo de Juego contra Máquina**. En este caso, el jugador se enfrentará a una máquina que hace disparos de forma aleatoria.

- **Modo de Juego para 2 Jugadores**. En este caso, dos jugadores pueden enfrentarse mediante un sistema que va alternando el turno entre ambos jugadores.

En cualquier caso, el programa generará de forma aleatoria un total de 6 barcos por jugador (3 barcos de tamaño 2, 2 barcos de tamaño 3 y 1 barco de tamaño 4) y los posicionará en el tablero correspondiente.

## 🛠️ Tecnologías y Prerrequisitos

- **Lenguaje:** Python
Este proyecto está desarrollado en **Python 3.12.10**. El juego utiliza varias librerías integradas en la biblioteca estándar de Python, por lo que **no requieren instalación adicional**:
   * `os` (Interacción con el sistema)
   * `subprocess` (Gestión de procesos del sistema)
   * `random` (Generación de mecánicas aleatorias)
   * `itertools` (Optimización de iteradores)

- **Librerías Externas:** 
Para que el proyecto funcione correctamente, es necesario instalar las siguientes librerías de terceros:
   * `NumPy` (Para el manejo eficiente de matrices y cálculos del juego)

Puedes instalarla automáticamente ejecutando el siguiente comando en tu terminal:
```bash
pip install numpy
```

## 💻 Instalación y Ejecución

1. Clona el repositorio:
```bash
git clone https://github.com/sarpiens/HLF_Project.git
```
2. Instala las dependencias:
```bash
pip install -r requirements.txt
```
3. Ejecuta el juego:
```bash
python3 main.py
```
