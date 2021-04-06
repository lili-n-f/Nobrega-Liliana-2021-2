from Game import Game
import random

class Blackjack(Game):
    def __init__(self, requirement, award, rules, message_requirement):
        super().__init__(requirement, 'Blackjack', award, rules, message_requirement = message_requirement)
        self.cards = {'A': {'ammount': 4, 'value': 1 or 11}, '2': {'ammount': 4, 'value': 2}, '3': {'ammount': 4, 'value': 3}, '4': {'ammount': 4, 'value': 4}, '5': {'ammount': 4, 'value': 5}, '6': {'ammount': 4, 'value': 6}, '7': {'ammount': 4, 'value': 7}, '8': {'ammount': 4, 'value': 8}, '9': {'ammount': 4, 'value': 9}, '10': {'ammount': 4, 'value': 10}, 'J': {'ammount': 4, 'value': 10}, 'Q': {'ammount': 4, 'value': 10}, 'K': {'ammount': 4, 'value': 10}} #diccionario con la información de cuántas cartas quedan por tipo y cuál es su valor si son tomadas

    def intro_game(self, player):
            can_play = True
            
            if self.won:
                print("\nYa ganaste este juego.\n")
            else:
                for item in self.requirement:
                    if item.lower() not in player.get_inventory():
                        can_play = False
                        print(f"\n{self.message_requirement.capitalize()}\n")
                        break
                if can_play and input(f"¿Deseas usar los objetos {self.requirement[0]} y {self.requirement[1]} para jugar este juego? [S] = sí, cualquier otro caracter = no: ").lower() == 's':
                    print("\n", f"¡BIENVENIDO AL JUEGO: {self.name.upper()}!".center(120, " "))
                    print(f"REGLAS: {self.rules}\n")
                    self.game_begins(player)
                   
    def game_begins(self, player):

        print("\n👀Comienza una nueva partida.👀")
        self.new_deck_of_cards() #este método permite usar un mazo nuevo, en el que están todas las 52 cartas sin usar (las cantidades de cada tipo de carta son 4)

        player_cards_value = crupier_cards_value = 0 

        input("\nPresiona 'enter' cuando estés listo para seguir.\n▶️ ")
        #inicialmente en un juego de blackjack, el jugador obtiene 2 cartas y el crupier 1.
        player_cards_value = self.pick_a_card(player.get_avatar(), player_cards_value)
        crupier_cards_value = self.pick_a_card('Crupier', crupier_cards_value)
        player_cards_value = self.pick_a_card(player.get_avatar(), player_cards_value)
            
        win = False

        while player_cards_value < 21 and input("¿Deseas tomar otra carta? [S] = sí, cualquier otro caracter = no: ").lower() == 's': #si la suma del valor de las cartas que ha tomado el jugador es menor que 21, puede tomar otra carta (si así lo decide el jugador al responder afirmativamente al input, es decir, 's')
            player_cards_value = self.pick_a_card(player.get_avatar(), player_cards_value)
        
        if player_cards_value <= 21: #si se pasa de 21, automáticamente pierde (ya que win = False y al llamarse el método win_or_lose se obtendrá que se perdió la partida) 
            
            while crupier_cards_value <= 16: #según las reglas del Blackjack el crupier toma cartas mientras esté por debajo al 17 y a partir del 17 no toma más cartas.
                crupier_cards_value = self.pick_a_card('Crupier', crupier_cards_value)

            if crupier_cards_value > 21 or player_cards_value > crupier_cards_value: #si el crupier se pasó, como ya se estableció que el jugador no se pasó de 21, el jugador gana (win = True). Si ninguno de los dos se pasó de 21 y el jugador tiene un puntaje mayor que el crupier, automáticamente está más cerca de 21 así que gana (de lo contrario, pierde: como ya win = False, al llamarse al método win_or_lose se obtiene que el jugador perdió la partida.).
                win = True
            elif player_cards_value == crupier_cards_value: #si ninguno de los dos se pasó y obtuvieron el mismo valor, hay un empate: no se pierde vidas pero se vuelve a jugar (win = None).
                win = None


        self.win_or_lose(player, win)

    def new_deck_of_cards(self):
        """Método para empezar cada partida con un mazo de cartas completo (con la cantidad total de cartas de un mazo normal).
        """
        self.cards = {'A': {'ammount': 4, 'value': 1 or 11}, '2': {'ammount': 4, 'value': 2}, '3': {'ammount': 4, 'value': 3}, '4': {'ammount': 4, 'value': 4}, '5': {'ammount': 4, 'value': 5}, '6': {'ammount': 4, 'value': 6}, '7': {'ammount': 4, 'value': 7}, '8': {'ammount': 4, 'value': 8}, '9': {'ammount': 4, 'value': 9}, '10': {'ammount': 4, 'value': 10}, 'J': {'ammount': 4, 'value': 10}, 'Q': {'ammount': 4, 'value': 10}, 'K': {'ammount': 4, 'value': 10}}

    def pick_a_card(self, player, cards_value):
        """Método para que el jugador del turno actual escoja una carta y se le sume el valor determinado de la misma al valor que el jugador llevaba ya.

        Args:
            player (str): nombre del jugador del turno actual.
            cards_value (int): valor acumulado de las cartas que ha tomado el jugador.

        Returns:
            int: valor acumulado de las cartas del jugador, después de tomar una carta.
        """
        card = random.choice(list(self.cards.keys())) #se toma una carta aleatoria (a partir de una lista de las llaves del diccionario cards)
        if self.cards[card]['ammount'] > 0: #si aún quedan cartas del tipo de carta que se escogió, entonces se resta 1 a la cantidad de cartas de este tipo en el mazo
            self.cards[card]['ammount'] -= 1
            print(f"\n\nTurno de {player}. Tomó un {card}.")
            if card == 'A': #si la carta es A, puede tener un valor de 11 o de 1: si al sumarle 11 no se pasa de 21, entonces éste es su valor: de lo contrario es 1.
                if cards_value + 11 <= 21:
                    cards_value += 11
                else:
                    cards_value += 1
            else: #si la carta no es A, el valor de la misma es el valor guardado en el diccionario del mazo de cartas
                cards_value += self.cards[card]['value']
            print(f"Su puntaje es ahora: {cards_value}.")
            input("\n▶️ ") #este input es para que el jugador tenga tiempo de leer qué ocurre en cada turno y luego seguir al presionar enter.
            return cards_value
        else:
            self.pick_a_card(player, cards_value) #si ya no hay cartas en el mazo del tipo escogido aleatoriamente, se vuelve a escoger una carta distinta.
    
    def win_or_lose(self, player, win):
        """Método para determinar si el usuario ganó, empató o perdió una partida. Si gana, llama al método de Player que saca los ítems usados para jugarlo de su inventario.

        Args:
            player (Player): instancia de la clase Player asociado al jugador que juega.
            win (bool or NoneType): variable que es True si el usuario ganó el juego, None si se empató y False si se perdió.
        """
        if win == True:
            print("\n🙌¡GANASTE!🙌")
            self.won = True
            print('''
         ______________________________________________________________________
        |                       ________________________ _________________     |
        |                      |                        |                 |    |
        |                      |                        |                 |    |
        |                      |                        |                 |    |
        |                      |                        |                 |    |
        |                      |                        |                 |    |
        |                      |                        |                 |    |
        |               ▒█▀▀█ ░█▀▀█ ▒█▄░▒█ ░█▀▀█ ▒█▀▀▀█ ▀▀█▀▀ ▒█▀▀▀       |    |
        |               ▒█░▄▄ ▒█▄▄█ ▒█▒█▒█ ▒█▄▄█ ░▀▀▀▄▄ ░▒█░░ ▒█▀▀▀   ==O |    |
        |               ▒█▄▄█ ▒█░▒█ ▒█░░▀█ ▒█░▒█ ▒█▄▄▄█ ░▒█░░ ▒█▄▄▄       |    |
        |                      |                        |                 |    |
        |                      |________________________|                 |    |
        |                      |                        |                 |    |
        |                      |                        |                 |    |
        |                      |                        |                 |    |
        |______________________|________________________|_________________|____|
        ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        ''')

            for item in self.requirement:
                player.use_item_from_inventory(item.lower())


        elif win == False: 
            player.lose_lives(1)
            print("\n❌PERDISTE❌")
            if player.get_lives() > 0: #si el jugador aún tiene vidas, entonces sigue con otra partida.
                self.game_begins(player)

        elif win == None:
            print("\n⚖️Hubo un empate.⚖️")
            self.game_begins(player) #si el jugador empata, no pierde una vida como cuando pierde la partida, pero vuelve a jugar.
        