from string import ascii_uppercase
from Game import Game

class Cryptogram(Game):

    def __init__(self, requirement, name, award, rules, questions, message_requirement):
        super().__init__(requirement, name, award, rules, questions, message_requirement)
            
    def game_begins(self, player):
        
        self.choose_random_question()
        
        win = False
        
        cipher_alphabet = []
        for i in range(len(ascii_uppercase)):
            if i < len(ascii_uppercase) - self.current_question['desplazamiento']: #se chequea que i sea menor que el largo del alfabeto menos el desplazamiento que hay que hacer ya que al usar como índice del alfabeto a i+self.current_question['desplazamiento'] se sobrepasaría el índice máximo del mismo
                cipher_alphabet.append(ascii_uppercase[i+self.current_question['desplazamiento']])
            else:
                cipher_alphabet.append(ascii_uppercase[i+self.current_question['desplazamiento']-len(ascii_uppercase)]) #de lo contrario, se le resta a i+self.current_question['desplazamiento'] el largo del alfabeto (es como si el alfabeto funcionara como un círculo, ya que al acabarse las letras vuelve al principio)

        print(*cipher_alphabet, sep= "  ") #esto muestra el alfabeto con las letras desplazadas, con cada letra separada por dos espacios
        print(*list(ascii_uppercase), sep= "  ") #y esto el alfabeto normal de la misma forma
        
        real_message = self.current_question['question'].replace('á', 'a').upper()
        ciphered_message = ''
        for character in real_message:
            if character in ascii_uppercase: 
                ciphered_message += cipher_alphabet[ascii_uppercase.index(character)] #como el orden en el que aparecen las letras 'codificadas' en el cipher_alphabet es el mismo orden de las letras del alfabeto que representan, podemos reemplazar cada letra normal por la letra del cipher_alphabet en su misma posición para codificar el mensaje
            elif character == " ": #si el mensaje tiene espacios, el mensaje en código también
                ciphered_message += " "

        print(f"\nMENSAJE: {ciphered_message}\n")

        while player.get_lives() > 0:
            answer = input("\nIngresa el mensaje descifrado: ").upper()
            if answer == real_message:
                print("✔️Mensaje descifrado correctamente.✔️")
                win = True
                break
            else:
                print("❌Mensaje no descifrado❌")
                player.lose_lives(1)

        self.win_or_lose(player, win)

    def win_or_lose(self, player, win):
        if win:
            print("\n🙌¡GANASTE EL RETO!🙌")
            print(f"Premio: 🏆 {self.award} 🏆")  
            player.add_item_to_inventory(self.award.lower()[:7]) #como en la API el award es 'Mensaje: Si estas gradudado puedes pisar el Samán' pero el requirement del juego de lógica es 'Mensaje', se añade al inventario "Mensaje" solamente (que es el award del juego desde el índice 0 hasta el 7 sin incluirlo)
            self.won = True
            if self.requirement != False:    
                player.use_item_from_inventory(self.requirement.lower())            
        else:
            print("\n❌PERDISTE EL RETO❌")