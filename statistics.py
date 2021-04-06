#no me funcionó nunca matplotlib para ver los gráficos en mi computadora
#import matplotlib.pyplot as plt

#no vi que fuera necesario usar un archivo de texto para las estadísticas: todos los datos ya se guardan con los objetos players en registered_players.txt
def game_statistics(players):
    """Genera y muestra los datos estadísticos acerca de los jugadores en el juego: 
    el Leaderboard (llama a una función leaderboard encargada de la generación de este top 5 por cada nivel de dificultad),  
    los cuartos más visitados por cada jugador y los usuarios que más juegan (ordenados de más partidas a menos partidas).

    Args:
        players (dict): diccionario que contiene la información de cada jugador, en el que los keys son el nombre de usuario de cada uno y los values el objeto de clase Player con la información de juego de cada jugador registrado.
    """
    if players: #chequea si hay algún jugador del que imprimir la info    
        
        print("\n", "LEADERBOARD".center(120, "-"))
        leaderboard(players, 'f')
        input("\n\nPresiona 'enter' para continuar\n▶️ ")
        leaderboard(players, 'm')
        input("\n\n▶️ ")
        leaderboard(players, 'd')
        input("\n\n▶️ ")

        print("\n", "CUARTOS MÁS VISITADOS POR JUGADOR".center(120, "-"), "\n")
    
        for player in players.values(): #.values() ya que players es un diccionario con llave el username del jugador y valor el objeto player asociado a dicho jugador.
            print(f"JUGADOR:\t{player.get_username()}")
            if player.get_rooms_visited(): #chequea si ha visitado algún cuarto alguna vez (es decir, el diccionario que devuelve el método es no vacío)
                rooms = list(player.get_rooms_visited().items()) #el método .get_rooms_visited() devuelve un diccionario con llave el nombre de cada cuarto y valor la cantidad de veces que se ha visitado dicho cuarto, luego se convierte en una lista de tuplas (key, value) usando el método .items() para luego poderla ordenar por orden de cantidad de visitas (de más a menos visitado)
                rooms = sorted(rooms, key = lambda room: room[1], reverse = True) #como se convierte al diccionario en una lista, cada elemento de esta lista es una tupla en la que el primer elemento (índice 0) es la clave (en este caso el nombre del cuarto) y el segundo (índice 1) es el valor asociado a la clave (en este caso el número de visitas a dicho cuarto). Así, se ordena de mayor a menor (por eso reverse = True) tomando en consideración el número de visitas
                for i, room in enumerate(rooms):
                    print(f"------{i+1}---------------------") #se suma 1 a i para que muestre el conteo a partir de 1 y así.
                    print(f"\t{room[0]}: visitado {room[1]} veces.")
                print()
                #nunca logré ver cómo se veían los gráficos en mi computadora. no sé qué hice mal, pero matplotlib no me ha mostrado ningún gráfico hasta ahora y se me acaban las ideas.
                # labels, sizes = zip(*rooms) #labels son los nombres de los cuartos, sizes la cantidad de veces que se visitó cada uno. el orden en ambas tuplas es igual (es decir el primer elemento de labels es el cuarto determinado y el primer elemento de sizes es la cantidad de veces que se visitó ese cuarto determinado, por ejemplo)
                # plt.pie(sizes, labels = labels, autopct = '%1.1f%%', shadow = True)
                # plt.show()



            else:
                print("Aún no ha visitado ningún cuarto.")
            
            input("\n\n▶️ ")

        

        print("\n", "USUARIOS QUE MÁS JUEGAN".center(120, "-"), "\n")
        top_players = sorted(list(players.values()), key = lambda player: len(player.get_game_info()), reverse = True) #se ordena la lista de valores (en este caso el objeto de la clase Player asociado al jugador) de players tomando en cuenta el largo de la lista que devuelve el método .get_game_info() de cada jugador registrado (ya que cada elemento de esta lista representa una partida jugada), de mayor a menor (por eso reverse = True). es decir, se ordena de mayor a menor cantidad de partidas jugadas por cada jugador
        for i, player in enumerate(top_players):
            print(f"------{i+1}---------------------") 
            print(f"JUGADOR:\t{player.get_username()}\nCANTIDAD DE PARTIDAS:\t{len(player.get_game_info())}.")
        
        #nunca pude ver estas gráficas de matplotlib.
        # player_names = [player.get_username() for player in top_players] #lo que va en eje x. el orden de jugador y veces jugadas es el mismo.
        # times_played = [len(player.get_game_info()) for player in top_players] #lo que va en eje y
        # plt.bar(player_names, times_played, color = 'pink')
        # plt.show()
        



        input("\n\n▶️ ")
    
    else:
        print("No hay jugadores registrados.")
   
def leaderboard(players, difficulty):
    """Función que genera el top 5 (por tiempo) por dificultad.

    Args:
        players (dict): diccionario que contiene la información de cada jugador, en el que los keys son el nombre de usuario de cada uno y los values el objeto de clase Player con la información de juego de cada jugador registrado.
        difficulty (str): string que indica el nivel de dificultad del que se busca realizar el top 5 de jugadores. Puede ser 'f' = Fácil, 'm' = Medio o 'd' = Difícil.
    """
    if difficulty == 'f':
        message = 'FÁCIL'
    elif difficulty == 'm':
        message = 'MEDIO'
    elif difficulty == 'd':
        message = 'DIFÍCIL'
    print(f"\nDIFICULTAD: {message}")

    player_times_per_difficulty = {}
    times_per_difficulty = []
    
    for player in players.values(): #player es cada objeto player guardado en players
        if player.get_best_times_per_difficulty(difficulty) != None: #chequea esto ya que el método usado devuelve None si no tiene un mejor tiempo en esa dificultad (sea porque no tiene juegos en esa dificultad o porque no ha ganado ninguna partida en dicha dificultad)
            player_times_per_difficulty[player.get_username()] = player.get_best_times_per_difficulty(difficulty) #guarda en un diccionario con llave el nombre de usuario del jugador la lista de sus mejores tiempos en esa dificultad
            for time in player_times_per_difficulty[player.get_username()]:    
                times_per_difficulty.append(time) #guarda cada tiempo individual de cada jugador en una lista
    
    times_per_difficulty.sort() #con sort, se ordenan los tiempos en la lista de menor a mayor 
    
    if times_per_difficulty: #chequea si hay algún tiempo que imprimir
        for i, time in enumerate(times_per_difficulty):
            if i < 5: #de este modo, sólo se imprimen los primeros 5 tiempos (los de índices del 0 al 4) y sus jugadores (o los primeros que haya, si es que no llega a 5)
                print(f"------{i+1}---------------------") 
                for player in player_times_per_difficulty:
                    if time in player_times_per_difficulty[player]:  #de esta forma se busca cuál fue el jugador que obtuvo el tiempo que se imprime
                        print(f"JUGADOR:\t{player}.\nTIEMPO:\t{time} segundos.")
                        break
            else:
                break

    else:
        print("No hay mejores tiempos para esta dificultad.")