import time, json, random, os
import colorama as cl
cl.init(convert=True)
g,r,cy,m,reset = cl.Fore.GREEN, cl.Fore.RED, cl.Fore.CYAN, cl.Fore.MAGENTA, cl.Fore.RESET # Defining Colors
location = os.path.join(os.path.dirname(__file__),'predictions.json')
def load_file(): # Just Rewriting predictions.json if it is corrupt!
    with open(location,'r+') as data:
        if os.stat(location).st_size == 0: # Check if File is Empty
            file = {"bad_predictions":{"X": [], "O": []}, "good_predictions":{"X": [], "O": []}}
        try:
            data_items = json.load(data)
            try:
                if type(data_items["bad_predictions"]) != dict: # Check Bad Values
                    data_items["bad_predictions"] = {"X": [], "O": []}
                data_bad_value = data_items["bad_predictions"]
            except KeyError:
                data_bad_value = {"X": [], "O": []}
                pass
            try:
                if type(data_items["good_predictions"]) != dict: # Check Good Values
                    data_items["good_predictions"] = {"X": [], "O": []}
                data_good_value = data_items["good_predictions"]
            except KeyError:
                data_good_value = {"X": [], "O": []}
                pass
            if set(["bad_predictions","good_predictions"]) != set(data_items.keys()): # Check Keys
                file = {"bad_predictions":data_bad_value, "good_predictions":data_good_value}
                data_items = file
            if set(["X","O"]) != set(data_items["bad_predictions"].keys()): # Check Sub Keys
                file = {"bad_predictions":{"X": [], "O": []}, "good_predictions":data_good_value}
            if set(["X","O"]) != set(data_items["good_predictions"].keys()): # Check Sub Keys
                file = {"bad_predictions":data_bad_value, "good_predictions":{"X": [], "O": []}}
            file = data_items
            if type(data_items["good_predictions"]["X"]) != list: # Check Sub Key Values
                data_items["good_predictions"]["X"] = []
            if type(data_items["good_predictions"]["O"]) != list: # Check Sub Key Values
                data_items["good_predictions"]["O"] = []
            if type(data_items["bad_predictions"]["X"]) != list: # Check Sub Key Values
                data_items["bad_predictions"]["X"] = []
            if type(data_items["bad_predictions"]["O"]) != list: # Check Sub Key Values
                data_items["bad_predictions"]["O"] = []
        except json.decoder.JSONDecodeError: # If file invalid, return default
            file = {"bad_predictions": {"X": [], "O": []}, "good_predictions": {"X": [], "O": []}}
        data.close()
    with open(location,'w') as data:
        json.dump(file,data) 
class gameplay: # Continue...  
    def __init__(self,a:list,b:list,c:list):
        self.a = a
        self.b = b
        self.c = c
    def bot(a:list,b:list,c:list,done_moves:list,bot_play:str=None,last_move:str=None,preference:bool=True):
        all_values = ['a1','a2','a3','b1','b2','b3','c1','c2','c3']
        for i in range(len(a)): # Change Game Board with Values (X, O)
            if not a[i].isspace():
                all_values.remove("a"+str(i+1))
            if not b[i].isspace():
                all_values.remove("b"+str(i+1))
            if not c[i].isspace():
                all_values.remove("c"+str(i+1))
        if preference: # Bot Prediction Bool
            count = 0
            while True:
                file = open(location,'r')
                data = json.load(file)
                if last_move != None:
                    for good_move in data["good_predictions"][bot_play]: # Check if Prediction in Good Moves
                        if set(done_moves) in set(good_move) and (good_move[[len(done_moves)]] not in done_moves):
                            return good_move[len(done_moves)-1] # Prediction
                    if data["bad_predictions"][bot_play] != [] and len(done_moves)>=2:
                        for bad_move in data["bad_predictions"][bot_play]:
                            try:
                                prediction = random.choice(all_values)
                                done_moves.append(prediction)
                            except IndexError:
                                done_moves.remove(prediction)
                                return None
                            done_moves,bad_move[:len(done_moves)], done_moves != bad_move[:len(done_moves)]
                            if done_moves != bad_move[:len(done_moves)]:
                                done_moves.remove(prediction)
                                return prediction
                            done_moves.remove(prediction)
                    else:
                        return random.choice(all_values)
                else:
                    count+=1
                if count >= 8 and prediction not in done_moves: # If Prediction in Bad Moves but no other alternative left
                    return prediction
                file.close()
        else:
            return all_values
    def gameplay(a,b,c,move,chance):
        try: # Update Game Board
            if 'a' in move:
                a[int(move[-1])-1] = chance
            if 'b' in move:
                b[int(move[-1])-1] = chance
            if 'c' in move:
                c[int(move[-1])-1] = chance
            return a,b,c
        except TypeError: # If Invalid Value return current a,b,c
            return a,b,c
    def check_win(a,b,c):
        for i in [0,1,2]:
            if a[i] == b[i] == c[i]: # If Vertical Win
                return a[i], ('a'+str(i+1), 'b'+str(i+1), 'c'+str(i+1))
        for i in [a,b,c]:
            if i[0]==i[1]==i[2]: # If Horizontal Win
                if i == a: # Return A Row
                    return i[0], ('a1','a2','a3')
                if i == b: # Return B Row
                    return i[0], ('b1','b2','b3')
                if i == c: # Return C Row
                    return i[0], ('c1','c2','c3')
        if a[0]==b[1]==c[2]: # If Diagonal Win - 1
            return b[1], ('a1','b2','c3')
        if a[-1]==b[1]==c[0]: # If Diagonal Win - 2
            return b[1], ('a3','b2','c1')
        return False, False # Else Return False
