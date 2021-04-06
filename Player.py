import time
from GameOverException import GameOverException

class Player:
    """Clase que guarda los datos de un jugador.
    """
    def __init__(self, username, password, age, avatar):
        self.__username = username
        self.__password = password
        self.__age = age #edad del usuario
        self.__avatar = avatar #nombre del avatar usado por el jugador en una partida
        self.__max_time = 0.0 #momento en el que debería terminar el tiempo de juego del jugador en una partida
        self.__game_info = [] #lista que guarda diccionarios que contiene la información de cada partida jugada (tiempo jugado, dificultad y si ganó o perdió)
        self.__game_difficulty = '' #dificultad de la partida que juega el usuario
        self.__lives = 0 #cantidad de vidas del jugador en una partida
        self.__clues = 0 #cantidad de pistas que el jugador puede pedir en una partida
        self.__inventory = [] #lista en la que se guardan los objetos ganados en cada partida
        self.__rooms_visited = {} #diccionario que guarda la información de cuántas veces se ha visitado cada cuarto en el juego
        self.__current_room = None #guarda en qué cuarto se encuentra el jugador en el juego

    #getters para obtener el valor de un atributo determinado
    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password
    
    def get_age(self):
        return self.__age

    def get_avatar(self):
        return self.__avatar

    def get_game_info(self):
        return self.__game_info

    def get_lives(self):
        return self.__lives
    
    def get_clues(self):
        return self.__clues

    def get_max_time(self):
        return self.__max_time

    def get_time_left(self): #en este caso, time left no es un atributo, es el tiempo que le queda al usuario en una partida
        return round(self.get_max_time() - time.time(), 2) #el tiempo máximo menos el tiempo actual nos dice cuánto tiempo le queda al jugador

    def get_inventory(self):
        return self.__inventory

    def get_rooms_visited(self):
        return self.__rooms_visited

    def get_current_room(self):
        return self.__current_room

    #setters para editar el valor de un atributo específico
    def set_max_time(self, time):
        self.__max_time = time
 
    def set_avatar(self, new_avatar):
        self.__avatar = new_avatar

    def set_lives_and_clues(self, live_number, clue_number): #como las vidas y pistas se 'settean' a la vez antes de comenzar un juego, sólo hay un método en vez de uno por cada uno
        self.__lives = live_number
        self.__clues = clue_number

    def set_game_difficulty(self, game_difficulty): #nos permite determinar a qué dificultad está jugando la partida el jugador
        self.__game_difficulty = game_difficulty

    #métodos diversos
    def visit_room(self, room):
        """Método que guarda que el jugador visitó un cuarto una vez más y actualiza el valor de current room al nuevo cuarto.

        Args:
            room (Room): cuarto que se visita.
        """
        #esto nos indica que visitó un determinado cuarto, que se pasa como parámetro, una vez más
        self.__rooms_visited[room.get_name()] = self.__rooms_visited.get(room.get_name(), 0) + 1 #si aún no ha visitado el cuarto, se le da como valor 0 y luego se le suma 1. si sí lo ha visitado, a la cantidad de veces que se ha visitado el cuarto se le suma 1
        self.__current_room = room #esto nos permite saber en qué cuarto está el jugador en todo momento del juego

    def lose_lives(self, number):
        """Método que hace que el usuario pierda un número determinado de vidas si se equivoca en un juego, por ejemplo.

        Args:
            number (float or int): número de vidas que se pierden.

        Raises:
            GameOverException: si el usuario ya no tiene un número positivo de vidas, pierde.
        """
        self.__lives -= number
        if self.__lives <= 0: #si al perder vidas resulta que el número de vidas es menor o igual a 0, el jugador ha perdido y se hace un raise GameOverException (se pone menor o igual a cero porque como en distintos juegos se resta una distinta cantidad de vidas, pueden descuadrarse los números y puede quedar con un número negativo de vidas como -0.25)
            raise GameOverException
    
    def gain_lives(self, number):
        """Método que permite al usuario ganar vidas.

        Args:
            number (float or int): número de vidas que se ganan.
        """
        self.__lives += number

    def use_clue(self):
        """Método que gasta una pista (resta al número de pistas disponible en una partida 1).
        """
        self.__clues -= 1

    def add_item_to_inventory(self, item):
        """Método que agrega al inventario del jugador un objeto.

        Args:
            item (str): objeto que se agrega al inventario.
        """
        self.__inventory.append(item)

    def use_item_from_inventory(self, item):
        """Método que se llama cuando se usa un objeto en un mini-juego. Imprime que se usó y se borra del inventario.

        Args:
            item (str): ítem a usar.
        """
        self.__inventory.remove(item)
        print(f"\nSe usó el siguiente objeto del inventario: {item.capitalize()}\n")
    
    def reset_inventory(self):
        """Método para resetear (vaciar) el inventario al inicio de cada partida para que no le queden al jugador objetos de partidas pasadas en el inventario.
        """
        self.__inventory = []
 
    def add_game_info(self, time_played, win):
        """Método para añadir la información de una nueva partida a la lista game_info.

        Args:
            time_played (float): número de segundos jugados en una partida.
            win (bool): True si ganó la partida, False en lo contrario.
        """
        self.__game_info.append({'time': time_played, 'difficulty': self.__game_difficulty, 'win': win})

    def get_best_times_per_difficulty(self, difficulty):
        """Método para obtener los mejores tiempos (ordenados de menor a mayor) que ha realizado en partidas ganadas un jugador, según la dificultad de la partida.

        Args:
            difficulty (str): dificultad determinada del que se busca los mejores tiempos ('f' si es fácil, 'm' si es medio, 'd' si es difícil).

        Returns:
            list: si tiene mejores tiempos para una determinada dificultad
            None: si no ha ganado una partida en esa dificultad.
        """
        best_times_in_order = sorted([game['time'] for game in self.get_game_info() if game['difficulty'] == difficulty and game['win'] == True])
        if best_times_in_order:
            return best_times_in_order
        else:
            return None
