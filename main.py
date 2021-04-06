import time
import player_functions
import room_functions
import statistics
import os
import signal
from GameOverException import GameOverException

def get_difficulty_info():
    """Función que obtiene la información de tiempo, vidas y pistas para cada nivel de dificultad del archivo difficulty.txt

    Returns:
        list: difficulty_info es una lista de tres listas: de cantidad de vidas, pistas y tiempo, respectivamente. Para cada lista, el primer elemento corresponde al modo Fácil, el segundo al Medio y el tercero al Difícil.
    
    """
    while True:
        try:

            difficulty_txt = open("difficulty.txt")
            difficulty_info = difficulty_txt.readlines()
            difficulty_txt.close()
            del difficulty_txt
            for i, info in enumerate(difficulty_info):
                #la siguiente operación permite que se reemplace cada elemento de la lista difficulty_info con una lista (antes removiendo el '\n' a la derecha de cada elemento original (info), correspondiente al salto de línea que tienen algunas de las líneas del archivo difficulty.txt) cuyos elementos son delimitados en info por ","
                difficulty_info[i] = info.rstrip("\n").split(",")
                for j, number in enumerate(difficulty_info[i]):
                    if i == 0 and number == '0': #esto valida que no se pueda colocar las vidas en 0 (ya que la primera lista, es decir la lista de índice i = 0, corresponde a las vidas) haciendo que el mínimo de vidas que se pueden tener es 1
                        difficulty_info[i][j] = 1
                    else:    
                        #la siguiente operación permite 'castear' todos los números de str a int
                        difficulty_info[i][j] = int(number)
            return difficulty_info
        
        except FileNotFoundError: #si no existe el file, se crea y se escribe en él los valores 'default'. luego, como se está en un loop, se vuelve a intentar la operación de lectura. 
            difficulty_txt = open("difficulty.txt", 'w')
            difficulty_txt.write('5,3,1\n5,3,2\n30,20,10')
            difficulty_txt.close()
            del difficulty_txt

def new_game(players):
    """Función que permite iniciar una nueva partida: se llaman a las funciones apropiadas para registrar un nuevo jugador con su avatar (register_player) o para permitir que el jugador ingrese a su cuenta ya existente y escoger su avatar (sign_in).
    Luego, permite al jugador escoger la dificultad de la partida. Finalmente, se inicia el juego con la primera narrativa.
    """

    print("\n", "NUEVA PARTIDA".center(120, "~"))

    if players: #chequea si hay algún jugador registrado
        if input("\n¿Ya tienes una cuenta? [S] = sí, cualquier otro caracter = no, deseo registrarme\n>").lower() == 's':
           player = player_functions.sign_in(players)
        else:
            player = player_functions.register_player(players)
    else: #si no hay ningún jugador registrado, necesariamente el usuario deberá registrarse para jugar
        player = player_functions.register_player(players)

    print("\n","DIFICULTAD DE PARTIDA".center(120, "-"))
    difficulty_info = get_difficulty_info()
    #TODO recuerda agregar tiempo
    print(f"""
        FÁCIL  😅: {difficulty_info[0][0]} vidas🧡 y {difficulty_info[1][0]} pistas🔍, y un tiempo de {difficulty_info[2][0]} minutos⏲️
        MEDIO  😐: {difficulty_info[0][1]} vidas🧡 y {difficulty_info[1][1]} pistas🔍, y un tiempo de {difficulty_info[2][1]} minutos⏲️
        DIFÍCIL😖: {difficulty_info[0][2]} vida 🧡 y {difficulty_info[1][2]} pistas🔍, y un tiempo de {difficulty_info[2][2]} minutos⏲️
    """)
    while True:
        game_difficulty = input("Ingresa el nivel de dificultad: [F], [M], [D]\n>").lower()
        if game_difficulty == 'f':
            player.set_lives_and_clues(difficulty_info[0][0], difficulty_info[1][0])
            time_difficulty = difficulty_info[2][0]
            break
        elif game_difficulty == 'm':
            player.set_lives_and_clues(difficulty_info[0][1], difficulty_info[1][1])
            time_difficulty = difficulty_info[2][1]
            break
        elif game_difficulty == 'd':
            player.set_lives_and_clues(difficulty_info[0][2], difficulty_info[1][2])
            time_difficulty = difficulty_info[2][2]
            break
        else:
            print("ERROR: opción inválida.\n")
    player.set_game_difficulty(game_difficulty)
    print("Dificultad escogida con éxito. ✔️")
    input("\nIngresa cualquier cosa cuando estés listo para comenzar el juego:\n▶️ ")

    first_narrative(time_difficulty, player)

