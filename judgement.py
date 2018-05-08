import copy
#cards=[[pattern,number]]
dic={"2":1, "3":2,"4":3,"5":4,"6":5,"7":6,"8":7,"9":8,"10":9,"J":10,"Q":11,"K":12,"A":13}
dic2={1:"2",2:"3",3:"4",4:"5",5:"6",6:"7",7:"8",8:"9",9:"10",10:"J",11:"Q",12:"K",13:"A"}

def rank_hand_card(cards):
    l=[]
    for i in cards:
        l.append([i[0],dic[i[1]]])
    l=sorted(l,key=lambda l:l[1])
    cardsnew=[]
    for i in l:
        
        cardsnew.append([i[0],dic2[i[1]]])
    return cardsnew

def countnumber(n,cards):
    l=[]
    for i in cards:
        l.append(i[1])
    l2=[]
    for i in l:
        if l.count(i)==n:
            l2.append(i)
    l2=set(l2)
    l2=list(l2)
    return l2

        
def if_straight(cards):
    cards=rank_hand_card(cards)
    l=[]
    for i in cards:
        l.append(i[1])
    
    for i in range(0,3):
        if dic[l[i]]<=9:
            if dic2[dic[l[i]]+1] in l:
                if dic2[dic[l[i]]+2] in l:
                    if dic2[dic[l[i]]+3] in l:
                        if dic2[dic[l[i]]+4] in l:
                            return True

def if_flush(cards):
    l=[]
    for i in cards:
        l.append(i[0])
    for i in l:
        if l.count(i) >=5:
            return True

def rank_type(cards):
    cards=rank_hand_card(cards)
    if if_straight(cards)==True and if_flush(cards)==True:
        return ["straight flush",9]
    elif len(countnumber(4,cards)) != 0:
        return ["four of a kind",8,dic[countnumber(4,cards)[0]]]
    elif len(countnumber(3,cards)) != 0 and len(countnumber(2,cards)) != 0:
        return ["fullhouse",7,dic[countnumber(3,cards)[0]]]
    elif if_flush(cards)==True:
        return ["flush", 6]
    elif if_straight(cards)==True:
        return ["straight", 5]
    elif len(countnumber(3,cards)) != 0:
        return ["three of a kind",4,dic[countnumber(3,cards)[0]]]
    elif len(countnumber(2,cards)) >1:
        l=[]
        for i in countnumber(2,cards):
            l.append(dic[i])
        return ["two pairs", 3, max(l)]
    elif len(countnumber(2,cards))==1:
        return ["one pair",2, countnumber(2,cards)[0]]
    else:
        l=[]
        for i in cards:
            l.append(dic[i[1]])
            
        return ["high card",1,max(l)]
#[{"player":name,handcard:[[],[]]},{}...]
#public[[],[]]

def find_winner(playerdiclist,public):
    l=[]
    
    for i in playerdiclist:
        l2=[]
        for k,v in i.items():
            x=copy.deepcopy(v)
            l2.append(x)
        
        l.append(l2)
    

    for i in l:
        for j in public:
            i[1].append(j)
    

    
    for i in l:
        i.append(rank_type(i[1]))
    winner=l[0][0]
    i=1
    while i < len(l):
        
        if l[i][2][1]>l[i-1][2][1]:
            winner=l[i][0]
            i+=1
        elif l[i][2][1]==l[i-1][2][1] and l[i][2][1] in [1,2,3,4,7,8]:
            if l[i][2][2]>l[i-1][2][2]:
                winner=l[i][0]
                i+=1
            elif l[i][2][2]==l[i-1][2][2]:
                winner=winner + ","+l[i][0]
                i+=1
            else:
                i+=1
        else:
            i+=1

    for i in playerdiclist:
        i["winner"]=winner

    for i in playerdiclist:
        for j in range(0,len(i["handcard"])-2):
            ["handcard"].pop()
        


    return playerdiclist,public

    
    




playerdiclist=[{"player":"tim","handcard":[["b","A"],["x","7"]]},\
               {"player":"tom","handcard":[["b","A"],["x","A"]]},\
               {"player":"oYo","handcard":[["x","A"],["x","7"]]}]
public=[["a","5"],["b","7"],["a","5"],["a","10"],["a","8"]]              

print(find_winner(playerdiclist,public))


    
    
        
