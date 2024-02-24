import pygame
from sys import exit
from random import randint
from tkinter.messagebox import showinfo

class RapidRoll:
    def __init__(self):
        self.dim = (600,600)
        self.fps = 60
        pygame.init()
        self.screen = pygame.display.set_mode(self.dim)
        pygame.display.set_caption("RAPID ROLL")
        pygame.display.flip()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Comic Sans MS', 20)
        self.start()
        
    def loadHighscore(self):
        fp = open("score/top.num",'r')
        self.highscores=fp.readlines()
        for i in range(len(self.highscores)):
            self.highscores[i]=int((self.highscores[i]).split('\n')[0])
        self.top = self.highscores[0]
        
    def saveHighscore(self):
        self.highscores.append(self.score)
        self.highscores.sort(reverse=True)
        self.highscores = self.highscores[:len(self.highscores)-1]
        for i in range(0,len(self.highscores)):
            self.highscores[i]=str(self.highscores[i])+"\n"
        fp = open("score/top.num","w")
        fp.writelines(self.highscores)
        
    def showEnd(self):            
        s = 'GAME END\n'
        s += 'Score : '+str(self.score)+'\n'
        s += 'Level : '+str(self.level)+'\n'
        s += 'Top : '+str(self.top)+'\n'
        showinfo('Game End',s)
        
    def showHighscores(self):
        s = ""
        for i in range(len(self.highscores)):
            s += f"{(i+1):02d} - {self.highscores[i]} {self.names[i]}"
        showinfo('Highscores',s)
        
    def showControls(self):
        s =  "right -> move ball to right\n"
        s += "left -> move ball to left\n"
        s += "p -> pause game\n"
        s += "h -> show highscores\n"
        s += "c -> show controls of game\n"
        s += "n -> new game\n"
        s += "i -> help\n"
        
        showinfo('Controls',s)
        
    def showHelp(self):
        s =  "FALL\n\n"
        s += "* Game similar to 'Rapid Roll' of Old Nokia.\n"
        s += "* The objective of game is earn score.\n"
        s += "* You begin with 3 lifes.\n"
        s += "* You lose life if you fall to outside of greate square or ball collide with ceil of game or you fall in triangles.\n"
        s += "* You earn score for each rectangle or set of triangles that go above ceil.\n"
        s += "* For each rectangle or set of triangles you earn (level+1) points.\n"
        s += "* There's chance of 1/10 of spawn a heart on rectangle.\n"
        s += "* You earn 1 life if you colide with hearts.\n"
        s += "* 3/4 spawn rectangle and 1/4 spawn set of triangles.\n"
        s += "* You level up when the number of rectangles and set triangles that go above ceil is more than (level+1)*100 . \n"
        s += "* Level of game determine velocity.\n"
        showinfo('Help',s)
        
    def new_game(self):
        self.fps = 60
        
        self.loadHighscore()
        
        # measures
        self.X = 100
        self.Y = 100
        self.size = 20
        self.radius = self.size//2
        self.sdx = self.dim[0]-2*self.X
        self.sdy = self.dim[1]-2*self.Y
        self.fdx = self.sdx//4 
        self.fdy = self.sdx//20 
        self.tdx = self.fdx//5
        self.tmdx = self.tdx//2
        self.mx = self.X+self.sdx
        self.my = self.Y+self.sdy
        self.size_pixel = 4
        
        self.speed = 1
        self.life = 3
        self.level = 0
        self.score = 0
        self.posx = self.X+(self.sdx//2)-(self.size//2)
        self.posy = self.Y+self.size
        self.ndel = 0
        
        self.floors = []
        self.tfloors = []
        self.hearts = []
        self.main = pygame.Rect((self.X,self.Y,self.sdx,self.sdy))
        self.ball = pygame.Rect((self.posx,self.posy,self.size,self.size))
        
    def drawInf(self):
        text_controls = self.font.render("PRESS 'c' for see CONTROLS",True,(0,0,0))
        text_hearts = self.font.render('Lifes : '+str(self.life),True,(0,0,0))
        text_top = self.font.render('TOP     : '+str(self.top),True,(0,0,0))
        text_score = self.font.render('SCORE : '+str(self.score),True,(0,0,0))
        text_level = self.font.render('LEVEL : '+str(self.level),True,(0,0,0))

        self.screen.blit(text_controls,(0,570))
        self.screen.blit(text_top, (0,0))
        self.screen.blit(text_score, (0,50))
        self.screen.blit(text_hearts, (0,510))
        self.screen.blit(text_level, (0,540))
        
    def drawFloors(self):
        for i in range(len(self.floors)):
            if self.tfloors[i]:
                pygame.draw.rect(self.screen,(0,0,0),self.floors[i])
            else:
                for j in range(5):
                    x0 = (self.floors[i]).left+j*self.tdx
                    x1 = x0+self.tmdx
                    x2 = x0+self.tdx
                    y0 = (self.floors[i]).top
                    y1 = y0+self.fdy
                    p=[(x0,y1),(x1,y0),(x2,y1)]
                    pygame.draw.polygon(surface=self.screen,color=(0,0,0),points=p)

    def drawHearts(self):
        for h in self.hearts:
            hx = h.left
            hy = h.top

            p = [(1,1),(1,2),
                 (5,1),(5,2),
                 (2,0),(3,1),(4,0),
                 (2,3),(3,4),(4,3)]
            for i in p:
                t = hx+i[0]*self.size_pixel , hy+i[1]*self.size_pixel
                r=pygame.Rect((t[0],t[1],self.size_pixel,self.size_pixel))
                pygame.draw.rect(self.screen,(0,0,0),r)        
    
    def draw(self):
        self.screen.fill((255,255,255))
        pygame.draw.rect(self.screen,(0,0,0),self.main,1)
        pygame.draw.circle(self.screen,(0,0,0),[self.posx+self.radius,self.posy+self.radius],self.radius,1)
        self.drawFloors()
        self.drawHearts() 
        self.drawInf()
        pygame.display.update()

    def createNewFloor(self):
        x = randint(self.fdx,self.mx-self.fdx)
        y = self.my-self.fdy
        r = pygame.Rect((x,y,self.fdx,self.fdy))
        self.floors.append(r)
        z = randint(0,3)
        self.tfloors.append(z!=0)
        
        if z!=0:
            z = randint(0,9)
            if (z==0):
                hx = x+(self.fdx//2)-2*self.size_pixel-(self.size_pixel//2)
                hy = y-5*self.size_pixel
                r = pygame.Rect((hx,hy,self.size_pixel*5,self.size_pixel*5))
                self.hearts.append(r)
    
    def moveElements(self,eltos,flag):
        v = []
        for i in range(len(eltos)):
            if (eltos[i]).top>self.Y:
                (eltos[i]).move_ip(0,-self.speed)
                v.append(False)
            else:
                v.append(True)
        for i in range(len(eltos)):
            if v[i]:
                del eltos[i]
                if flag:
                    self.score += (self.level+1)
                    self.ndel += 1
                    del self.tfloors[i]
    
    def collision(self):
        # points of ball
        a0 = self.ball.left
        a1 = a0+self.size
        b0 = self.ball.top
        b1 = b0+self.size
        
        for i in range(len(self.floors)):
            # points of floors
            x0 = (self.floors[i]).left
            x1 = x0+self.fdx
            y0 = (self.floors[i]).top
            y1 = y0+self.fdy
            
            b = False
            if self.ball.clipline((x0, y0), (x1, y0)):
                self.posy=y0-self.size
                b = True
            elif self.ball.clipline((x0, y0), (x0, y1)):
                self.posx = x0-self.size
                b = True
            elif self.ball.clipline((x1, y0), (x1, y1)):
                self.posx = x1
                b = True
                
            if b and (not self.tfloors[i]):
                return True
        return False
                
    def checkColHeart(self):
        v = []
        for i in range(len(self.hearts)):
            if self.ball.colliderect(self.hearts[i]):
                self.life+=1
                v.append(i)
        for i in v:
            del self.hearts[i]
    
    def moveBall(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.posx>self.X:
                self.posx-=self.speed
        if keys[pygame.K_RIGHT]:
            if self.posx<(self.dim[0]-self.X-self.size):
                self.posx+=self.speed
    
    def fall(self):
        if (self.posy<(self.dim[1]-self.Y-self.size)):
            self.posy+=self.speed
        else:
            self.respawn()
        
    def respawn(self):
        self.life-=1
        self.posx = self.X+(self.sdx//2)-(self.size//2)
        self.posy = self.Y+self.size
        self.floors = []
        self.tfloors = []
        self.hearts = []
        
    def close(self):
        self.saveHighscore()
        pygame.quit()
        exit()
        
    def pause(self):
        p = True
        while p:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    self.close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.close()
                    elif event.key == pygame.K_p:
                        p = False
                    elif event.key == pygame.K_h:
                        self.showHighscores()
                    elif event.key == pygame.K_c:
                        self.showControls()
        
    def start(self):
        self.new_game()
        count = 0
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.close()
                    elif event.key == pygame.K_p:
                        self.pause()
                    elif event.key == pygame.K_h:
                        self.showHighscores()
                    elif event.key == pygame.K_c:
                        self.showControls()
                    elif event.key == pygame.K_n:
                        self.saveHighscore()
                        count = 0
                        self.showEnd()
                        self.new_game()
                    elif event.key == pygame.K_i:
                        self.showHelp()
            
            self.moveElements(self.floors,True)
            self.moveElements(self.hearts,False)
                        
            if count==60:
                self.createNewFloor()
            count = (count+1)%61
                
                
            self.moveBall()
            self.fall()
            self.checkColHeart()
            if self.collision():
                self.respawn()
            if self.ball.clipline((self.X, self.Y), (self.X+self.sdx, self.Y)):
                self.respawn()
            if (self.life==0):
                self.saveHighscore()
                self.showEnd()
                break
            if (self.ndel>=((self.level+1)*100)):
                self.level+=1
                if self.level<=20:
                    self.fps += 10
                    
            self.ball = pygame.Rect((self.posx,self.posy,self.size,self.size))
                

            
            self.draw()
            self.clock.tick(self.fps)


if __name__=="__main__":
    RapidRoll()