def first_narrative(time_difficulty, player):
    """Función que muestra la primera narrativa del juego.

    Args:
        time_difficulty (int): número de minutos máximo para el juego según la dificultad.
        player (Player): instancia de la clase Player asociado al jugador que juega.
    """
    time.sleep(0.25)
    os.system('clear') #'limpia' todo lo que hay en la terminal.
    input("Presiona 'enter' para continuar\n▶️ ")
    print("\nHoy 5 de marzo de 2021, la Universidad sigue en cuarentena (esto no es novedad)...")
    input("\n▶️ ")
    print("...lo que sí es novedad es que se robaron un Disco Duro de la Universidad, del cuarto de redes...")
    input("\n▶️ ")
    print("...que tiene TODA la información de SAP de estudiantes, pagos y asignaturas.")
    input("\n▶️ ")
    print("\n¡Necesitamos que nos ayudes a recuperar el disco!")
    input("\n▶️ ")
    print(f"\nPara eso tienes {time_difficulty} minutos, antes de que el servidor se caiga y no se pueda hacer más nada.")
    input("\n▶️ ")
    print(f"{player.get_avatar()}... ¿Aceptas el reto?")
    print("\n\t[S] = sí", "\t|\t", "[N] = no")
    user_input = input("\n>").lower()
    if user_input == 'n':
        print("¿Seguro que no quieres?")
        input("\n▶️ ")
        print("Tipo, ¿en serio?")
        input("\n▶️ ")
        print("Tú fuiste el que entró al juego.")
        input("\n▶️ ")
        print("Deberías reconsiderar.")
        input("\n▶️ ")
        print("De hecho ni siquiera importa lo que quieras.")
        input("\n▶️ ")
        print("Estás avisado.")
        input("\n▶️ ")
        print(f"{player.get_avatar()}... ¿Aceptas el reto?\n\n\t[S] = sí", "\t|\t", "cualquier otra cosa = no, pero realmente no tengo otra opción")
        input("\n>")
    elif user_input != 'n' and user_input != 's':
        print("¿Es en serio?")
        input("\n▶️ ")
        print("¿Ya vamos a empezar así?")
        input("\n▶️ ")
        print("Te doy DOS OPCIONES.")
        input("\n▶️ ")
        print("DOS.")
        input("\n▶️ ")
        print("NI MÁS, NI MENOS.")
        input("\n▶️ ")
        print("¿Y tú...me haces esto?")
        input("\n▶️ ")
        print("Espero que estés feliz contigo mismo.")
        input("\n▶️ ")
        print("De todas formas no me importa tu opinión.")
        input("\n▶️ ")
        print(f"{player.get_avatar()}... ¿Aceptas el reto?\n\n\t[Literalmente cualquier cosa] = sí", "\t|\t", "Eso es todo, no hay otra opción")
        input("\n>")
    game(time_difficulty, player)

