#!/usr/bin/env python3

def generarTablero() -> list:
    tablero = []

    cantidadDeFilas = 0
    while cantidadDeFilas != 8:
        tablero.append([" "] * 8)
        cantidadDeFilas += 1

    tablero[3][3] = "B"
    tablero[3][4] = "N"
    tablero[4][3] = "N"
    tablero[4][4] = "B"

    return tablero

def colorDeFicha(tablero: list, pos: list) -> str:
    return tablero[pos[0]][pos[1]]

def casillaVacia(tablero: list, pos: list) -> bool:
    return colorDeFicha(tablero, pos) == " "

def traducirPosicion(pos: str) -> list:
    dictLetras = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7}
    return [int(pos[1])-1, dictLetras[pos[0]]]

def resPos(pos1: list, pos2: list) -> list:
    return [pos1[0]-pos2[0], pos1[1]-pos2[1]]

def sumPos(pos1: list, pos2: list) -> list:
    return [pos1[0]+pos2[0], pos1[1]+pos2[1]]

def enTablero(pos: str) -> bool:
    letras = {"A","B","C","D","E","F","G","H"}

    # Revisa que el segundo carácter sea valido intentando convertirlo a un int,
    # en caso de falla, no es una posición que exista dentro del tablero, siendo
    # que el segundo carácter de la posición debe ser un numero entero

    try:
        int(pos[1])
    except:
        return False

    return (pos[0] in letras) and (1 <= int(pos[1]) <= 8)

def posNumericaEnTablero(pos: list) -> bool:
    return (0 <= pos[0] <= 7) and (0 <= pos[1] <= 7)

def posicionesAlrededor(pos: list) -> list:
    posiciones = []

    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            # Se revisa que x e y no sean 0 siendo que en este caso nos estaría
            # dando la misma posición que ingresamos
            if posNumericaEnTablero(sumPos(pos, (x, y))) and not (x == 0 and y == 0):
                posiciones.append(sumPos(pos, (x, y)))

    return posiciones

def fichasParaVoltear(tablero: list, pos: list, color: str) -> list:
    posiciones = []

    # Revisa si la casilla donde se intenta poner la ficha esta vacía, en caso
    # de que no lo estuviera no existen jugadas posibles siendo que no se puede
    # poner la ficha en una posición ya ocupada por otra ficha

    if not casillaVacia(tablero, pos):
        return []

    # Revisa las posiciones alrededor de la ficha y solo revisa si hay un
    # flanqueo posible en las direcciones donde las fichas tengan un color
    # opuesto al de la ficha que esta realizando la jugada

    for fichaPosible in posicionesAlrededor(pos):
         if colorDeFicha(tablero, fichaPosible) == colorContrario(color):
            # Se determina hacia donde debería avanzar la búsqueda y se guardan
            # la ficha de donde partimos y la ficha primer ficha del color
            # opuesto que ya encontramos previamente
            tendencia = resPos(fichaPosible, pos) # Indica la dirección hacia donde tenemos que avanzar
            posibleRecta = []
            nuevaPos = fichaPosible
            posibleRecta.append(pos) # Se guarda la posición de la ficha que ingresamos
            posibleRecta.append(nuevaPos) # Se guarda la ficha aledaña que encontramos del color opuesto

            # Avanzar hasta encontrar un elemento de nuestro color o un espacio en blanco
            while colorDeFicha(tablero, nuevaPos) == colorContrario(color) and posNumericaEnTablero(sumPos(nuevaPos, tendencia)):
                nuevaPos = sumPos(nuevaPos, tendencia)
                posibleRecta.append(nuevaPos)

            # Si el ultimo elemento que encontramos es de nuestro color, es una
            # posición valida, caso contrario de si es un espacio en blanco se descarta la posición
            if colorDeFicha(tablero, nuevaPos) == color:
                for i in posibleRecta:
                    posiciones.append(i)

    return posiciones

def ponerFicha(tablero: list, pos: list, color: str) -> list:
    tablero[pos[0]][pos[1]] = color
    return tablero

def colorContrario(colorOriginal: str) -> str:
    colores = {"N":"B","B":"N"}
    return colores[colorOriginal]

def pisarLista(listaAnidada: list) -> list:
    listaPlana = []
    for elemento in listaAnidada:
        if type(elemento) == list or type(elemento) == tuple:
            for items in elemento:
                listaPlana.append(items)
        else:
            listaPlana.append(elemento)

    return listaPlana

def obtenerArchivo() -> str:
    archivo = input("Ingrese la dirección del archivo: ")
    nombreValido = False

    while not nombreValido:
        try:
            if open(archivo,"r"):
                nombreValido = True
        except:
            archivo = input("Dirección invalida, ingrese nuevamente la dirección del archivo: ")

    return archivo

