from Game import Game
import random
class ShuffledWords(Game):
    def __init__(self, requirement, name, award, rules, questions):
        super().__init__(requirement, name, award, rules, questions)

    def game_begins(self, player):
        self.choose_random_question()
        
        win = False

        print(f"\n{self.current_question['question']}\nCategoría: {self.current_question['category']}")
        
        jumbled_words = []
        for word in self.current_question['words']:
            new_word = list(word)
            random.shuffle(new_word)
            new_word = "".join(new_word)
            while new_word == word: #para evitar que una palabra 'mezclada' quede igual que la palabra original, se sigue mezclando la palabra hasta obtener algo distinto a la palabra original 
                new_word = list(word)
                random.shuffle(new_word)
                new_word = "".join(new_word)
            jumbled_words.append(new_word) #la función shuffle sólo mezcla listas, por tanto se convierte la palabra (el string) en una lista, luego se aplica el shuffle y finalmente con el método .join (con "" ya que no queremos que haya ningún espacio ni caracter extra entre cada letra de la palabra) se vuelve a tener un string, que es lo que se añade a la lista de palabras mezcladas (una vez se obtenga una palabra distinta a la palabra original como ya se mencionó)

        while player.get_lives() > 0:
            print("Palabras:")
            for word in jumbled_words:
                print(word)

            answer = input("Ingresa una de las palabras organizada correctamente: ").lower()
            if answer in jumbled_words: #si la respuesta de la persona ya fue reemplazada en jumbled_words, entonces ya fue conseguida esa palabra
                print("\nLa palabra ingresada ya está entre las palabras mostradas.\n")
            elif answer in self.current_question['words']:
                print("\n✔️Palabra correcta.✔️\n")
                jumbled_words[self.current_question['words'].index(answer)] = answer #se sustituye la palabra mezclada por la palabra conseguida.
            else:
                print("\n❌Palabra incorrecta.❌\n")
                player.lose_lives(0.5)
            
            if jumbled_words == self.current_question['words']: #si ya todas las palabras mezcladas fueron desmezcladas, gana
                win = True
                break

        self.win_or_lose(player, win)
        
    def win_or_lose(self, player, win):
        if win:
            print("\n🙌¡GANASTE EL RETO!🙌")
            print(f"Premio: 🏆 {self.award}: bptsp05-7r3m3nd4-m473r14 🏆")
            player.add_item_to_inventory(self.award.lower()+": bptsp05-7r3m3nd4-m473r14")
            self.won = True
        else:
            print("\n❌PERDISTE EL RETO❌")