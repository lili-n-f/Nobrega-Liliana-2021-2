from Game import Game

class BooleanLogic(Game):
    def __init__(self, requirement, name, award, rules, questions, message_requirement):
        super().__init__(requirement, name, award, rules, questions, message_requirement)

    def game_begins(self, player):
        self.choose_random_question()
        
        win = False

        print(f"\n{self.current_question['question']}")
        
        while player.get_lives() > 0:
            answer = input("Ingresa el valor de out (True o False): ").capitalize()
            if answer != 'True' and answer != 'False':
                print("❌Ingreso inválido.❌")
                player.lose_lives(0.5)
            elif answer == self.current_question['answer']:
                print("✔️¡Respuesta correcta!✔️")
                win = True
                break
            else:
                print("❌Respuesta incorrecta.❌")
                player.lose_lives(0.5)

        self.win_or_lose(player, win)