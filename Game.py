import random
from abc import ABC, abstractmethod

class Game(ABC):
    """Clase padre de todos los mini-juegos del juego.
    """
    def __init__(self, requirement, name, award, rules, questions = None, message_requirement = None):
        self.message_requirement = message_requirement #mensaje que se muestra si se necesita algún objeto en el inventario para jugar el juego
        self.requirement = requirement #requerimiento de objeto en el inventario del usuario para jugar el juego; False si no se necesita objeto.
        self.name = name #nombre de juego
        self.award = award #premio al ganar el juego
        self.rules = rules #reglas del juego
        self.questions = questions #preguntas del juego
        self.won = False #atributo que es False si el juego aún no ha sido ganado por el jugador en una partida y True si ya lo ganó.
        self.current_question = {} #pregunta escogida del atributo questions para que el jugador juegue en una partida
        self.current_clues = [] #lista de pistas disponibles para el usuario en un juego
        self.clues_index = 0 #índice usado para recorrer la lista de pistas para el usuario en un juego
 
 
    def intro_game(self, player):
        """Método para iniciar el juego. Si ya se ganó, avisa esto al jugador. Si requiere un objeto específico en el 
        inventario del jugador y no lo tiene, le muestra el mensaje asociado al requerimiento. Si no lo ha ganado y tiene
        el objeto requerido, da una bienvenida al juego y llama al método game_begins para que verdaderamente comience el juego.

        Args:
            player (Player): instancia de la clase Player asociado al jugador que juega.
        """
        can_play = True
        
        if self.won:
            print("\nYa ganaste este juego.\n")
        elif self.requirement: #chequea si tiene un requirement
            if self.requirement.lower() not in player.get_inventory(): #se hace el chequeo con lower() dado que todos los awards los doy usando también lower()
                can_play = False
                print(f"\n{self.message_requirement.capitalize()}\n")
        
        if can_play and not self.won:       
            if (self.requirement and input(f"\n¿Deseas usar el objeto {self.requirement.lower()} de tu inventario para jugar este juego? [S] = sí, cualquier otro caracter = no: ").lower() == 's') or not self.requirement: #si tiene un requirement y tú lo tienes en tu inventario (ya que can_play es verdad), te pregunta si quieres usar el objeto para jugar. si no tiene requirement, te permite jugar y ya.
                print("\n", f"¡BIENVENIDO AL JUEGO: {self.name.upper()}!".center(120, " "))
                print(f"REGLAS: {self.rules}\n")
                self.game_begins(player)

    @abstractmethod
    def game_begins(self, player):
        """Método para jugar el determinado juego.

        Args:
            player (Player): instancia de la clase Player asociado al jugador que juega.
        """
        pass

    def choose_random_question(self):
        """Método para escoger una pregunta aleatoria de las guardadas en el atributo questions para una partida determinada.
        """
        if self.questions != None: #si tiene preguntas de donde escoger una aleatoria, se hace    
            self.current_question = random.choice(self.questions)

    def define_current_clues(self):
        """Método para obtener las pistas que el usuario tendrá disponible para un juego.
        """
        for key in self.current_question.keys():
            if 'clue' in key:
                self.current_clues.append(self.current_question[key].capitalize())

    def ask_for_clues(self, player):
        """Método para dar al usuario la opción de obtener una pista en un juego (si es que todavía le quedan pistas
        al jugador y aún hay pistas que mostrarle).

        Args:
            player (Player): instancia de la clase Player asociado al jugador que juega.
        """
        if player.get_clues() > 0 and self.clues_index < len(self.current_clues): #mientras clues_index sea menor al largo de la lista de las preguntas disponibles será un índice válido. Si no es válido, significa que ya se le ha mostrado al usuario todas las pistas disponibles en un juego.
            if input("\n¿Quieres una pista? [S] = sí, cualquier otro caracter = no: ").lower() == 's':
                print(self.current_clues[self.clues_index])
                self.clues_index += 1
                player.use_clue()

    def win_or_lose(self, player, win):
        """Método para determinar si el usuario ganó o perdió una partida. Si gana, le da su premio y llama al método de Player que saca los ítems usados para jugarlo de su inventario.

        Args:
            player (Player): instancia de la clase Player asociado al jugador que juega.
            win (bool): variable que es True si el usuario ganó el juego y False en lo contrario.
        """
        if win:
            print("\n🙌¡GANASTE EL RETO!🙌")
            print(f"Premio: 🏆 {self.award} 🏆")
            player.add_item_to_inventory(self.award.lower())
            self.won = True
            if self.requirement != False:    
                player.use_item_from_inventory(self.requirement.lower())            
        else:
            print("\n❌PERDISTE EL RETO❌")
