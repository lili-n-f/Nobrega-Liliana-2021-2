class RoomObject:
    """Clase asociada a cada objeto que se encuentra en un cuarto del juego.
    """
    def __init__(self, name, position, images, game):
        self.__name = name
        self.__position = position 
        self.__images = images
        self.__game = game
        self.__is_cleared = False
    
    def __str__(self): #permite que, cuando se imprima un objeto de la clase RoomObject se muestre una imagen determinada
        if self.get_is_cleared(): #si el juego ya se ganó y por tanto el objeto está 'clear', muestra la imagen de que ya fue jugado (segunda imagen guardada en lista images), de lo contrario se imprime la imagen inicial de que no fue ganado aún
            return self.__images[1]
        else:
            return self.__images[0]

    #getters para obtener el valor de determinados atributos
    def get_name(self):
        return self.__name
 
    def get_game(self):
        return self.__game

    def get_is_cleared(self):
        if self.get_game().won: #si el juego asociado al objeto se ha ganado ya (el atributo won del juego devuelve True si ya se ganó el juego y False si no)
            self.__is_cleared = True
        return self.__is_cleared

        

    