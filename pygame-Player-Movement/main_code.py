import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

bg_surf = pygame.image.load("pygame-master\pygame-Player-Movement\Images\game_bg.png").convert()
bg_surf = pygame.transform.scale(bg_surf, (1280, 720))

goalleft_surf = pygame.image.load("pygame-master\pygame-Player-Movement\Images\goal_left.png").convert_alpha()
goalleft_surf = pygame.transform.scale(goalleft_surf, (238, 280))
goalleft_rect = goalleft_surf.get_rect(midbottom=(-15, 520))

goalright_surf = pygame.image.load("pygame-master\pygame-Player-Movement\Images/goal_right.png").convert_alpha()
goalright_surf = pygame.transform.scale(goalright_surf, (238, 280))
goalright_rect = goalright_surf.get_rect(midbottom=(1295, 520))

playerleft_surf = pygame.image.load("pygame-master\pygame-Player-Movement\Images/LeftChar.png").convert_alpha()
playerleft_surf = pygame.transform.scale(playerleft_surf, (75, 120))
playerleft_rect = playerleft_surf.get_rect(midbottom=(120, 500))

kickplayerleft_surf = pygame.image.load("pygame-master\pygame-Player-Movement\Images\kick_leftchar.png").convert_alpha()
kickplayerleft_surf = pygame.transform.scale(kickplayerleft_surf, (75, 120))
kickplayerleft_flipped_surf = pygame.transform.flip(kickplayerleft_surf, True, False)

kickplayerright_surf = pygame.image.load("pygame-master\pygame-Player-Movement\Images\kick_rightchar.png").convert_alpha()
kickplayerright_surf = pygame.transform.scale(kickplayerright_surf, (75, 120))
kickplayerright_flipped_surf = pygame.transform.flip(kickplayerright_surf, True, False)

playerleft_flipped_surf = pygame.transform.flip(playerleft_surf, True, False)
playerleft_flipped_surf = pygame.transform.scale(playerleft_flipped_surf, (75, 120))

playerright_surf = pygame.image.load("pygame-master/pygame-Player-Movement/Images/player.png").convert_alpha()
playerright_surf = pygame.transform.scale(playerright_surf, (75, 120))
playerright_rect = playerright_surf.get_rect(midbottom=(1160, 500))

playerright_flipped_surf = pygame.transform.flip(playerright_surf, True, False)
playerright_flipped_surf = pygame.transform.scale(playerright_flipped_surf, (75, 120))

ball_surf = pygame.image.load("pygame-master\pygame-Player-Movement\Images/soccerball.png").convert_alpha()
ball_surf = pygame.transform.scale(ball_surf, (42, 42))
ball_startpos = (640, 20)
ball_rect = ball_surf.get_rect(midtop=(ball_startpos))
ball_rotation_angle = 0
goalWidth = 150
goalHeight = 240

gravity = 0.55  # Gravitatsiooni tugevus
jump_strength = -18
playerleft_upspeed = 0  # Algne ülesliikumise kiirus
playerright_upspeed = 0
ball_upspeed = 15
ball_speed = 0
ball_rotation = 10
ball_slowing = 1.08
is_left_player_on_ground = True
is_right_player_on_ground = True
is_ball_on_ground = False

move_speed = 6
playerleft_facing_goal = True
playerright_facing_goal = True#

inGoal_left = False
inGoal_right = False

