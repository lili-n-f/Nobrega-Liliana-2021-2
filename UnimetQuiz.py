from Game import Game
import random

class UnimetQuiz(Game):
    def __init__(self, requirement, name, award, rules, questions):
        super().__init__(requirement, name, award, rules.replace("o por acabarse el tiempo", ""), questions) #hago un replace de "o por acabarse el tiempo" por un str vacío ya que el juego ya no tiene límite de tiempo, por lo que no tiene sentido mostrarle eso en las instrucciones al jugador.
        self.used_questions = [] #lista de preguntas que fueron usadas las veces pasadas en una partida

    def choose_random_question(self):
        """Método para escoger una pregunta aleatoria de las guardadas en el atributo questions para una partida determinada. Para este juego específicamente se pide que si la persona vuelve a jugar, que sea una pregunta distinta.
        """
        #para este juego se pide que si la persona vuelve a jugar, que le salga una pregunta distinta. de la siguiente forma se escoge al azar una pregunta hasta que la misma no esté entre las preguntas ya usadas.
        if len(self.used_questions) < len(self.questions):
            self.current_question = random.choice(self.questions)
            while self.current_question in self.used_questions:
                self.current_question = random.choice(self.questions)
            self.used_questions.append(self.current_question)
        else: #si ya todas las preguntas fueron usadas, se 'resetea' el proceso: la lista used_questions se vacía y se llama al método para obtener otra pregunta.
            self.used_questions = []
            self.choose_random_question()
    
    def game_begins(self, player):
        self.choose_random_question()
        self.define_current_clues()

        win = False

        print(f"PREGUNTA:\n{self.current_question['question']}\n")
        
        answers = []
        for key in self.current_question:
            if 'answer' in key: #sólo se meten en la lista answers los valores guardados en el diccionario current_question cuyas llaves contienen la palabra 'answer'
                answers.append(self.current_question[key])
        random.shuffle(answers) #esto permite que las respuestas posibles estén en un orden aleatorio.

        for i, possible_answer in enumerate(answers):
            print(f"\t{i+1}. {possible_answer}.")
        
        
        
        while player.get_lives() > 0: #loop del juego (sigue jugando mientras el jugador tenga vidas)
            try:
                self.ask_for_clues(player)
                answer = int(input("\nIngresa el número de la respuesta correcta.\nRespuesta: "))
                
                if answer in range(1, len(answers)+1): #como las opciones que se muestran van del 1 al largo de la lista, su respuesta, para ser válida, debería estar entre el 1 y el largo de la lista (como el range no incluye el límite superior, al largo de la lista de respuestas se le suma 1)

                    if answers[answer-1] == self.current_question['correct_answer']: #se resta 1 a answer ya que los índices que se le muestran son los índices de cada posible respuesta en la lista answers, sumados más 1.
                        print("✔️¡Respuesta correcta!✔️")
                        win = True
                        break #al hacer un break se sale del loop del juego y, como win = True al llamarse al método win_or_lose se obtendrá que se ganó el juego
                    else:   
                        raise ValueError
                else:
                    raise IndexError 

            except (ValueError, IndexError): #cuando el usuario ingrese un valor que no puede ser casteado a int o haya escogido una opción incorrecta, o si ingresa un valor que no es un índice válido para la lista answers
                print("❌Respuesta incorrecta.❌")
                player.lose_lives(0.5)

        self.win_or_lose(player, win)
