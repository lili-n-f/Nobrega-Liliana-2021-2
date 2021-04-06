from Game import Game
import random

class EmojiMemory(Game):
    def __init__(self, requirement, name, award, rules, questions):
        super().__init__(requirement, name, award, rules, questions)

    def ask_for_clues(self, player, grid, x, y):
        """Método para dar al usuario la opción de obtener una pista en un juego (si es que todavía le quedan pistas
        al jugador y aún hay pistas que mostrarle). En este caso, se le dice al jugador dónde está en el grid la pareja
        del emoji que consiguió ese turno.

        Args:
            player (Player): instancia de la clase Player asociado al jugador que juega.
            grid (list): lista de listas cuyos elementos son los emojis que representan las cartas ya volteadas (o bien, los valores reales de cada carta).
            x (int): coordenada en horizontal del emoji conseguido ese turno.
            y (int): coordenada en vertical del emoji conseguido ese turno.
            """
        if player.get_clues() > 0 and self.clues_index < len(self.current_clues):
            if input("\n¿Quieres una pista? [S] = sí, cualquier otro caracter = no: ").lower() == 's':
                for i in range(len(grid)):
                    for j in range(len(grid[i])):
                        if (i,j) != (x,y) and grid[i][j] == grid[x][y]:
                            print(f"Las coordenadas de la carta que buscas son: ({i}, {j}).")
                            break
                self.clues_index += 1
                player.use_clue()

    def game_begins(self, player):
         
        def show_grid(grid_with_cards_turned):
            """Función para mostrar las cartas al jugador.

            Args:
                grid_with_cards_turned (list): lista de listas cuyos elementos son los emojis que representan las cartas que se han ido volteando (o no) a lo largo del juego.
            """

            print("\n\tCARTAS:")
            for i, line in enumerate(grid_with_cards_turned):
                print(i, *line, sep = "  ") #esto imprime las cartas de cada fila, en conjunto con el número correspondiente a la coordenada horizontal de las cartas de cada fila
            print(" ",*range(len(grid_with_cards_turned[0])), sep= "   ") #esto muestra los números correspondientes a las coordenadas en vertical de las cartas
        
        def ask_for_coordinates(grid_with_cards_turned):
            """Pide al usuario las coordenadas (el número de fila y el número de columna) de la carta que desea destapar del 'grid' (el conjunto de cartas/emojis que se han destapado, o no, a lo largo de la partida) en el juego de memoria.

            Args:
                grid_with_cards_turned (list): lista de listas cuyos elementos son los emojis que representan las cartas que se han ido volteando (o no) a lo largo del juego.

            Raises:
                ValueError: si el usuario ingresa un valor inválido de coordenadas (sea porque no está en el rango del número de filas (que es igual para todas las filas, razón por la que validar que esté en el rango del largo de la primera fila es suficiente) y columnas o porque ya esa carta fue destapada, es decir, la carta no es 🌚 que representa las cartas boca abajo)

            Returns:
                int: retorna los valores de las variables x y y, que son enteros que representan, respectivamente, el número de fila y de columna correspondiente a la carta que se desea voltear.
            """
            while True: #loop para el try-except de validación de las coordenadas ingresadas de la carta    
                try:
                    x = int(input("\n\nIngresa la coordenada en horizontal correspondiente a la carta que deseas levantar: ")) 
                    y = int(input("Ingresa la coordenada en vertical correspondiente a la carta que deseas levantar: "))
                    if x not in range(len(grid_with_cards_turned[0])) or y not in range(len(grid_with_cards_turned)) or grid_with_cards_turned[x][y] != '🌚': 
                        raise ValueError
                    return (x,y)
                except ValueError: #si se ingresa un valor que no puede ser casteado a int o un valor inválido de coordenadas (sea porque no está en el rango del número de filas (que es igual para todas las filas, razón por la que validar que esté en el rango del largo de la primera fila es suficiente) y columnas o porque ya esa carta fue destapada, es decir, la carta no es 🌚 que representa las cartas boca abajo)
                    print("Coordenadas inválidas. Valida tus datos e intenta otra vez.")
        
        self.choose_random_question()
        self.define_current_clues()

        grid = eval(self.current_question['question']) #con la función eval obtenemos una lista de listas a partir del string dado en el api
        #a continuación, se ordenan aleatoriamente las listas que componen a la matriz grid
        for line in grid:
            random.shuffle(line)
        #luego, se ordena aleatoriamente la lista de listas
        random.shuffle(grid)

        grid_with_cards_turned = []
        for i in range(len(grid)):
            grid_with_cards_turned.append([])
            for j in range(len(grid[i])):
                grid_with_cards_turned[i].append("🌚") #grid_with_cards_turned es lo que se le muestra al usuario (es una lista de listas con la misma cantidad de elementos que grid, en los que cada 🌚 representa las "cartas" volteadas)

        win = False

        while player.get_lives() > 0:

            show_grid(grid_with_cards_turned)
            x1,y1 = ask_for_coordinates(grid_with_cards_turned)
            grid_with_cards_turned[x1][y1] = grid[x1][y1] #se 'voltea' la 'carta': el 🌚 de la posición elegida se reemplaza por el emoji en la misma posición de la lista de listas 'grid' que contiene a todos los emojis 'destapados' 

            show_grid(grid_with_cards_turned)
            self.ask_for_clues(player, grid, x1, y1) #luego de que haya jugado una primera carta, puede pedir la pista que le dice dónde está su pareja
            x2,y2 = ask_for_coordinates(grid_with_cards_turned)
            grid_with_cards_turned[x2][y2] = grid[x2][y2] #igualmente, se voltea la carta

            show_grid(grid_with_cards_turned)
            if grid_with_cards_turned[x1][y1] == grid_with_cards_turned[x2][y2]: #si las cartas volteadas son iguales, entonces se encontró un par, si no, no.
                print("\n✔️¡Par conseguido!✔️\n")
                if grid == grid_with_cards_turned: #si el grid original y el grid con el que ha estado jugando el usuario (grid_with_cards_turned) son iguales, entonces ya el usuario consiguió todos los pares
                    win = True
                    break
            else:
                print("\n❌Intento fallido.❌\n")
                player.lose_lives(0.25)
                grid_with_cards_turned[x1][y1] = grid_with_cards_turned[x2][y2] = "🌚" #si no lo adivinaste, entonces vuelven a girar las cartas.

            input("Presiona 'enter' para seguir\n▶️ ")


        self.win_or_lose(player, win)
