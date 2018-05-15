from tkinter import *
import hashlib

class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name
        self.total_money = StringVar()
        self.my_money = StringVar()
        self.prompt_words = StringVar()
        self.highest = StringVar()
        self.test = 0
        self.re = '0'
        self.waiting = True
        self.my_already = 0
        self.pic = PhotoImage(file=r"img/back.png")
        self.ppic = PhotoImage(file=r"img/back.png")
        


    #settings
    def set_init_window(self):
        self.init_window_name.title("Texas Hold'em   by:Tommy, Sophie & Sumner")      #set name 
        self.init_window_name.geometry('1200x670+10+10')                 #set size
        self.init_window_name["bg"] = "#8FBC8F"                            #make the window green 
        self.init_window_name.attributes("-alpha",1)                  #make the window light

    #restart
    def restart(self):
        self.test = 0
        self.re = '0'
        self.waiting = True
        self.my_already = 0
        self.card_one.config(image = self.ppic)
        self.card_two.config(image = self.ppic)
        self.card_three.config(image = self.ppic)
        self.card_four.config(image = self.ppic)
        self.card_five.config(image = self.ppic)

        self.player_oneone.config(image = self.pic)
        self.player_onetwo.config(image = self.pic)
        self.player_twoone.config(image = self.pic)
        self.player_twotwo.config(image = self.pic)
        self.player_threeone.config(image = self.pic)
        self.player_threetwo.config(image = self.pic)
        self.player_fourone.config(image = self.pic)
        self.player_fourtwo.config(image = self.pic)
        self.player_fiveone.config(image = self.pic)
        self.player_fivetwo.config(image = self.pic)


        
    #buttons
    def set_buttons(self):
        self.skip_button = Button(self.init_window_name, text="Lowest", bg="white", width=10,command=self.skip)
        self.bet_button = Button(self.init_window_name, text="Bet", bg="white", width=10,command=self.bet)
        self.all_button = Button(self.init_window_name, text="All in", bg="white", width=10,command=self.all)
        self.skip_button.grid(row=5, column=4)
        self.bet_button.grid(row=5, column=6)
        self.all_button.grid(row=5, column=8)

      

    #5cards
    def fivecards(self):
        
        
        self.card_one = Label(self.init_window_name,image=self.pic)
        self.card_two = Label(self.init_window_name,image=self.pic)
        self.card_three = Label(self.init_window_name,image=self.pic)
        self.card_four = Label(self.init_window_name,image=self.pic)
        self.card_five = Label(self.init_window_name,image=self.pic)
        self.card_one.grid(row=3,column=2)
        self.card_two.grid(row=3,column=4)
        self.card_three.grid(row=3,column=6)
        self.card_four.grid(row=3,column=8)
        self.card_five.grid(row=3,column=10)

    #players
    def players(self):
        

        self.player_oneone = Label(self.init_window_name,image = self.ppic)
        self.player_onetwo = Label(self.init_window_name,image = self.ppic)
        self.player_twoone = Label(self.init_window_name,image = self.ppic)
        self.player_twotwo = Label(self.init_window_name,image = self.ppic)
        self.player_threeone = Label(self.init_window_name,image = self.ppic)
        self.player_threetwo = Label(self.init_window_name,image = self.ppic)
        self.player_fourone = Label(self.init_window_name,image = self.ppic)
        self.player_fourtwo = Label(self.init_window_name,image = self.ppic)
        self.player_fiveone = Label(self.init_window_name,image = self.ppic)
        self.player_fivetwo = Label(self.init_window_name,image = self.ppic)
        
        self.player_oneone.grid(row=0,column=0)
        self.player_onetwo.grid(row=0,column=1)
        self.player_twoone.grid(row=0,column=3)
        self.player_twotwo.grid(row=0,column=4)
        self.player_threeone.grid(row=0,column=6)
        self.player_threetwo.grid(row=0,column=7)
        self.player_fourone.grid(row=0,column=9)
        self.player_fourtwo.grid(row=0,column=10)
        self.player_fiveone.grid(row=0,column=12)
        self.player_fivetwo.grid(row=0,column=13)
        
        
        self.pone = Label(self.init_window_name, text="Player 1",bg="#8FBC8F")
        self.ptwo = Label(self.init_window_name, text="Player 2",bg="#8FBC8F")
        self.pthree = Label(self.init_window_name, text="Player 3",bg="#8FBC8F")
        self.pfour = Label(self.init_window_name, text="Player 4",bg="#8FBC8F")
        self.pfive = Label(self.init_window_name, text="Player 5",bg="#8FBC8F")

        self.pone.grid(row=1,column=0)
        self.ptwo.grid(row=1,column=3)
        self.pthree.grid(row=1,column=6)
        self.pfour.grid(row=1,column=9)
        self.pfive.grid(row=1,column=12)


    #blank
    def blank(self):
        self.blank_a = Label(self.init_window_name, width=10,height=8, bg="#8FBC8F")
        self.blank_b = Label(self.init_window_name, width=12,height=2, bg="#8FBC8F")
        self.blank_c = Label(self.init_window_name, width=12,height=2, bg="#8FBC8F")

        self.blank_a.grid(row=2,column=5)
        self.blank_b.grid(row=4,column=11)
        self.blank_c.grid(row=6,column=11)


    #jackpot
    def total(self):
        self.total_money.set(" 0")
        self.total = Label(self.init_window_name, text= 'Total Jackpot:\n'+self.total_money.get(),bg="#8FBC8F")
        self.total.grid(row=2,column=9,columnspan =4)

    #change jackpot
    def c_total(self,n):
        self.total_money.set(str(n))
        self.total.config(text= 'Total Jackpot:\n'+self.total_money.get())


        

    #my money
    def mine(self):
        self.my_money.set(" 10000")
        self.property = Label(self.init_window_name, text= 'My Property:\n'+self.my_money.get(),bg="#8FBC8F")
        self.property.grid(row=2,column=3)

    #change my money
    def c_mine(self,n):
        self.my_money.set(str(n))
        self.property.config(text= 'My Property:\n'+self.my_money.get())
        self.waiting = True
        self.my_already = int(self.re)

        

    #highest bet
    def high(self):
        self.highest.set(" 0")
        self.high = Label(self.init_window_name, text= 'Highest Bet:\n'+self.highest.get(),bg="#8FBC8F")
        self.high.grid(row=2,column=7)
        
    #change highest bet
    def c_high(self,n):
        self.highest.set(str(n))
        self.high.config(text= 'Highest Bet:\n'+self.highest.get())

        

    #prompt
    def prompt(self):
        self.prompt_words.set('Time to bet! Raise your bet to:')
        self.prompt = Label(self.init_window_name, text = self.prompt_words.get(),bg = "#8FBC8F")
        self.prompt.grid(row=6 ,column =5,columnspan =4)



    #change prompt
    def c_prompt(self,n):
        if n ==1:
            self.prompt_words.set('Time to bet! Raise your bet to:')
            self.prompt.config(text = self.prompt_words.get())        
        elif n == 2:
            self.prompt_words.set('Wait until everyone has finished!')
            self.prompt.config(text = self.prompt_words.get())
        elif n == 3:
            self.prompt_words.set('Wrong bet! Do it again!')
            self.prompt.config(text = self.prompt_words.get())
            self.waiting = True
        elif n == 4:
            self.prompt_words.set('You won! \n You have 20 seconds to check out the result!')
            self.prompt.config(text = self.prompt_words.get())
        elif n == 5:
            self.prompt_words.set('Good luck next time! \n You have 20 seconds to check out the result!')
            self.prompt.config(text = self.prompt_words.get())
        elif n == 6:
            self.prompt_words.set('You donot have enough money!')
            self.prompt.config(text = self.prompt_words.get())

        


    #entry

    def entry(self):
        self.e= Entry(self.init_window_name)
        self.e.grid(row=7,column=6,columnspan=2)
        

    #skip
    def skip(self):
        print (self.highest.get())
        self.re = self.highest.get()
        self.my_already = int(self.highest.get())
        self.waiting = False

    #bet
    def bet(self):
        print(self.e.get())
        self.re = self.e.get()
        
        
            
        self.waiting = False
        #print( self.my_already)

    

    #all
    def all(self):
        print(self.my_money.get())
        if int(self.my_money.get()) > 0:
            self.re = str(int(self.my_money.get())+self.my_already)
            
            self.waiting = False
            print(self.re)
        else:
            self.c_prompt(6)


    #first round
    def round_one(self,a,b,c):
        self.cp_one = PhotoImage(file =r'img/'+a[0]+a[1]+'.png')
        self.cp_two = PhotoImage(file =r'img/'+b[0]+b[1]+'.png')
        self.cp_three = PhotoImage(file =r'img/'+c[0]+c[1]+'.png')
        
        self.card_one.config(image = self.cp_one)
        self.card_two.config(image = self.cp_two)
        self.card_three.config(image = self.cp_three)


    #second round
    def round_two(self,d):
        self.cp_four = PhotoImage(file =r'img/'+d[0]+d[1]+'.png')
        self.card_four.config(image = self.cp_four)

    #third round
    def round_three(self,e):
        self.cp_five = PhotoImage(file =r'img/'+e[0]+e[1]+'.png')
        self.card_five.config(image = self.cp_five)


    #show everyone's cards
    def show(self,f,g,h,i,j,k,l,m,n,o):
        self.sp_one = PhotoImage(file =r"img/"+f[0]+f[1]+'.png')
        self.sp_two = PhotoImage(file =r'img/'+g[0]+g[1]+'.png')
        self.sp_three = PhotoImage(file =r'img/'+h[0]+h[1]+'.png')
        self.sp_four = PhotoImage(file =r'img/'+i[0]+i[1]+'.png')
        self.sp_five = PhotoImage(file =r'img/'+j[0]+j[1]+'.png')
        self.sp_six = PhotoImage(file =r'img/'+k[0]+k[1]+'.png')
        self.sp_seven = PhotoImage(file =r'img/'+l[0]+l[1]+'.png')
        self.sp_eight = PhotoImage(file =r'img/'+m[0]+m[1]+'.png')
        self.sp_nine = PhotoImage(file =r'img/'+n[0]+n[1]+'.png')
        self.sp_ten = PhotoImage(file =r'img/'+o[0]+o[1]+'.png')
        

        

        
        self.player_oneone.config(image = self.sp_one)
        self.player_onetwo.config(image = self.sp_two)
        self.player_twoone.config(image = self.sp_three)
        self.player_twotwo.config(image = self.sp_four)
        self.player_threeone.config(image = self.sp_five)
        self.player_threetwo.config(image = self.sp_six)
        self.player_fourone.config(image = self.sp_seven)
        self.player_fourtwo.config(image = self.sp_eight)
        self.player_fiveone.config(image = self.sp_nine)
        self.player_fivetwo.config(image = self.sp_ten)

    #judge if still waiting
    def wait(self):
        return self.waiting

    #get the returned value
    def back(self):
        return self.re

    #my cards
    def my_cards(self,x,y):
        self.mp_one = PhotoImage(file =r'img/'+x[0]+x[1]+'.png')
        
        self.mp_two = PhotoImage(file =r'img/'+y[0]+y[1]+'.png')
        
        self.my_cardone = Label(self.init_window_name,image = self.mp_one)
        self.my_cardtwo = Label(self.init_window_name, image = self.mp_two)
        self.my_card_words = Label(self.init_window_name, text = "My cards:",bg = "#8FBC8F")
        self.my_card_words.grid(row = 8, column =6, columnspan =2)

        self.my_cardone.grid(row = 9, column = 6)
        self.my_cardtwo.grid(row =9, column = 7)


    #new cards
    def c_my_cards(self,x,y):
        self.mp_three = PhotoImage(file =r'img/'+x[0]+x[1]+'.png')
        self.mp_four = PhotoImage(file =r'img/'+y[0]+y[1]+'.png')
        
        self.my_cardone.config(self.init_window_name,image = self.mp_three)
        self.my_cardtwo.config(self.init_window_name,image = self.mp_four)


    
        


'''def gui_start():
    init_window = Tk()              
    cardgame = MY_GUI(init_window)
    
    cardgame.set_init_window()
    cardgame.set_buttons()
    cardgame.fivecards()
    cardgame.players()
    cardgame.blank()
    cardgame.total()
    cardgame.mine()
    cardgame.prompt()
    cardgame.entry()
    cardgame.high()
    #cardgame.my_cards(['Club','A'],['Heart','4'])
    #cardgame.round_one(['Club','2'],['Diamond','8'],['Heart','7'])
    #cardgame.c_prompt(3)
    cardgame.c_mine(7000)
    #cardgame.c_total(12000)
    #cardgame.c_high(3000)
    #cardgame.restart()
    cardgame.all()

    init_window.mainloop()          


gui_start()'''