class tictactoe:
    cl.init(convert=True)
    os.system("cls" or "clear")
    def __init__(self):
        self.mode = None
    def welcome(self):
        cl.init(convert=True)
        os.system("cls" or "clear")
        print(cy+"""WELCOME TO THE TIC TAC TOE Game!
        
        Select A Mode:
        """)
    def select_mode(self):
        cl.init(convert=True)
        while self.mode not in ['1','2']:
            self.mode = input(f"{cy}Type {r}1{cy} for {r}singleplayer{cy} and {m}2{cy} for {m}multiplayer{cy}.\nPreference: ")
            if self.mode not in ['1','2']:
                print(r+"\nERROR! Enter one of the following values: 1, 2")
        return self.mode
    def board(self,a,b,c):
        return f"""{r} _______ _______ _______
|       |       |       |
|   {cy}{a[0]}{r}   |   {cy}{a[1]}{r}   |   {cy}{a[2]}{r}   |
|       |       |       |
|‾‾‾‾‾‾‾|‾‾‾‾‾‾‾|‾‾‾‾‾‾‾|
|   {cy}{b[0]}{r}   |   {cy}{b[1]}{r}   |   {cy}{b[2]}{r}   |
|       |       |       |
|‾‾‾‾‾‾‾|‾‾‾‾‾‾‾|‾‾‾‾‾‾‾|
|   {cy}{c[0]}{r}   |   {cy}{c[1]}{r}   |   {cy}{c[2]}{r}   |
|       |       |       |
 ‾‾‾‾‾‾‾ ‾‾‾‾‾‾‾ ‾‾‾‾‾‾‾"""+reset
    def instructions(self, type:str=f"{r}singeplayer"):
        cl.init(convert=True)
        os.system("cls" or "clear")
        print(f"{cy}Starting {type}{cy} game!"+reset)
        if type != f"{m}multiplayer":
            time.sleep(1)
            print(cy+"\nLoading bot",end="") # Animation Time
            time.sleep(1)
            print(".",end="")
            time.sleep(1)
            print(".",end="")
            time.sleep(1)
            print(".\n"+reset,end="")
            time.sleep(0.5)
            print(g+"\nBot successfully loaded!"+reset)
            time.sleep(2)
        print(f"""{cy}Here's the set of instructions on how to play:

The board is of a 3x3 width. The row-column namings are as follows:
Row {m}1{cy}: {g}a{cy}   |   Column {m}1{cy}: {g}1{cy}
Row {m}2{cy}: {g}b{cy}   |   Column {m}2{cy}: {g}2{cy}
Row {m}3{cy}: {g}c{cy}   |   Column {m}3{cy}: {g}3{cy}

Example: Typing {m}a1{cy} would give you this:
 {r}_______ _______ _______
|       |       |       |
|   {cy}X{r}   |       |       |
|       |       |       |
|‾‾‾‾‾‾‾|‾‾‾‾‾‾‾|‾‾‾‾‾‾‾|
|       |       |       |
|       |       |       |
|‾‾‾‾‾‾‾|‾‾‾‾‾‾‾|‾‾‾‾‾‾‾|
|       |       |       |
|       |       |       |
 ‾‾‾‾‾‾‾ ‾‾‾‾‾‾‾ ‾‾‾‾‾‾‾"""+reset)
    def get_move(self, all_slots, available_slots, done_moves, a, b, c, player:str=f"{cy}Type your input: {r}"):
        count = 0
        while True:
            if count >=5: # Tip to print board when more than 5+ invalid args entered
                print(f"{m}Protip:\n{cy}You can type {m}board{cy} to see the board!\n")
                count = 0
                time.sleep(0.75)
            move = input(player)
            if move.casefold() == 'available':
                print(f"{cy}Here's the list of all available slots: {r}{', '.join(available_slots)}{cy}.\n")
                count+=1
            elif move.casefold() == "slots":
                print(f"{cy}Here's the list of all possible slots: {r}{', '.join(all_slots)}{cy}.\n")
                count+=1
            elif move.casefold() == "board":
                print(f"\n{cy}Here's the board:")
                print(self.board(a,b,c))
                count=0
            elif move not in all_slots:
                print(f"{r}ERROR! Please enter a correct value, you entered {g+move+r}! Type {g}slots{r} to see all slot names!\n")
                count+=1
            elif move not in available_slots or move in done_moves:
                print(f"{r}ERROR! Please enter a valid value, the value {g+move+r} is already filled! Type {g}available{r} to see all available slots!\n")
                count+=1
            else:
                return move
    def singeplayer(self, bot_scores:list=[(0, 0), (0, 0), 0]):
        cl.init(convert=True)
        self.instructions()
        a = [' ',' ',' ']
        b = [' ',' ',' ']
        c = [' ',' ',' ']
        move_history, last_move, done_moves, move_count = [], None, [], 0
        type = 0 # Define Type to ignore "reference before assignment" error
        while type not in ['1','2']:
            cl.init(convert=True)
            type = input(f"{cy}Type {r}1{cy} if you would like to play as {r}X{cy} and {m}2{cy} for {m}O{cy}.\nPreference: ")
            if type not in ['1','2']:
                print(f"\n{r}ERROR! Enter either {m}1{r} or {m}2{reset}")
        if type == '1':
            cl.init(convert=True)
            os.system("cls" or "clear")
            print(f"{cy}You have selected to play as {r}X{cy}!") 
            bot_play = 'O'
        else:
            print(f"{cy}You have selected to play as {m}O{cy}!")
            bot_play = 'X'
        while True:
            all_slots, available_slots = ['a1','a2','a3','b1','b2','b3','c1','c2','c3'], gameplay.bot(a,b,c,done_moves,bot_play,preference=False)
            if type=="1": # If user is X
                move = self.get_move(all_slots, available_slots, done_moves, a,b,c)
                done_moves.append(move)
                move_history.append(move)
                move_count += 1
                a,b,c = gameplay.gameplay(a,b,c,move,'X') # Update Game Board
                last_move = move_history[-1] # Get Last Move for bot prediction
                winner, win_area = gameplay.check_win(a,b,c)
                if winner not in ['X','O']: # Check Win
                    if move_count < 9: # Check if Round Over
                        print(f"{g}Bot is thinking",end="") # Animation Time
                        time.sleep(0.75)
                        print(".",end="")
                        time.sleep(0.75)
                        print(".",end="")
                        time.sleep(0.75)
                        print(".",end="")
                        time.sleep(0.75)
                        prediction = gameplay.bot(a,b,c,done_moves,bot_play,last_move) # Get Prediction
                        done_moves.append(prediction)
                        move_history.append(prediction) # Append Moves
                        move_count += 1
                        a,b,c = gameplay.gameplay(a,b,c,prediction,'O') # Update Game Board
                        print(f"\n{r}Bot selected: {cy}{prediction}")
                        print(self.board(a,b,c))
                winner, win_area = gameplay.check_win(a,b,c)
            elif type=="2": # If user is O
                print(f"{g}Bot is thinking",end="") # Animation Time
                time.sleep(0.75)
                print(".",end="")
                time.sleep(0.75)
                print(".",end="")
                time.sleep(0.75)
                print(".",end="")
                time.sleep(0.75)
                prediction = gameplay.bot(a,b,c,done_moves,bot_play,last_move) # Get Prediction
                done_moves.append(prediction)
                move_history.append(prediction)
                move_count += 1
                last_move = move_history[-1]
                a,b,c = gameplay.gameplay(a,b,c,prediction,'X') # Update Game Board
                print(f"\n{r}Bot selected: {cy}{prediction}")
                print(self.board(a,b,c))
                winner, win_area = gameplay.check_win(a,b,c)
                if winner not in ['X','O']: # Check Win
                    if move_count < 9: # Check if Round Over
                        move = self.get_move(all_slots, available_slots, done_moves, a, b, c)
                        done_moves.append(move)
                        move_history.append(move) # Append Moves
                        move_count += 1
                        last_move = move_history[-1] # Get Last Move for bot prediction
                        a,b,c = gameplay.gameplay(a,b,c,move,'O') # Update Game Board
                winner, win_area = gameplay.check_win(a,b,c)
            if winner in ['X','O']:
                if bot_play == 'X':
                    del move_history[0]
                if (winner == 'O' and type == '2') or (winner == 'X' and type == '1'):
                    if type == '1':
                        bot_scores[0][0]+=1
                    elif type == '2':
                        bot_scores[0][1]+=1
                    for i in win_area: # Color the winning part
                        if 'a' in i:
                            a[int(i[-1])-1] = g+a[int(i[-1])-1]
                        if 'b' in i:
                            b[int(i[-1])-1] = g+b[int(i[-1])-1]
                        if 'c' in i:
                            c[int(i[-1])-1] = g+c[int(i[-1])-1]
                    print(self.board(a,b,c))
                    print(f"{g}You WON! Well played!")
                    file = open(location,'r')
                    data = json.load(file)
                    file.close()
                    if move_history in data["good_predictions"][bot_play]:
                        data["good_predictions"][bot_play].remove(move_history)
                    if move_history not in data["bad_predictions"][bot_play]:
                        data["bad_predictions"][bot_play].append(move_history)
                                            
                else:
                    if type == '1':
                        bot_scores[1][0]+=1
                    elif type == '2':
                        bot_scores[1][1]+=1
                    for i in win_area: # Color the winning part
                        if 'a' in i:
                            a[int(i[-1])-1] = g+a[int(i[-1])-1]
                        if 'b' in i:
                            b[int(i[-1])-1] = g+b[int(i[-1])-1]
                        if 'c' in i:
                            c[int(i[-1])-1] = g+c[int(i[-1])-1]
                    print(self.board(a,b,c))
                    print(f"{r} You LOST! Better luck next time!")
                    file = open(location,'r')
                    data = json.load(file)
                    file.close()
                    if move_history in data["bad_predictions"][bot_play]:
                        data["bad_predictions"][bot_play].remove(move_history)
                    if move_history not in data["good_predictions"][bot_play]:
                        data["good_predictions"][bot_play].append(move_history)                        
                file = open(location,'w')
                json.dump(data,file)
                file.close()
                return bot_scores
            if (' ' in a) or (' ' in b) or (' ' in c): # Check if game draw
                pass    
            else:
                print(self.board(a,b,c))
                print(f"{cy}Game DRAW!")
                bot_scores[2]+=1
                return bot_scores
    def multiplayer(self, player_scores:list=[0, 0, 0]):
        cl.init(convert=True)
        a = [' ',' ',' ']
        b = [' ',' ',' ']
        c = [' ',' ',' ']
        move_history, done_moves, move_count = [], [], 0
        player_1 = str(input(f"\n{cy}Player 1 Name: {r}"))
        while True:
            player_2 = str(input(f"{cy}Player 2 Name: {m}"))
            if player_2 != player_1:
                break
            else:
                print(f"\n{r}ERROR! Both players can't have the same name!\n")
        self.instructions(f"{m}multiplayer")
        while True:
            all_slots, available_slots = ['a1','a2','a3','b1','b2','b3','c1','c2','c3'], gameplay.bot(a,b,c,done_moves,preference=False)
            if move_count > 0:
                print(self.board(a,b,c))
            move_1 = self.get_move(all_slots, available_slots, done_moves, a,b,c, f"{r}{player_1} (X): {cy}")
            done_moves.append(move_1)
            move_count += 1
            a,b,c = gameplay.gameplay(a,b,c,move_1,'X') # Update Game Board
            winner, win_area = gameplay.check_win(a,b,c) 
            if winner not in ['X','O']: # Check Win
                if move_count < 9: # Check if Round Over
                    print(self.board(a,b,c))
                    move_2 = self.get_move(all_slots, available_slots, done_moves, a,b,c, f"{m}{player_2} (O): {cy}",)
                    done_moves.append(move_2)
                    move_count += 1
                    a,b,c = gameplay.gameplay(a,b,c,move_2,'O') # Update Game Board
                    winner, win_area = gameplay.check_win(a,b,c)
            if winner in ['X','O']:
                for i in win_area: # Color the winning part
                    if 'a' in i:
                        a[int(i[-1])-1] = g+a[int(i[-1])-1]
                    if 'b' in i:
                        b[int(i[-1])-1] = g+b[int(i[-1])-1]
                    if 'c' in i:
                        c[int(i[-1])-1] = g+c[int(i[-1])-1]
                print(self.board(a,b,c))
                if winner == 'X': # Player 1 Win
                    print(f"{g+player_1+r} (X){g} Won! Well played!")
                    player_scores[0]+=1
                    return (player_1, player_2, player_scores)
                elif winner == 'O': # Player 2 Win
                    print(f"{g+player_2+m} (O){g} Won! Well played!")
                    player_scores[1]+=1
                    return (player_1, player_2, player_scores)
            if (' ' in a) or (' ' in b) or (' ' in c): # Check if game draw
                pass    
            else:
                print(self.board(a,b,c))
                print(f"{cy}Game DRAW!")
                player_scores[2]+=1
                return (player_1, player_2, player_scores)

