import pygame
from pygame import surface
from pygame import time
from pygame import display
from pygame import image
from pygame.constants import QUIT
from sys import exit
from random import choice, randint, choice

#Initialing the pygame --- mandatory
pygame.init()

#setting up main background screen ----- Black
screen=pygame.display.set_mode((800, 400))

#setting/importing up game sound
bg_music=pygame.mixer.Sound('pygame/music.wav')
bg_music.play()
bg_music.set_volume(0.01)

#setting up different background chronologically above the main background
sky_surface=pygame.image.load('pygame/Sky.png').convert()
ground_surface=pygame.image.load('pygame/ground.png').convert()
ground_rect=ground_surface.get_rect(topleft=(0, 300))

#Player and Obstacles classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1=pygame.image.load('pygame/player_walk_1.png').convert_alpha()
        player_walk_2=pygame.image.load('pygame/player_walk_2.png').convert_alpha()
        self.player_walk=[player_walk_1, player_walk_2]
        self.player_index=0
        self.player_jump=pygame.image.load('pygame/jump.png').convert_alpha()

        self.jump_sound=pygame.mixer.Sound('pygame/audio_jump.mp3')
        self.jump_sound.set_volume(0.08)

        self.image=self.player_walk[self.player_index]
        self.rect=self.image.get_rect(midbottom=(80,300))
        self.gravity=0
    
    def player_input(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity=-20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity+=1
        self.rect.y+=self.gravity
        if self.rect.bottom >= 300: self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index+=0.1
            if self.player_index >= len(self.player_walk): self.player_index=0
            self.image=self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type=='fly':
            fly_frame1=pygame.image.load('pygame/fly1.png').convert_alpha()
            fly_frame2=pygame.image.load('pygame/fly2.png').convert_alpha()
            self.frame=[fly_frame1, fly_frame2]
            y_pos=210
        else:
            snail_frame1=pygame.image.load('pygame/snail1.png').convert_alpha() 
            snail_frame2=pygame.image.load('pygame/snail2.png').convert_alpha() 
            self.frame=[snail_frame1, snail_frame2]
            y_pos=300

        self.animation_index = 0
        self.image=self.frame[self.animation_index]
        self.rect=self.image.get_rect(midbottom=(randint(900, 1100), y_pos))
    
    def animation_state(self):
        self.animation_index+=0.1
        if self.animation_index >=len(self.frame): self.animation_index = 0
        self.image=self.frame[int(self.animation_index)]

    def destroy(self):
        if self.rect.x == -100:
            self.kill

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()


#Displayboard function
def display_score():
    current_time=int((pygame.time.get_ticks()-start_time)/1000)
    score_surface=test_font.render(f'{current_time}', False, (64,64,64))
    score_rect=score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect )
    return str(current_time)

#checking collision of sprite and groups from different class
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacles_group, False):
        obstacles_group.empty()
        gameover=pygame.mixer.Sound('pygame/gameover.wav')
        gameover.set_volume(0.3)
        gameover.play()
        gameover.play()
        return False
    else: return True

#Naming the title of the Game ---- Dispayed in title bar
pygame.display.set_caption('Predators')
clock=pygame.time.Clock()

#importing font for displaying letters in the game 
test_font=pygame.font.Font('pygame/Pixeltype.ttf', 50)


#Characters group
obstacles_group=pygame.sprite.Group()


player=pygame.sprite.GroupSingle()
player.add(Player())

obstacle_rect_list=[]


# player_gravity=0
game_active=False
start_time=0
game_score=0


#Variables used after the GAME ENDS
#PLAYER IMAGE FOR DISPLAYING AFTER THE GAME ENDS
player_stand=pygame.image.load('pygame/player_stand.png').convert_alpha()
player_stand=pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect=player_stand.get_rect(center=(400,180))

#GAME NAME VARIABLE
game_name=test_font.render('Predators', False, 'Green')
game_name=pygame.transform.rotozoom(game_name, 0, 1.2)
game_name_rect=game_name.get_rect(center=(400, 60))

#TOTAL SCORE BOARD
total_score=test_font.render(f'Total Score: {game_score}', False, 'Red')
total_score_rect=total_score.get_rect(center=(400, 300))

#GAME RESTARTING MESSAGE
restart_inst=test_font.render('Enter  "SPACE"  to  restart', False, 'White')
restart_inst=pygame.transform.rotozoom(restart_inst, 0, 0.8)
restart_inst_rect=restart_inst.get_rect(center=(400, 350))

#GAME TIMER
obstacle_timer=pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)    #TRIGEGERING TIMER EVERY 1.5 SEC


#Starting game with while loop ----  main game section which takes user input
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
           
            if event.type==obstacle_timer:
                obstacles_group.add(Obstacles(choice(['snail', 'fly', 'snail']))) 
                
        elif game_active==False:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    game_active=True
                    start_time=pygame.time.get_ticks()

    
    if game_active:    
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, ground_rect)

        
        game_score=display_score() 

        player.draw(screen)
        player.update()

        obstacles_group.draw(screen)
        obstacles_group.update()

        # CHECKING COLLISION BETWEEN PLAYER AND SNAIL
        game_active=collision_sprite()
    else:
        obstacle_rect_list.clear()
        end_player_surface=pygame.image.load('pygame/player_walk_1.png').convert_alpha()
        player_rect=end_player_surface.get_rect(center=(80, 300))
        player_gravity=0
         
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)
        if game_score!=0:
            screen.blit(restart_inst, restart_inst_rect)
            #TOTAL SCORE BOARD
            total_score=test_font.render(f'Total Score: {game_score}', False, 'Red')
            total_score_rect=total_score.get_rect(center=(400, 300))
            screen.blit(total_score, total_score_rect)
        else:
            screen.blit(restart_inst, restart_inst_rect)
             
    pygame.display.update()
    clock.tick(60)