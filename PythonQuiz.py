from Game import Game

class PythonQuiz(Game):
    def __init__(self, requirement, name, award, rules, questions, message_requirement):
        super().__init__(requirement, name, award, rules, questions, message_requirement)

    def game_begins(self, player):
        self.choose_random_question()
        self.define_current_clues()

        win = False

        if self.questions.index(self.current_question) == 0:
            answer = 50
        elif self.questions.index(self.current_question) == 1:
            answer = 'estudio en la metro ingenieria de sistemas'

        frase = self.current_question['question'][self.current_question['question'].index('=')+2 : len(self.current_question['question'])].replace('. Escribe en una línea de código como extraer de este string los 50 en formato entero', '').replace('"', '')

        print(f"\n{self.current_question['question']}\n")
        
        while player.get_lives() > 0:
            self.ask_for_clues(player)
            print(f'\nfrase = "{frase}"')
            user_input = input("Solución: ")
            try:
            
                if 'frase' in user_input and '#' not in user_input and 'answer' not in user_input and eval(user_input) == answer: #la primera condición chequea que la solución del usuario esté manipulando la variable dada llamada 'frase' y no forzando la respuesta, como por ejemplo escribiendo int(50). La segunda evalúa que no hayan comentarios en el código (porque si no, el usuario podría escribir la respuesta como 'int(50) #frase' por ejemplo). La tercera ve que el usuario no coloque 'answer' en su código, ya que de este modo podría hacer, por ejemplo print(answer, frase) y se vería la respuesta. La última evalúa como código lo ingresado por el usuario para ver si da la respuesta
                    print("✔️Código ejecutado exitosamente.✔️")
                    win = True
                    break
                else:
                    raise RuntimeError
            except (RuntimeError, SyntaxError, NameError, IndexError, TypeError, ZeroDivisionError, ImportError, KeyError, ValueError, UnboundLocalError, AttributeError): #si lo que ingresó no da el resultado buscado o el usuario se equivoca al escribir el código (evito usar except sin ningún exception específico dado que el juego en total funciona dentro de un try-except, en el que manejan las excepciones de TimeoutError y GameOverException. Si justamente el usuario, en este juego, se llegara a quedar sin tiempo o vidas, respectivamente, en lugar de terminarse el juego en total, se entraría al código indentado después del except, si el mismo no maneja errores específicos).
                print("❌El código ingresado es incorrecto.❌\n")
                player.lose_lives(0.5)

        self.win_or_lose(player, win)