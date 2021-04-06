from Game import Game

class FindTheLogic(Game):
    def __init__(self, requirement, name, award, rules, questions, message_requirement):
        super().__init__(requirement, name, award, rules, questions, message_requirement)
    
    def intro_game(self, player):
        can_play = True
        
        if self.won:
            print("\nYa ganaste este juego.\n")

        else:
            for item in self.requirement:
                    if item.lower() not in player.get_inventory():
                        can_play = False
                        print(f"\n{self.message_requirement.capitalize()}\n")
                        player.lose_lives(1)
                        break
            
            if can_play and input(f"¿Deseas usar los objetos {self.requirement[0]} y {self.requirement[1]} para jugar este juego? [S] = sí, cualquier otro caracter = no: ").lower() == 's':
                print("\n", f"¡BIENVENIDO AL JUEGO: {self.name.upper()}!".center(120, " "))
                print(f"REGLAS: {self.rules}\n")
                self.game_begins(player)
                
    def game_begins(self, player):
        self.choose_random_question()

        win = False

        if self.questions.index(self.current_question) == 0:
            answer = 67
        elif self.questions.index(self.current_question) == 1:
            answer = 41

        print(f"\n{self.current_question}\n")
        
        while player.get_lives() > 0:
            
            try:
                user_input = int(input("Respuesta: "))
                if user_input == answer:    
                    print("✔️¡Respuesta correcta!✔️")
                    win = True
                    break
                else:
                    raise ValueError
            except ValueError: #si el usuario ingresa algo que no puede ser casteado a int o su respuesta es incorrecta
                print("❌Respuesta incorrecta.❌\n")
                player.lose_lives(1)

        self.win_or_lose(player, win)

    def win_or_lose(self, player, win):
        if win:
            print("\n🙌¡GANASTE EL RETO!🙌")
            print(f"Premio: 🏆 {self.award} 🏆")
            player.add_item_to_inventory(self.award.lower())
            self.won = True
            for item in self.requirement:
                player.use_item_from_inventory(item.lower())           
        else:
            print("\n❌PERDISTE EL RETO❌")