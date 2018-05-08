"""
Created on Tue Jul 22 00:47:05 2014

@author: alina, zzhang
"""

import time
import socket
import select
import sys
import string
import indexer_student
import json
import pickle as pkl
from chat_utils import *
import chat_group as grp
from dealing import *
from judgement import *

ready_player = 0

class Server:
    def __init__(self):
        self.new_clients = [] #list of new sockets of which the user id is not known
        self.logged_name2sock = {} #dictionary mapping username to socket
        self.logged_sock2name = {} # dict mapping socket to user name
        self.all_sockets = []
        self.group = grp.Group()
        #start server
        self.server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(SERVER)
        self.server.listen(5)
        self.all_sockets.append(self.server)
        #initialize past chat indices
        self.indices={}
        # sonnet
        self.sonnet_f = open('AllSonnets.txt.idx', 'rb')
        self.sonnet = pkl.load(self.sonnet_f)
        self.sonnet_f.close()
        #following stores the data for game
        self.shuffled = False
        self.gameinfo = [] #dictionaries store info of the game players
        self.bet = 200
        self.jackpot = 0
        self.name_list = []
        self.served_cards = []
        self.cards_count = 3
        self.player_count = 0



    def new_client(self, sock):
        #add to all sockets and to new clients
        print('new client...')
        sock.setblocking(0)
        self.new_clients.append(sock)
        self.all_sockets.append(sock)

    def login(self, sock):
        #read the msg that should have login code plus username
        try:
            msg = json.loads(myrecv(sock))
            if len(msg) > 0:

                if msg["action"] == "login":
                    name = msg["name"]
                    if self.group.is_member(name) != True:
                        #move socket from new clients list to logged clients
                        self.new_clients.remove(sock)
                        #add into the name to sock mapping
                        self.logged_name2sock[name] = sock
                        self.logged_sock2name[sock] = name
                        #load chat history of that user
                        if name not in self.indices.keys():
                            try:
                                self.indices[name]=pkl.load(open(name+'.idx','rb'))
                            except IOError: #chat index does not exist, then create one
                                self.indices[name] = indexer_student.Index(name)
                        print(name + ' logged in')
                        self.group.join(name)
                        mysend(sock, json.dumps({"action":"login", "status":"ok"}))
                    else: #a client under this name has already logged in
                        mysend(sock, json.dumps({"action":"login", "status":"duplicate"}))
                        print(name + ' duplicate login attempt')
                else:
                    print ('wrong code received')
            else: #client died unexpectedly
                self.logout(sock)
        except:
            self.all_sockets.remove(sock)

    def logout(self, sock):
        #remove sock from all lists
        name = self.logged_sock2name[sock]
        pkl.dump(self.indices[name], open(name + '.idx','wb'))
        del self.indices[name]
        del self.logged_name2sock[name]
        del self.logged_sock2name[sock]
        self.all_sockets.remove(sock)
        self.group.leave(name)
        sock.close()

#==============================================================================
# main command switchboard
#==============================================================================
    def handle_msg(self, from_sock):
        #read msg code

        msg = myrecv(from_sock)
        if len(msg) > 0:
#==============================================================================
# handle connect request this is implemented for you
#==============================================================================
            msg = json.loads(msg)
            if msg["action"] == "connect":
                to_name = msg["target"]
                from_name = self.logged_sock2name[from_sock]
                if to_name == from_name:
                    msg = json.dumps({"action":"connect", "status":"self"})
                # connect to the peer
                elif self.group.is_member(to_name):
                    to_sock = self.logged_name2sock[to_name]
                    self.group.connect(from_name, to_name)
                    the_guys = self.group.list_me(from_name)
                    msg = json.dumps({"action":"connect", "status":"success"})
                    for g in the_guys[1:]:
                        to_sock = self.logged_name2sock[g]
                        mysend(to_sock, json.dumps({"action":"connect", "status":"request", "from":from_name}))
                else:
                    msg = json.dumps({"action":"connect", "status":"no-user"})
                mysend(from_sock, msg)
#==============================================================================
# handle message exchange: IMPLEMENT THIS
#==============================================================================
            elif msg["action"] == "exchange":
                from_name = self.logged_sock2name[from_sock]
                # Finding the list of people to send to
                # and index message
                self.indices[from_name].add_msg_and_index(text_proc(msg["message"], from_name))
                the_guys = self.group.list_me(from_name)[1:]
                for g in the_guys:
                    to_sock = self.logged_name2sock[g]
                    result = msg["message"]
                    self.indices[g].add_msg_and_index(text_proc(msg["message"], from_name))
                    mysend(to_sock, json.dumps({"action":"exchange", "message":result, "from": from_name}))

#==============================================================================
# the "from" guy has had enough (talking to "to")!
#==============================================================================
            elif msg["action"] == "disconnect":
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                self.group.disconnect(from_name)
                the_guys.remove(from_name)
                if len(the_guys) == 1:  # only one left
                    g = the_guys.pop()
                    to_sock = self.logged_name2sock[g]
                    mysend(to_sock, json.dumps({"action":"disconnect"}))
