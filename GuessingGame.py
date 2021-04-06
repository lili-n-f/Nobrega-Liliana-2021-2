from Game import Game

class GuessingGame(Game):
    def __init__(self, requirement, name, award, rules, questions, message_requirement):
        super().__init__(requirement, name, award, rules, questions, message_requirement)
        self.__password = 'bptsp05-7r3m3nd4-m473r14'

    def intro_game(self, player):
        """Método para iniciar el juego. Si ya se ganó, avisa esto al jugador. Si no tiene la contraseña en el 
        inventario del jugador, le muestra el mensaje asociado al requerimiento. Si no lo ha ganado y tiene
        el objeto requerido, pide la contraseña y, si es ingresada correctamente, da una bienvenida al juego y 
        llama al método game_begins para que verdaderamente comience el juego. Si no la ingresa bien, no le permite jugar.

        Args:
            player (Player): instancia de la clase Player asociado al jugador que juega.
        """
        
        if self.won:
            print("\nYa ganaste este juego.\n")
        elif self.requirement.lower() not in player.get_inventory():
            print(f"\n{self.message_requirement.capitalize()}\n") 
        elif input("\nContraseña: ") == self.__password:
            print("✔️Contraseña correcta.✔️\n")
            print(f"¡BIENVENIDO AL JUEGO: {self.name.upper()}!".center(120, " "))
            print(f"REGLAS: {self.rules}\n")
            self.game_begins(player)
        else:
            print("❌Contraseña incorrecta.❌\n")

    def game_begins(self, player):
        
        self.choose_random_question()
        self.define_current_clues()

        win = False
        print(f"\nADIVINANZA: {self.current_question['question']}")

        while player.get_lives() > 0:
            self.ask_for_clues(player)
            
            answer = input("\nRespuesta: ")
            
            if answer in self.current_question['answers']:
                print("✔️¡Adivinaste!✔️")
                win = True
                break
            else:
                print("❌Respuesta incorrecta.❌\n")
                player.lose_lives(0.5)

        self.win_or_lose(player, win)
