import pygame
import helicopter
import enemy_heli
import boat
import sprites
import random

pygame.mixer.pre_init(44100, - 16, 1, 512)
pygame.init()


pygame.display.set_icon(sprites.icon)
display_width = 800
display_height = 600
game_display = pygame.display.set_mode((display_width, display_height))


font = "8-Bit-Madness.ttf"



def message_to_screen(message, textfont, size, color):
    my_font = pygame.font.Font(textfont, size)
    my_message = my_font.render(message, 0, color)

    return my_message
#CORES
white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
red =(255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

for convert_sprites in sprites.all_sprites:
    convert_sprites.convert_alpha()

clock = pygame.time.Clock()
FPS = 30

player = helicopter.Helicopter(100, display_height/2-40)
moving = True
godmode = False

#Pontos
score = 0
highscore_file = open('highscore.dat', "r")
highscore_int = int(highscore_file.read())

#NUVENS QUE PASSAM NO CENARIO
cloud_x = 800
cloud_y = random.randint(0, 400)

#VARIAVEIS DO INIMIGO
enemy_heli = enemy_heli.EnemyHeli(-100, display_height/2-40)
enemy_heli_alive = False

boat = boat.Boat(-110, 430)
boat_alive = False
#NAVE ESPACIAL
spaceship_x = 800
spaceship_y = random.randint(0, 400)
spaceship_alive = False   # VIDAS
spaceship_hit_player = False
warning_once = True
warning = False # MENSAGEM DE ATENÇAO
warning_counter = 0
warning_message = message_to_screen("!", font, 200, red) # A COR DA MENSAGEM E O TAMANHO

#VARIAVEIS DOS BALOES
balloon_x = 800
balloon_y = random.randint(0, 400)

#Variaveis de tiro
bullets = []
#VARIAVEIS DA BOMBAS
bombs = []
#EFEITOS SONOROS
shoot = pygame.mixer.sound('sounds/shoot.wav')
pop = pygame.mixer.sound('sounds/pop.wav')
bomb = pygame.mixer.sound('sounds/bomb.wav')
explosion = pygame.mixer.sound('sounds/explosion.wav')
explosion2 = pygame.mixer.sound('sounds/explosion2.wav')
select = pygame.mixer.sound('sounds/select.wav')
select2 = pygame.mixer.sound('sounds/select2.wav')
alert = pygame.mixer.sound('sounds/alert.wav')
whoosh = pygame.mixer.sound('sounds/whoosh.wav')

#CRIANDO O MENU
def main_menu():
    global cloud_x
    global  cloud_y

    menu = True

    selected = 'play'

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN: # COLOCANDO UMA TECLA DO TECLADO
                if event.key == pygame.K_w or event.key == pygame.K_UP: # ADICIONANDO A TECLA
                    pygame.mixer.Sound.play(select) # ADICIONA O EFEITO SONORO
                    selected = "play"

                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    pygame.mixer.Sound.play(select)
                    selected = 'quit'

                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    pygame.mixer.Sound.play(select2)
                    if selected == "play": # ENTRA UMA CONDIÇÃO AQUI DE ESCOLHA
                        menu = False
                    if select == 'quit':
                        pygame.quit()
                        quit()
        game_display.blit(sprites.background, (0, 0)) # PARA PASSAR OS ICONES
        game_display.blit(sprites.cloud, (cloud_x, cloud_x)) # IMAGENS DA NUVENS
        if cloud_x <= 800 - 1100:
            cloud_x = 800
            cloud_y = random.randint(0, 400)
        else:
            if not player.wreck_start:
                cloud_x -= 5
            if godmode: # MENSAGENS QUE IRAM APARECER NO JOGO
                title = message_to_screen("HELICOPTERO (GODMODE)", font, 80, yellow) # NOME DA JANELA
            else:
                title = message_to_screen("HELICOPTERO", font, 100, black)
            controls_1 = message_to_screen("USE WASD PARA MOVER, SPACE PARA ATIRAR", font, 30, black)
            controls_2 = message_to_screen("USE SHIFT PARA JOGAR BOMBA, P PARA PAUSAR", font, 30, black)

            if selected == "JOGAR": # PARA INICIAR O JOGO OU NAO
                play = message_to_screen("JOGAR", font, 75, white)
            else:
                play = message_to_screen("JOGAR", font, 75, black)

            if selected == "SAIR":
                game_quit = message_to_screen("SAIR", font, 75, white)
            else:
                game_quit = message_to_screen("SAIR", font, 75, black)

                title_rect = title.get_rect() # TITULO
                # CRIAÇÃO DAS VARIAVEIS
                controls_1_rect = controls_1.get_rect()
                controls_2_rect = controls_2.get_rect()
                play_rect = play.get_rect()
                quit_rect = game_quit.get_rect()

                game_display.blit(title, (display_width/2 - (title_rect[2]/2), 40)) # COLOANDO A MEDIDA DAS VARIAVEIS

                game_display.blit(controls_1, (display_width / 2 - (controls_1_rect[2] / 2), 120)) # ESCOLHE A POSIÇÃO NA TELA
                game.display.blit(controls_2, (display_width / 2 - (controls_2_rect[2] / 2), 140))
                game_display.blit(play, (display_width / 2 - (play_rect[2] / 2), 200))
                game_display.blit(game_quit, (display_width / 2 - (game_quit_rect[2] / 2), 260))

                pygame.draw.rect(game_display, blue, (0, 500, 800, 100)) #NO CASO AQUI ESTAMOS DESENHANDO O MAR

                pygame.display.update()
                pygame.display.set_caption("VELOCIADADE DO HELICOPTER" + str(int(clock.get_fps())) + "POR SEGUNDO") #ATUALIZAÇÃO DA JANELA
                clock.tick(FPS)

def pause (): # CRIANDO A VARIAVEL DE PAUSE
    global highscore_file
    global highscore_int

    paused = True

    player.moving_up = False
    player.moving_left = False
    player.moving_down = False
    player.moving_right = False

    paused_text = message_to_screen("JOGO PAUSADO !", font, 100, black)
    paused_text_rect = paused_text.get_rect()
    game_display.blit(paused_text, (display_width / 2 - (paused_text_rect[2] / 2), 40)) #CRIANDO A JANELA DE PUSE

    pygame.display.update()
    clock.tick(15) # NOSSA CONTAGEM
#CRIANDO A FUNÇÃO DE PAUSAR DO GAME
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score > highscore_int:
                    highscore_file = open('highscore.dat', "w") #MOSTRANDO A PONTUAÇÃO QUANDO PAUSAR
                    highscore_file.write(str(score))
                    highscore_file.close()
                    pygame.quit()
                    quit()
                # CRIANDO A TECLA COM A FUNÇÃO DE PAUSE
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pygame.mixer.Sound.play(select)
                        paused = False
def game_loop(): # CRIANDO O LOP
    global spaceship_x
    global spaceship_y
    global spaceship_alive
    global spaceship_hit_player
    global warning # MENSAGEM DE ATENÇÃO
    global warning_counter
    global warning_once

    global bullets
    global moving

    global highscore_file # ARMAZENAMENTO DA CONTAGEM DE PONTOS
    global highscore_int
    global score # PONTOS

    global cloud_x #NUVENS
    global cloud_y

    global enemy_heli_alive # O NOSSO INIMIGO
    global boat_alive # A VIDA DO NAVIO

    game_exit = False
    game_over = False

    gamer_over_selected = "JOGAR NOVAMENTE"

    while not game_exit:
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if score > highscore_int:
                        highscore_file = open('highscore.dat', "w")
                        highscore_file.write(str(score))
                        highscore_file.close()
                        pygame.quit()
                        quit()

                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w or event.key == pygame.K_UP:
                            pygame.mixer.Sound.play(select)
                            gamer_over_selected = "VOLTA AO JOGO"

                        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                            pygame.mixer.Sound.play(select)
                            gamer_over_selected = "quit"

                            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                                pygame.mixer.Sound.play(select2)
                                if  gamer_over_selected == "VOLTA AO JOGO":
                                    if score > highscore_int:
                                        highscore_file = open('highscore.dat', "w")
                                        highscore_file.write(str(score))
                                        highscore_file.close()
                                        game_over = False

                                        score = 0
                                        #PASSANDO O TAMANHO DO BALÃO
                                        balloon_x = 800

                                        enemy_heli.x = -100
                                        enemy_heli_alive = False # VIDAS DO INIMIGOS
                                        enemy_heli.bullets = [] # BALAS DO INIMIGOS

                                        boat.x = -110
                                        boat_alive = False
                                        boat.bullets = []

                                        spaceship_x = 800
                                        spaceship_alive = False
                                        warning = False
                                        warning_counter = 0 # CONTADOR
                                        warning_counter = 0
                                       # FUNÇÃO DO PLAY
                                        player.wreck_start = False
                                        player.y = display_height/ 2-40
                                        player.x = 100
                                        player.wrecked = False
                                        player.health = 3 # VIDAS DO PLAYER
                                        bullets = []

                                        game_loop()
                                    if gamer_over_selected == "quit":
                                        pygame.quit()
                                        quit()

                # MENSAGENS
            gamer_over_text = message_to_screen("JOGO OVER", font, 100, black)
            your_score = message_to_screen("SUA PONTUAÇÃO FOI: " + str(score), font, 50, black) # MOSTRA A PONTUAÇÃO
            if gamer_over_selected == "JOGAR NOVAMENTE":
                player_again = message_to_screen("JOGAR NOVAMENTE", font, 75, white)
            else:
                player_again = message_to_screen("JOGAR NOVAMENTE", font, 75, black)
            if gamer_over_selected == "quit":
                    game_quit = message_to_screen("QUIT", font, 75, white)
            else:
                    gamer_quit = message_to_screen("QUIT", font, 75, black)


            game_over_rect = gamer_over_text.get_rect()
            your_score_rect = your_score.get_rect()
            play_again_rect = play_again.get_rect()
            gamer_quit_rect = gamer_quit.get_rect()
            # JANELA DO GAMER OVER
            game_display.blit(gamer_over_text, (display_width / 2 - game_over_rect[2] / 2, 40))
            game_display.blit(your_score, (display_width / 2 - your_score_rect[2] / 2+5, 100))
            game_display.blit(player_again, (display_width / 2 - play_again_rect[2] / 2, 200))
            game_display.blit(gamer_quit, (display_width / 2 - gamer_quit_rect[2] / 2, 260))

            pygame.display.update()
            pygame.display.set_caption("VELOCIDADE DO HELICOPTER" + str(int(clock.get_fps())) + "POR SEGUNDO")
            clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score > highscore_int:
                    highscore_file = open('highscore.dat', "w")
                    highscore_file.write(str(score))
                    highscore_file.close()
                    pygame.quit()
                    quit()

                if moving: # PARA FAZER O MEU BARCO ANDA

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:
                            player.moving_up = True

                        if event.key == pygame.K_a:
                            player.moving_left = True

                        if event.key == pygame.K_s:
                            player.moving_down = True

                        if event.key == pygame.K_d:
                            player.moving_right = True

                        if event.key == pygame.K_SPACE:
                            if not player.wreck_start:
                                pygame.mixer.Sound.play(shoot) # COLOCANDO O SOM DO TIRO
                                bullets.append([player.x, player.y]) # PARA FAZER AS BALAS APARECEREM

                        if event.key == pygame.K_LSHIFT:
                            if not player.wreck_start:
                                pygame.mixer.Sound.play(bomb)
                                bombs.append([player.x, player.y])

                        if event.key == pygame.K_p:
                            pygame.mixer.Sound.play(select)
                            pause()

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_w:
                            player.moving_up = False

                        if event.key == pygame.K_a:
                            player.moving_left = False

                        if event.key == pygame.K_s:
                            player.moving_down = False

                        if event.key == pygame.K_d:
                            player.moving_right = False
                #VIDA DO PLAYER
        if player.health < 1: # SE SOR ATINGIDO É MENOS 1 VIDA
            pygame.mixer.Sound.play(explosion) # se eu for atirando o som de explosãp
            player.wrecked() # CONTAGEM DE PERCA DE VIDA

        if player.wrecked: #SE EU FOR ATINGIDO VAI PASSA A VARIAVEL TRUE E VAI SUBTRAIR AS VIDAS ATE 0
            game_over = True
        #CRIANDO O FUNDO COM AS NUVENS
        game_display.blit(sprites.background, (0, 0))
        game_display.blit(sprites.cloud, (cloud_x, cloud_y))
        if cloud_x <= 800 - 1100:
            cloud_x = 800
            cloud_y = random.randint(0, 400)
        else:
            if not player.wreck_start:
                cloud_x -= 5

        #CRIAR O NOSSO HELICOPITERO
        game_display.blit(player.current, (player.x, player.y)) # PLAYER
        game_display.blit(enemy_heli.current, (enemy_heli.x, enemy_heli.y)) # INIMIGO
        game_display.blit(sprites.spaceship, (spaceship_x, spaceship_y))
        game_display.blit(sprites.boat, (boat.x, boat.y)) #BARCO

        player.player_init()
        enemy_heli.init()
        boat.init()

        if not player.wreck_start and not player.wrecked:
            for draw_bullet in bullets: # BALAS
                pygame.draw.rect(game_display, black, (draw_bullet[0]+90, draw_bullet[1]+40, 10, 10)) #DESENHANDO AS BALAS
            for move_bullet in range(len(bullets)):
                bullets[move_bullet][0] +=40
            for del_bullet in bullets:
                if del_bullet[0]>=800:
                    bullets.remove(del_bullet)

        if not player.wreck_start and not player.wrecked: # DESENHANDO AS BOMBAS
            for draw_bomb in bombs:
                pygame.draw.rect(game_display, black, (draw_bomb[0]+55, del_bomb[1]+70, 20, 20))
            for move_bomb in range(len(bombs)):
                bombs[move_bomb][1] +=20
            for del_bomb in bombs:
                if del_bomb[1]>=600:
                    bombs.remove(del_bomb)

        if not player.wreck_start and not player.wrecked and not game_over:
            for draw_bullet in enemy_heli.bullets: #ATRIBUIR AO INIMIGO
                pygame.draw.rect(game_display, gray, (draw_bullet[0], draw_bullet[1]+40, 40, 10)) # QUANDO O INIMIGO ATIRA
                pygame.draw.rect(game_display, red, (draw_bullet[0]+30, draw_bullet[1]+40, 10, 10)) # QUANDO O INIMIGO ACERTA O PLAYER
            for move_bullet in range(len(enemy_heli.bullets)):
                enemy_heli.bullets[move_bullet][0] -=15
            for del_bullet in enemy_heli.bullets:
                if del_bullet[0]<=-40:
                    enemy_heli.bullets.remove(del_bullet)

        if not player.wrecked_start and not player.wrecked and not game_over:
            for draw_bullet in boat.bullets:
                pygame.draw.rect(game_display, gray, (draw_bullet[0]+40, draw_bullet[1]+30, 20, 20))
            for move_bullet in range(len(boat.bullets)):
                boat.bullets[move_bullet][0] -=10
                boat.bullets[move_bullet][1] -=10
            for del_bullet in boat.bullets:
                if del_bullet[1]<=-40:
                    boat.bullets.remove(del_bullet)

        for pop_balloon in bullets:
            if balloon_x < pop_balloon[0]+90 < balloon_x+70 and balloon_y < pop_balloon[1]+40 < balloon_y+100:
                pygame.mixer.Sound.play(pop)
                bullets.remove(pop_balloon)
                balloon_x = 800 - 870  # MEDIDAS DO BALAO
                score += 50 #PONTOS POR BALÃO
            elif balloon_x < pop_balloon[0]+100 < balloon_x+70 and balloon_y < pop_balloon[1]+50 < balloon_y+100:
                pygame.mixer.Sound.play(pop)
                bullets.remove(pop_balloon)
                balloon_x = 800 - 870
                score += 50

        for pop_balloon in bombs:
            if balloon_x < pop_balloon[0]+55 < balloon_x+70 and balloon_y < pop_balloon[1]+70 < balloon_y+100:
                pygame.mixer.Sound.play(pop)
                bombs.remove(pop_balloon)
                balloon_x = 800 - 870
                score += 50
            elif balloon_x < pop_balloon[0]+75 < balloon_x+70 and balloon_y < pop_balloon[1]+90 < balloon_y+100:
                pygame.mixer.Sound.play(pop)
                bombs.remove(pop_balloon)
                balloon_x = 800 - 870
                score += 50

            spaceship_spaw_num = random.randint(0, 100)
            if spaceship_spaw_num == 50 and not spaceship_alive and score > 450:
                warning = True

            if warning:
                if warning_once:
                    pygame.mixer.Sound.play(alert)
                    warning_once = False
                game_display.blit(warning_message, (750, spaceship_y-15))
                if warning_counter > 45:
                    pygame.mixer.Sound.play(whoosh)
                    spaceship_alive = True
                    warning_counter = 0
                    warning = False
                    warning_once = True
                else:
                    warning_counter +=1
                    # PLAY
                if spaceship_alive: # SE ELE AINDA ESTIVER COM VIDA
                    spaceship_x -=30
                if spaceship_x <0-100:
                    spaceship_hit_player = False
                    spaceship_alive = False
                    spaceship_x = 800
                    spaceship_y = random.randint(0, 400)
                    #INIMIGO HELICOP
                enemy__spawn_num = random.randint(0, 100)
                if not enemy_heli_alive and score > 250 and enemy__spawn_num == 50:
                    enemy_heli_alive = True
                    enemy_heli.x = 800
                    #INIMIGO BARCO
                boat_spawn_num = random.randint(0, 200)
                if score > 700 and boat_spawn_num == 100 and not boat_alive:
                    boat.x = 800
                    boat_alive = True

                if boat.x <= -110:
                    boat_alive = False
                #TRABALHANDO AS COLISÕES
                    #INIMIGO BALAS
                for hit_enemy_heli in bullets:
                    if enemy_heli.x < hit_enemy_heli[0]+90 < enemy_heli.x+100\
                        or enemy_heli.x < hit_enemy_heli[0]+100 < enemy_heli.x+100:
                        if enemy_heli.y < hit_enemy_heli[1]+40 < enemy_heli.y+80\
                            or enemy_heli.y < hit_enemy_heli[1]+50 < enemy_heli.y+80:
                            if not enemy_heli.x > 600:
                                pygame.mixer.Sound.play(explosion2)
                                score += 150
                                bullets.remove(hit_enemy_heli)
                                enemy_heli.x = -100
                                enemy_heli_alive = False

                for hit_spaceship in bullets:
                    if spaceship_x < hit_spaceship[0]+90 < spaceship_x+100\
                        or spaceship_x < hit_spaceship[0]+100 < spaceship_x+100:
                        if spaceship_y < hit_spaceship[1]+40 < spaceship_y +80\
                            or spaceship_y < hit_spaceship[1]+50 < spaceship_y+80:
                            if not spaceship_x > 700:
                                pygame.mixer.Sound.play(explosion2)
                                bullets.remove(hit_spaceship)
                                score +=200
                                spaceship_hit_player = False
                                spaceship_alive = False
                                spaceship_x = 800
                                spaceship_y = random.randint(0, 400)
                                #BOMBAS
                for hit_spaceship in bombs:
                    if spaceship_x < hit_spaceship[0]+55 < spaceship_x+100\
                        or spaceship_x < hit_spaceship[0]+65 < spaceship_x+100:
                        if spaceship_y < hit_spaceship[1]+70 < spaceship_y +80\
                            or spaceship_y < hit_spaceship[1]+80 < spaceship_y+80:
                            if not spaceship_x > 700:
                                pygame.mixer.Sound.play(explosion2)
                                bombs.remove(hit_spaceship)
                                score +=200
                                spaceship_hit_player = False
                                spaceship_alive = False
                                spaceship_x = 800
                                spaceship_y = random.randint(0, 400)

                for hit_boat in bullets:
                    if boat.x < hit_boat[0] + 90 < boat.x + 110 or boat.x < hit_spaceship[0] + 100 < boat.x + 110:
                        if boat.y < hit_boat[1] + 40 < boat.y + 70 or boat.y < hit_boat[1] + 50 <boat.y + 70:
                            if not boat.x > 780:
                                pygame.mixer.Sound.play(explosion2)
                                bullets.remove(hit_boat)
                                score += 200
                                boat_alive = False
                                boat.x = -110
                    # BOMBAS DO BOAT
                for hit_boat in bombs:
                    if boat.x < hit_boat[0] + 55 < boat.x + 110 or boat.x < hit_spaceship[0] + 75 < boat.x + 110:
                        if boat.y < hit_boat[1] + 70 < boat.y + 70 or boat.y < hit_boat[1] + 90 < boat.y + 70:
                            if not boat.x > 780:
                                pygame.mixer.Sound.play(explosion2)
                                bombs.remove(hit_boat)
                                score += 200
                                boat_alive = False
                                boat.x = -110
                    #BALOES
                if balloon_x < player.x < balloon_x + 70 or balloon_x < player.x + 100 < balloon_x + 70:
                    if balloon_y < player.y < balloon_y + 80 or balloon_y < player.y + 80 < balloon_y + 80:
                        pygame.mixer.Sound.play(explosion)
                        player.damaged = True
                        player.health -= 1
                        balloon_x = 800 - 870
                    #PLAYER
                for hit_player in enemy_heli.bullets:
                    if player.x < hit_player[0] < player.x + 100 or player.x < hit_player[0] + 40 < player.x +100:
                        if player.y < hit_player[1] + 40 < player.y + 80 or player.y < hit_player[1] + 50 < player.y + 80:
                            pygame.mixer.Sound.play(explosion)
                            player.damaged = True
                            player.health -= 1
                            enemy_heli.bullets.remove(hit_player)
                    # ATAQUES DO BOAT
                for hit_player in boat.bullets:
                    if player.x < hit_player[0] < player.x + 100 or player.x < hit_player[0] + 20 < player.x + 100:
                        if player.y < hit_player[1] < player.y + 80 or player.y < hit_player[1] + 20 < player.y + 80:
                            pygame.mixer.Sound.play(explosion)
                            if not boat.boat_hit_player:
                                player.damaged = True
                                player.health -= 1
                                boat.bullets.remove(hit_player)
                    #CONDIÇÃO DO BOAT
                if boat.x < player.x < boat.x + 110 or boat.x < player.x + 100 < boat.x + 110:
                    if boat.y < player.y < boat.y + 70 or boat.y < player.y + 80 < boat.y + 70:
                        if not boat.boat_hit_player:
                            pygame.mixer.Sound.play(explosion)
                            player.damaged = True
                            player.health -= 1
                            boat.boat_hit_player = True

                if spaceship_x < player.x < spaceship_x + 100 or spaceship_x < player.x + 100 < spaceship_x + 100:
                    if spaceship_y < player.y < spaceship_y + 88 or spaceship_y < player.y + 80 < spaceship_y + 88:
                        if not spaceship_hit_player:
                            pygame.mixer.Sound.play(explosion)
                            player.damaged = True
                            player.health -= 1
                            spaceship_hit_player = True


                game_display.blit(sprites.balloon, (balloon_x, balloon_y))
                if balloon_x <=800 - 870:
                    balloon_x = 800 # TAMANHA DO BALÃO
                    balloon_y = random.randint(0, 400)
                else:
                    if not player.wreck_start:
                        balloon_x -= 7
                    #PARA APARECER A NOSSA PONTUAÇÃO
                game_display.blit(message_to_screen("PONTOS : {}".format(score), font, 50, black),(10, 10))

                if score < highscore_int:
                    hi_score_message = message_to_screen("CONTAGEM : {}".format(highscore_int), font, 50, black)
                else:
                    highscore_file = open('Pontuacao Maxima.dat', "w")
                    highscore_file.write(str(score))
                    highscore_file.close()
                    highscore_file = open('Pontuacao MAxima.dat', "r")
                    highscore_int = int(highscore_file.read())
                    highscore_file.close()
                    hi_score_message = message_to_screen("CONTAGEM : {}".format(highscore_int), font, 50, yellow)
                    hi_score_message_rect = hi_score_message.get_rect()
                    game_display.blit(hi_score_message, (800-hi_score_message_rect[2]-10, 10)) #COLOCANDO NA TELA O SCORE
                    #DESENHANDO AS VIDAS
                if player.health >=1:
                    game_display.blit(sprites.icon, (10, 50)) #ICONES DE VIDA
                    if player.health >=2:
                        game_display.blit(sprites.icon, (10+32+10, 50))
                        if player.health >=3:
                            game_display.blit(sprites.icon, (10+32+10+32+10, 50))
                        # COMEÇO DO JOGO
                if godmode:
                    score = 1000 # COMEÇA COM 1000 PONTOS
                    player.health = 3 # COMEÇA COM 3 VIDAS
                    #MAR ou OCEANO
                pygame.draw.rect(game_display, blue, (0, 500, 800, 100))

                pygame.display.update() #PARA ATUALIZAR

                pygame.display.set_caption("VELOCIDADE DO HELICOPTER" + str(int(clock.get_fps())) + "POR SEGUNDOS")
                clock.tick(FPS)
      #TERMINADO O LOOP
main_menu()
game_loop()
pygame.quit()
quit()