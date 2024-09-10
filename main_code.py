import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

bg_surf = pygame.image.load("Images\game_bg.png").convert() #image import + optimization
bg_surf = pygame.transform.scale(bg_surf, (1280, 720)) 

goalleft_surf = pygame.image.load("Images\goal_left.png").convert_alpha()
goalleft_surf = pygame.transform.scale(goalleft_surf, (153, 180))
goalleft_rect = goalleft_surf.get_rect(midbottom = (0, 520))

goalright_surf = pygame.image.load("Images\goal_right.png").convert_alpha()
goalright_surf = pygame.transform.scale(goalright_surf, (153, 180))
goalright_rect = goalright_surf.get_rect(midbottom = (1280, 520))

playerleft_surf = pygame.image.load("Images\LeftChar.png").convert_alpha()
playerleft_surf = pygame.transform.scale(playerleft_surf, (75, 120)) 
playerleft_x = 120
playerleft_y = 500
playerleft_rect = playerleft_surf.get_rect(midbottom = (playerleft_x, playerleft_y)) #teeb ristküliku ümber: saab erinevatest kohtadest liigutada + pärast hea collisioneid kontrollida 

playerright_surf = pygame.image.load("Images/RightChar.png").convert_alpha() #image import + optimization + jääb läbipaistev
playerright_surf = pygame.transform.scale(playerright_surf, (75, 120))
playerright_x = 1160
playerright_y = 500
playerright_rect = playerright_surf.get_rect(midbottom = (playerright_x, playerright_y))

ball_surf = pygame.image.load("Images\soccerball.png").convert_alpha()
ball_rect = ball_surf.get_rect()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() #lõpetab while True loopi

    screen.blit(bg_surf, (0, 0))
    screen.blit(goalleft_surf, (goalleft_rect))
    screen.blit(goalright_surf, (goalright_rect))
    screen.blit(playerleft_surf,(playerleft_rect))
    screen.blit(playerright_surf,(playerright_rect))



    pygame.display.update()
    clock.tick(60) #fps