from kandinsky import *
from ion import *
from time import sleep,monotonic
from random import randint

class B():
  def __init__(self,x,y,t=""):
    self.x = x
    self.y = y
    self.typ = t
    
  def Draw(self):
    if self.typ == "ground":
      fill_rect(self.x,self.y,20,20,(30,30,30))
      fill_rect(self.x+2,self.y+2,18,18,(15,15,15))

    else:
      fill_rect(self.x,self.y,20,20,"black")
      fill_rect(self.x+2,self.y+2,18,18,(100,100,100))

class Game():
  def __init__(self):
    self.isPlaying = True
    self.menu = True
    self.b = []
    self.enterExit = [False,False]
    self.p = [0,0]
    self.pSpeed = 5
    self.noC = None
    self.victory_b = []
    self.difficulty = 1
    
  def WriteCenter(self,txt,y=103,fg="w",bg="black",padx=0):
    x = int(160-(len(txt)*10)/2)
    draw_string(txt,x+padx,y,fg,bg)

  def DrawMenu(self):
    fill_rect(0,0,320,222,(100,100,100))
    self.WriteCenter("- ALWAYS FURTHER -",25,(50,200,50),(100,100,100))
    self.WriteCenter("Press <OK>",128,"w",(100,100,100))
    
  def GenRoom(self):
    fill_rect(0,0,320,222,(100,100,100))
    self.WriteCenter("Room in generation...",103,"w",(100,100,100))
    self.b.clear()
    self.enterExit = [False,False]
    
    for x in range(0,320,20):
      column = []
      for y in range(0,220,20):
        block = None
        
        if x == 0 or x == 300:
          block = B(x,y,"5")
        
        elif y == 0:
          if not self.enterExit[1]: 
            a = randint(0,14-int(x/20))
            if 14-int(x/20) < 0:
              print("---ERROR---\nIn GenRoom, 14-int(x/20) < 0")
              quit()
            if a == 0:
              block = B(x,y,"ground")
              self.enterExit[1]=True
            else:
              block = B(x,y,"5")
          else:
            block = B(x,y,"5")
        
        elif y == 200:
          if not self.enterExit[0]:
            a = randint(0,14-int(x/20))
            if 14-int(x/20) < 0:
              print("---ERROR---\nIn GenRoom, 14-int(x/20) < 0")
              quit()
            if a == 0:
              block = B(x,y,"ground")
              self.p = [x+6,236]
              self.enterExit[0]=True
            else:
              block = B(x,y,"5")
          else:
            block = B(x,y,"5")
        
        else:
          block = B(x,y,"ground")  
        column.append(block)
      
      self.b.append(column)
      self.noC = get_pixel(5,5)

  def NewGame(self):
    self.pSpeed=5
    self.menu=False
    self.GenRoom()
    while self.p[1] > 187:
      self.Draw()
      self.p[1]-=self.pSpeed
      sleep(0.2)
    self.pSpeed=10
  
  def Menu(self):
    sleep(0.5)

    if keydown(KEY_OK):
      self.NewGame()
    if keydown(KEY_EXE):
      fill_rect(0,0,320,222,(100,100,100))
      self.WriteCenter("Press <return> to quit",103,"w",(100,100,100))
      self.isPlaying=False
      
  def Draw(self):
    fill_rect(0,0,320,222,"black")
    
    for i in self.b:
      for elem in i:
        elem.Draw()
    
    fill_rect(self.p[0],self.p[1],10,10,"w")
    
  def Win(self):
    fill_rect(0,0,320,222,(75,75,75))
    self.WriteCenter("VICTORY",50,"yellow",(75,75,75),50)
    self.WriteCenter("Go to next level...",100,"w",(75,75,75),50)
    self.p = [55,236]
    while self.p[1]>-10:
      self.p[1]-=self.pSpeed
      for i in self.victory_b:
        i.Draw()
      fill_rect(self.p[0],self.p[1],10,10,"w")
      fill_rect(0,220,320,2,"black")
      sleep(0.12)
    self.difficulty+=1
    self.NewGame()

  def Run(self):
    if keydown(KEY_EXE):
      self.menu=True
      self.DrawMenu()
      sleep(0.25)
      return

    if self.p[1] < -10:
      self.Win()
      
      if keydown(KEY_OK):
        self.NewGame()
      
      sleep(0.3)
      return

    self.Draw()
    
    if keydown(KEY_UP) and not get_pixel(self.p[0],self.p[1]-self.pSpeed)==self.noC and not get_pixel(self.p[0]+10,self.p[1]-self.pSpeed)==self.noC:
      self.p[1]-= self.pSpeed
    elif keydown(KEY_DOWN) and not get_pixel(self.p[0],self.p[1]+10+self.pSpeed)==self.noC and not get_pixel(self.p[0]+10,self.p[1]+self.pSpeed+10)==self.noC:
      self.p[1]+= self.pSpeed
    elif keydown(KEY_RIGHT) and not get_pixel(self.p[0]+10+self.pSpeed,self.p[1])==self.noC and not get_pixel(self.p[0]+10+self.pSpeed,self.p[1]+10)==self.noC:
      self.p[0]+= self.pSpeed
    elif keydown(KEY_LEFT) and not get_pixel(self.p[0]-self.pSpeed,self.p[1])==self.noC and not get_pixel(self.p[0]-self.pSpeed,self.p[1]+10)==self.noC:
      self.p[0]-= self.pSpeed
        
    sleep(0.25)

g = Game()

for i in range(11):
  g.victory_b.append(B(20,i*20))
  g.victory_b.append(B(80,i*20))
  g.victory_b.append(B(40,i*20,"ground"))
  g.victory_b.append(B(60,i*20,"ground"))
  

g.DrawMenu()
sleep(0.5)
while g.isPlaying:
  if g.menu:
    g.Menu()
  else:
    g.Run()