def game(time_difficulty, player):
    """Función del juego: en ésta se muestra la narrativa 2, se empieza el tiempo y a continuación 
    el juego (dentro de un try, es un loop hasta que se gane en el que se llama a la función go_to_room que es la función en la cual el jugador va a cuartos e interactúa con objetos, etc.).
    Si se acabara el tiempo (como se hace un raise TimeoutError al pasar esto), se entra al código indentado luego del except TimeoutError. Lo mismo si se acaban las vidas, pero con el error GameOverException.
    Por último, se guarda la información de la partida (tiempo jugado, si se ganó o no) y se muestra la narrativa final (depende de si perdió o ganó y, en este último caso, de qué avatar usó).

    Args:
        time_difficulty (int): número de minutos máximo para el juego según la dificultad.
        player (Player): instancia de la clase Player asociado al jugador que juega.
    """
    winner = False
    laboratory, library, plaza, corridor, server_room = room_functions.define_rooms()
    
    print(f"\nBienvenido {player.get_avatar()}, gracias por tu disposición a ayudarnos a resolver este inconveniente.")
    input("\n▶️ ")
    print("Te encuentras actualmente ubicado en la biblioteca, revisa el menú de opciones para ver qué acciones puedes realizar.\nRecuerda que el tiempo corre más rápido que un trimestre en este reto.")
    input("\nPresiona 'enter' para comenzar el tiempo.\n▶️ ")

    start_time = time.time() #time.time() devuelve el tiempo actual, representado en segundos después de Epoch
    max_time = start_time + time_difficulty*60 #max_time es el tiempo máximo en el que terminaría el juego (es decir, el momento final de juego si se juega hasta terminarse el tiempo). se multiplica time_difficulty por 60 ya que time_difficulty está expresado en minutos y se necesitan los segundos.
    player.set_max_time(max_time)
    signal.signal(signal.SIGALRM, time_over)   #cuando se obtiene la señal de la alarma luego del tiempo de juego, se llama a la función time_over (que es el handler) la cual hace un raise TimeoutError      
    signal.alarm(60*time_difficulty) #envía una señal cuando ha pasado el tiempo de juego (como time_difficulty está expresado en minutos y signal.alarm() toma segundos como parámetro, se multiplica por 60 los minutos del tiempo de juego.)

    room = library #se empieza en la biblioteca, por tanto el valor inicial de room, así como el primer cuarto que visita el jugador en cada juego, es la biblioteca (library)
    player.visit_room(room)
    try:
        while not winner:
            room = room_functions.go_to_room(room, player)
            if room == server_room and server_room.get_objects()[0].get_is_cleared(): #si se está en el cuarto de servidores y el primer objeto (es decir la puerta) ya está en estado cleared (es decir, el método get_is_cleared retorna True ya que el minijuego asociado a él ya fue ganado) significa que se ganó el juego. al actualizar winner a True, se sale del loop y se ejecuta el código después del try except.
                winner = True
                signal.alarm(0) #al hacer esto se detiene la señal de alarma, ya que ya no es necesario porque se ganó el juego.

    except TimeoutError: #como el handler de la señal de alarma hace un raise TimeoutError una vez termine el tiempo dado, se sale del juego una vez se tiene este error y se entra en el código indentado después de este except
        os.system('clear')
        print("\n\n", "❌⏰¡SE ACABÓ EL TIEMPO!⏰❌".center(120, " "), "\n\n")

    except GameOverException: #como el método lose_lives de la clase Player hace un raise GameOverException cuando se tiene cero o menos vidas, al perder todas las vidas se ejecuta el código indentado después de este except
        os.system('clear')
        print("\n\n", "❌☠️PERDISTE TODAS TUS VIDAS☠️❌".center(120, " "), "\n\n")
        signal.alarm(0) #detiene la señal de alarma ya que ya se perdió el juego y no es necesaria

    time_played = round(time.time() - start_time, 2) #el tiempo jugado es la variación entre el tiempo actual (al momento de acabar el juego) y el tiempo de comienzo
    player.add_game_info(time_played, winner)

    if not winner:
        print('''
                        
                           ░██████╗░░█████╗░███╗░░░███╗███████╗  ░█████╗░██╗░░░██╗███████╗██████╗░
                           ██╔════╝░██╔══██╗████╗░████║██╔════╝  ██╔══██╗██║░░░██║██╔════╝██╔══██╗
                           ██║░░██╗░███████║██╔████╔██║█████╗░░  ██║░░██║╚██╗░██╔╝█████╗░░██████╔╝
                           ██║░░╚██╗██╔══██║██║╚██╔╝██║██╔══╝░░  ██║░░██║░╚████╔╝░██╔══╝░░██╔══██╗
                           ╚██████╔╝██║░░██║██║░╚═╝░██║███████╗  ╚█████╔╝░░╚██╔╝░░███████╗██║░░██║
                           ░╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝  ░╚════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝
            ''')
        time.sleep(2)
        input("\n\nPresiona 'enter' para seguir.\n▶️ ")
        print(f"\nDerrotado, unos vigilantes te consiguen en {player.get_current_room().get_name()}. \nTe preguntan qué estás haciendo en la universidad, pero, por estar llorando, no logras contestar.\nTu dificultad para responder hace que los vigilantes sospechen de ti. \n'¿Será que fue {player.get_avatar()} quien robó el Disco Duro?' se preguntan.")
        input("\n▶️ ")
        print(f"\nPor supuesto, no querían saltar de cabeza a conclusiones, así que hicieron una pequeña investigación. \nDigo, ¿quién les creería si dijeran que {player.get_avatar()} robó un Disco Duro?")
        input("\n▶️ ")
        print("\n¡No consiguieron nada en contra tuyo!🙌🥳")
        input("\n▶️ ")
        print("\n...Sin embargo, las noticias corren rápido. Muy rápido. Sobre todo si son falsas:")
        input("\n▶️ ")
        print("\nUn grupo de personas descontentas con lo que suponen que hiciste se desahogan en su red social preferida.")
        input("\n▶️ ")
        print("𝐂𝐀𝐍𝐂𝐄𝐋𝐋𝐄𝐃 𝐄𝐍𝐃𝐈𝐍𝐆: Te cancelaron en Twitter ✌️😞")
        input("\nPresiona 'enter' para ir al menú principal\n▶️ ")
        os.system('clear')

    else:
        os.system('clear')
        print('''
                                        
                                ░██████╗░░█████╗░███╗░░██╗░█████╗░░██████╗████████╗███████╗
                                ██╔════╝░██╔══██╗████╗░██║██╔══██╗██╔════╝╚══██╔══╝██╔════╝
                                ██║░░██╗░███████║██╔██╗██║███████║╚█████╗░░░░██║░░░█████╗░░
                                ██║░░╚██╗██╔══██║██║╚████║██╔══██║░╚═══██╗░░░██║░░░██╔══╝░░
                                ╚██████╔╝██║░░██║██║░╚███║██║░░██║██████╔╝░░░██║░░░███████╗
                                ░╚═════╝░╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝╚═════╝░░░░╚═╝░░░╚══════╝
            ''')
        time.sleep(2)
        input("Presiona 'enter' para continuar\n▶️ ")
        print("¡Felicidades! Has logrado evitar una catástrofe en la Unimet.")
        input("\n▶️ ")
        if player.get_avatar() == 'Benjamín Scharifker':
            print("\nComo recompensa por el gran servicio que le prestaste a la Unimet,\nel resto de las autoridades de la universidad decidió por fin hacerte una estatua:")
            input("\n▶️ ")
            print("\nPor generaciones se recordará al rector Benjamín Scharifker \ncomo el rector que salvó a la Universidad Metropolitana de un... ¿ataque informático?\nAlgo así, nadie sabe exactamente qué pasó.")
            input("\n▶️ ")
            print("\n𝐒𝐓𝐀𝐓𝐔𝐄 𝐄𝐍𝐃𝐈𝐍𝐆: ahora la Unimet tiene una estatua más. 👤 \n¡Pero esta vez es de ti! Disfrútala, supongo.")
        elif player.get_avatar() == 'Eugenio Mendoza' or player.get_avatar() == 'Gandhi':
            print("\nPersonas alrededor de toda Venezuela querían saber quién fue el valiente héroe que salvó a la Unimet.")
            input("\n▶️ ")
            print("\nSin embargo, tú sabes que tu secreto no puede ser revelado...")
            input("\n▶️ ")
            print(f"\nQuién sabe qué pasaría si las personas supieran que la estatua de {player.get_avatar()} en la Unimet puede cobrar vida.\nSí, como en Toy Story, pero una estatua del tamaño de una persona. Espeluznante, ¿cierto?")
            input("\n▶️ ")
            print("\n𝐔𝐍𝐊𝐍𝐎𝐖𝐍 𝐇𝐄𝐑𝐎 𝐄𝐍𝐃𝐈𝐍𝐆: se crearán leyendas alrededor del acontecimiento del día de hoy.\nIncluso habrá gente que dirá que fue una estatua. Qué loco, ¿no?")
        elif player.get_avatar() == 'Pelusa':
            print("\nAl notar que el momento del desastre nunca llegó, distintas personas se acercaron a las\ninstalaciones de la universidad preguntándose qué había pasado.")
            input("\n▶️ ")
            print("\nAl notarte en el cuarto de servidores, rieron con ternura.")
            input("\n▶️ ")
            print("\n'¡Qué linda gatita! ¿Será que quien recuperó el Disco Duro la dejó aquí por accidente?'")
            input("\n▶️ ")
            print("\nTu sangre hierve por la rabia. ¿Por qué no pueden ver que fuiste tú?")
            input("\n▶️ ")
            print("\n...")
            input("\n▶️ ")
            print("\nCierto.")
            input("\n▶️ ")
            print("\nEres un gato.")
            input("\n▶️ ")
            print("\n𝐊𝐈𝐓𝐓𝐘 𝐄𝐍𝐃𝐈𝐍𝐆: nadie cree que fuiste tú quien salvó a la Unimet, pero al menos eres un gato.\nTe conformas con las caricias que te dan las personas curiosas sobre el incidente.")
        elif player.get_avatar() == 'Estudiante Estresad@':
            print("\nPara recompensar el gran servicio que le prestaste a la Universidad este día,\nlas autoridades de la Unimet deciden que te mereces la mejor de las recompensas.")
            input("\n▶️ ")
            print("\nTe dan a escoger entre dos opciones: \n(1) una beca 100% o (2) la ayuda de los mejores tutores en todas tus materias.")
            input("\n▶️ ")
            option = input("\nTú, por supuesto, escoges ... >")
            if option == '1':
                print("\n¡La beca! ¡Claro! Con lo mucho que te cuesta pagar los trimestres a veces, una beca 100% sería una ayuda INMENSA.")
                input("\n▶️ ")
                print("\nDesafortunadamente, notas muy pronto lo difícil que es mantener dicha beca.")
                input("\n▶️ ")
                print("\n𝐒𝐓𝐑𝐄𝐒𝐒𝐄𝐃 𝐄𝐍𝐃𝐈𝐍𝐆: ya no quieres jugar más a la Universidad. 😞")
            elif option == '2':
                print("\n¡Los tutores! Te gusta poder ver las materias a tu propio paso sin la presión de mantener una beca \ny la ayuda de tutores suena maravillosa.")
                input("\n▶️ ")
                print("\nTe encanta poder obtener ayuda en cualquier momento que la necesites a través de videollamada, \npero muy por dentro sabes que prefieres la interacción en vivo.")
                input("\n▶️ ")
                print("\n𝐂𝐎𝐕𝐈𝐃 𝐄𝐍𝐃𝐈𝐍𝐆: visitaste a uno de tus tutores y no siguieron las precauciones necesarias.\nTe dio Covid-19 (pero tranquilo, se te quitó). ¡USA UNA MÁSCARILLA!😷")
            elif not option: #si le dio a enter sin responder nada
                print("\n...Nada. No necesitas nada para sentirte recompensado. \nEl mero hecho de haber ayudado a tu Universidad te hace sentir inmensamente feliz y satisfecho.")
                input("\n▶️ ")
                print("\n𝐍𝐎𝐁𝐋𝐄 𝐄𝐍𝐃𝐈𝐍𝐆: tu noble respuesta -o falta de respuesta- conmueve a las autoridades de la Universidad.\nVives el resto de tu vida sin pensar en ese día en el que salvaste a la Unimet.")
            else:
                print("\nLas autoridades te miran confundidas mientras miras al horizonte, sin ningún tipo de expresión en tu rostro.")
                input("\n▶️ ")
                print(f"\n'{option}' susurras para ti mismo.")
                input("\n▶️ ")
                print("\nComienzas a reír, ya que te gusta escoger opciones distintas a las que te presentan.")
                input("\n▶️ ")
                print("\nDesafortunadamente las autoridades de la Universidad no lo encuentran tan gracioso.\nTodo lo contrario, de hecho: lo consideran una falta de respeto inmensa,\nque merece el peor de los castigos.")
                input("\n▶️ ")
                print("\n𝐒𝐄𝐂𝐑𝐄𝐓 𝐄𝐍𝐃𝐈𝐍𝐆: te botaron de la Unimet.")
        input("\nPresiona 'enter' para ir al menú principal\n▶️ ")
        os.system('clear')

