import pickle
import os
from Player import Player
    
def register_player(players):
    """Función de registro de jugador: pide nombre de usuario, contraseña, edad, llama a la función para obtener el avatar que usará en la partida 
    y guarda los datos del nuevo jugador al archivo registered_players.txt llamando a la función indicada.

    Args:
        players (dict): diccionario de jugadores ya registrados. Tiene como llaves los nombres de usuario de cada uno y como valores las instancias de la clase Player asociados a cada jugador.


    Raises:
        Exception: si la edad ingresada fue menor o igual a cero (edades inválidas).

    Returns:
        player (Player): intancia de la clase Player asociado al jugador que se acaba de registrar.
    """

    print("\n", "REGISTRO".center(120, "-"))
    
    
    print("\n", "NOMBRE DE USUARIO".center(120, "-"), "\nPodrá tener caracteres alfanuméricos y una longitud máxima de 30 caracteres. \nTu nombre de usuario debe ser ÚNICO: si ya fue registrado, deberás ingresar otro.")
    while True: #loop infinito para realizar la validación del nombre de usuario (una vez se ingrese un nombre válido, se sale del loop)
    
        username = input("Ingresa el nombre de usuario que quieras usar (no podrás cambiarlo después):\n>")
        
        if not (username.isalnum()) or len(username) > 30:
            print("ERROR: Nombre de usuario inválido.\n")
        
        elif username in players:
            print(f"El nombre de usuario '{username}' ya fue tomado.\n")
            
        else:
            print("Nombre de usuario válido. ✔️")
            break


    print("\n", "CONTRASEÑA".center(120, "-"), "\nDeberá tener entre 8 y 30 caracteres. No está permitido el uso de espacios.")
    while True: #loop para validación de la contraseña
        password = input("Ingresa la contraseña a utilizar (no podrás cambiarla después):\n>")

        if password.count(" ") != 0 or not (8 <= len(password) <= 30):
            print("ERROR: contraseña inválida.\n")
        else:
            print("Contraseña válida. ✔️")
            break


    print("\n", "EDAD".center(120, "-"), "\nDebes ingresar tu edad como un número natural.")
    while True:
        try:
            age = int(input("Ingresa tu edad:\n>"))
            if age <= 0:
                raise Exception
            print("Edad válida. ✔️")
            break
        except:
            print("ERROR: edad inválida.\n")                
    
    avatar = ask_for_avatar()

    print("\n✔️¡Jugador registrado exitosamente!✔️")

    player = Player(username, password, age, avatar)
    players[username] = player 
    
    load_data_to_txt('registered_players.txt', players)
    return player
        
def ask_for_avatar():
    """Función que pregunta al usuario qué avatar quiere usar. Se le pregunta esto al usuario antes de empezar cada partida.

    Raises:
        Exception: si el usuario colocó un número fuera de range(1,6) (opción inválida para los avatares).

    Returns:
        str: nombre del avatar escogido
    """
    
    print("\n", "AVATAR".center(120, "-"), "\nPara esta partida podrás escoger entre...\n\t1. Benjamín Scharifker 🏫🎓\n\t2. Eugenio Mendoza 🕴️\n\t3. Pelusa 😻\n\t4. Gandhi 👤☮️\n\t5. ✨Estudiante Estresad@✨")
    while True:
        try:
            avatar = int(input("\nIngresa el número del avatar que deseas usar:\n>"))

            if avatar in range(1,6):

                print("Avatar escogido exitosamente. ✔️")

                if avatar == 1:
                    return 'Benjamín Scharifker'

                elif avatar == 2:
                    return 'Eugenio Mendoza'

                elif avatar == 3:
                    return 'Pelusa'

                elif avatar == 4:
                    return 'Gandhi'

                elif avatar == 5:
                    return 'Estudiante Estresad@'

            else:
                raise Exception

        except:
            print("ERROR: opción inválida.")
        
def get_data_from_txt(file_name, data):
    """Función para obtener los datos serializados de un archivo txt.

    Args:
        file_name (str): nombre del archivo txt donde conseguir los datos.
        data (dict): datos a actualizar con los datos que se encuentran en el archivo.

    Returns:
        dict: datos obtenidos del archivo.
    """

    while True:
            
        try:    
            
            read_binary = open(file_name, 'rb')
            if os.stat(file_name).st_size != 0: #chequea si hay algún dato registrado que leer (es decir, si su 'size' es distinto a 0)
                data = pickle.load(read_binary)
            read_binary.close()
            del read_binary
            return data
        
        except FileNotFoundError: #si el file no existe, se crea. y como se está en un loop, se vuelve nuevamente a intentar la operación de lectura.
            file = open(file_name, 'w')
            file.close()
            del file

def load_data_to_txt(file_name, data):
    """Función para cargar datos a un archivo txt mediante serialización.

    Args:
        file_name (str): nombre del archivo txt donde cargar los datos.
        data (dict): datos a cargar.
    """

    write_binary = open(file_name, 'wb')
    data = pickle.dump(data, write_binary)
    write_binary.close()
    del write_binary
    del data

def sign_in(players):
    """Función que permite que un usuario, si tiene una cuenta, ingrese a ella a partir de su nombre de usuario y contraseña.

    Args:
        players (dict): diccionario de jugadores ya registrados. Tiene como llaves los nombres de usuario de cada uno y como valores las instancias de la clase Player asociados a cada jugador.

    Returns:
        Player: si se ingresa correctamente a una cuenta (nombre de usuario y contraseña correcta) o si es necesario registrarse (ya que la función register_player también retorna una instancia de Player)
    """
    while True:
        username = input("Nombre de usuario:\n>")
        password = input("Contraseña:\n>")
        if username in players and password == players[username].get_password():
            print("\n✔️¡Ingreso exitoso!✔️")
            avatar = ask_for_avatar()
            players[username].set_avatar(avatar)
            players[username].reset_inventory()
            return players[username]
        else:
            print("ERROR: nombre de usuario o contraseña errada.")
            if input("\n¿Quieres intentar otra vez? [S] = sí, cualquier otro caracter = no, quiero registrarme\n>").lower() != 's':
                return register_player(players)