is_left_kicking = False
left_kick_timer = 0
is_right_kicking = False
right_kick_timer = 0
kick_duration = 500 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()  # Kontrollib klahvivajutusi
    isSimpleCollide = pygame.Rect.colliderect(playerleft_rect, playerright_rect)




    areColliding = pygame.Rect.colliderect(playerleft_rect, playerright_rect) and (
                (playerleft_rect.left < playerright_rect.left and (keys[pygame.K_d] or keys[pygame.K_LEFT])) or (
                    playerleft_rect.right > playerright_rect.right and (keys[pygame.K_a] or keys[pygame.K_RIGHT])))
    leftTouchingBall = pygame.Rect.colliderect(playerleft_rect, ball_rect) and ((keys[pygame.K_d] and ball_rect.right > playerleft_rect.right) or (keys[pygame.K_a] and ball_rect.x < playerleft_rect.x))
    rightTouchingBall = pygame.Rect.colliderect(playerright_rect, ball_rect) and ((keys[pygame.K_RIGHT] and ball_rect.left > playerright_rect.left) or (keys[pygame.K_LEFT] and ball_rect.x < playerright_rect.x))
    leftShift = 0
    rightShift = 0
    ballShift = 0
    tempSpeed = move_speed
    if areColliding:
        tempSpeed = move_speed / 1.4
        # LIIKUMINE
    if keys[pygame.K_d]:
        leftShift += tempSpeed
        if areColliding:
            rightShift += tempSpeed

        if leftTouchingBall:
            ballShift += tempSpeed

        playerleft_facing_goal = True

    if keys[pygame.K_a]:
        leftShift += -tempSpeed
        if areColliding:
            rightShift += -tempSpeed
        if leftTouchingBall:
            ballShift -= tempSpeed
        playerleft_facing_goal = False

    if keys[pygame.K_RIGHT]:
        rightShift += tempSpeed
        if areColliding:
            leftShift += tempSpeed
        if rightTouchingBall:
            ballShift += tempSpeed
        playerright_facing_goal = False

    if keys[pygame.K_LEFT]:
        rightShift += - tempSpeed
        if areColliding:
            leftShift += -tempSpeed
        if rightTouchingBall:
            ballShift -= tempSpeed
        playerright_facing_goal = True

    playerleft_rect.x += leftShift
    playerright_rect.x += rightShift
    ball_rect.x += ballShift

    if playerleft_rect.left < 0:
        playerleft_rect.left = 0
    elif playerleft_rect.right > 1280:
        playerleft_rect.right = 1280

    if playerright_rect.right > 1280:
        playerright_rect.right = 1280
    elif playerright_rect.left < 0:
        playerright_rect.left = 0


    leftTouchingBallVertically = pygame.Rect.colliderect(playerleft_rect, ball_rect) and ball_rect.top > playerleft_rect.top
    rightTouchingBallVertically = pygame.Rect.colliderect(playerright_rect, ball_rect) and ball_rect.top > playerright_rect.top

    #Mangija loomine
    if (leftTouchingBallVertically and keys[pygame.K_q]):
        ballDir = 1
        if (playerleft_facing_goal == False):
            ballDir = -1
        ball_speed = 12 * ballDir
        ball_upspeed = -14
        is_left_kicking = True
        left_kick_timer = pygame.time.get_ticks()
    if (rightTouchingBallVertically and keys[pygame.K_KP0]):
        ballDir = 1
        if (playerright_facing_goal == True):
            ballDir = -1
        ball_speed = 12 * ballDir
        ball_upspeed = -14
        is_right_kicking = True
        right_kick_timer = pygame.time.get_ticks()

    if is_left_kicking and pygame.time.get_ticks() - left_kick_timer >= kick_duration:
        is_left_kicking = False

    if is_right_kicking and pygame.time.get_ticks() - right_kick_timer >= kick_duration:
        is_right_kicking = False


    #Mängija põrkumine mängijast
    isOneOnTopOfOther = isSimpleCollide and (playerleft_rect.top > playerright_rect.top or playerright_rect.top > playerleft_rect.top)
    if isOneOnTopOfOther:
        if playerleft_rect.top < playerright_rect.top:
            playerleft_upspeed = -13
        else:
            playerright_upspeed = -13





    # HÜPPAMINE
    # Vasak mängija hüpe
    if keys[pygame.K_w] and is_left_player_on_ground:  # W
        playerleft_upspeed = jump_strength
        is_left_player_on_ground = False

    # P arem mängija hüpe
    if keys[pygame.K_UP] and is_right_player_on_ground:  # ÜLES
        playerright_upspeed = jump_strength
        is_right_player_on_ground = False

    playerleft_upspeed += gravity  # Lisab gravitatsiooni
    playerright_upspeed += gravity
    ball_upspeed += gravity

    playerleft_rect.y += playerleft_upspeed  # Liigutab vasakut mängijat
    playerright_rect.y += playerright_upspeed  # Liigutab paremat mängijat
    ball_rect.y += ball_upspeed
    ball_rect.x += ball_speed

    ###################################################################################################
    # Vasak mangija varavas
    if playerleft_rect.right <= goalWidth or playerleft_rect.left >= 1280 - goalWidth:
        if playerleft_rect.top <= goalHeight + 20 <= playerleft_rect.bottom and playerleft_upspeed < 0:
            playerleft_upspeed = 0

        elif playerleft_rect.bottom >= goalHeight >= playerleft_rect.top:
            playerleft_rect.bottom = goalHeight
            playerleft_upspeed = 0
            is_left_player_on_ground = True

    # Parem mangija varavas
    if playerright_rect.right <= goalWidth or playerright_rect.left >= 1280 - goalWidth:
        if playerright_rect.top <= goalHeight + 20 <= playerright_rect.bottom and playerright_upspeed < 0:
            playerright_upspeed = 0

        elif playerright_rect.bottom >= goalHeight >= playerright_rect.top:
            playerright_rect.bottom = goalHeight
            playerright_upspeed = 0
            is_right_player_on_ground = True

    #################################################################################################

    if playerleft_rect.bottom >= 500:  # Maapind vasak mängija
        playerleft_rect.bottom = 500
        playerleft_upspeed = 0
        is_left_player_on_ground = True

    if playerright_rect.bottom >= 500:  # Maapind parem mängija
        playerright_rect.bottom = 500
        playerright_upspeed = 0
        is_right_player_on_ground = True


    # palli porkumine mangijast
    if (pygame.Rect.colliderect(ball_rect, playerleft_rect) and ball_rect.top < playerleft_rect.top-20) or (pygame.Rect.colliderect(ball_rect, playerright_rect) and ball_rect.top < playerright_rect.top-20):
        if (abs(ball_speed) < 2):
            ball_speed = 2
        ball_upspeed = -8

        if (pygame.Rect.colliderect(ball_rect, playerleft_rect)):
            if (playerleft_facing_goal):
                ball_speed = abs(ball_speed)
            else:
                ball_speed = -abs(ball_speed)
        else:
            if (playerright_facing_goal):
                ball_speed = -abs(ball_speed)
            else:
                ball_speed = abs(ball_speed)




    # palli porkumine seinast##########################################################
    elif ball_rect.left <= 0 or ball_rect.right >= 1280 or pygame.Rect.colliderect(ball_rect,
                                                                                 playerleft_rect) or pygame.Rect.colliderect(
            ball_rect, playerright_rect):
        if ball_rect.left <= 0:
            ball_rect.left = 0
        if ball_rect.right >= 1280:
            ball_rect.right = 1280

        ball_speed = -ball_speed
        if abs(ball_speed) > 10:
            ball_speed /= 1.6
        else:
            ball_speed /= 1.3





    # palli porkumine varavast
    if ball_rect.right <= goalWidth or ball_rect.left >= 1280 - goalWidth:

        if ball_rect.top <= goalHeight + 20 <= ball_rect.bottom and ball_upspeed < 0:
            ball_upspeed = 0
            ball_speed = ball_speed / ball_slowing

        elif ball_rect.bottom >= goalHeight >= ball_rect.top:
            ball_rect.bottom = goalHeight
            if ball_upspeed <= 1.5:
                is_ball_on_ground = True
                ball_upspeed = 0
            else:
                ball_upspeed = -1 * (ball_upspeed / 1.6)

            ball_speed = ball_speed / ball_slowing
    if ball_rect.bottom > 500:
        ball_rect.bottom = 500
        if ball_upspeed <= 1.5:
            is_ball_on_ground = True
            ball_upspeed = 0
        else:
            ball_upspeed = -1 * (ball_upspeed / 1.6)
        ball_speed = ball_speed / ball_slowing
    
    #pall varava sees #########################################

    if ball_rect.colliderect(goalleft_rect):
        if ball_rect.right <= goalleft_rect.right and ball_rect.bottom >= goalleft_rect.top:
            inGoal_left = True
    
    elif ball_rect.colliderect(goalright_rect):
        if ball_rect.left >= goalright_rect.left and ball_rect.bottom >= goalright_rect.top:
            inGoal_right = True

    ###########################################################

    if (abs(ball_speed) < 0.01):
        ball_speed = 0
    screen.blit(bg_surf, (0, 0))
    screen.blit(goalleft_surf, goalleft_rect)
    screen.blit(goalright_surf, goalright_rect)

    #oigele poole vaatamine##################################

    # vasak mangija
    if is_left_kicking:
        if playerleft_facing_goal:
            screen.blit(kickplayerleft_surf, playerleft_rect)  # Show left player kicking sprite facing right
        else:
            screen.blit(kickplayerleft_flipped_surf, playerleft_rect)  # Show flipped left player kicking sprite
    else:
        if playerleft_facing_goal:
            screen.blit(playerleft_surf, playerleft_rect)  # Show normal sprite facing right
        else:
            screen.blit(playerleft_flipped_surf, playerleft_rect)  # Show flipped normal sprite

    # parem mangija
    if is_right_kicking:
        if playerright_facing_goal:
            screen.blit(kickplayerright_surf, playerright_rect)  # Show right player kicking sprite facing left
        else:
            screen.blit(kickplayerright_flipped_surf, playerright_rect)  # Show flipped right player kicking sprite
    else:
        if playerright_facing_goal:
            screen.blit(playerright_surf, playerright_rect)  # Show normal sprite facing left
        else:
            screen.blit(playerright_flipped_surf, playerright_rect)  # Show flipped normal sprite

    ##########################################################

    ball_rotation_angle -= ball_speed * 2
    if ball_rotation_angle > 360:
        ball_rotation_angle -= 360
    elif ball_rotation_angle < 0:
        ball_rotation_angle += 360

    rotated_ball_surf = pygame.transform.rotate(ball_surf, ball_rotation_angle)
    rotated_ball_rect = rotated_ball_surf.get_rect(center=ball_rect.center)

    screen.blit(rotated_ball_surf, rotated_ball_rect)

    pygame.display.update()
    clock.tick(60)