def main() -> None:
    # Se generan los valores iniciales para el juego
    archivo = open(obtenerArchivo(),"r")
    tablero = generarTablero()
    error = False

    # Obtiene los valores sobre el nombre de los jugadores y su color, ademas
    # del color inicial de la partida

    primerJugador = archivo.readline().strip()
    segundoJugador = archivo.readline().strip()
    colorJugada = archivo.readline().strip()

    nombresJugadores = [primerJugador[:-2], segundoJugador[:-2]]
    colorJugadores = [primerJugador[-1:], segundoJugador[-1:]]

    # Comienza a leer la primera linea de jugadas en el archivo
    nuevaLinea = archivo.readline()
    numeroDeLinea = 3 # Las 3 primeras lineas son de los jugadores y color inicial, por lo que nuestro contador parte del 3

    while nuevaLinea != "" and not error:
        # Elimina caracteres innecesarios como espacios o \n
        posOriginal = nuevaLinea.strip()

        # Previene leer EOF o espacios en blanco, los cuales se tienen que saltar
        if len(posOriginal) == 2 and enTablero(posOriginal):
            posTraducida = traducirPosicion(posOriginal)

            # Revisa si existen flanqueos posibles, en caso de que no existan se
            # genera un error para indicar en que linea sucede
            flanqueos = fichasParaVoltear(tablero, posTraducida, colorJugada)
            if flanqueos != []:
                for ficha in flanqueos:
                    tablero = ponerFicha(tablero, ficha, colorJugada)
            else:
                error = True

        # Revisa si el string es vacío o tiene espacios, si no cumple con esto
        # da un error, esto funciona siendo que un string vacío devuelve el
        # valor False y como ya utilizamos la función strip() anteriormente si
        # el string es puramente espacios nos va a devolver un string vacío

        elif posOriginal:
            error = True

        # Avanzar a la nueva linea
        nuevaLinea = archivo.readline()
        colorJugada = colorContrario(colorJugada)
        numeroDeLinea += 1

    # Mostrar el tablero ,de una forma visual una vez que ya se termino de
    # interpretar la partida
    print("\n\033[48;5;16m      A   B   C   D   E   F   G   H      \033[0m")
    print("\033[48;5;16m   \u001b[48;5;34m", "+---"*8+"+","\033[48;5;16m   \u001b[0m")

    for x, y in enumerate(tablero):
        print("\033[48;5;16m", x+1, "\033[0m", end="")
        for i in y:
            if i == "B":
                print("\u001b[48;5;34m","| "+"\u001b[97m"+"■"+"\033[0m", end="")
            elif i == "N":
                print("\u001b[48;5;34m","| "+"\u001b[30m"+"■"+"\033[0m", end="")
            else:
                print("\u001b[48;5;34m","| "+i, end="")
        print("\033[48;5;34m | \033[48;5;16m", x+1, "\033[0m")
        print("\033[48;5;16m   \u001b[48;5;34m", "+---"*8+"+","\033[48;5;16m   \u001b[0m")

    print("\033[48;5;16m      A   B   C   D   E   F   G   H      \033[0m")

    # Obtener el puntaje basándose en la cantidad de fichas de cada color en el tablero
    tableroPisado = pisarLista(tablero)
    puntajeJugadores = [tableroPisado.count(colorJugadores[0]), tableroPisado.count(colorJugadores[1])]

    # Muestra el nombre de cada jugador junto a su cantidad de fichas
    print("\n \u001b[34mPuntajes:\u001b[0m\n ",
            "•",nombresJugadores[0]+":", puntajeJugadores[0],"\n ",
            "•",nombresJugadores[1]+":", puntajeJugadores[1])

    # En caso de error, se muestra cual es la linea que genera el error, sino se muestra el ganador
    # de la partida o empate si fuera el caso
    if error:
        print("\n\u001b[31m [x] Error:\u001b[0m Posicion invalida en linea", numeroDeLinea)
    elif puntajeJugadores[0] == puntajeJugadores[1]:
        print("\n\u001b[32m [✓] Partida valida:\u001b[0m es un empate\n")
    elif puntajeJugadores[0] > puntajeJugadores[1]:
        print("\n\u001b[32m [✓] Partida valida:\u001b[0m", nombresJugadores[0], "es el ganador \n")
    else:
        print("\n\u001b[32m [✓] Partida valida:\u001b[0m", nombresJugadores[1], "es el ganador \n")

    archivo.close()

if __name__ == '__main__':
   main()
