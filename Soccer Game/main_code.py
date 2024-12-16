import pygame
from sys import exit
import time
import os

base_dir = "Game Files"
images_dir = os.path.join(base_dir, "Images")
music_dir = os.path.join(base_dir, "music")
fonts_dir = os.path.join(base_dir, "Fonts")

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

# Taustapilt
bg_surf = pygame.image.load(os.path.join(images_dir, "game_bg.png")).convert()
bg_surf = pygame.transform.scale(bg_surf, (1280, 720))

# Menüü taustapilt
menuBackground_surf = pygame.image.load(os.path.join(images_dir, "MenuBackground.jpg")).convert()
menuBackground_surf = pygame.transform.scale(menuBackground_surf, (1280, 720))

# Väravad
goalleft_surf = pygame.image.load(os.path.join(images_dir, "goal_left.png")).convert_alpha()
goalleft_surf = pygame.transform.scale(goalleft_surf, (238, 280))
goalleft_rect = goalleft_surf.get_rect(midbottom=(-15, 520))

goalright_surf = pygame.image.load(os.path.join(images_dir, "goal_right.png")).convert_alpha()
goalright_surf = pygame.transform.scale(goalright_surf, (238, 280))
goalright_rect = goalright_surf.get_rect(midbottom=(1295, 520))

# Vasaku mängija pildid
playerleft_surf = pygame.image.load(os.path.join(images_dir, "LeftChar.png")).convert_alpha()
playerleft_surf = pygame.transform.scale(playerleft_surf, (80, 125))
playerleft_rect = playerleft_surf.get_rect(midbottom=(130, 500))

kickplayerleft_surf = pygame.image.load(os.path.join(images_dir, "kick_leftchar.png")).convert_alpha()
kickplayerleft_surf = pygame.transform.scale(kickplayerleft_surf, (80, 125))
kickplayerleft_flipped_surf = pygame.transform.flip(kickplayerleft_surf, True, False)

playerleft_flipped_surf = pygame.transform.flip(playerleft_surf, True, False)
playerleft_flipped_surf = pygame.transform.scale(playerleft_flipped_surf, (80, 125))

# Parema mängija pildid
playerright_surf = pygame.image.load(os.path.join(images_dir, "player.png")).convert_alpha()
playerright_surf = pygame.transform.scale(playerright_surf, (80, 125))
playerright_rect = playerright_surf.get_rect(midbottom=(1160, 500))

kickplayerright_surf = pygame.image.load(os.path.join(images_dir, "kick_rightchar.png")).convert_alpha()
kickplayerright_surf = pygame.transform.scale(kickplayerright_surf, (80, 125))
kickplayerright_flipped_surf = pygame.transform.flip(kickplayerright_surf, True, False)

playerright_flipped_surf = pygame.transform.flip(playerright_surf, True, False)
playerright_flipped_surf = pygame.transform.scale(playerright_flipped_surf, (80, 125))

# Pall
ball_surf = pygame.image.load(os.path.join(images_dir, "soccerball.png")).convert_alpha()
ball_surf = pygame.transform.scale(ball_surf, (54, 54))

# Muusika
pygame.mixer.music.load(os.path.join(music_dir, "worldcup.mp3"))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

# Mängu muutujad
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

rectangle = pygame.Rect(555, 25, 170, 85)

font = pygame.font.Font((os.path.join(fonts_dir, "Sports.ttf")), 40)
smallfont = pygame.font.Font((os.path.join(fonts_dir, "Sports.ttf")), 20)
scorefont = pygame.font.Font((os.path.join(fonts_dir, "Sports.ttf")), 69)
shadow_color = (0, 0, 0)
shadow_offset = (3, 3)

ball_startpos = (640, 20)
ball_rect = ball_surf.get_rect(midtop=(ball_startpos))

goalWidth = 150
goalHeight = 240

