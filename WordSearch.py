#Clase adaptada de https://github.com/mast3rsoft/WordSearch para su uso en la creación de la sopa de letras (atributo grid de clase LetterSoup) en el juego LetterSoup

import random
class WordSearch():
    """Clase que genera una sopa de letras aleatoria (de dimensiones 15x15 si no se especifica cuáles son) a partir de una lista de palabras.
    """
    horizontal = 0 #estos valores son los que representan a cada dirección: si para una palabra se escogiera el número aleatorio 0, se estaría escogiendo que su dirección sea horizontal, por ejemplo
    vertical = 1
    diagonal = 2
    reverse_horizontal = 3
    reverse_vertical = 4
    reverse_diagonal = 5
    reverse_flip_diagonal = 6
    flip_diagonal = 7
    invalid_value = -100
    def __init__(self, search_words, max_x = 15, max_y = 15):
        self.max_x = max_x #número de letras que aparecen en cada fila
        self.max_y = max_y #número de filas que hay. en este caso los valores 'default' de max_x y max_y son ambos 15 (ya que en las instrucciones se pide que sea una sopa de letras de 15x15)
        self.grid = [] # grid será una lista de listas de strings (letras)
        self.search_words = search_words  #search_words es una lista de strings (de palabras)
        for row in range(0, self.max_y):
            self.grid.append([])
            for column in range(0, self.max_x):
                self.grid[row].append('*') #se crea inicialmente la lista de listas grid con '*' en lugar de letras
        for word in search_words:
            direction = random.randint(0, 7) #por cada palabra se escoge una posición aleatoria
            while not self.add_word_to_grid(word, self.invalid_value , self.invalid_value , direction): #si el método devuelve False se entra a este loop
                pass
        self.fill_rest_of_grid() #cuando se haya colocado cada palabra en el grid, se llama a esta función que rellena el resto de los espacios vacíos (que siguen siendo '*') con una letra aleatoria en el alfabeto inglés
    
    def add_word_to_grid(self, word, x, y, direction):
        if len(word) == 0:
            return True
        # word tiene un largo > 0
        # se valida si hay que escoger una posición aleatoria (es decir, si su posición en x o en y sigue siendo el valor que devuelve self.invalid_value (-100, que es una coordenada imposible en este caso), es decir chequea si es la primera vez que se llama a esta función para una palabra)
        if x == self.invalid_value or y == self.invalid_value: 
            while True:
                y = random.randint(0, self.max_y - 1) #de 0 a self.max_y-1 (y en la siguiente línea self.max_x) porque en las listas se empieza a contar desde 0 
                x = random.randint(0, self.max_x - 1)
                if self.grid[y][x] == '*': #esto significa que la posición no ha sido tomada por otra palabra porque en el grid sigue habiendo un '*' en lugar de una letra y por tanto no se tiene que escoger otra posición aleatoria 
                    break
        # valida si x y y son válidos  
        if x == self.max_x or x < 0:
            return False
        if y == self.max_y or y < 0:
            return False          
        if not (self.grid[y][x] == "*" or self.grid[y][x] == word[0]): #si la posición no está libre (no es '*') o si ya se colocó una letra distinta a la que se quiere colocar en ese espacio 
            return False
        undo_value = self.grid[y][x]  #estos 'undos' sirven por si al intentar colocar una letra de word en el grid no funciona (de este modo, se puede devolver el grid a lo que solía ser originalmente antes de intentar esto)
        undo_x = x
        undo_y = y 
        self.grid[y][x] = word[0] #se pone la primera letra en la posición escogida
        # se escribe el resto de la palabra (cambiando en x o y dependiendo de la dirección aleatoria que se escogió para la palabra)
        if direction == self.horizontal:
            x += 1
        elif direction == self.vertical:
            y += 1
        elif direction == self.diagonal:
            y += 1
            x += 1
        elif direction == self.reverse_horizontal:
            x -= 1
        elif direction == self.reverse_vertical:
            y -= 1
        elif direction == self.reverse_diagonal:
            y -= 1
            x -= 1
        elif direction == self.flip_diagonal:
            x += 1
            y -= 1 
        elif direction == self.reverse_flip_diagonal:
            x -= 1
            y += 1             
        if self.add_word_to_grid(word[1:], x, y, direction):
            # si el resto de la palabra se logra colocar en posición dentro del grid, se retorna True (si toda la palabra se logró colocar, al final se devolvería True y se saldría del loop de while not self.add_word_to_grid(word, self.invalid_value , self.invalid_value , direction) dentro de __init__)
            return True
        else:
            # si al intentar colocar el resto de la palabra no funcionó algo, se hace undo para devolver el grid a lo que era originalmente y se retorna False porque aún no se ha terminado de colocar la palabra de manera válida en el grid, por lo que volverá a intentar
            y = undo_y
            x = undo_x
            self.grid[y][x] = undo_value
            return False       
    
    def fill_rest_of_grid(self):
        for row in self.grid:
            for i in range(len(row)):
                if row[i] == '*':
                    row[i] = 'abcdefghijklmnopqrstuvwxyz'[random.randint(0,25)] #se escoge una letra aleatoria del alfabeto inglés para rellenar el resto de los espacios que quedaron vacíos (siguen siendo '*' después de haber colocado todas las palabras en el grid de la sopa de letras)