def time_over(signal, frame): 
    #Función 'handler' de la señal de alarma una vez se acaba el tiempo del juego. Hace un raise TimeoutError.
    raise TimeoutError
    
def instructions():
    """Función que muestra las instrucciones generales del juego y luego permite que el usuario escoja si quiere ver las instrucciones de algún minijuego específico.
    """

    print("INSTRUCCIONES".center(120, "-"))
    print("""
    El juego consiste en diferentes cuartos donde hay objetos, tal que cada objeto tiene un mini-juego a completar.
Cada vez que ganas uno de estos juegos, obtienes una recompensa que te puede servir para resolver la problemática principal.
   Para llevar a cabo las diferentes acciones (interactuar con objetos, ver las vidas restantes, ir a otros cuartos...)
                tendrás que ingresar por teclado la opción que desees a partir de un menú de opciones.
                """)
    print("-"*120)
    input("Presiona 'enter' para seguir.\n▶️ ")
    while True:
        option = input("\nINSTRUCCIONES PARA CADA MINI-JUEGO: ingresa...\n\n\t1. Sopa de letras\n\t2. Preguntas sobre Python\n\t3. Adivinanzas\n\t4. Ahorcado\n\t5. Preguntas de matemáticas\n\t6. Criptograma\n\t7. Encuentra la lógica\n\t8. Quizziz\n\t9. Memoria\n\t10. Lógica Booleana\n\t11. Blackjack\n\t12. Palabra Mezclada\n\t13. Número aleatorio (Escoge un número entre)\n\tCualquier otro caracter: volver al menú principal\n>")
        if option == '1':
            print("\nSOPA DE LETRAS: se te mostrará una sopa de letras en la cual deberás conseguir tres palabras. Cuando hayas conseguido una, \nintrodúcela por teclado. ¡Cuidado con los errores ortográficos!\n")
        elif option == '2':
            print("\nPREGUNTAS SOBRE PYTHON: se te mostrará un problema que debes resolver escribiendo UNA SOLA línea de código, usando Python. \n¡Procura trabajar con la variable dada! Evita escribir comentarios en tu línea de código.\n")
        elif option == '3':
            print("\nADIVINANZAS: se te mostrará una adivinanza y tú deberás introducir por teclado la respuesta a la misma. \n¡No te compliques y sé preciso!\n")
        elif option == '4':
            print("\nAHORCADO: se te mostrará una pequeña descripción acerca de una palabra y, a continuación, espacios correspondientes \na cada letra de la misma, así como el dibujo de la horca. El juego funciona como cualquier otro\njuego del ahorcado: ingresa por teclado, una por una, las letras que crees que forman parte de la palabra. \nTienes sólo 6 oportunidades para equivocarte, si no ¡el ahorcado morirá!\n")
        elif option == '5':
            print("\nPREGUNTAS DE MATEMÁTICAS: se te mostrará un pequeño problema de derivadas que deberás resolver. \nTranquilo, puedes usar calculadora, esto no es un examen. \nSi el resultado no es entero, puedes usar números decimales o fracciones (ejemplo: 0.5 o 1/2).\n")
        elif option == '6':
            print("\nCRIPTOGRAMA: se te mostrará la información necesaria para decodificar un mensaje y, luego, un mensaje en código. \nIntroduce por teclado el mensaje decodificado una vez lo hayas conseguido.\n")
        elif option == '7':
            print("\nENCUENTRA LA LÓGICA: se te mostrará un problema matemático con símbolos, cuyos valores deberás descifrar a partir de \nla información dada. Luego, introduce por teclado la respuesta al problema.\n")
        elif option == '8':
            print("\nQUIZZIZ: tendrás que responder una pregunta de selección simple acerca de la cultura unimetana. \n¡Evita ingresar opciones inválidas! Si lo haces, contará como una respuesta incorrecta.\n")
        elif option == '9':
            print("\nMEMORIA: funciona como cualquier juego de memoria, en el cual tienes cartas boca abajo y vas destapándolas de par en par,\ncon el fin de conseguir todos los pares iguales. En este caso, las cartas son emojis y la forma en las que las destapas es \ningresando por teclado sus coordenadas en horizontal y vertical (es decir, el número de su fila y luego de su columna).\n")
        elif option == '10':
            print("\nLÓGICA BOOLEANA: se te mostrará un pequeño problema de lógica booleana en función de ciertas variables cuyos valores \nson dados (True o False). Luego, deberás introducir por teclado el resultado final (True o False). \n¡Cuidado con los errores ortográficos!\n")
        elif option == '11':
            print("\nBLACKJACK: funciona como cualquier otro juego de Blackjack: se te dan dos cartas y el Crupier (en este caso, la computadora) toma una.\nLuego, tienes la opción de tomar más cartas o quedarte, con el fin de que la suma de los valores de tus cartas den tan cerca\ncomo sea posible de 21, SIN sobrepasarlo. Si lo sobrepasas, pierdes automáticamente. Luego, el crupier tomará sus cartas:\nquien esté más cerca de 21 gana.\n")
        elif option == '12':
            print("\nPALABRA MEZCLADA: se te mostrarán una serie de palabras mezcladas, todas relacionadas con una categoría dada, \nque deberás desmezclar. Una vez consigas una palabra, introdúcela por teclado. ¡Cuidado con los errores ortográficos!\n")
        elif option == '13':
            print("\nNÚMERO ALEATORIO: se te pedirá que ingreses un número dentro de un rango de números. Luego, podrás usar UNA pista \npara saber si tu número estuvo muy o un poco por debajo o por arriba del número real.\n")
        else:
            break
        input("Presiona 'enter' para seguir.\n▶️ ")
   
def main():
    """Función main para el inicio del juego: contiene el menú principal de opciones.
    """
    players = {}
    players = player_functions.get_data_from_txt('registered_players.txt', players)

    print("\n", "BIENVENIDO A ✨ESCAPAMET✨".center(120, " "))
    print("¡Uno de los únicos juegos interactivos tipo escape-room ambientados en la Unimet!".center(120, " "))
    while True:
        print("\n","MENÚ PRINCIPAL".center(120, '~'))
        print("\nINGRESA:\n\t1. Para comenzar una nueva partida 🎮\n\t2. Para ver las instrucciones del juego 🤓\n\t3. Para ver los records 📈\n\t4. Para salir 😞\n")
        user_input = input(">")
        if user_input == '1':
            new_game(players)
            player_functions.load_data_to_txt('registered_players.txt', players)
        elif user_input == '2':
            instructions()
        elif user_input == '3':
            statistics.game_statistics(players)
        elif user_input == '4':
            print("\nAdiós 👋\n")
            break
        else:
            print("\nIngreso inválido")

if __name__ == '__main__':
    main()