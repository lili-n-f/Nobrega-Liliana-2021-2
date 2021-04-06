from Game import Game
import random

class RandomNumber(Game):
    def __init__(self, requirement, name, award, rules, questions):
        super().__init__(requirement, name, award, rules, questions)

    def ask_for_clues(self, player, range_upper_limit, number, guess):
        """Método para dar al usuario la opción de obtener una pista en un juego (si es que todavía le quedan pistas
        al jugador y aún hay pistas que mostrarle). En este caso, te dice si el número adivinado está muy/un poco por arriba/por abajo del número real.

        Args:
            player (Player): instancia de la clase Player asociado al jugador que juega.
            range_upper_limit (int): límite superior del rango de números entre los cuales se escogió un número aleatorio.
            number (int): número que el usuario debe adivinar.
            guess (int): número adivinado por el usuario.
        """
        if player.get_clues() > 0 and self.clues_index < len(self.current_clues):
            
            if input("\n¿Quieres una pista? [S] = sí, cualquier otro caracter = no: ").lower() == 's':
                #se considera que un número está muy por encima/debajo cuando la diferencia entre lo adivinado y el número real es más grande que el resultado del límite superior del rango divido enteramente entre dos. se considera que está un poco por encima o debajo si la diferencia es menor a lo antes dicho.
                if guess > number: 
                    if guess-number > range_upper_limit//2:
                        print("Lo que dijiste está muy por encima.")
                    else:
                        print("Lo que dijiste está un poco por encima.")
                else:
                    if number-guess > range_upper_limit//2:
                        print("Lo que dijiste está muy por debajo.")
                    else:
                        print("Lo que dijiste está un poco por debajo.")
                
                self.clues_index += 1
                player.use_clue()

    def game_begins(self, player):
        self.choose_random_question()
        self.define_current_clues()
        
        failed_tries = 0
        win = False

        print(f"\n{self.current_question['question']}\n")
        number_range = self.current_question['question'][self.current_question['question'].index("entre")+6:].split("-") #esto toma el rango que retorna la api como un string, considerando que el rango se presenta cuando se dice '...entre [número inicial]-[número final]'. por tanto, desde el índice en el que empieza la palabra entre, sumada más 6 (para que el índice inicial sea después de esta palabra y el espacio después de la misma) hasta el final está el rango buscado. luego, se usa punto split con el caracter '-' ya que es este el que separa los números. se obtiene así una lista con 2 números: el primero siendo el inicio del rango y el segundo el final del rango.
        
        number = random.randint(int(number_range[0]), int(number_range[1])) #aquí se escoge un número aleatorio entre los números del rango dado en la api

        while player.get_lives() > 0:

            try:
                guess = int(input("Ingresa el número: "))
                if guess == number:
                    print("✔️¡Número adivinado!✔️")
                    win = True
                    break
                else:
                    print("❌Número incorrecto.❌")
                    failed_tries += 1
                    self.ask_for_clues(player, int(number_range[1]), number, guess)
            except ValueError: #si el usuario ingresa un valor que no puede ser convertido a int
                failed_tries += 1
                print("❌Ingreso inválido.❌")
            
            if failed_tries == 3: #según las reglas del juego, por cada tres intentos fallidos, se pierden 0.25 vidas. 
                player.lose_lives(0.25)
                failed_tries = 0 #se reinicia el valor de los intentos fallidos (luego, cuando vuelva a equivocarse tres veces, perderá nuevamente las 0.25 vidas y se reiniciará de nuevo el conteo de intentos fallidos)

        self.win_or_lose(player, win)

    def win_or_lose(self, player, win):
        if win:
            print("\n🙌¡GANASTE EL RETO!🙌")
            print(f"Premio: 🏆 {self.award} 🏆")
            player.add_item_to_inventory(self.award.lower().replace("í", "i"))
            self.won = True
        else:
            print("\n❌PERDISTE EL RETO❌")
