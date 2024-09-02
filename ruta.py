from collections import deque #Importamos la clase deque para manejar colas
import math #Importamos math para el uso de funciones matematicas
from colorama import Fore, Style, init #Importamos colorama para darle color al camino

init(autoreset=True) # Inicializamos el colorama

# Definimos la funcion para encontrar los caminos
def encontrar_camino(matriz, buscar_camino_largo=False):
    filas, columnas = len(matriz), len(matriz[0])
    
    # Definimos  los movimientos de arriba, abajo, izquierda y derecha
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Buscamos primero las posiciones de inicio en i y fin en f
    inicio = fin = None # Indicamos las posicionesde i y f como no encontradas
    for r in range(filas): # Creamos un bulce anidado para r como fila
        for c in range(columnas): # y para c en columnas
            if matriz[r][c] == 'i': # Verificmaos la posicion (r,c) de i
                inicio = (r, c)  # Guardamos la posicion de i que es el inicio
            elif matriz[r][c] == 'f': # Verificamos la posicion de f
                fin = (r, c)  # Guardamos la posicion de f que es el fin

    # Creamos una cola para realizar la busqueda
    cola = deque([(inicio, [inicio], 0)])  # Estructura de deque es posicion_actual, camino_actual, suma_actual)
    visitados = set()  # Para no visitar la misma posicion dosveces
    mejor_camino = None # Iniciamos variable
    mejor_suma = math.inf  # Empezamos con valor infinito positivo para poder actualziar la variable
    mejor_longitud = -math.inf  # Empezamos con la mejor longitud negativa para poder actualizar la variable

    while cola: # Cremos el bucle principal
        (actual, camino, suma_actual) = cola.popleft() # Extaemos el primer elemento de la cola:
        #La posicion, lista de posiciones ya visitados y la suma total

        if actual == fin: # Si llegamos a la posicion de fin, comprobamos
            if buscar_camino_largo: # Buscamos camino largo
                if len(camino) > mejor_longitud: # Si la longitud actual es mayor que la encontrada, actualizamos
                    mejor_longitud = len(camino)
                    mejor_camino = camino
            else:
                if abs(suma_actual) < abs(mejor_suma): # Si la suma total es menor que la suma encontrada, actualizamos
                    mejor_suma = suma_actual
                    mejor_camino = camino
            continue

        visitados.add(actual) # Marcamos la posicion actual como visitada

        # Exploramos los movimientos posibles
        for movimiento in movimientos: # literamos los posobles caminos
            fila_siguiente, columna_siguiente = actual[0] + movimiento[0], actual[1] + movimiento[1] # Calculamos la posicion de la matriz despuesde del mov
            if 0 <= fila_siguiente < filas and 0 <= columna_siguiente < columnas and (fila_siguiente, columna_siguiente) not in visitados: # Verificamos limites y visitadas
                valor_siguiente = matriz[fila_siguiente][columna_siguiente] # Obtenemos valor en la nueva posicion encontrada
                if valor_siguiente == 'i' or valor_siguiente == 'f': # Definimos valor 0 a "i" y "f" para no afectar sumas
                    valor_siguiente = 0  # Asi los valores de "i" y "f" no afectan la suma
                else:
                    valor_siguiente = int(valor_siguiente)  # Conviertims el valor a entero cuando no es "i" o "f"
                cola.append(((fila_siguiente, columna_siguiente), camino + [(fila_siguiente, columna_siguiente)], suma_actual + valor_siguiente)) #Agregamos posicion del camino y suma
    
    # Devolvemos el mejor camino encontrado y la suma total
    return mejor_camino, mejor_suma if not buscar_camino_largo else mejor_longitud

# Definimos funcion para darle color al camino encontrado
def mostrar_matriz(matriz, camino, color, resaltar_inicio_fin=False):
    for fila in range(len(matriz)):
        fila_str = ""
        for col in range(len(matriz[0])):
            valor = matriz[fila][col]
            if (fila, col) in camino: # Marcamos el camino de color
                fila_str += f"{color}{str(valor):4}{Style.RESET_ALL}"
            else:# Mostramos los numeros normales
                if valor == 'i' or valor == 'f':
                    fila_str += f"{Fore.BLUE}{str(valor):4}{Style.RESET_ALL}" if resaltar_inicio_fin else f"{str(valor):4}"
                else:
                    fila_str += f"{str(valor):4}"
        print(fila_str)
    print()

# Definimos la matriz
matriz = [
    [-3,-3,2,-3,3,-2,-2,1,2,0,2,0,1],
    [2,3,'i',-1,-1,3,2,0,-3,-3,2,2,1],
    [1,-3,-3,2,3,1,3,3,2,1,-2,-2,3],
    [0,0,3,0,3,-3,-2,-3,0,2,2,1,1],
    [2,-1,-1,-3,3,3,0,-3,1,-2,2,0,1],
    [0,3,-1,1,-1,-2,2,-2,2,-1,-2,-3,0],
    [0,3,2,0,1,1,2,3,-1,-3,0,0,-2],
    [3,3,-3,-2,3,-3,-1,-3,3,-2,2,-2,-1],
    [-2,-2,1,0,-1,0,3,0,0,-2,2,-3,-1],
    [-3,3,0,-1,-3,1,2,-3,2,-3,0,2,-2],
    [-3,-3,-3,3,-2,0,-2,-3,1,0,1,-1,-2],
    [-1,0,1,2,1,0,'f',0,-3,3,3,-2,-1],
    [1,-3,1,0,1,2,3,1,-2,3,3,0,3]
]

# Encuentra el mejor camino de 'i' a 'f'
camino_corto, suma_corta = encontrar_camino(matriz)
camino_largo, longitud_larga = encontrar_camino(matriz, buscar_camino_largo=True)

# Imprimimos el camino corto en la matriz
if camino_corto: # Marcamos valores en verde
    matriz_corto = [row[:] for row in matriz]  # Copiamos la matriz original para reusarla
    for (fila, columna) in camino_corto:
        if matriz_corto[fila][columna] not in ['i', 'f']:
            matriz_corto[fila][columna] = str(matriz_corto[fila][columna])

    # Msstramos la matriz con el camino corto en verde
    mostrar_matriz(matriz_corto, camino_corto, Fore.GREEN)
    # Imprimimos el valor total del camino corto
    print(f"Valor total del camino corto es: {suma_corta}\n")

# Imprimimos el camino largo en la matriz
if camino_largo: # Marcamos el camino largo en la matriz en rojo
    matriz_largo = [row[:] for row in matriz]  # Nuevamente copiamos la matriz original para reusarla
    for (fila, columna) in camino_largo:
        if matriz_largo[fila][columna] not in ['i', 'f']:
            matriz_largo[fila][columna] = str(matriz_largo[fila][columna])

    # Mostramos la matriz con el camino largo en rojo
    mostrar_matriz(matriz_largo, camino_largo, Fore.RED)
    # Imprimimos la suma del camino largo
    print(f"Valor total del camino largo es: {longitud_larga}\n")
