from Game import Game
from sympy import diff, Symbol, lambdify
from sympy.parsing.sympy_parser import parse_expr
from math import cos, tan, sin, pi, isclose
from fractions import Fraction

class MathQuestions(Game):
    def __init__(self, requirement, name, award, rules, questions, message_requirement):
        super().__init__(requirement, name, award, rules, questions, message_requirement)

    def game_begins(self, player):

        self.choose_random_question()
        self.define_current_clues()

        win = False
    
        function = self.current_question['question'][self.current_question['question'].index("=")+1: ].replace("sen", "sin")
        print(f"\n{self.current_question['question']}")


        x = {'x': Symbol('x')}
        function = parse_expr(function, x)
        derivative = diff(function, x['x'])
        result = lambdify(x['x'], derivative)
        x_value = eval(self.current_question['question'][self.current_question['question'].index('en')+2: self.current_question['question'].index('f(x)')-1])
        result = result(x_value)


        self.ask_for_clues(player)

        while player.get_lives() > 0:
            try:

                answer = Fraction(input("\nSi la respuesta no es entera, puedes utilizar fracciones (ejemplo: 0.5 = 1/2).\nRespuesta: "))
               
                if isclose(answer, result): #uso isclose porque a veces el programa obtiene valores como -0.20000000000000007 en lugar de -0.2 Así, se obtiene que la respuesta del usuario es correcta si la diferencia entre la respuesta y el resultado es menor o igual a 1e-9 unidades
                    print("✔️¡Respuesta correcta!✔️")
                    win = True
                    break
                else:
                    raise ValueError

            except (ValueError, ZeroDivisionError): #si ingresó algo que no es un número o el número incorrecto, o ingresó 1/0 o algo parecido
                print("❌Respuesta incorrecta❌")
                player.lose_lives(0.25)
        
        self.win_or_lose(player, win)

    def win_or_lose(self, player, win):
        if win:
            print("\n🙌¡GANASTE EL RETO!🙌")
            print(f"Premio: 🏆 {self.award} 🏆")
            player.gain_lives(1)
            self.won = True
            player.use_item_from_inventory(self.requirement.lower())
        else:
            print("\n❌PERDISTE EL RETO❌")
