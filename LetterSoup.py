from Game import Game
from WordSearch import WordSearch

class LetterSoup(Game):
    def __init__(self, requirement, name, award, rules, questions):
        super().__init__(requirement, name, award, rules, questions)
        self.letter_soup_grid = [] #sopa de letras

    def game_begins(self, player):
        self.choose_random_question()
        self.define_current_clues()

        win = False

        #words =  ''
        words = []
        for key in self.current_question:
            if 'answer' in key: #se agrega a words (que es un string en el que cada palabra está separada por una coma) todas las palabras (cuyo key/clave contiene 'answer', por ejemplo un key podría ser answer_1)
                words.append(self.current_question[key].lower())

        self.letter_soup_grid = WordSearch(words)
        answers = {}
        for word in self.letter_soup_grid.search_words: #este atributo de letter_soup_grid (que es un objeto de la clase WordSearch) es una lista de las palabras a buscar en la sopa de letras
            answers[word] = False #el False representa que aún no se ha conseguido la palabra en la sopa de letras. al cambiarlo a True se indica que ya fue conseguida.


        while player.get_lives() > 0 and win == False: #sigues jugando hasta que ganes o te quedes sin vidas
                        
            #esto es la sopa de letras que se muestra al usuario
            print("\n","_"*48) #esta y la siguiente línea muestran la parte superior del marco de la sopa de letras
            print("|"," "*47, '|', sep='') 
            for line in self.letter_soup_grid.grid: #este atribujo de letter_soup_grid es la lista de listas que conforma a la sopa de letras
                print('|', *line, '|', sep='  ') #esto muestra algo como |  A  B  C  ...  | por cada línea de la sopa de letras
            print("|","_"*47, '|', sep='') #esta línea muestra el marco inferior de la sopa de letras

            self.ask_for_clues(player)

            answer = input("\nPalabra: ").lower()
            

            if answer in answers:
                if answers[answer]: #si answers[answer] devuelve True significa que la palabra ya fue conseguida anteriormente
                    print("👀La palabra ya fue conseguida anteriormente.👀\n")
                else:
                    print("✔️¡Palabra encontrada!✔️\n")
                    answers[answer] = True
                    
            else:
                print("❌La palabra no se encuentra en la sopa de letras.❌\n")
                player.lose_lives(0.5)

            win = True
            for word in answers:
                if not answers[word]: #si alguna palabra sigue sin haber sido encontrada, entonces aún no se ha ganado y por tanto win es False. De lo contrario, win es True y se sale del ciclo while
                    win = False
                    break
            
        self.win_or_lose(player, win)

    def win_or_lose(self, player, win):
        if win:
            print("\n🙌¡GANASTE EL RETO!🙌")
            print(f"Premio: 🏆 {self.award} 🏆")
            player.gain_lives(1)
            self.won = True
        else:
            print("\n❌PERDISTE EL RETO❌")