# Liikumine
gravity = 1.1
ball_gravity = 0.6
jump_strength = -19.5
playerleft_upspeed = 0  # Algne ülesliikumise kiirus
playerright_upspeed = 0
ball_upspeed = 15
ball_speed = 0
ball_rotation = 10
ball_slowing = 1.4
is_left_player_on_ground = True
is_right_player_on_ground = True
is_ball_on_ground = False
move_speed = 6
playerleft_facing_goal = True
playerright_facing_goal = True
ball_rotation_angle = 0

# Löömine
is_left_kicking = False
kick_cooldown = 500
left_kick_timer = 0
right_kick_timer = 0
is_right_kicking = False
kick_duration = 500


# Skoorimine
inGoal_left = False
inGoal_right = False
score_right = 6
score_left = 6
gamewinner = 'ishowspeed'

# Mängu seisund
game_state = 'main_menu'
game_stop = False
game_running = False
resetTimer = 100

# Helitugevuse reguleerimine
button_width = 200
button_height = 50
increase_button_rect = pygame.Rect(100, 300, button_width, button_height)
decrease_button_rect = pygame.Rect(100, 400, button_width, button_height)
volume_master = 0.5
last_volume_change_time = 0
volume_change_cooldown = 0.1

########################################################################
def draw_text_with_shadow(surface, text, font, color, pos, shadow_color=(0, 0, 0), shadow_offset=(2, 2)):

    # Render the shadow text
    shadow_text = font.render(text, True, shadow_color)
    shadow_pos = (pos[0] + shadow_offset[0], pos[1] + shadow_offset[1])
    surface.blit(shadow_text, shadow_pos)

    # Render the main text on top of the shadow
    main_text = font.render(text, True, color)
    surface.blit(main_text, pos)

def handle_button_clicks():
    global volume_master, last_volume_change_time
    mouse_x, mouse_y = pygame.mouse.get_pos()
    current_time = time.time()
    if current_time - last_volume_change_time >= volume_change_cooldown:
        if increase_button_rect.collidepoint(mouse_x, mouse_y):
            if pygame.mouse.get_pressed()[0]:
                # Kui vajutatakse helitugevuse suurendamise nuppu, suurenda helitugevust 0.1 võrra
                volume_master = min(volume_master + 0.1, 1.0)  # Max helitugevus on 1.0
                pygame.mixer.music.set_volume(volume_master)
                last_volume_change_time = current_time
        elif decrease_button_rect.collidepoint(mouse_x, mouse_y):
            if pygame.mouse.get_pressed()[0]:
            # Kui vajutatakse helitugevuse vähendamise nuppu, vähenda helitugevust 0.1 võrra
                volume_master = max(volume_master - 0.1, 0.0)  # Min helitugevus on 0.0
                pygame.mixer.music.set_volume(volume_master)
                last_volume_change_time = current_time

def resetpos(): # paneb mängijad ja palli algpositsioonile
    playerright_rect.midbottom = (1160, 500)
    playerleft_rect.midbottom = (120, 500)
    ball_rect.midbottom = ball_startpos
    playerleft_facing_goal = True
    playerright_facing_goal = True
    ball_upspeed = 15
    ball_speed = 0
    return False

def winner(): # näitab võitja nime, restart võimalus
    winner_text = font.render(gamewinner + " player wins!", True, WHITE)
    winner_text_rect = winner_text.get_rect(center=(640, 250))
    screen.blit(winner_text, winner_text_rect)

    replay_text = font.render("Press Enter to Restart", True, WHITE)
    replay_text_rect = replay_text.get_rect(center=(640, 450))
    screen.blit(replay_text, replay_text_rect)

