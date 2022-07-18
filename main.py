# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 17:30:47 2022

@author: rsp97
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 18:40:17 2022

@author: rsp97
"""


import pygame
import os
import random
import sys
import neat
import math
import time

pygame.init()

#global constants
screen_height = 600
screen_width = 1100
screen = pygame.display.set_mode((screen_width,screen_height),pygame.RESIZABLE)

#get current time
mytime = time.localtime()
#set title
pygame.display.set_caption('DINO RUN')


running = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

jumping = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))


ducking = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]


#obstacles images (cactus- small, large)
small_cactus = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
large_cactus = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

bird = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

cloud = [pygame.image.load(os.path.join("Assets/Other", "Cloud.png")),
         pygame.image.load(os.path.join("Assets/Other", "stars.png"))]

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))
                                         
font=pygame.font.Font('freesansbold.ttf', 20)

class Dinosaur:
    x_pos = 80
    y_pos = 310
    y_pos_duck=380
    JUMP_VEL = 8.5
    
    def __init__(self,img=running[0]):
        
        self.duck_img = ducking
        self.dino_duck = False
        self.image = img
        self.dino_run = True
        self.dino_jump = False
        
        self.jump_vel = self.JUMP_VEL
        self.rect = pygame.Rect(self.x_pos, self.y_pos, img.get_width(), img.get_height())
        #coloured hit box
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.step_index = 0
        
    def update(self,userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
            
        if self.step_index >= 10:
            self.step_index = 0
        
        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
    
    def duck(self):
       self.image = self.duck_img[self.step_index // 5]
       self.dino_rect = self.image.get_rect()
       self.dino_rect.x = self.x_pos
       self.dino_rect.y = self.y_pos_duck
       self.step_index += 1    
   
     
    def jump(self):
        self.image=jumping
        if self.dino_jump:
            self.rect.y -= self.jump_vel*4   #important --------------->>>>>
            self.jump_vel -= 0.8
        if self.jump_vel <= -self.JUMP_VEL:
            self.dino_jump = False
            self.dino_run = True
            self.jump_vel = self.JUMP_VEL
            
    def run(self):
        self.image = running[self.step_index // 5]
        self.dino_rect=self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos
        self.step_index += 1
        
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        #draw rectangle 
        pygame.draw.rect(screen, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height),2)
        #put end of line
        for obstacle in obstacles:
            pygame.draw.line(screen, self.color, (self.rect.x + 54, self.rect.y + 12), obstacle.rect.center, 2)

class Cloud:
    def __init__(self,img=cloud[0]):
        self.x = screen_width + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = img
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = screen_width + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class Star(pygame.sprite.Sprite):
	def __init__(self, x, y, type):
		super(Star, self).__init__()
		image = pygame.image.load(os.path.join("Assets/Other", "stars.png"))
		self.image_list = []
		for i in range(3):
			img = image.subsurface((0, 20*(i), 18, 18))
			self.image_list.append(img)
		self.image = self.image_list[type-1]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
        
	def draw(self, SCREEN):
		SCREEN.blit(self.image, self.rect)
        
class Obstacle:
    def __init__(self, image, number_of_cactuses):
        self.image = image
        self.type = number_of_cactuses
        self.rect = self.image[self.type].get_rect()
        self.rect.x = screen_width
        
    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
    
    def draw(self,screen):
        screen.blit(self.image[self.type], self.rect)        

class SmallCactus(Obstacle):
    def __init__(self, image, number_of_cactuses):
        super().__init__(image, number_of_cactuses)
        self.rect.y=325  
        
class LargeCactus(Obstacle):
    def __init__(self, image, number_of_cactuses):
        super().__init__(image, number_of_cactuses)
        self.rect.y=300


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 240
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


def remove(index):
    dinosaurs.pop(index)
    ge.pop(index) #remove genome
    nets.pop(index) #nets
    
def distance(pos_a, pos_b):
    dx = pos_a[0]-pos_b[0]
    dy = pos_a[1]-pos_b[1]
    return math.sqrt(dx**2+dy**2)

def read_score_from_file():
    f=open("F_High_Score.txt","r")
    return f.read()
    f.close()
    

def eval_genomes(genomes, config):
    global game_speed, x_pos_bg, y_pos_bg, obstacles, dinosaurs, ge, nets, points
    clock = pygame.time.Clock()
    points=0
    global highest_points_from_file
    cloud=Cloud()
    type = random.randint(1, 3)
    y = random.randint(40, 100)
    stars=Star(screen_width, y, type)    
    
    highest_points_from_file=read_score_from_file()
    print(highest_points_from_file)
    
    obstacles=[] #store created obstacles
    dinosaurs = [] #list i have created to put multiple dinosaurs
    ge = [] # genomes ==> dino-fitness level, nodes and connection store into list
    nets = [] #neural net object of each individual dino.
    
    #################
    x_pos_bg=0
    y_pos_bg=380
    game_speed=20
    
    for genome_id, genome in genomes:
        dinosaurs.append(Dinosaur())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0
    
        
    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            #increase game speed when score reach multiple of 100 points
            game_speed += 1
        #display score on screen    
        text=font.render(f'Points: {str(points)}',True, (0,255,0))
        screen.blit(text,(950, 50)) #blit()=copy the contents of one Surface onto another Surface 

        #display high-score on screen
        text1=font.render(f'Highest Points: {str(highest_points_from_file)}',True, (0,255,0))
        screen.blit(text1,(725, 50)) #blit()=copy the contents of one Surface onto another Surface 
    
    def statistics():
        global dinosaurs, game_speed, ge
        text_1=font.render(f'Dinosaurs Alive: {str(len(dinosaurs))}', True, (0,255,0))
        text_2=font.render(f'Generation: {pop.generation+1}', True, (0,255,0))
        text_3=font.render(f'Game Speed: {str(game_speed)}', True, (0,255,0))
    
        screen.blit(text_1, (50, 450))
        screen.blit(text_2, (50, 480))
        screen.blit(text_3, (50, 510))
        
    #create moving background
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        screen.blit(BG, (x_pos_bg, y_pos_bg))
        screen.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg=0
        x_pos_bg -= game_speed
        
     
    #pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
    run=True
    flag_high_score=True
    flag_display_high_score=False
    highest_points=0
    
    while run:
        # #display score on screen    
        # text=font.render(f'Points: {str(points)}',True, (0,0,0))
        # screen.blit(text,(950, 50)) #blit()=copy the contents of one Surface onto another Surface 
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        #reset screen
        if mytime.tm_hour >= 5 and mytime.tm_hour <= 16:
            screen.fill((255, 255, 255))
            print("if")
        else:
            screen.fill((25, 25, 25))   
        
        userInput = pygame.key.get_pressed()

        
        for dinosaur in dinosaurs:
            #dinosaur.update()
            dinosaur.draw(screen)
            dinosaur.update(userInput)

        if len(dinosaurs) == 0:
            break
        
        #generate cactuses randomly on screen
        if len(obstacles)==0:
            rand_int=random.randint(0, 2)
            if rand_int == 0:
                obstacles.append(SmallCactus(small_cactus, random.randint(0, 2)))
            elif rand_int == 1:
                obstacles.append(LargeCactus(large_cactus, random.randint(0, 2)))
            elif rand_int == 2:
                obstacles.append(Bird(bird))
                
        for obstacle in obstacles:
            obstacle.draw(screen)
            obstacle.update()
            for i, dinosaur in enumerate(dinosaurs):
                if dinosaur.rect.colliderect(obstacle.rect): #colliderect() = to add collision
                    ge[i].fitness -= 1 #decrease their chance of passing their genes to the next generation of dino. 
                    remove(i) #game quit
                    flag_high_score=True
                    
        if(flag_high_score==False and len(dinosaurs)==0):
            #open file
            file = open("F_High_Score.txt", "r")
            
            high_score_in_file=file.read().strip()
            
            high_score_in_file=int(high_score_in_file) #convert str to int
            print(type(high_score_in_file))
            
            file.close()
            if(high_score_in_file<points):
                #input text
                highest_points = points  
                #score_collision = points
                #store high_score value in file            
                #add variable value in file    
                file = open("F_High_Score.txt", "w")
                file.write(str(highest_points))
                file.close()
            #close file
            flag_high_score=False
            #flag_display_high_score=True

        user_input=pygame.key.get_pressed()
        
        
        for i, dinosaur in enumerate(dinosaurs):
            #input of each indicidual dino.
            output = nets[i].activate((dinosaur.rect.y, #y position
                                       distance( (dinosaur.rect.x, dinosaur.rect.y), obstacle.rect.midtop ) # last 2 line => distance()-> distance to the next obstacle into its neural network
                                       ))
            
            if output[0] > 0.5 and dinosaur.rect.y == dinosaur.y_pos: #after and -> 2nd=dino is not currently jumping then initiate jump 
                dinosaur.dino_jump=True
                dinosaur.dino_run=False
                 
        statistics()
        score()
        if(int(highest_points_from_file)<int(points)):
            highest_points_from_file=read_score_from_file()
        
        background()        
        cloud.draw(screen)
        cloud.update()
        stars.draw(screen)
        clock.tick(30)
        pygame.display.update()
        

    
    
        
    
def menu(death_count):
    global points
    run = True
    while run:
        
        if mytime.tm_hour >= 5 and mytime.tm_hour <= 16:
            screen.fill((255, 255, 255))
        else:
            screen.fill((50, 50, 50))
            #print("else block")
            
        
        font = pygame.font.Font('freesansbold.ttf', 30)

        try:
            if death_count == 0:
                text = font.render("Press any Key to Start", True, (0, 255, 0))
            elif death_count > 0:
                text = font.render("Press any Key to Restart", True, (0, 255, 0))
                score = font.render("Your Score: " + str(points), True, (0, 255, 0))
                scoreRect = score.get_rect()
                scoreRect.center = (screen_width // 2, screen_height // 2 + 50)
                screen.blit(score, scoreRect)
        except:
            print("error occured")
            exit()
        
        
        textRect = text.get_rect()
        textRect.center = (screen_width // 2, screen_height// 2)
        screen.blit(text, textRect)
        screen.blit(running[0], (screen_width// 2 - 20, screen_height// 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                #setup the NEAT
                def run(config_path):  
                    global pop
                    config = neat.config.Config(
                        neat.DefaultGenome,
                        neat.DefaultReproduction,
                        neat.DefaultSpeciesSet,
                        neat.DefaultStagnation,
                        config_path
                    )
                    
                    pop = neat.Population(config)
                    pop.run(eval_genomes,50)

                if __name__ == '__main__':
                    if os.path.getsize("F_High_Score.txt") == 0: 
                        f=open("F_High_Score.txt","w")
                        f.write("0")
                        f.close()
                        print("file is empty")
                    local_dir = os.path.dirname(__file__)
                    config_path = os.path.join(local_dir, 'venv_library_root/config.txt')
                    run(config_path)
                


menu(death_count=0)


#call main function
#main()




#next
#add function that show high score on console.
#