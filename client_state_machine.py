"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
from guitest import *
import json

class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s
        self.handcard = ""
        self.give = 0
        self.wait = True
        self.init_window = True
        self.cardgame = True
        self.firstgame = True
        self.finish =True
                    
    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = json.dumps({"action":"connect", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"search", "target":term}))
                    search_rslt = json.loads(myrecv(self.s))["results"][1:].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p' and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"][1:].strip()
                    if (len(poem) > 0):
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.peer = peer_msg["from"]
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer
                    self.out_msg += '. Chat away!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.state = S_CHATTING
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Start Gaming
#
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        elif self.state == S_GAMING:
            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)

                #系统消息，玩家消息
                if peer_msg["action"] == "server_msg":
                    print("<INFO>\n",peer_msg["info"],"\n<INFO>")
                    
                #receive server variable at the end of the game
                if peer_msg["action"] == "gameinfodic":
                    gameinfo = peer_msg["info"]

                    #update the gui
                    if self.me in gameinfo[0]['winner']:
                        self.give = 4
                        self.cardgame.c_prompt(self.give)
                    else:
                        self.give = 5
                        self.cardgame.c_prompt(self.give)

                    self.init_window.update()

                    allcards=[]
                    for i in gameinfo:
                        allcards.append(i['handcard'][0])
                        allcards.append(i['handcard'][1])

                    self.cardgame.show(allcards[0],allcards[1],allcards[2],allcards[3],allcards[4],
                                       allcards[5],allcards[6],allcards[7],allcards[8],allcards[9])

                    for dic in  gameinfo:
                        if dic['player']== self.me:
                            money = dic['money']
                            self.cardgame.c_mine(money)
                            self.cardgame.c_total(gameinfo[0]['jackpot'])
                            self.cardgame.c_high(gameinfo[0]['highest_bet'])

                    self.init_window.update()
                    
                    

                if peer_msg["action"] == "game" and peer_msg["ready"] == "allready":
                    mysend(self.s, json.dumps({"action":"game", "player":self.me, "ready":"allready"}))
                    print("NEXT ROUND START!")

                #一轮看牌以及盲注
                elif peer_msg["action"] == "game" and peer_msg["ready"] == "firstbet":
                    if self.init_window == True:
                        self.init_window = Tk()

                    if self.cardgame == True:
                        self.cardgame = MY_GUI(self.init_window)

                    if self.firstgame == True:
                        #initial the gui
                    
    
                        self.cardgame.set_init_window()
                        self.cardgame.set_buttons()
                        self.cardgame.fivecards()
                        self.cardgame.players()
                        self.cardgame.blank()
                        self.cardgame.total()
                        self.cardgame.mine()
                        self.cardgame.prompt()
                        self.cardgame.entry()
                        self.cardgame.high()
                        self.firstgame = False
                        self.cardgame.my_cards(peer_msg['handcard'][0], peer_msg['handcard'][1])

                        self.init_window.update()
                    else:
                        self.cardgame.restart()
                        self.cardgame.c_high(0)
                        self.cardgame.c_total(0)
                        self.cardgame.c_my_cards(peer_msg['handcard'][0], peer_msg['handcard'][1])
                        self.give = 1
                        self.cardgame.c_prompt(self.give)
                        self.init_window.update()
                    
                    print("\nmoney",peer_msg["money"],"\nleast bet", peer_msg["least_bet"],"\nhandcard",peer_msg["handcard"])
                    money = peer_msg["money"]
                    bet=100

                    self.wait = True

                    while self.wait == True:
                        self.wait = self.cardgame.wait()
                        print(self.wait)
                        self.init_window.update()
                        if self.wait == False:
                            bet = self.cardgame.back()
                            if bet.isdigit() and int(bet) >= peer_msg['least_bet']:
                                bet = int(bet)
                                break
                            else:

                                self.give = 3
                                self.wait = True
                                self.cardgame.c_prompt(self.give)
                                self.init_window.update()
                        '''while bet < peer_msg["least_bet"] and bet != 0:
                        bet = input("Your Prefered Bet For Your Card?\n")'''





                            
                    self.give =2
                    self.cardgame.c_prompt(self.give)
                    self.init_window.update()
                    mysend(self.s, json.dumps({"action": "game", "ready": "firstbet", "player": self.me, "bet": bet}))
                    
                    
                        
                        



                if peer_msg["action"] == "game" and peer_msg["ready"] == "secondbet":
                    print("\nmoney",peer_msg["money"],"\nHighest Bet Last Round:", peer_msg["least_bet"])
                    money = peer_msg["money"]
                    bet=100
                    

                    #update the gui
                    self.give = 1
                    self.cardgame.c_prompt(self.give)
                    self.cardgame.c_mine(peer_msg['money'])
                    self.cardgame.c_high(peer_msg['least_bet'])
                    self.cardgame.c_total(peer_msg['jackpot'])
                    self.cardgame.round_one(peer_msg['served_cards'][0],peer_msg['served_cards'][1],peer_msg['served_cards'][2])
                    self.init_window.update()
                    

                    self.wait = True

                    while self.wait == True:
                        self.wait = self.cardgame.wait()
                        self.init_window.update()
                        if self.wait == False:
                            bet = self.cardgame.back()
                            if bet.isdigit() and int(bet) >= peer_msg['least_bet']:
                                bet = int(bet)
                                break
                            else:

                                self.give = 3
                                self.wait = True
                                self.cardgame.c_prompt(self.give)
                                self.init_window.update()
                        '''while bet < peer_msg["least_bet"] and bet != 0:
                        bet = input("Your Prefered Bet For Your Card?\n")'''

                    self.give = 2
                    self.cardgame.c_prompt(self.give)
                    self.init_window.update()
                    mysend(self.s,json.dumps({"action": "game", "ready": "secondbet", "player": self.me, "bet": bet}))


                if peer_msg["action"] == "game" and peer_msg["ready"] == "thirdbet":
                    print("\nmoney",peer_msg["money"],"\nHighest Bet Last Round:", peer_msg["least_bet"])
                    money = peer_msg["money"]
                    bet = 100

                    #update the gui
                    self.give = 1
                    self.cardgame.c_prompt(self.give)
                    self.cardgame.c_mine(peer_msg['money'])
                    self.cardgame.c_high(peer_msg['least_bet'])
                    self.cardgame.c_total(peer_msg['jackpot'])
                    self.cardgame.round_two(peer_msg['served_cards'][3])
                    self.init_window.update()
                    


                    
                    self.wait = True

                    while self.wait == True:
                        self.wait = self.cardgame.wait()
                        self.init_window.update()
                        if self.wait == False:
                            bet = self.cardgame.back()
                            if bet.isdigit() and int(bet) >= peer_msg['least_bet']:
                                bet = int(bet)
                                break
                            else:

                                self.give = 3
                                self.wait = True
                                self.cardgame.c_prompt(self.give)
                                self.init_window.update()
                        '''while bet < peer_msg["least_bet"] and bet != 0:
                        bet = input("Your Prefered Bet For Your Card?\n")'''

                    self.give = 2
                    self.cardgame.c_prompt(self.give)
                    self.init_window.update()
                    mysend(self.s,json.dumps({"action": "game", "ready": "thirdbet", "player": self.me, "bet": bet}))


                if peer_msg["action"] == "game" and peer_msg["ready"] == "fourthbet":
                    print("\nmoney",peer_msg["money"],"\nHighest Bet Last Round:", peer_msg["least_bet"])
                    money = peer_msg["money"]
                    bet = 100

                    
                    #update the gui
                    self.give = 1
                    self.cardgame.c_prompt(self.give)
                    self.cardgame.c_mine(peer_msg['money'])
                    self.cardgame.c_high(peer_msg['least_bet'])
                    self.cardgame.c_total(peer_msg['jackpot'])
                    self.cardgame.round_three(peer_msg['served_cards'][4])
                    self.init_window.update()
                    


                    
                    self.wait = True

                    while self.wait == True:
                        self.wait = self.cardgame.wait()
                        self.init_window.update()
                        if self.wait == False:
                            bet = self.cardgame.back()
                            if bet.isdigit() and int(bet) >= peer_msg['least_bet']:
                                bet = int(bet)
                                break
                            else:

                                self.give = 3
                                self.wait = True
                                self.cardgame.c_prompt(self.give)
                                self.init_window.update()
                        '''while bet < peer_msg["least_bet"] and bet != 0:
                        bet = input("Your Prefered Bet For Your Card?\n")'''

                    self.give = 2
                    self.cardgame.c_prompt(self.give)
                    self.init_window.update()
                    mysend(self.s,json.dumps({"action": "game", "ready": "final", "player": self.me, "bet": bet}))






        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":my_msg}))

                if my_msg == "@game":
                    ready = "0"
                    mysend(self.s, json.dumps({"action": "game", "ready":"request", "player":self.me}))
                    print("Waiting other players to ready!")
                    mysend(self.s, json.dumps({"action": "game", "player":self.me, "ready": True}))


                elif my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''

            if len(peer_msg) > 0:    # peer's stuff, coming in
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"

                elif peer_msg["action"] == "game" and peer_msg["ready"] == "request":
                    print(peer_msg)
                    ready = print((peer_msg["from"] + " invited you to play a game, Are you ready to play a Taxes Poker game?"))
                    print("Waiting other players to ready!")
                    mysend(self.s, json.dumps({"action": "game", "player": self.me, "ready": True}))


                elif peer_msg["action"] == "game" and peer_msg["ready"] == "allready":
                    print("Game Start!")
                    mysend(self.s, json.dumps({"action":"game", "player":self.me, "ready":"allready"}))
                    self.state = S_GAMING
                    print("send a start message to server")




                elif peer_msg["action"] == "disconnect":
                    self.state = S_LOGGEDIN
                else:
                    self.out_msg += peer_msg["from"] +": "+ peer_msg["message"]


            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg
