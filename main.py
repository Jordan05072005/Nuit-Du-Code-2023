import pyxel
import random
import time
class Game():
    def __init__(self):
        self.x_screen=128
        self.y_screen=128
        pyxel.init(self.x_screen,self.y_screen,title="Invasion")
        pyxel.load("map.pyxres")                   #chargement de la map
        self.x_player1=self.x_screen/2
        self.y_player1=self.y_screen/2
        self.x_player2=self.x_screen/2-20
        self.y_player2=self.y_screen/2-20
        self.vague=0          
        self.hit_box_all={'skin':{'base':{"co":[1,1,1]},                                      #skin ===> nom skin ===>[hitbox_x, hitbox_y,écart sur l'appli pyxel entre le bord et le debut du perso]
        'bald_man':{'gauche':[14,15,0],'droite':[14+2,15,2],'haut':[14+2,15,2],'bas':[13+1,15,1]}},
        'mob':{"parasite":{'gauche':[10+3,15,3],'droite':[10+3,15,3],'haut':[10+3,15,3],'bas':[10+3,15,3]},
        "slime":{'gauche':[12+2,8,2],'droite':[12+2,8,2],'haut':[12+2,8,2],'bas':[12+2,8,2]},
        'zombie':{'gauche':[6+4,16,4],'droite':[6+6,16,6],'haut':[8+4,16,4],'bas':[8+4,16,4]},
        'boss_K_9':{'gauche':[26+3,16,3],'droite':[26+3,16,3],'haut':[26+3,16,3],'bas':[26+3,16,3]},
        'fire_ball':[6,10,5,2]                                                                     #fireball===> [hitbox_x ,hitbox_y,ecart_x,ecart_y]
        }}     
        self.hit_box_items=5              #hit box items
        self.hit_box=10   #Hit box des joueurs et des monstre basique
        self.move_speed_player_base=1.5
        self.move_speed1=self.move_speed_player_base
        self.move_speed2=self.move_speed_player_base
        self.mob_speed={'parasite':0.5 ,
        'zombie':1.25 ,'slime': 0.5,'boss_K_9':0.25}
        self.skin_player1={'base':[72,80,0],
        'bald_man':{"bas":[72,128,9],"haut":[88,128,9],"gauche":[104,128,9],'droite':[120,128,9],"cut_bas":[72,160,9],"cut_haut":[88,160,9],"cut_gauche":[104,160,9],"cut_droite":[120,160,9]}}
        self.name_skin_player1='bald_man'
        self.skin_player2={'base':[88,80,0],
        'bald_man':{"bas":[72,144,9],"haut":[88,144,9],"gauche":[104,144,9],'droite':[120,144,9],"cut_bas":[72,176,9],"cut_haut":[88,176,9],"cut_gauche":[104,176,9],"cut_droite":[120,176,9]}}
        self.name_skin_player2='bald_man'
        self.mobs=[]
        self.powers_up=[]
        self.power_up_activated=[]
        self.time_power_up=5
        self.o=1
        self.ancien_postion_mob='bas'
        self.ancien_postion_player1='bas'
        self.ancien_postion_player2='bas'
        self.ancien_cut_postion_player1=''
        self.ancien_cut_postion_player2=''
        self.life_base=190
        self.life_player1=self.life_base
        self.life_player2=self.life_base
        self.degat=10
        self.degat_boss=20
        self.etat='start' 
        self.button={'play':{"x":40,"y":45,"hitbox_x":46,'hitbox_y':22,'bordure_x':1,'bordure_y':1,"pushing_on":False},
        'restart':{"x":40,"y":45,"hitbox_x":46,'hitbox_y':22,'bordure_x':1,'bordure_y':1,"pushing_on":False}}  
        self.life_boss_K_9=200
        self.point_player1=0
        self.point_player2=0
        self.index=0
        self.fire_ball_boss={'gauche': [],'droite':[],'haut':[],'bas':[]}
#power up
        self.up_life=50
        self.up_speed=3
        pyxel.run(self.update,self.draw)             #run la fenetre pyxel

    def move_players(self):            #déplacement des joueurs 
#player 2 déplacement 
        if pyxel.btn(pyxel.KEY_UP):
            self.y_player2-=self.move_speed2
            self.ancien_postion_player2='haut'
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y_player2+=self.move_speed2
            self.ancien_postion_player2='bas'
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x_player2+=self.move_speed2
            self.ancien_postion_player2='droite'
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x_player2-=self.move_speed2
            self.ancien_postion_player2='gauche'
#player 1 déplacement 
        if pyxel.btn(pyxel.KEY_Z):
            self.y_player1-=self.move_speed1
            self.ancien_postion_player1='haut'
        if pyxel.btn(pyxel.KEY_S):
            self.y_player1+=self.move_speed1
            self.ancien_postion_player1='bas'
        if pyxel.btn(pyxel.KEY_D):
            self.x_player1+=self.move_speed1
            self.ancien_postion_player1='droite'
        if pyxel.btn(pyxel.KEY_Q):
            self.x_player1-=self.move_speed1
            self.ancien_postion_player1='gauche'
    
    def creation_monster(self):                                           #création des vagues de monstres 
        if self.vague==0 and len(self.mobs)==0:
            self.mobs.append([0,self.y_screen/2-20,'parasite']) #porte gauche
            self.mobs.append([self.x_screen/2,0,'parasite']) #haut 
            self.mobs.append([self.x_screen-20,self.y_screen/2-20,'slime']) #droite
            self.mobs.append([self.x_screen/2,self.y_screen-20,'slime']) #bas
            self.vague+=1
        
        elif self.vague==1 and len(self.mobs)==0:
            self.mobs.append([0,self.y_screen/2-20,'parasite']) #porte gauche
            self.mobs.append([self.x_screen/2,0,'parasite'])
            self.mobs.append([self.x_screen-20,self.y_screen/2-20,'parasite'])
            self.mobs.append([self.x_screen/2,self.y_screen-20,'slime'])
            self.mobs.append([self.x_screen/2-20,0,'parasite']) #haut 
            self.mobs.append([self.x_screen-20,self.y_screen/2-30,'slime']) #droite
            self.vague+=1

        elif self.vague==2 and len(self.mobs)==0:
            self.mobs.append([0,self.y_screen/2-20,'parasite']) #porte gauche
            self.mobs.append([self.x_screen/2,0,'slime'])
            self.mobs.append([self.x_screen-20,self.y_screen/2-20,'slime'])
            self.mobs.append([self.x_screen/2,self.y_screen-20,'parasite'])
            self.mobs.append([self.x_screen/2-20,0,'slime']) #haut 
            self.mobs.append([self.x_screen-20,self.y_screen/2-30,'slime']) #droite
            self.mobs.append([0,self.y_screen/2-40,'parasite']) #porte gauche
            self.mobs.append([self.x_screen/2-40,0,'slime'])
            self.vague+=1
        elif self.vague==3 and len(self.mobs)==0:
            self.mobs.append([0,self.y_screen/2-20,'zombie']) #porte gauche
            self.mobs.append([self.x_screen/2,0,'zombie']) #haut 
            self.mobs.append([self.x_screen-20,self.y_screen/2-20,'zombie']) #droite
            self.mobs.append([self.x_screen/2,self.y_screen-20,'zombie']) #bas
            self.vague+=1
        elif self.vague==4 and len(self.mobs)==0:
            self.mobs.append([self.x_screen/2,0,'boss_K_9'])
            self.vague+=1

    def boss_specificity(self):
        for boss in self.mobs:
            if boss[2] == 'boss_K_9':
                if self.life_boss_K_9>0:
                    if (pyxel.frame_count % 38 == 0):                #toute les 1 seconde et demi
                        self.fire_ball_boss['haut'].append([boss[0]+(self.hit_box_all['mob']['boss_K_9'][self.ancien_postion_mob][0])/2,boss[1]])
                        self.fire_ball_boss['droite'].append([boss[0]+self.hit_box_all['mob']['boss_K_9'][self.ancien_postion_mob][0],boss[1]+(self.hit_box_all['mob']['boss_K_9'][self.ancien_postion_mob][1])/2])
                        self.fire_ball_boss['bas'].append([boss[0]+(self.hit_box_all['mob']['boss_K_9'][self.ancien_postion_mob][0])/2,boss[1]+self.hit_box_all['mob']['boss_K_9'][self.ancien_postion_mob][1]])
                        self.fire_ball_boss['gauche'].append([boss[0],boss[1]+(self.hit_box_all['mob']['boss_K_9'][self.ancien_postion_mob][1])/2])
                    if (pyxel.frame_count % 1 == 0):
                        for fire_ball in self.fire_ball_boss:
                            if fire_ball == 'gauche':
                                for fireball_gauche in self.fire_ball_boss[fire_ball]: 
                                    fireball_gauche[0]-=1
                            elif fire_ball == 'droite':
                                for fireball_droite in self.fire_ball_boss[fire_ball]: 
                                    fireball_droite[0]+=1
                            elif fire_ball == 'haut':
                                for fireball_haut in self.fire_ball_boss[fire_ball]: 
                                    fireball_haut[1]-=1
                            elif fire_ball == 'bas':
                                for fireball_bas in self.fire_ball_boss[fire_ball]: 
                                    fireball_bas[1]+=1
                else:
                    self.fire_ball_boss=[]

                                
                        


        

    def target_monster(self):                              #système de targuet des monstres avec les joueurs 
        for ennemis in self.mobs :
            if min(abs(self.x_player1-ennemis[0]),abs(self.y_player1-ennemis[1]))<=min(abs(self.x_player2-ennemis[0]),abs(self.y_player2-ennemis[1])) or self.life_player2<=0:
                if ennemis[0]>self.x_player1:
                    ennemis[0]-=self.mob_speed[ennemis[2]]
                    self.ancien_postion_mob='gauche'
                if ennemis[0]<self.x_player1: 
                    ennemis[0]+=self.mob_speed[ennemis[2]]
                    self.ancien_postion_mob='droite'
                if ennemis[1]<self.y_player1:
                    ennemis[1]+=self.mob_speed[ennemis[2]]
                    self.ancien_postion_mob='bas'
                if ennemis[1]>self.y_player1:
                    ennemis[1]-=self.mob_speed[ennemis[2]]
                    self.ancien_postion_mob='haut'
            if min(abs(self.x_player1-ennemis[0]),abs(self.y_player1-ennemis[1]))>=min(abs(self.x_player2-ennemis[0]),abs(self.y_player2-ennemis[1])) or self.life_player1<=0:
                if ennemis[0]>self.x_player2:
                    ennemis[0]-=self.mob_speed[ennemis[2]]
                    self.ancien_postion_mob='gauche'
                if ennemis[0]<self.x_player2:
                    ennemis[0]+=self.mob_speed[ennemis[2]]
                    self.ancien_postion_mob='droite'
                if ennemis[1]<self.y_player2:
                    ennemis[1]+=self.mob_speed[ennemis[2]]
                    self.ancien_postion_mob='bas'
                if ennemis[1]>self.y_player2:
                    ennemis[1]-=self.mob_speed[ennemis[2]]
                    self.ancien_postion_mob='haut'
    
    def create_power_up(self):    #création des différents power up
        o=random.randint(1,2)
        if o==1:
            self.powers_up.append([random.randint(10,self.x_screen-30),random.randint(10,self.y_screen-30),False,0,0,"speed"])             #Création des powers up (arg:co en x , co en y ,power up activé ou non, temps du power up , qui a eu le power up ,type de power up)
        else:
            self.powers_up.append([random.randint(10,self.x_screen-30),random.randint(10,self.y_screen-30),False,0,0,"life"])
        return

    def manage_power_up(self):             #fonctionnemmnt des powers up
        for items in self.powers_up:
            if items[2]==True :
                items[0],items[1]=10000,10000
                if items[5]=='speed':
                    if (pyxel.frame_count % 30 == 0): 
                        items[3]+=1 
                    if items[4]==1:
                        self.move_speed1=self.up_speed
                    elif items[4]==2:
                        self.move_speed2=self.up_speed
                    if  items[3]==self.time_power_up:
                        if items[4]==1:
                            self.move_speed1=self.move_speed_player_base
                        elif items[4]==2:
                            self.move_speed2=self.move_speed_player_base
                        self.powers_up.remove(items)
                elif items[5]=='life':
                    if items[4]==1:
                        self.life_player1+=self.up_life
                    elif items[4]==2:
                        self.life_player2+=self.up_life
                    if self.life_player1>self.life_base:
                        self.life_player1=self.life_base
                    if self.life_player2>self.life_base:
                        self.life_player2=self.life_base

                    self.powers_up.remove(items)
                    

            



    def collision(self):        #gérer les collisions 
#collision perso
        if 0>self.x_player1:
            self.x_player1=0
        if self.x_player1>self.x_screen-20:
            self.x_player1=self.x_screen-20
        if self.y_player1<0:
            self.y_player1=0
        if self.y_player1>self.y_screen-20:
            self.y_player1=self.y_screen-20

        if 0>self.x_player2:
            self.x_player2=0
        if self.x_player2>self.x_screen-20:
            self.x_player2=self.x_screen-20
        if self.y_player2<0:
            self.y_player2=0
        if self.y_player2>self.y_screen-20:
            self.y_player2=self.y_screen-20

#collision mob
        for ennemis in self.mobs:
            if ennemis[2]=='boss_K_9':
                if self.life_boss_K_9<=0:
                    self.mobs.remove(ennemis)
            if self.x_player1+self.hit_box_all['skin'][self.name_skin_player1][self.ancien_postion_player1][2]>ennemis[0]+self.hit_box_all["mob"][ennemis[2]][self.ancien_postion_mob][0] or self.x_player1+self.hit_box_all['skin'][self.name_skin_player1][self.ancien_postion_player1][0]<ennemis[0]+self.hit_box_all["mob"][ennemis[2]][self.ancien_postion_mob][2] or self.y_player1>ennemis[1]+self.hit_box_all["mob"][ennemis[2]][self.ancien_postion_mob][1] or self.y_player1+self.hit_box_all['skin'][self.name_skin_player1][self.ancien_postion_player1][1]<ennemis[1]:
                pass
            else :
                if ennemis[2]=='boss_K_9':
                    if pyxel.btnr(pyxel.KEY_E):
                        self.life_boss_K_9-=10
                        self.point_player1+=1
                        break
                    else:
                        if (pyxel.frame_count % 30 == 0):
                            self.life_player1-=self.degat_boss
                else:
                    if pyxel.btnr(pyxel.KEY_E):
                        self.mobs.remove(ennemis)
                        self.point_player1+=1
                        break
                    else:
                        if (pyxel.frame_count % 30 == 0):
                            self.life_player1-=self.degat

            if self.x_player2+self.hit_box_all['skin'][self.name_skin_player2][self.ancien_postion_player2][2]>ennemis[0]+self.hit_box_all["mob"][ennemis[2]][self.ancien_postion_mob][0] or self.x_player2+self.hit_box_all['skin'][self.name_skin_player2][self.ancien_postion_player2][0]<ennemis[0]+self.hit_box_all["mob"][ennemis[2]][self.ancien_postion_mob][2] or self.y_player2>ennemis[1]+self.hit_box_all["mob"][ennemis[2]][self.ancien_postion_mob][1] or self.y_player2+self.hit_box_all['skin'][self.name_skin_player2][self.ancien_postion_player2][1]<ennemis[1]:
                pass
            else :
                if ennemis[2]=="boss_K_9":
                    if pyxel.btnr(pyxel.KEY_SHIFT):
                        self.life_boss_K_9-=10
                        self.point_player2+=1
                        break
                    else:
                        if (pyxel.frame_count % 30 == 0):
                            self.life_player2-=self.degat_boss

                else:
                    if pyxel.btnr(pyxel.KEY_SHIFT):
                        self.mobs.remove(ennemis)
                        self.point_player2+=1
                        break
                    else:
                        if (pyxel.frame_count % 30 == 0):
                            self.life_player2-=self.degat
