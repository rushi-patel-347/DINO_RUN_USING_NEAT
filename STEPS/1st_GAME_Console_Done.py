# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 17:50:44 2022

@author: rsp97
"""

#Note:-
############
#I have created full gaming console ->Next--> apply AI

############

import pygame
import os
import random
import sys

pygame.init()

#global constants
screen_height = 700
screen_width = 1100
screen = pygame.display.set_mode((screen_width,screen_height))

running = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

jumping = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

#obstacles images (cactus- small, large)
small_cactus = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
large_cactus = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))
                                         
font=pygame.font.Font('freesansbold.ttf', 20)

class Dinosaur:
    x_pos = 80
    y_pos = 310
    JUMP_VEL = 8.5
    
    def __init__(self,img=running[0]):
        self.image=img
        self.dino_run = True
        self.dino_jump = False
        self.jump_vel = self.JUMP_VEL
        self.rect = pygame.Rect(self.x_pos, self.y_pos, img.get_width(), img.get_height())
        self.step_index = 0
        
    def update(self):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.step_index >= 10:
            self.step_index=0
        
    def jump(self):
        self.image=jumping
        if self.dino_jump:
            self.rect.y -= self.jump_vel*4
            self.jump_vel -= 0.8
        if self.jump_vel <= -self.JUMP_VEL:
            self.dino_jump = False
            self.dino_run = True
            self.jump_vel = self.JUMP_VEL
            
    def run(self):
        self.image = running[self.step_index // 5]
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos
        self.step_index += 1
        
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

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

def remove(index):
    dinosaurs.pop(index)

def main():
    global game_speed, x_pos_bg, y_pos_bg, obstacles, dinosaurs, points
    clock = pygame.time.Clock()
    points=0
    
    obstacles=[] #store created obstacles
    dinosaurs = [Dinosaur()] #list i have created to put multiple dinosaurs
    x_pos_bg=0
    y_pos_bg=380
    game_speed=20
    
    def score():
        global points, game_speed
        points+=1
        if points % 100 == 0:
            #increase game speed when score reach multiple of 100 points
            game_speed += 1
        #display score on screen    
        text=font.render(f'Points: {str(points)}',True, (0,0,0))
        screen.blit(text,(950, 50)) #blit()=copy the contents of one Surface onto another Surface 
    
    #create moving background
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        screen.blit(BG, (x_pos_bg, y_pos_bg))
        screen.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg=0
        x_pos_bg -= game_speed
        
        
    run=True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((255,255,255))        
        
        for dinosaur in dinosaurs:
            dinosaur.update()
            dinosaur.draw(screen)
        
        if len(dinosaurs) == 0:
            break
        
        #generate cactuses randomly on screen
        if len(obstacles)==0:
            rand_int=random.randint(0, 1)
            if rand_int == 0:
                obstacles.append(SmallCactus(small_cactus, random.randint(0, 2)))
            elif rand_int == 1:
                obstacles.append(LargeCactus(large_cactus, random.randint(0, 2)))
                
        for obstacle in obstacles:
            obstacle.draw(screen)
            obstacle.update()
            for i, dinosaur in enumerate(dinosaurs):
                if dinosaur.rect.colliderect(obstacle.rect): #colliderect() = to add collision
                    remove(i) #game quit
                    #take screenshot during collision
                    rect = pygame.Rect(screen.get_rect())
                    sub = screen.subsurface(rect)
                    pygame.image.save(sub, "collision_screenshot.jpg")
                    
                    #input text
                    score_collision = points
                     
                    #open file
                    file = open("Collision_Data.txt", "a")
                     
                    #add variable
                    file.write("input_dictionary = " + str(score_collision) + "\n")
                     
                    #close file
                    file.close()
                     
                    f = open('Collision_Data.txt', 'r')
                    if f.mode=='r':
                        contents= f.read()
                    
                    #stop the game
                    run=False
                    
        
        user_input=pygame.key.get_pressed()
        
        for i, dinosaur in enumerate(dinosaurs):
            if user_input[pygame.K_SPACE]:
                dinosaur.dino_jump=True
                dinosaur.dino_run=False
                
        score()
        background()        
        clock.tick(30)
        pygame.display.update()

#call main function
main()