def draw_main_menu(): # Põhimenüü
    global font
    title_text = font.render("Soccer Game", True, WHITE)
    start_text = font.render("Press Enter to Start", True, WHITE)

    # Tekst keskel
    title_rect = title_text.get_rect(center=(640, 250))
    start_rect = start_text.get_rect(center=(640, 450))

    screen.blit(menuBackground_surf, (0, 0))
    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)

    handle_button_clicks()

    # Nupud
    pygame.draw.rect(screen, GREEN, increase_button_rect)
    pygame.draw.rect(screen, RED, decrease_button_rect)

    # Nuppude tekstid
    increase_text = smallfont.render('+ Volume', True, WHITE)
    decrease_text = smallfont.render('- Volume', True, WHITE)
    screen.blit(increase_text, (increase_button_rect.x + 20, increase_button_rect.y + 10))
    screen.blit(decrease_text, (decrease_button_rect.x + 20, decrease_button_rect.y + 10))

    # Kuvab helitugevuse
    volume_text = smallfont.render(f'Volume: {int(volume_master * 100)}%', True, WHITE)
    volume_text = smallfont.render(f'Volume: {int(volume_master * 100)}%', True, WHITE)
    screen.blit(volume_text, (100, 250))

def apply_blur(surface, scale_factor=0.1):
    """Applies a blur effect to the given surface."""
    # Get the dimensions of the surface
    small_width = int(surface.get_width() * scale_factor)
    small_height = int(surface.get_height() * scale_factor)

    # Scale down
    small_surface = pygame.transform.scale(surface, (small_width, small_height))

    # Scale up
    blurred_surface = pygame.transform.scale(small_surface, surface.get_size())

    return blurred_surface

def pause_menu():

    blurred_snapshot = apply_blur(game_snapshot)  # Blur the snapshot

    # Display the blurred background
    screen.blit(blurred_snapshot, (0, 0))

    # Display pause menu text
    title_text = 'Soccer Game'
    pause_text = 'Paused'

    draw_text_with_shadow(screen, pause_text, font, WHITE, (545, 360), shadow_color, shadow_offset)
    draw_text_with_shadow(screen, title_text, font, WHITE, (480, 250), shadow_color, shadow_offset)
   ##################################################################### GAME LOGIC ############################################################################