#==============================================================================
#                 listing available peers: IMPLEMENT THIS
#==============================================================================
            elif msg["action"] == "list":
                from_name = self.logged_sock2name[from_sock]
                all_peers = self.group.list_all(from_name)
                mysend(from_sock, json.dumps({"action":"list", "results":all_peers}))
#==============================================================================
#             retrieve a sonnet : IMPLEMENT THIS
#==============================================================================
            elif msg["action"] == "poem":
                number = int(msg["target"])
                from_name = self.logged_sock2name[from_sock]
                user = indexer_student.PIndex("AllSonnets.txt")
                poem = " ".join(user.get_poem(number))
                print('here:\n', poem)
                mysend(from_sock, json.dumps({"action":"poem", "results": poem}))
#==============================================================================
#                 time
#==============================================================================
            elif msg["action"] == "time":
                ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
                mysend(from_sock, json.dumps({"action":"time", "results":ctime}))
#==============================================================================
#                 search: : IMPLEMENT THIS
#==============================================================================
            elif msg["action"] == "search":
                # get search search_rslt
                from_name = self.logged_sock2name[from_sock]
                #search_rslt = "needs to use self.indices search to work"
                term = msg["target"]
                search_rslt = "".join(self.indices[from_name].search(term))

                print('server side search: ' + search_rslt)
                mysend(from_sock, json.dumps({"action":"search", "results":search_rslt}))

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#             Start a Texas Poker Game among all people in the chat room
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
            elif msg["action"] == "game" and msg["ready"] == "request":
                global ready_player
                print("ServerSide", msg["player"], "wants to play a game!" )
                from_name = self.logged_sock2name[from_sock]
                # Finding the list of people to send to
                the_guys = self.group.list_me(from_name)[1:]
                for g in the_guys:
                    to_sock = self.logged_name2sock[g]
                    mysend(to_sock, json.dumps({"action": "game", "ready":"request", "from": from_name}))


            elif msg["action"] == "game" and msg["ready"] == True:
                global ready_player
                ready_player += 1
                print("ServerSide,",msg["player"], "is ready")
                print(ready_player,"/",len(self.group.list_me(msg["player"])))
                if ready_player == len(self.group.list_me(msg["player"])):
                        from_name = self.logged_sock2name[from_sock]
                        the_guys = self.group.list_me(from_name)
                        for g in the_guys:
                            to_sock = self.logged_name2sock[g]
                            mysend(to_sock, json.dumps({"action": "game","ready":"allready","from":from_name}))

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

            elif msg["action"] == "game" and msg["ready"] == "allready":
                print("game, allready run judge shuffled or not")

                # 这保证了只发一遍牌
                if self.shuffled == False:
                    name_list = self.group.list_me(msg["player"])
                    self.shuffled = True
                    random.shuffle(card)
                    self.served_cards = card[-6:-1]
                    print(self.served_cards)
                    len_namelist = len(name_list)
                    card_list = []
                    for i in range(0,len_namelist):
                        card_list.append([card[2*i],card[2*i+1]])
                    print(card_list)
                    print("card list synthesized")
                    self.name_list = name_list
                    # this defines a starter
                    self.round_starter = [self.name_list[0], 0]

                    for n in name_list:
                        if len(self.gameinfo) <= len(name_list):
                            self.gameinfo.append({'player':n, 'money':10000, "winner":"", 'handcard':card_list[name_list.index(n)]})
                        else:
                            for dics in self.gameinfo:
                                if dics["player"] == n:
                                    dics["handcard"]:card_list[name_list.index(n)]

                        for dic in self.gameinfo:
                            if dic["player"] == n:
                                money = dic["money"]

                        to_sock = self.logged_name2sock[n]
                        mysend(to_sock,json.dumps({"action":"game", "ready":"firstbet","handcard":card_list[name_list.index(n)],\
                                                   "money":money,"least_bet":200}))
                    print("player",n,"handcard",card_list[name_list.index(n)])
                else:
                    pass


            elif msg["action"] == "game" and msg["ready"] == "giveup":
                for info_dict in self.gameinfo:
                    if info_dict["player"] == msg["player"]:
                        info_dict["winner"] = "giveup"
                self.name_list.remove(msg["player"])
                print("A player has given up", self.name_list)

            elif msg["action"] == "game" and msg["ready"] == "firstbet":
                for info_dict in self.gameinfo:
                    if info_dict["player"] == msg["player"]:
                        info_dict["money"] -= msg["bet"]

                self.jackpot += msg["bet"]
                self.player_count += 1
                if self.bet <= msg["bet"]:
                    self.bet = msg["bet"]
                to_sock = self.logged_name2sock[msg["player"]]
                mysend(to_sock, json.dumps({"action": "server_msg", "info": ("Round finished, JACKPOT:\n" + "   " \
                                                                             + str(self.jackpot) + "\n3 of 5 served cards:\n" \
                                                                             + str(self.served_cards[:-2]))}))
                if self.player_count == len(self.name_list):
                    self.player_count = 0
                    for n in self.name_list:
                        to_sock = self.logged_name2sock[n]
                        for dic in self.gameinfo:
                            if dic["player"] == n:
                                money = dic["money"]
                        mysend(to_sock,json.dumps({"action":"game","ready":"secondbet","money":money,"least_bet":self.bet}))

            elif msg["action"] == "game" and msg["ready"] == "secondbet":
                for info_dict in self.gameinfo:
                    if info_dict["player"] == msg["player"]:
                        info_dict["money"] -= (msg["bet"] - self.bet)
                self.jackpot += (msg["bet"] - self.bet)
                self.player_count += 1
                if self.bet <= msg["bet"]:
                    self.bet = msg["bet"]
                to_sock = self.logged_name2sock[msg["player"]]
                mysend(to_sock, json.dumps({"action": "server_msg", "info": ("Round finished, JACKPOT:\n" + "   " \
                                                                             + str(self.jackpot) + "\n4 of 5 served cards:\n" \
                                                                             + str(self.served_cards[:-1]))}))
                if self.player_count == len(self.name_list):
                    self.player_count = 0
                    for n in self.name_list:
                        to_sock = self.logged_name2sock[n]
                        for dic in self.gameinfo:
                            if dic["player"] == n:
                                money = dic["money"]
                        print({"action": "game", "ready": "thirdbet", "money": money, "least_bet": self.bet})
                        mysend(to_sock, json.dumps({"action": "game", "ready": "thirdbet", "money": money, "least_bet": self.bet}))


            elif msg["action"] == "game" and msg["ready"] == "thirdbet":
                for info_dict in self.gameinfo:
                    if info_dict["player"] == msg["player"]:
                        info_dict["money"] -= (msg["bet"] - self.bet)
                self.jackpot += (msg["bet"] - self.bet)
                self.player_count += 1
                if self.bet <= msg["bet"]:
                    self.bet = msg["bet"]
                to_sock = self.logged_name2sock[msg["player"]]
                mysend(to_sock, json.dumps({"action": "server_msg", "info": ("Round finished, JACKPOT:\n" + "   " \
                                                                             + str(self.jackpot) + "\n5 of 5 served cards:\n" \
                                                                             + str(self.served_cards))}))
                if self.player_count == len(self.name_list):
                    self.player_count = 0
                    for n in self.name_list:
                        to_sock = self.logged_name2sock[n]
                        for dic in self.gameinfo:
                            if dic["player"] == n:
                                money = dic["money"]
                        mysend(to_sock, json.dumps({"action": "game", "ready": "fourthbet", "money": money, "least_bet": self.bet}))

            elif msg["action"] == "game" and msg["ready"] == "final":
                for info_dict in self.gameinfo:
                    if info_dict["player"] == msg["player"]:
                        info_dict["money"] -= (msg["bet"] - self.bet)
                self.jackpot += (msg["bet"] - self.bet)
                self.player_count += 1
                if self.bet <= msg["bet"]:
                    self.bet = msg["bet"]
                to_sock = self.logged_name2sock[msg["player"]]
                mysend(to_sock, json.dumps({"action": "server_msg","info":"Waiting other players to FINISH their last raise"}))

                if self.player_count == len(self.name_list):
                    self.player_count = 0
                    winners_candidate = []
                    for info_dict in self.gameinfo:
                        if info_dict["winner"] != "giveup":
                            winners_candidate.append(info_dict)
                        else:
                            info_dict["winner"] = ""
                    print(winners_candidate)
                    #print(winner)
                    winners,self.served_cards = find_winner(winners_candidate, self.served_cards)
                    winner = winners[0]["winner"]
                    print(winner)
                    for n in self.name_list:
                        if winner == n:
                            for info_dict in self.gameinfo:
                                if info_dict["player"] == n:
                                    info_dict["money"] += self.jackpot
                                    money = info_dict.money
                    self.name_list = []
                    self.jackpot = 0
                    self.bet = 200
                    self.cards_count = 3
                    mysend(to_sock, json.dumps({"action": "server_msg","info":("The Winner is " + winner+ "\nAsset: " + str(money))}))











#==============================================================================
#                 the "from" guy really, really has had enough
#==============================================================================

        else:
            #client died unexpectedly
            self.logout(from_sock)

#==============================================================================
# main loop, loops *forever*
#==============================================================================
    def run(self):
        print ('starting server...')
        while(1):
           read,write,error=select.select(self.all_sockets,[],[])
           print('checking logged clients..')
           for logc in list(self.logged_name2sock.values()):
               if logc in read:
                   self.handle_msg(logc)
           print('checking new clients..')
           for newc in self.new_clients[:]:
               if newc in read:
                   self.login(newc)
           print('checking for new connections..')
           if self.server in read :
               #new client request
               sock, address=self.server.accept()
               self.new_client(sock)


def main():
    server=Server()
    server.run()


main()
