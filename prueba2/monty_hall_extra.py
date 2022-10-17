"""
PROBLEMA MONTY HALL EXTENDIDO  A 4 PUERTAS Y SIN CONOCER DÓNDE ESTÉ EL PREMIO
En este script se analiza qué pasaría si se agrega una puerta más (sin premio) al problema original y que el presentador no sepa en qué puerta está el premio. 
"""

import random
from random import choice


def generate_doors():
    """ Función que genera una lista representando las puertas y luego aleatoriamente se asigna el premio

    Returns:
        List:   Un arreglo de 3 elementos, representando las puertas.
    """
    doors = ["cabra", "cabra", "auto", "cabra"]
    random.shuffle(doors)
    return doors


def open_door(monty_sel, doors):
    """
    Función que simula a Monty Hall abrir 2 puertas sin saber dónde está el premio.
    Args:
        monty_sel (List): Corresponde los 2 números de puertas que ha seleccionado Monty Hall.
        doors (List): Lista que representa las puertas generadas anteriormente.

    Returns:
        List: Lista modificada con la puerta que Monty Hall abrió.
    """
    doors[monty_sel[0]] = "open"
    doors[monty_sel[1]] = "open"
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

    for i in range(attemps):
        lista_excluidos = []
        numero_monty = []

        # Se generan las 4 puertas de manera aleatoria.
        doors = generate_doors()

        # Participante selecciona una puerta
        player_selection = random.randint(0, 3)
        # En lista_excluidos se almacena los números seleccionados por el participante y por Monty Hall para no sean escogidos nuevamente.
        lista_excluidos.append(player_selection)
        while len(lista_excluidos) < 3:
            elem = choice([i for i in range(0, 4) if i not in lista_excluidos])
            # En numero_monty se almacenan los números seleccionados aleatoriamente por Monty Hall.
            numero_monty.append(elem)
            lista_excluidos.append(elem)

        # Monty Hall abre udos puertas seleccionadas al azar.
        doors = open_door(numero_monty, doors)

        # Si las puertas abiertas no contienen el auto y además ha escogido cambiar, entraría por esta opción, caso contrario pierde el juego.
        if "auto" in doors and options == "C":
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
