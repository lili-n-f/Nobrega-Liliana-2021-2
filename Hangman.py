from Game import Game

class Hangman(Game):
    
    def __init__(self, requirement, name, award, rules, questions):
        super().__init__(requirement, name, award, rules, questions)
    
    def game_begins(self, player):
        
        self.choose_random_question()
        self.define_current_clues()

        win = False
        man = ['''
        ___
        |
        |
        |
       _|____''',
        '''
        ___
        |   O
        |
        |
       _|____''',
        '''
        ___
        |   O
        |   |
        |
       _|____''',
        '''
        ___
        |   O
        |   |
        |  /
       _|____''',
        '''
        ___
        |   O
        |   |
        |  / \\
       _|____''',
        '''
        ___
        |   O
        |  /|
        |  / \\
       _|____''',
        '''
        ___
        |   O/
        |  /|
        |  / \\
       _|____'''
        ]
        man_appearance = 0
        
        word_spaces = []
        for letter in self.current_question['answer']:
            word_spaces.append('_')
        
        print(f"\n👀SOBRE LA PALABRA: {self.current_question['question']}👀\n")
        
        while player.get_lives() > 0 and man_appearance < (len(man)-1): #si man_appearance (que es el índice de la imagen del ahorcado que se muestra) llega a la última imagen (len(man) -1 ya que en las listas se cuenta a partir del 0) ya perdió y por tanto se sale del loop del juego   
            
            if '_' not in word_spaces: #si ya no quedan espacios en blanco, entonces el jugador adivinó todas las letras y ganó
                win = True
                break
            
            print("\n\n",*word_spaces)
            print(man[man_appearance])
            
            self.ask_for_clues(player)
            
            guess = input("\nLetra: ").upper()
            if len(guess) == 1 and guess in self.current_question['answer'].upper(): #si lo que adivinó el usuario es de un caracter y el mismo está en la respuesta, entonces pudo adivinar una letra de la palabra (o haber colocado una letra que ya ha adivinado)
                if guess not in word_spaces:
                    print("✔️¡Adivinaste!✔️")
                    guess_indices = []
                    for i, letter in enumerate(self.current_question['answer'].upper()): 
                        if letter == guess:
                            guess_indices.append(i) #con esto, nos permite guardar en cuáles posiciones está la letra que adivinó la persona, para luego reemplazar los espacios vacíos ("_") con la letra determinada.
                    for index in guess_indices:
                        word_spaces[index] = guess
                else:
                    print("👀La letra ingresada ya fue jugada👀")
            else:
                print("❌Lo ingresado no forma parte de la palabra❌")
                player.lose_lives(0.25)
                man_appearance += 1


        print(man[man_appearance]) 
        print("\n", *word_spaces)

        self.win_or_lose(player, win)
