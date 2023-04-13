from kandinsky import *
from ion import *
from time import *
from random import *
from math import ceil

class Note():
  def __init__(self):
    self.touche = "KEY_LEFT"
    self.ico = "<"
    self.c = "red"
    self.co = None
    self.l = [[78,0],[158,0],[238,0]]
    self.size = 20
    
  def Start(self):
    self.c = choice(["red","blue","green","pink"])
    if self.c == "red":
      self.touche = "KEY_LEFT"
      self.ico = "<"
    if self.c == "blue":
      self.touche = "KEY_RIGHT"
      self.ico=">"
    if self.c == "green":
      self.touche = "KEY_DOWN"
      self.ico="v"
    if self.c == "pink":
      self.touche = "KEY_UP"
      self.ico="^"
    
    self.co = choice(self.l)
    self.co[0] = self.co[0]-int((self.size-5)/2)
    
  def Draw(self,speed):
    fill_rect(self.co[0],self.co[1]-int(float(speed)*1.5),self.size,self.size,"black")
    fill_rect(self.co[0],self.co[1],self.size,self.size,self.c)
    draw_string(self.ico,self.co[0]+int(self.size/3),self.co[1]+int(self.size/7),"w",self.c)
    self.co[1]+=speed

co = [155,200]
speed = 1
gameSpeed = 0.02
started = True
line = [[78,0],[158,0],[238,0]]
note = []
timer = 0.0
tps = 1.5
pts = 0
ptsC = "w"
tpsRst = 60.0
tpsRstC = "w"
tm = 0.0
counter = 0
counter2 = 0
t = 0.0
t2 = 10
isSparkle = False
sparkle = 1
sp = 0.0
sp2 = 0.1
spCo = (0,0)
spColour = None
cAnimTps = 0.0
cAnimTps2 = 0.2
cAnimAdd=-10
cAnimY=150

def Explode(colour,c):
  global sparkle,isSparkle,sp
  fill_rect(c[0]-5*sparkle,c[1]-5*sparkle,25+10*sparkle,25+10*sparkle,"black")
  fill_rect(c[0]-5*sparkle,c[1]-5*sparkle,25+10*sparkle,25+10*sparkle,colour)
  fill_rect(c[0]+5-5*sparkle,c[1]+5-5*sparkle,15+10*sparkle,15+10*sparkle,"black")
  if monotonic()-sp>sp2:
    sp=monotonic()
    sparkle+=1
  if sparkle>2:
    isSparkle=False
    fill_rect(c[0]-5*sparkle,c[1]-5*sparkle,25+10*sparkle,25+10*sparkle,"black")
    sparkle=1
    fill_rect(0,185,320,50,"black")

fill_rect(0,0,400,300,"black")
timer = monotonic()
while started:
  a = monotonic()
  if tpsRst<0:
    started=False
  
  fill_rect(0,2,50,20,"black")
  draw_string("T: "+str(ceil(tpsRst)),0,2,tpsRstC,"black")
  draw_string("P: "+str(pts),0,20,ptsC,"black")
  for i in line:
    fill_rect(i[0],i[1],5,300,(50,50,50))
  fill_rect(0,180,320,5,"w")
  
  if monotonic()-timer>tps:
    n = Note()
    n.Start()
    note.append(n)
    timer=monotonic()

  if monotonic()-t>t2:
    gameSpeed = gameSpeed/1.1
    tps = tps/1.2
    t=monotonic()

  for i in note:
    i.Draw(speed)
    if (i.co[1]+i.size)>=180 and i.co[1]<=185:
      if keydown(eval(i.touche)):
        fill_rect(i.co[0]-2,i.co[1]-2,i.size+4,i.size+4,"black")
        
        isSparkle=True
        sp=monotonic()
        spCo=i.co
        spColour=i.c
        
        note.remove(i)
        pts+=1
        counter2+=1
        counter+=1
        ptsC="g"
        tm=monotonic()
    elif i.co[1]>222:
      if pts>0:
        fill_rect(0,20,50,15,"black")
        pts-=1
        ptsC="r"
        tm=monotonic()
      counter+=1
      note.remove(i)
  
  if monotonic()-cAnimTps>cAnimTps2:
    cAnimTps=monotonic()
    cAnimAdd=-cAnimAdd
    cAnimY+=cAnimAdd
  
  if isSparkle:
    Explode(spColour,spCo)
  
  sleep(gameSpeed)
  
  tpsRst -= monotonic()-a
  if monotonic()-tm>0.5:
    ptsC="w"

fill_rect(0,0,400,300,"black")
draw_string("Congratulation Player !",50,20,"w","black")
draw_string("You made "+str(pts)+" points !",40,50,"w","black")
a = counter2/counter*100
draw_string(str(a)[0:5]+"% ("+str(counter2)+" on "+str(counter)+")",30,80,"w","black")
if a==100:
  draw_string("PERFECT !",20,130,"g","black")
elif a>=80:
  draw_string("AMAZING !",20,130,"b","black")
elif a>=50:
  draw_string("Good !",20,130,"y","black")
elif a>=25:
  draw_string("Train you !",20,130,"o","black")
else:
  draw_string("So bad...  :(",20,130,"r","black")
