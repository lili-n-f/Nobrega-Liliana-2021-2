class Room:
    """Clase que representa a los cuartos del juego.
    """
    def __init__(self, name, objects, room_image, left_room = None, right_room = None):
        self.__name = name #nombre del cuarto
        self.__objects = objects #lista de objetos RoomObject del cuarto en cuestión
        self.__room_image = room_image  #str o lista de strings que representan las imágenes del cuarto.
        self.__left_room = left_room   #qué cuarto (si es que hay alguno) tiene a la izquierda
        self.__right_room = right_room  #qué cuarto tiene a la derecha (si es que tiene)


    def __str__(self): #esto permite que cuando se haga print de un objeto de la clase room, se imprima la imagen del cuarto.
        if type(self.__room_image) == str: #la mayoría de los tipos de cuartos tienen sólo una imagen (y por tanto el atributo room_image es un string) que es la que se imprime en todo momento 
            return self.__room_image
        else: #sin embargo, para el corredor del laboratorio, se tienen dos imágenes, por lo que el atributo room_image es una lista de dos strings (cada uno, una imagen).
            if self.get_objects()[0].get_is_cleared(): #si el juego del objeto del corredor (es decir la puerta) ya fue ganado y por tanto la puerta está "cleared", se imprime la imagen de la puerta abierta, de lo contrario se imprime la puerta cerrada
                return self.__room_image[1]
            else:
                return self.__room_image[0]

    #getters (métodos que devuelven el valor de un atributo)
    def get_name(self):
        return self.__name

    def get_objects(self):
        return self.__objects
 
    def get_left_room(self):
        return self.__left_room

    def get_right_room(self):
        return self.__right_room

    #setters para cambiar el valor de un atributo (como no es necesario cambiar el nombre o los objetos de un cuarto después de instanciar esta clase, no se hacen setters de éstos.)
    def set_left_room(self, left_room):
        self.__left_room = left_room
    
    def set_right_room(self, right_room):
        self.__right_room = right_room 
