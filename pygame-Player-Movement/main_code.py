import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

bg_surf = pygame.image.load("Images\game_bg.png").convert()
bg_surf = pygame.transform.scale(bg_surf, (1280, 720))

goalleft_surf = pygame.image.load("Images\goal_left.png").convert_alpha()
goalleft_surf = pygame.transform.scale(goalleft_surf, (238, 280))
goalleft_rect = goalleft_surf.get_rect(midbottom=(-15, 520))

goalright_surf = pygame.image.load("Images/goal_right.png").convert_alpha()
goalright_surf = pygame.transform.scale(goalright_surf, (238, 280))
goalright_rect = goalright_surf.get_rect(midbottom=(1295, 520))

playerleft_surf = pygame.image.load("Images/LeftChar.png").convert_alpha()
playerleft_surf = pygame.transform.scale(playerleft_surf, (75, 120)) 
playerleft_rect = playerleft_surf.get_rect(midbottom=(120, 500))

playerleft_flipped_surf = pygame.transform.flip(playerleft_surf, True, False)
playerleft_flipped_surf = pygame.transform.scale(playerleft_flipped_surf, (75, 120)) 

playerright_surf = pygame.image.load("Images/RightChar.png").convert_alpha()
playerright_surf = pygame.transform.scale(playerright_surf, (75, 120))
playerright_rect = playerright_surf.get_rect(midbottom=(1160, 500))

playerright_flipped_surf = pygame.transform.flip(playerright_surf, True, False)
playerright_flipped_surf = pygame.transform.scale(playerright_flipped_surf, (75, 120))

ball_surf = pygame.image.load("Images/soccerball.png").convert_alpha()
ball_rect = ball_surf.get_rect()

goalWidth = 150
goalHeight = 240

gravity = 0.55  # Gravitatsiooni tugevus
jump_strength = -20
playerleft_upspeed = 0  # Algne ülesliikumise kiirus
playerright_upspeed = 0
is_left_player_on_ground = True
is_right_player_on_ground = True

move_speed = 6
playerleft_facing_goal = True
playerright_facing_goal = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    keys = pygame.key.get_pressed() # Kontrollib klahvivajutusi

    #LIIKUMINE
    if keys[pygame.K_d]:
        playerleft_rect.x += move_speed
        playerleft_facing_goal = True

    if keys[pygame.K_a]:
        playerleft_rect.x -= move_speed
        playerleft_facing_goal = False

    if keys[pygame.K_RIGHT]:
        playerright_rect.x += move_speed
        playerright_facing_goal = False

    if keys[pygame.K_LEFT]:
        playerright_rect.x -= move_speed
        playerright_facing_goal = True


    if playerleft_rect.left < 0:
        playerleft_rect.left = 0
    elif playerleft_rect.right > 1280:
        playerleft_rect.right = 1280

    if playerright_rect.right > 1280:
        playerright_rect.right = 1280
    elif playerright_rect.left < 0:
        playerright_rect.left = 0;

    # HÜPPAMINE
    # Vasak mängija hüpe
    if keys[pygame.K_w] and is_left_player_on_ground:  # W
        playerleft_upspeed = jump_strength
        is_left_player_on_ground = False

    #P arem mängija hüpe
    if keys[pygame.K_UP] and is_right_player_on_ground:  # ÜLES
        playerright_upspeed = jump_strength
        is_right_player_on_ground = False

    playerleft_upspeed += gravity # Lisab gravitatsiooni
    playerright_upspeed += gravity

    playerleft_rect.y += playerleft_upspeed # Liigutab vasakut mängijat
    playerright_rect.y += playerright_upspeed # Liigutab paremat mängijat


    if playerleft_rect.right <= goalWidth or playerleft_rect.left >= 1280 - goalWidth :
        if  playerleft_rect.top <= goalHeight + 20 <= playerleft_rect.bottom and playerleft_upspeed < 0:
            playerleft_upspeed = 0;

        elif playerleft_rect.bottom >= goalHeight >= playerleft_rect.top:
            playerleft_rect.bottom = goalHeight
            playerleft_upspeed = 0
            is_left_player_on_ground = True




    if playerright_rect.right <= goalWidth or playerright_rect.left >= 1280 - goalWidth :
        if  playerright_rect.top <= goalHeight + 20 <= playerright_rect.bottom and playerright_upspeed < 0:
            playerright_upspeed = 0;

        elif playerright_rect.bottom >= goalHeight >= playerright_rect.top:
            playerright_rect.bottom = goalHeight
            playerright_upspeed = 0
            is_right_player_on_ground = True




    if playerleft_rect.bottom >= 500:  # Maapind vasak mängija
        playerleft_rect.bottom = 500
        playerleft_upspeed = 0
        is_left_player_on_ground = True

    if playerright_rect.bottom >= 500:  # Maapind parem mängija
        playerright_rect.bottom = 500
        playerright_upspeed = 0
        is_right_player_on_ground = True



    screen.blit(bg_surf, (0, 0))
    screen.blit(goalleft_surf, goalleft_rect)
    screen.blit(goalright_surf, goalright_rect)

    if playerleft_facing_goal:
        screen.blit(playerleft_surf, playerleft_rect)
    else:
        screen.blit(playerleft_flipped_surf, playerleft_rect)
    
    if playerright_facing_goal:
        screen.blit(playerright_surf, playerright_rect)
    else:
        screen.blit (playerright_flipped_surf, playerright_rect)

    screen.blit(ball_surf, ball_rect)

    pygame.display.update()
    clock.tick(60)