#collision avec les powers up
        for items in self.powers_up:
            if self.x_player1+self.hit_box_all['skin'][self.name_skin_player1][self.ancien_postion_player1][2]>items[0]+self.hit_box_items or self.x_player1+self.hit_box_all['skin'][self.name_skin_player1][self.ancien_postion_player1][0]<items[0] or self.y_player1>items[1]+self.hit_box_items or self.y_player1+self.hit_box_all['skin'][self.name_skin_player1][self.ancien_postion_player1][1]<items[1]:
                pass
            else :
                items[2]=True 
                items[4]=1
            
            if self.x_player2+self.hit_box_all['skin'][self.name_skin_player2][self.ancien_postion_player2][2]>items[0]+self.hit_box_items or self.x_player2+self.hit_box_all['skin'][self.name_skin_player2][self.ancien_postion_player2][0]<items[0] or self.y_player2>items[1]+self.hit_box_items or self.y_player2+self.hit_box_all['skin'][self.name_skin_player2][self.ancien_postion_player2][1]<items[1]:
                pass
            else :
                items[2]=True 
                items[4]=2
#collision avec les fires balls
        for direction in self.fire_ball_boss:
            for ball_fire in range(len(self.fire_ball_boss[direction])-1):
                if self.x_player1+self.hit_box_all['skin'][self.name_skin_player1][self.ancien_postion_player1][2]>self.fire_ball_boss[direction][ball_fire][0]+self.hit_box_all['mob']['fire_ball'][2]+self.hit_box_all['mob']['fire_ball'][0] or self.x_player1+self.hit_box_all['skin'][self.name_skin_player1][self.ancien_postion_player1][0]<self.fire_ball_boss[direction][ball_fire][0]+self.hit_box_all['mob']['fire_ball'][2] or self.y_player1>self.fire_ball_boss[direction][ball_fire][1]+self.hit_box_all['mob']['fire_ball'][1]+self.hit_box_all['mob']['fire_ball'][3] or self.y_player1+self.hit_box_all['skin'][self.name_skin_player1][self.ancien_postion_player1][1]<self.fire_ball_boss[direction][ball_fire][1]+self.hit_box_all['mob']['fire_ball'][3]:
                    pass

                else:
                    self.life_player1-=self.degat
                    self.fire_ball_boss[direction][ball_fire][0]=1000
                    

                if self.x_player2+self.hit_box_all['skin'][self.name_skin_player2][self.ancien_postion_player2][2]>self.fire_ball_boss[direction][ball_fire][0]+self.hit_box_all['mob']['fire_ball'][2]+self.hit_box_all['mob']['fire_ball'][0] or self.x_player2+self.hit_box_all['skin'][self.name_skin_player2][self.ancien_postion_player2][0]<self.fire_ball_boss[direction][ball_fire][0]+self.hit_box_all['mob']['fire_ball'][2] or self.y_player2>self.fire_ball_boss[direction][ball_fire][1]+self.hit_box_all['mob']['fire_ball'][1]+self.hit_box_all['mob']['fire_ball'][3] or self.y_player2+self.hit_box_all['skin'][self.name_skin_player2][self.ancien_postion_player2][1]<self.fire_ball_boss[direction][ball_fire][1]+self.hit_box_all['mob']['fire_ball'][3]:
                    pass

                else:
                    self.life_player2-=self.degat
                    self.fire_ball_boss[direction][ball_fire][0]=1000

                
                if self.fire_ball_boss[direction][ball_fire][0]+self.hit_box_all['mob']['fire_ball'][2]<=0 or self.fire_ball_boss[direction][ball_fire][0]+self.hit_box_all['mob']['fire_ball'][2]+self.hit_box_all['mob']['fire_ball'][0]>=self.x_screen or self.fire_ball_boss[direction][ball_fire][1]+self.hit_box_all['mob']['fire_ball'][3]<=0 or self.fire_ball_boss[direction][ball_fire][1]+self.hit_box_all['mob']['fire_ball'][3]+self.hit_box_all['mob']['fire_ball'][1]>=self.y_screen:
                    self.fire_ball_boss[direction][ball_fire][0]=1000

            
        




    def page(self,pages):
        if pyxel.mouse_x>self.button[pages]['x']+self.button[pages]['bordure_x']+self.button[pages]['hitbox_x'] or pyxel.mouse_x<self.button[pages]['x']+self.button[pages]['bordure_x'] or pyxel.mouse_y>self.button[pages]['y']+self.button[pages]['bordure_y']+self.button[pages]['hitbox_y'] or pyxel.mouse_y<self.button[pages]['y']+self.button[pages]['bordure_y']:
            self.button[pages]['pushing_on']=False
        else:
            self.button[pages]['pushing_on']=True
            if pages=='play':
                if pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT) or pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btn(pyxel.MOUSE_BUTTON_MIDDLE):
                        self.etat=True
            elif pages=='restart':
                if pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT) or pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btn(pyxel.MOUSE_BUTTON_MIDDLE):      
                    self.x_player1=self.x_screen/2
                    self.y_player1=self.y_screen/2
                    self.x_player2=self.x_screen/2-20
                    self.y_player2=self.y_screen/2-20
                    self.vague=0   
                    self.powers_up=[]
                    self.power_up_activated=[]  
                    self.mobs=[]
                    self.ancien_postion_mob='bas'
                    self.ancien_postion_player1='bas'
                    self.ancien_postion_player2='bas'
                    self.ancien_cut_postion_player1=''
                    self.ancien_cut_postion_player2=''
                    self.life_player1=self.life_base
                    self.life_player2=self.life_base
                    self.life_boss_K_9=200
                    self.point_player1=0
                    self.point_player2=0
                    self.fire_ball_boss={'gauche': [],'droite':[],'haut':[],'bas':[]}
                    self.etat=True
            



    
    def update(self):                     #mise à jours du jeu 
        if self.etat == True:
            if self.life_player1<=0 or self.life_player2<=0 or self.life_boss_K_9<=0:
                self.etat="restart"
                 
            self.move_players()
            self.collision()
            self.creation_monster()
            self.target_monster()
            self.boss_specificity()
            if (pyxel.frame_count % 125==0):
                self.create_power_up()
            self.manage_power_up()


            if pyxel.btnr(pyxel.KEY_SPACE):
                self.etat='pause'                                                                                                                                                                                         
        elif self.etat == 'pause' :
            if pyxel.btnr(pyxel.KEY_SPACE):
                self.etat=True   
            
        elif self.etat=='start':
            self.page('play')
        elif self.etat=='restart':
            self.page('restart')
        
                
        
    def count_frame_animation(self) :
        self.index+=1
        if self.index>1:
            self.index=0   
    
    
    def draw(self):                                 #mise à jours de l'écran et gérer tous les graphismes
        pyxel.cls(0)
        if self.etat ==True :
            pyxel.mouse(False)
            pyxel.bltm(0,0, 0, 0,0, 128*8,128*8)
            if self.life_player1>0:
                if self.ancien_postion_player1=='gauche':
                    if pyxel.btn(pyxel.KEY_E):
                        pyxel.blt(self.x_player1,self.y_player1,0,self.skin_player1[self.name_skin_player1]['cut_gauche'][0],self.skin_player1[self.name_skin_player1]['cut_gauche'][1],16,16,self.skin_player1[self.name_skin_player1]['cut_gauche'][2])
                    else:
                        pyxel.blt(self.x_player1,self.y_player1,0,self.skin_player1[self.name_skin_player1]['gauche'][0],self.skin_player1[self.name_skin_player1]['gauche'][1],16,16,self.skin_player1[self.name_skin_player1]['gauche'][2])
                elif self.ancien_postion_player1=='droite':
                    if pyxel.btn(pyxel.KEY_E):
                        pyxel.blt(self.x_player1,self.y_player1,0,self.skin_player1[self.name_skin_player1]['cut_droite'][0],self.skin_player1[self.name_skin_player1]['cut_droite'][1],16,16,self.skin_player1[self.name_skin_player1]['cut_droite'][2])
                    else:
                        pyxel.blt(self.x_player1,self.y_player1,0,self.skin_player1[self.name_skin_player1]['droite'][0],self.skin_player1[self.name_skin_player1]['droite'][1],16,16,self.skin_player1[self.name_skin_player1]['droite'][2])
                elif self.ancien_postion_player1=='haut':
                    if pyxel.btn(pyxel.KEY_E):
                        pyxel.blt(self.x_player1,self.y_player1,0,self.skin_player1[self.name_skin_player1]['cut_haut'][0],self.skin_player1[self.name_skin_player1]['cut_haut'][1],16,16,self.skin_player1[self.name_skin_player1]['cut_haut'][2])
                    else:
                        pyxel.blt(self.x_player1,self.y_player1,0,self.skin_player1[self.name_skin_player1]['haut'][0],self.skin_player1[self.name_skin_player1]['haut'][1],16,16,self.skin_player1[self.name_skin_player1]['haut'][2])
                elif self.ancien_postion_player1=='bas':
                    if pyxel.btn(pyxel.KEY_E):
                        pyxel.blt(self.x_player1,self.y_player1,0,self.skin_player1[self.name_skin_player1]['cut_bas'][0],self.skin_player1[self.name_skin_player1]['cut_bas'][1],16,16,self.skin_player1[self.name_skin_player1]['cut_bas'][2])
                    else:
                        pyxel.blt(self.x_player1,self.y_player1,0,self.skin_player1[self.name_skin_player1]['bas'][0],self.skin_player1[self.name_skin_player1]['bas'][1],16,16,self.skin_player1[self.name_skin_player1]['bas'][2])
            
            
           
            if self.life_player2>0:
                if self.ancien_postion_player2=='gauche':
                    if pyxel.btn(pyxel.KEY_SHIFT):
                        pyxel.blt(self.x_player2,self.y_player2,0,self.skin_player2[self.name_skin_player2]['cut_gauche'][0],self.skin_player2[self.name_skin_player2]['cut_gauche'][1],16,16,self.skin_player2[self.name_skin_player2]['cut_gauche'][2])
                    else:
                        pyxel.blt(self.x_player2,self.y_player2,0,self.skin_player2[self.name_skin_player2]['gauche'][0],self.skin_player2[self.name_skin_player2]['gauche'][1],16,16,self.skin_player2[self.name_skin_player2]['gauche'][2])
                elif self.ancien_postion_player2=='droite':
                    if pyxel.btn(pyxel.KEY_SHIFT):
                        pyxel.blt(self.x_player2,self.y_player2,0,self.skin_player2[self.name_skin_player2]['cut_droite'][0],self.skin_player2[self.name_skin_player2]['cut_droite'][1],16,16,self.skin_player2[self.name_skin_player2]['cut_droite'][2])
                    else:
                        pyxel.blt(self.x_player2,self.y_player2,0,self.skin_player2[self.name_skin_player2]['droite'][0],self.skin_player2[self.name_skin_player2]['droite'][1],16,16,self.skin_player2[self.name_skin_player2]['droite'][2])
                elif self.ancien_postion_player2=='haut':
                    if pyxel.btn(pyxel.KEY_SHIFT):
                        pyxel.blt(self.x_player2,self.y_player2,0,self.skin_player2[self.name_skin_player2]['cut_haut'][0],self.skin_player2[self.name_skin_player2]['cut_haut'][1],16,16,self.skin_player2[self.name_skin_player2]['cut_haut'][2])
                    else:
                        pyxel.blt(self.x_player2,self.y_player2,0,self.skin_player2[self.name_skin_player2]['haut'][0],self.skin_player2[self.name_skin_player2]['haut'][1],16,16,self.skin_player2[self.name_skin_player2]['haut'][2])
                elif self.ancien_postion_player2=='bas':
                    if pyxel.btn(pyxel.KEY_SHIFT):
                        pyxel.blt(self.x_player2,self.y_player2,0,self.skin_player2[self.name_skin_player2]['cut_bas'][0],self.skin_player2[self.name_skin_player2]['cut_bas'][1],16,16,self.skin_player2[self.name_skin_player2]['cut_bas'][2])
                    else:
                        pyxel.blt(self.x_player2,self.y_player2,0,self.skin_player2[self.name_skin_player2]['bas'][0],self.skin_player2[self.name_skin_player2]['bas'][1],16,16,self.skin_player2[self.name_skin_player2]['bas'][2])
           
            for ennemis in self.mobs:
                if ennemis[2]=='parasite':
                    pyxel.blt(ennemis[0],ennemis[1],0,72,0,16,16,0)
                elif ennemis[2] == 'slime':
                    pyxel.blt(ennemis[0],ennemis[1],0,96,8,16,16,9)
                elif ennemis[2]=='zombie':
                    if self.ancien_postion_mob=='gauche':
                        pyxel.blt(ennemis[0],ennemis[1],0,120,48,16,16,2)
                    elif self.ancien_postion_mob=='droite':
                        pyxel.blt(ennemis[0],ennemis[1],0,120,24,16,16,2)
                    elif self.ancien_postion_mob=='haut':
                        pyxel.blt(ennemis[0],ennemis[1],0,96,24,16,16,2)
                    elif self.ancien_postion_mob=='bas':
                        pyxel.blt(ennemis[0],ennemis[1],0,72,24,16,16,2)
                for fire_ball in self.fire_ball_boss:
                    for fireball_gauche in self.fire_ball_boss[fire_ball]:                            
                        pyxel.blt(fireball_gauche[0],fireball_gauche[1],0,144,96,16,16,0)
                if ennemis[2] == "boss_K_9":
                    pyxel.blt(ennemis[0],ennemis[1],0,72,48,16,16,9)
                    pyxel.blt(ennemis[0]+16,ennemis[1],0,88,48,16,16,9)
                    pyxel.blt(ennemis[0],ennemis[1]+16,0,72,64,16,16,9)
                    pyxel.blt(ennemis[0]+16,ennemis[1]+16,0,88,64,16,16,9)
                
            


                    


            for items in self.powers_up:
                if items[5]=='speed':
                    pyxel.blt(items[0],items[1],0,112,96,16,16,0)
                elif items[5]=='life':
                    pyxel.blt(items[0],items[1],0,128,96,16,16,0)
                    
            if self.life_player1>=self.life_base:    #système de vie joueur 1
                pyxel.blt(40,0,0,112,64,16,16,0)
            if self.life_player1>=self.life_base-20:
                pyxel.blt(40,0,0,128,64,16,16,0)
            if self.life_player1>=self.life_base-40:
                pyxel.blt(30,0,0,112,64,16,16,0)
            if self.life_player1>=self.life_base-60:
                pyxel.blt(30,0,0,128,64,16,16,0)
            if self.life_player1>=self.life_base-80:
                pyxel.blt(20,0,0,112,64,16,16,0)
            if self.life_player1>=self.life_base-100:
                pyxel.blt(20,0,0,128,64,16,16,0)
            if self.life_player1>=self.life_base-120:
                pyxel.blt(10,0,0,112,64,16,16,0)
            if self.life_player1>=self.life_base-140:
                pyxel.blt(10,0,0,128,64,16,16,0)
            if self.life_player1>=self.life_base-160:
                pyxel.blt(0,0,0,112,64,16,16,0)
            if self.life_player1>=self.life_base-180:
                pyxel.blt(0,0,0,128,64,16,16,0)


            if self.life_player2>=self.life_base:           #système de vie joueur 2
                pyxel.blt(78,0,0,112,64,16,16,0)
            if self.life_player2>=self.life_base-20:
                pyxel.blt(78,0,0,128,64,16,16,0)
            if self.life_player2>=self.life_base-40:
                pyxel.blt(88,0,0,112,64,16,16,0)
            if self.life_player2>=self.life_base-60:
                pyxel.blt(88,0,0,128,64,16,16,0)
            if self.life_player2>=self.life_base-80:
                pyxel.blt(98,0,0,112,64,16,16,0)
            if self.life_player2>=self.life_base-100:
                pyxel.blt(98,0,0,128,64,16,16,0)
            if self.life_player2>=self.life_base-120:
                pyxel.blt(108,0,0,112,64,16,16,0)
            if self.life_player2>=self.life_base-140:
                pyxel.blt(108,0,0,128,64,16,16,0)
            if self.life_player2>=self.life_base-160:
                pyxel.blt(118,0,0,112,64,16,16,0)
            if self.life_player2>=self.life_base-180:
                pyxel.blt(118,0,0,128,64,16,16,0)
        
        elif self.etat == 'start':
            pyxel.bltm(0,0, 0, 128,0, 128*8,128*8)
            pyxel.mouse(True)
            if self.button['play']['pushing_on']==True:
                pyxel.blt(self.button['play']['x'],self.button['play']['y'],0,144,144,16,16,9)
                pyxel.blt(self.button['play']['x']+16,self.button['play']['y'],0,160,144,16,16,9)
                pyxel.blt(self.button['play']['x']+32,self.button['play']['y'],0,176,144,16,16,9)
                pyxel.blt(self.button['play']['x'],self.button['play']['y']+16,0,144,160,16,16,9)
                pyxel.blt(self.button['play']['x']+16,self.button['play']['y']+16,0,160,160,16,16,9)
                pyxel.blt(self.button['play']['x']+32,self.button['play']['y']+16,0,176,160,16,16,9)

            else:
                pyxel.blt(self.button['play']['x'],self.button['play']['y'],0,144,112,16,16,9)
                pyxel.blt(self.button['play']['x']+16,self.button['play']['y'],0,160,112,16,16,9)
                pyxel.blt(self.button['play']['x']+32,self.button['play']['y'],0,176,112,16,16,9)
                pyxel.blt(self.button['play']['x'],self.button['play']['y']+16,0,144,128,16,16,9)
                pyxel.blt(self.button['play']['x']+16,self.button['play']['y']+16,0,160,128,16,16,9)
                pyxel.blt(self.button['play']['x']+32,self.button['play']['y']+16,0,176,128,16,16,9)

        elif self.etat=='pause':
            pyxel.bltm(0,0, 0, 128,0, 128*8,128*8)
            pyxel.blt(55,80,0,168,0,16,16,9)
        elif self.etat == 'restart':
            pyxel.bltm(0,0, 0, 374,0, 128*8,128*8)
            pyxel.mouse(True)
            if self.button['restart']['pushing_on']==True:
                pyxel.blt(self.button['restart']['x'],self.button['restart']['y'],0,144,56,16,16,9)
                pyxel.blt(self.button['restart']['x']+16,self.button['restart']['y'],0,160,56,16,16,9)
                pyxel.blt(self.button['restart']['x']+32,self.button['restart']['y'],0,176,56,16,16,9)
                pyxel.blt(self.button['restart']['x'],self.button['restart']['y']+16,0,144,72,16,16,9)
                pyxel.blt(self.button['restart']['x']+16,self.button['restart']['y']+16,0,160,72,16,16,9)
                pyxel.blt(self.button['restart']['x']+32,self.button['restart']['y']+16,0,176,72,16,16,9)

            else:
                pyxel.blt(self.button['restart']['x'],self.button['restart']['y'],0,144,24,16,16,9)
                pyxel.blt(self.button['restart']['x']+16,self.button['restart']['y'],0,160,24,16,16,9)
                pyxel.blt(self.button['restart']['x']+32,self.button['restart']['y'],0,176,24,16,16,9)
                pyxel.blt(self.button['restart']['x'],self.button['restart']['y']+16,0,144,40,16,16,9)
                pyxel.blt(self.button['restart']['x']+16,self.button['restart']['y']+16,0,160,40,16,16,9)
                pyxel.blt(self.button['restart']['x']+32,self.button['restart']['y']+16,0,176,40,16,16,9)
            if (pyxel.frame_count % 13==0):
                    self.count_frame_animation()
            if self.life_player1<=0 or self.life_player1>0 and self.life_player2>0 and self.point_player1<self.point_player2:
                pyxel.blt(87,72,0,176,96,16,16,0)     #couronne
                if self.index==1:
                    pyxel.blt(25,90,0,72,192,16,16,9)                  #joueur 1 triste animation 1
                    pyxel.blt(87,90,0,104,208,16,16,9)               #joueur 2 heureux animation 1
                else:
                    pyxel.blt(25,90,0,88,192,16,16,9)               #joueur 1 triste animation 2
                    pyxel.blt(87,90,0,120,208,16,16,9)             #joueur 2 heureux animation 2
            elif self.life_player2<=0 or self.life_player1>0 and self.life_player2>0 and self.point_player1>self.point_player2:
                pyxel.blt(25,72,0,176,96,16,16,0)     #couronne
                if self.index==1:
                    pyxel.blt(25,90,0,104,192,16,16,9)            #joueur 1 heureux animation 1
                    pyxel.blt(87,90,0,72,208,16,16,9)           #joueur 2 triste animation 1
                else:
                    pyxel.blt(25,90,0,120,192,16,16,9)            #joueur 1 heureux animation 2
                    pyxel.blt(87,90,0,88,208,16,16,9)         #joueur 2 triste animation 2
            else:
                pyxel.blt(25,72,0,176,96,16,16,0)     #couronne
                pyxel.blt(87,72,0,176,96,16,16,0)     #couronne
                if self.index==1:
                    pyxel.blt(25,90,0,104,192,16,16,9)            #joueur 1 heureux animation 1
                    pyxel.blt(87,90,0,104,208,16,16,9)               #joueur 2 heureux animation 1
                else:
                    pyxel.blt(25,90,0,120,192,16,16,9)            #joueur 1 heureux animation 2
                    pyxel.blt(87,90,0,120,208,16,16,9)             #joueur 2 heureux animation 2

            pyxel.text(20, 108, "Score:"+str(self.point_player1), 7)
            pyxel.text(82, 108, "Score:"+str(self.point_player2), 7)

                    

            


   
jeux=Game()
