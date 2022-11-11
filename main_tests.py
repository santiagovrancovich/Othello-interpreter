import pytest
from main import *

def test_generarTablero():
    assert generarTablero() == [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', 'B', 'N', ' ', ' ', ' '],
                                [' ', ' ', ' ', 'N', 'B', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

def test_casillaVacia():
    assert casillaVacia(generarTablero(), [2,2]) == True
    assert casillaVacia(generarTablero(), [3,3]) == False
    assert casillaVacia(generarTablero(), [0,7]) == True
    assert casillaVacia(generarTablero(), [4,3]) == False

def test_colorDeFicha():
    assert colorDeFicha(generarTablero(), [3,3]) == "B"
    assert colorDeFicha(generarTablero(), [3,4]) == "N"
    assert colorDeFicha(generarTablero(), [4,4]) == "B"
    assert colorDeFicha(generarTablero(), [0,0]) == " "

def test_traducirPosicion():
    assert traducirPosicion("A3") == [2, 0]
    assert traducirPosicion("H1") == [0, 7]
    assert traducirPosicion("E6") == [5, 4]
    assert traducirPosicion("C4") == [3, 2]

def test_resPos():
    assert resPos([4,4], [3,3]) == [1,1]
    assert resPos([5,2], [3,4]) == [2,-2]
    assert resPos([0,0], [2,2]) == [-2,-2]
    assert resPos([2,2], [0,0]) == [2,2]

def test_sumPos():
    assert sumPos([4,4], [3,3]) == [7,7]
    assert sumPos([2,3], [4,5]) == [6,8]
    assert sumPos([0,0], [2,2]) == [2,2]
    assert sumPos([2,2], [0,0]) == [2,2]

def test_enTablero():
    assert enTablero("ZZ") == False
    assert enTablero("I3") == False
    assert enTablero("A9") == False
    assert enTablero("89") == False
    assert enTablero("AH") == False
    assert enTablero("C5") == True

def test_posicionesAlrededor():
    assert posicionesAlrededor([0, 0]) == [[0, 1], [1, 0], [1, 1]]
    assert posicionesAlrededor([0, 7]) == [[0, 6], [1, 6], [1, 7]]
    assert posicionesAlrededor([0, 5]) == [[0, 4], [0, 6], [1, 4], [1, 5], [1, 6]]
    assert posicionesAlrededor([2, 2]) == [[1, 1], [1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2], [3, 3]]

def test_posNumericaEnTablero():
    assert posNumericaEnTablero([-1,9]) == False
    assert posNumericaEnTablero([2,5]) == True
    assert posNumericaEnTablero([10,5]) == False
    assert posNumericaEnTablero([-2,-5]) == False

def test_fichasParaVoltear():
    assert fichasParaVoltear(generarTablero(), [3,2], "N") == [[3, 2], [3, 3], [3, 4]]
    assert fichasParaVoltear(generarTablero(), [3,2], "B") == []
    assert fichasParaVoltear(generarTablero(), [4,2], "B") == [[4,2], [4,3], [4,4]]
    assert fichasParaVoltear(generarTablero(), [4,2], "N") == []
    assert fichasParaVoltear(generarTablero(), [1,1], "B") == []

def test_ponerFicha():
    tablero = generarTablero()
    tablero[4][4] = "N"

    assert ponerFicha(generarTablero(), [4,4], "N") == tablero

def test_colorContrario():
    assert colorContrario("N") == "B"
    assert colorContrario("B") == "N"

def test_pisarLista():
    assert pisarLista([["a","b","c"], ["d","e"]]) == ["a","b","c","d","e"]
    assert pisarLista([["a","b","c"], ["d","e"], "fg"]) == ["a","b","c","d","e","fg"]
    assert pisarLista([1,2,3,4,5]) == [1,2,3,4,5]