if __name__ == "__main__": # Making the whole thing function!
    try:
        play_again, player_scores, bot_scores = '1', [0, 0, 0], [[0, 0], [0, 0], 0]
        while play_again != 2:
            if play_again == '1':
                load_file()
                ttt = tictactoe() # Instance
                ttt.welcome()
                mode = ttt.select_mode()
                if mode == '1':
                    bot_scores = ttt.singeplayer(bot_scores)
                    player_x, player_o = bot_scores[0]
                    draw = bot_scores[2]
                    bot_x, bot_o = bot_scores[1]
                    player_wins = player_x+player_o
                    bot_wins = bot_x+bot_o
                    total = player_wins+bot_wins+draw
                    time.sleep(1)
                    print(f"{cy}Scores:\n\n{r}You: {g}{player_wins}\n{r}Wins as X: {g}{player_x}\n{r}Wins as {m}O{r}: {g}{player_o}\n\n{m}Bot: {g}{bot_wins}\n{r}Wins as X: {g}{bot_x}\n{r}Wins as {m}O{r}: {g}{bot_o}\n{cy}Draws: {g}{draw}\n{r}Total: {g}{total}\n")
                    time.sleep(0.5)
                    play_again = input(f"\n{cy}Type {r}1{cy} if you want to play again!\nInput: {r}")
                elif mode == '2':
                    player_scores = ttt.multiplayer(player_scores)
                    player_1, player_2 = player_scores[0], player_scores[1]
                    one, two, draw = player_scores[2]
                    time.sleep(1)
                    print(f"{cy}Scores:\n\n{r+player_1} (X): {g}{one}\n{m+player_2} (O): {g}{two}\n{cy}Draws: {g}{draw}\n{r}Total: {g}{one+two+draw}")
                    time.sleep(0.5)
                    play_again = input(f"\n{cy}Type {r}1{cy} if you want to play again!\nInput: {r}")
            else:
                break
    except:
        print(f"\n{r}Waves Off!")
        exit()