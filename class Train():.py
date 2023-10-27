class Train():
    def __init__(self,body,pos):
        self.body = body
        self.pos = pos
        self.dlg = len(body)
        self.kier = self.kierunek(self.body)
        self.pauza = 0
        self.wagony=[[]]*self.dlg
    def kierunek(self,body):
        if body[0].isupper(): return(1)
        return(0)

def pozycja(track,poc,ini):
    if poc.kier==0:
        if ini==0: poc.pos=(poc.pos+1)%len(track)
        for x in range(poc.dlg):poc.wagony[x]=(track[(poc.pos-x)%len(track)])
    else:
        if ini==0: poc.pos=(poc.pos-1)%len(track)
        for x in range(poc.dlg):poc.wagony[x]=(track[(poc.pos+x)%len(track)])
    return(poc)

def czek(a,b):
    for c in b.wagony:
        for d in a.wagony:
            if d==c: return(True)
    a.wagony.sort()
    for c in range(1,a.dlg):
        if a.wagony[c]==a.wagony[c-1]: return (True)
    return (False)


def track_decode(track):
    ciag,punkt,wektor=[],[],1
    wektory={1:[0,1],2:[1,1],3:[-1,1],4:[1,0],5:[1,-1],6:[-1,0],7:[-1,-1],8:[0,-1]}
    wektory_pos={
    1:["1-1","1\\2","1/3","1+1","1S1"],
    2:["1-1","2\\2","4|4","2X2","2S2"],
    3:["6|6","3/3","3S3","3X3","1-1"],
    4:["4|4","4S4","4+4","4\\2","4/5"],
    5:["5/5","5S5","5X5","8-8","4|4"],
    6:["6|6","6/3","6\\7","6+6","6S6"],
    7:["7\\7","7X7","7S7","8-8","6|6"],
    8:["8-8","8+8","8S8","8\\7","8/5"]
    }
    track=track.split("\n")
    for a in range(len(track[0])):
        if track[0][a]!=" ": break
    ciag.append([0,a,track[0][a]])
    while True:
        last=ciag[len(ciag)-1]
        for a in wektory_pos[wektor]:
            przesun=wektory[int(a[0])]
            if last[0]+przesun[0]>=0 and last[1]+przesun[1]>=0 and last[0]+przesun[0]<len(track) and last[1]+przesun[1]<len(track[last[0]+przesun[0]]):
                if track[last[0]+przesun[0]][last[1]+przesun[1]]==a[1]:
                    if last[0]+przesun[0]==ciag[0][0] and last[1]+przesun[1]==ciag[0][1] and len(ciag)!=1: return (ciag)
                    ciag.append([last[0]+przesun[0],last[1]+przesun[1],a[1]])
                    wektor=int(a[2])
    return (ciag)

def train_crash(track, a_train, a_train_pos, b_train, b_train_pos, limit):
    #print(track, a_train, a_train_pos, b_train, b_train_pos, limit)
    pa=Train(a_train,a_train_pos)
    pb=Train(b_train,b_train_pos)
    track2=track_decode(track)
    pa=pozycja(track2,pa,1)
    pb=pozycja(track2,pb,1)
    if czek(pa, pb) or czek(pb, pa):return(0)
    for x in range(limit):
        if track2[pa.pos][2]=="S" and x!=0 and pa.body[0] not in "Xx":
            if pa.pauza==0: pa.pauza=pa.dlg-1
            else: pa.pauza-=1
        if track2[pb.pos][2]=="S" and x!=0 and pb.body[0] not in "Xx":
            if pb.pauza==0:pb.pauza=pb.dlg-1
            else: pb.pauza-=1
        if pa.pauza==0: pa=pozycja(track2,pa,0)
        if pb.pauza==0: pb=pozycja(track2,pb,0)
        if czek(pa, pb) or czek(pb, pa):return(x+1)
    return(-1)