def play():
        global game_stop, inGoal_left, inGoal_right, resetTimer, ball_speed, score_left, score_right, gamewinner, is_left_player_on_ground, is_right_player_on_ground, is_ball_on_ground, is_left_kicking, is_right_kicking, playerleft_upspeed, playerright_upspeed, ball_upspeed, playerleft_facing_goal, playerright_facing_goal, ball_rotation_angle, left_kick_timer, right_kick_timer, kick_cooldown
        isSimpleCollide = pygame.Rect.colliderect(playerleft_rect, playerright_rect)
        isOneOnTopOfOther = isSimpleCollide and (playerleft_rect.top > playerright_rect.top or playerright_rect.top > playerleft_rect.top)
        # Kui värav, siis kõik algpositsioonidele
        if game_stop:
                resetTimer -= 1
        if resetTimer <= 0:
                resetTimer = 60
                game_stop = False
                inGoal_left = False
                inGoal_right = False
                ball_speed = 0
                resetpos() # Mäng algseisundisse

        # Kas mängijad on üksteisega kokku põrganud
        isSimpleCollide = pygame.Rect.colliderect(playerleft_rect, playerright_rect)

        # Kas mängijad põrkasid üksteisega kokku ja kas nad liiguvad vastassuunas
        areColliding = pygame.Rect.colliderect(playerleft_rect, playerright_rect) and (
                (playerleft_rect.left < playerright_rect.left and (keys[pygame.K_d] or keys[pygame.K_LEFT])) or (
                playerleft_rect.right > playerright_rect.right and (keys[pygame.K_a] or keys[pygame.K_RIGHT])))
      
        # Kas mängijad puutuvad palli
        leftTouchingBall = pygame.Rect.colliderect(playerleft_rect, ball_rect)
        rightTuchingBall = pygame.Rect.colliderect(playerright_rect, ball_rect)
        leftTouchingBallAndMoving = leftTouchingBall and (
                (keys[pygame.K_d] and ball_rect.right > playerleft_rect.right) or (
                keys[pygame.K_a] and ball_rect.x < playerleft_rect.x)) and playerleft_upspeed == 0
        rightTouchingBallAndMoving = rightTuchingBall and (
                (keys[pygame.K_RIGHT] and ball_rect.left > playerright_rect.left) or (
                keys[pygame.K_LEFT] and ball_rect.x < playerright_rect.x)) and playerright_upspeed == 0


        # Liikumise muutujad
        leftShift = 0
        rightShift = 0
        ballShift = 0
        tempSpeed = move_speed

        # Liikumine
        if not game_stop:
            if areColliding:
                tempSpeed = move_speed / 1.4

            # Vasak mängija liikumine
            if keys[pygame.K_d]:
                leftShift += tempSpeed
                if areColliding:
                    rightShift += tempSpeed

                if leftTouchingBallAndMoving or (areColliding and rightTuchingBall):
                    ballShift += tempSpeed

                if playerleft_upspeed != 0 and playerleft_facing_goal:
                    leftShift += 1.5
                playerleft_facing_goal = True

            if keys[pygame.K_a]:
                leftShift += -tempSpeed
                if areColliding:
                    rightShift += -tempSpeed
                if leftTouchingBallAndMoving or (areColliding and rightTuchingBall):
                    ballShift -= tempSpeed
                if playerleft_upspeed != 0 and playerleft_facing_goal:
                    leftShift -= 1.5
                playerleft_facing_goal = False

            # Parem mängija liikumine
            if keys[pygame.K_RIGHT]:
                rightShift += tempSpeed
                if areColliding:
                    leftShift += tempSpeed
                if rightTouchingBallAndMoving or (areColliding and leftTouchingBall):
                    ballShift += tempSpeed
                if playerright_upspeed != 0 and playerright_facing_goal:
                    rightShift += 1.5
                playerright_facing_goal = False

            if keys[pygame.K_LEFT]:
                rightShift -= tempSpeed
                if areColliding:
                    leftShift += -tempSpeed
                if rightTouchingBallAndMoving or (areColliding and leftTouchingBall):
                    ballShift -= tempSpeed
                if playerright_upspeed != 0 and playerright_facing_goal:
                    rightShift -= 1.5
                playerright_facing_goal = True

            # Liigutamine kokkupuutel
            playerleft_rect.x += leftShift
            playerright_rect.x += rightShift

            ball_rect.x += ballShift
        # Piirangud, et mängijad ei läheks ekraanist välja
        if playerleft_rect.left < 0:
            playerleft_rect.left = 0
        elif playerleft_rect.right > 1280:
            playerleft_rect.right = 1280

        if playerright_rect.right > 1280:
            playerright_rect.right = 1280
        elif playerright_rect.left < 0:
            playerright_rect.left = 0

        # Peaga löömine
        leftTouchingBallVertically = pygame.Rect.colliderect(playerleft_rect,
                                                             ball_rect) and ball_rect.top > playerleft_rect.top
        rightTouchingBallVertically = pygame.Rect.colliderect(playerright_rect,
                                                              ball_rect) and ball_rect.top > playerright_rect.top

        # Jalaga löömine
        if game_stop == False:
            # Vasak löömine timeriga
            if keys[pygame.K_q]:
                current_time = pygame.time.get_ticks()
                if not is_left_kicking and (current_time - left_kick_timer >= kick_cooldown):
                    is_left_kicking = True
                    left_kick_timer = current_time
                    if leftTouchingBallVertically:
                        ballDir = 1
                        if playerleft_facing_goal == False:
                            ballDir = -1
                        ball_speed = 9 * ballDir
                        ball_upspeed = -14

            # Parem löömine timeriga
            if keys[pygame.K_KP0]:
                current_time = pygame.time.get_ticks()
                if not is_right_kicking and (current_time - right_kick_timer >= kick_cooldown):
                    right_kick_timer = current_time
                    is_right_kicking = True
                    if rightTouchingBallVertically:
                        ballDir = 1
                        if playerright_facing_goal == True:
                            ballDir = -1
                        ball_speed = 9 * ballDir
                        ball_upspeed = -14

            # Lõpetab löömise pärast timerit
            if is_left_kicking and pygame.time.get_ticks() - left_kick_timer >= kick_duration:
                is_left_kicking = False

            if is_right_kicking and pygame.time.get_ticks() - right_kick_timer >= kick_duration:
                is_right_kicking = False

        # Mängija põrkumine üksteisest
        isOneOnTopOfOther = isSimpleCollide and (
                playerleft_rect.top > playerright_rect.top or playerright_rect.top > playerleft_rect.top)
        if isOneOnTopOfOther:
            if playerleft_rect.top < playerright_rect.top:
                playerleft_upspeed = -13
            else:
                playerright_upspeed = -13

        # HÜPPAMINE        
        if (game_stop == False):
            # Vasak mängija hüpe
            if keys[pygame.K_w] and is_left_player_on_ground:  # W
                playerleft_upspeed = jump_strength
                is_left_player_on_ground = False

            # Parem mängija hüpe
            if keys[pygame.K_UP] and is_right_player_on_ground:  # ÜLES
                playerright_upspeed = jump_strength
                is_right_player_on_ground = False

            if keys[pygame.K_s] and is_left_player_on_ground == False:  # W
                playerleft_upspeed += 0.85
            if keys[pygame.K_DOWN] and is_right_player_on_ground == False:  # W
                playerright_upspeed += 0.85

        # Lisab gravitatsiooni
        playerleft_upspeed += gravity  
        playerright_upspeed += gravity
        ball_upspeed += ball_gravity

        playerleft_rect.y += playerleft_upspeed  # Liigutab vasakut mängijat
        playerright_rect.y += playerright_upspeed  # Liigutab paremat mängijat
        ball_rect.y += ball_upspeed
        ball_rect.x += ball_speed

        ###################################################################################################
        # Vasak mangija varavas
        if playerleft_rect.right <= goalWidth or playerleft_rect.left >= 1280 - goalWidth:
            if playerleft_rect.top <= goalHeight + 20 <= playerleft_rect.bottom and playerleft_upspeed < 0:
                playerleft_upspeed = 0

            elif playerleft_rect.bottom <= goalHeight:
                playerleft_rect.bottom = goalHeight
                playerleft_upspeed = 0
                is_left_player_on_ground = True

        # Parem mangija varavas
        if playerright_rect.right <= goalWidth or playerright_rect.left >= 1280 - goalWidth:
            if playerright_rect.top <= goalHeight + 20 <= playerright_rect.bottom and playerright_upspeed < 0:
                playerright_upspeed = 0

            elif playerright_rect.bottom <= goalHeight:
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
        if (pygame.Rect.colliderect(playerleft_rect, ball_rect) and ball_rect.top < playerleft_rect.top - 10) or (
                pygame.Rect.colliderect(playerright_rect, ball_rect) and ball_rect.top < playerright_rect.top - 10):
            if (abs(ball_speed) < 4):
                if (ball_speed < 0):
                    ball_speed = 4
                else:
                    ball_speed = 4
            ball_upspeed = abs(ball_upspeed) * -1
            if abs(ball_upspeed) < 10:
                ball_upspeed = -10

            if (pygame.Rect.colliderect(ball_rect, playerleft_rect)):
                if (playerleft_rect.centerx < ball_rect.centerx):
                    ball_speed = -abs(ball_speed)
                else:
                    ball_speed = abs(ball_speed)

            else:
                if (playerright_rect.centerx < ball_rect.centerx):
                    ball_speed = -abs(ball_speed)
                else:
                    ball_speed = abs(ball_speed)

        #palli porkumine mangija alt
        if pygame.Rect.colliderect(ball_rect,
                                   playerleft_rect) and playerleft_upspeed > 0 and playerleft_rect.bottom < ball_rect.bottom:
            dir = 1
            if (playerleft_rect.centerx < ball_rect.centerx):
                dir = -1
            ball_upspeed = 4
            ball_speed = 8 * dir
            playerleft_upspeed = -8
        if pygame.Rect.colliderect(ball_rect,
                                   playerright_rect) and playerright_upspeed > 0 and playerright_rect.bottom < ball_rect.bottom:
            dir = 1
            if (playerright_rect.centerx > ball_rect.centerx):
                dir = -1
            ball_upspeed = 4
            ball_speed = 8 * dir
            playerright_upspeed = -8


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

        if (abs(ball_speed) < 0.01):
            ball_speed = 0

        # pall varava sees 
        if game_stop == False:
            if ball_rect.colliderect(goalleft_rect):
                if ball_rect.right <= goalleft_rect.right and ball_rect.bottom >= goalleft_rect.top:
                    inGoal_left = True
                    score_right += 1

            elif ball_rect.colliderect(goalright_rect):
                if ball_rect.left >= goalright_rect.left and ball_rect.bottom >= goalright_rect.top:
                    inGoal_right = True
                    score_left += 1

        # palli libisemine varavast
        if pygame.Rect.colliderect(ball_rect, goalleft_rect) and ball_rect.top < goalleft_rect.top and abs(
                ball_speed) < 4:
            if (ball_speed < 0):
                ball_speed = -4
            else:
                ball_speed = 4

        if pygame.Rect.colliderect(ball_rect, goalright_rect) and ball_rect.top < goalright_rect.top and abs(
                ball_speed) < 4:
            if (ball_speed < 0):
                ball_speed = -4
            else:
                ball_speed = 4

        # Skoori näitamine
        text = scorefont.render((str(score_left) + ' - ' + str(score_right)), True, BLACK)
        text_rect = text.get_rect(center=rectangle.center)

        if score_left >= 7:
            gamewinner = 'Left'
        elif score_right >= 7:
            gamewinner = 'Right'
        
        # Piltide kuvamine
        screen.blit(bg_surf, (0, 0))
        screen.blit(goalleft_surf, goalleft_rect)
        screen.blit(goalright_surf, goalright_rect)

        # oigele poole vaatamine##################################
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

        # Pall väravas
        if inGoal_right or inGoal_left:
            game_stop = True

        # Palli pöörlemine
        ball_rotation_angle -= ball_speed * 2
        if ball_rotation_angle > 360:
            ball_rotation_angle -= 360
        elif ball_rotation_angle < 0:
            ball_rotation_angle += 360

        # Palli kuvamine
        rotated_ball_surf = pygame.transform.rotate(ball_surf, ball_rotation_angle)
        rotated_ball_rect = rotated_ball_surf.get_rect(center=ball_rect.center)

        screen.blit(rotated_ball_surf, rotated_ball_rect)

        # Skoori näitamine
        pygame.draw.rect(screen, WHITE, rectangle)
        screen.blit(text, text_rect)

##########################################################################################################################################################

while True:
    screen.fill(BLACK)

    keys = pygame.key.get_pressed()  # Kontrollib klahvivajutusi

    # Mängu sulgemine
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Põhimenüü
    if game_state == 'main_menu':
        if keys[pygame.K_RETURN]:
            score_left = 0
            score_right = 0
            resetpos()
            game_state = 'game_running'
        draw_main_menu()

    # Mäng läbi
    if game_state == 'winner_screen':
        if keys[pygame.K_RETURN]:
            score_left = 0
            score_right = 0
            resetpos()
            game_state = 'game_running'
        winner()



    # Mäng käib
    if game_state == 'game_running':
        if score_left >= 7 or score_right >= 7:
            game_state = 'winner_screen'
        play()
        if keys[pygame.K_ESCAPE]:
            game_snapshot = screen.copy()
            game_state = 'pause_menu'


    #paus
    if game_state == 'pause_menu':
        if keys[pygame.K_RETURN]:
            game_state = 'game_running'
        pause_menu()

    pygame.display.update()
    clock.tick(60)
