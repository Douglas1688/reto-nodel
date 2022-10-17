"""
EL PROBLEMA DE MONTY HALL
Es un problema matemático de probabilidad basado en el concurso televisivo 
estadounidense Trato hecho (Let's Make a Deal). El problema fue planteado y 
resuelto por el matématico Steve Selvin en la revista American Statistician 
en 1975 y posteriormente popularizado por Marilyn vos Savant en Parade Magazine
en 1990. El problema fue bautizado con  el nombre del presentador de dicho concurso.

En este script se simula dicha paradoja ingresando N cantidad de partidas e ingresando
C (cambiar de puerta) o SN (sin cambiar de puerta) se podrá determinar qué la probabilidad
de ganar el juego si cambia de opción.

Luego de realizar la simulación 100K y 1M de veces, quedó demostrado que un participante 
tiene el 66.66% de ganar y el 33.33% de perder si elige cambiar de puerta.

En el script monty_hall_extra.py se analiza qué pasaría si se añade una puerta más y se 
desconoce dónde está el premio.
"""

import random

def generate_doors():
    """ Función que genera una lista representando las puertas y luego aleatoriamente se asigna el premio

    Returns:
        List:   Un arreglo de 3 elementos, representando las puertas.
    """
    doors = ["cabra", "cabra", "auto"]
    random.shuffle(doors)
    return doors

def open_door(player_sel, doors):
    """
    Función que simula a Monty Hall abrir una puerta que esconde una cabra en base a la elección del participante.
    Args:
        player_sel (int): Corresponde al número que haya escogido el participante.
        doors (List): Lista que representa las puertas que va a seleccionar el participante.

    Returns:
        List: Lista modificada con la puerta que Monty Hall abrió.
    """
    open = player_sel
    if doors[player_sel] == "auto":
        open = random.randint(0, 2)
        while open == player_sel:
            open = random.randint(0, 2)
        doors[open] = "open"
    else:
        index = doors.index("auto")
        while open == player_sel or open == index:
            open = random.randint(0, 2)
        doors[open] = "open"
    return doors


def main():
    selection = ['C', 'SN']
    attemps = ""
    options = ""
    # Bucle que valida el ingreso de las opciones C o SN
    while options not in selection:
        try:
            attemps = int(
                input("Ingrese la cantidad de veces a realizar el juego: "))
            options = input(
                "Desea realizar analisis con CAMBIO(C) O SIN CAMBIO(SN): ").upper()
        except Exception as e:
            print(e)

    victories = 0
    defeats = 0

    for _ in range(attemps):
        # Se generan las puertas de manera aleatoria.
        doors = generate_doors()

        # Participante selecciona una puerta
        player_selection = random.randint(0, 2)

        # Monty Hall abre una puerta que contiene una cabra
        doors = open_door(player_selection, doors)

        # Entra por esta opción si se desea saber la probabilidad de ganar si se cambia de puerta.
        if options == "C":
            if player_selection == doors.index("auto"):
                player_selection = doors.index("cabra")
            elif player_selection == doors.index("cabra"):
                player_selection = doors.index("auto")

        # Se incrementa el número de victorias o derrotas.
        if doors[player_selection] == "auto":
            victories = victories + 1
        else:
            defeats = defeats + 1
    print(f"{attemps} intentos")
    print(f"Ganaste {victories} veces.")
    print(f"Perdiste {defeats} veces.")

    print("Porcentaje de victorias: {:.2f}%".format(((victories/attemps)*100)))


if __name__ == "__main__":
    main()
