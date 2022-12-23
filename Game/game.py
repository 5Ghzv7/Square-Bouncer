import pygame
import sys
sys.dont_write_bytecode = True
import pathlib
import random
import threading as th
import time

import arduinoConfig as ardC

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load(r"Game\img\player\player.png").convert_alpha()
        self.rect = self.image.get_rect(center=(random.randint(300, display_width-300), random.randint(200, display_height-200)))
        
        rand_xy = random.choice((2, -2))
        self.dx, self.dy = rand_xy, rand_xy

    def update(self) -> None:
        # ?
        self.wallBouncing()
        
        # Collision and Score updating
        sq_coll = pygame.sprite.groupcollide(player, square, False, False, pygame.sprite.collide_rect_ratio(0.75))
        if sq_coll: self.collMovement()

        global change_goal_state, score
        goal_coll = pygame.sprite.groupcollide(player, goal, False, False, pygame.sprite.collide_rect_ratio(0.9))
        if goal_coll:
            self.collMovement()
            score += 1
            change_goal_state = True
            
        if pygame.sprite.groupcollide(player, square, False, False, pygame.sprite.collide_rect_ratio(0.75)):
            self.bufferscore = score
            if self.bufferscore+2 == score:
                rand_xy = random.choice((2, -2))
                self.dx, self.dy = rand_xy, rand_xy
                self.collMovement()
            
    def wallBouncing(self) -> None:
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.top < 0: self.dy *= -1
        if self.rect.bottom > display_height: self.dy *= -1
        if self.rect.left < 0: self.dx *= -1
        if self.rect.right > display_width: self.dx *= -1
            
    def collMovement(self) -> None:
        self.rect.x -= self.dx
        self.dx *= -1
        self.dx += 1 #random.choice((0, 1))
        self.rect.y -= self.dy
        self.dy *= -1
        self.dy += 1 #random.choice((0, 1))

class Square(pygame.sprite.Sprite):
    def __init__(self, lane: str, plot: int, sq_angle: float) -> None:
        super().__init__()
        
        # Loading Sprite
        self.image = pygame.image.load(r"Game\img\square\square.png")
        
        # Changing Angle
        self.image = pygame.transform.rotate(surface=self.image, angle=sq_angle).convert_alpha()
        
        if lane == "right":
            if plot == 0: self.rect = self.image.get_rect(midbottom=(display_width-100, (display_height-30)/6))
            if plot == 1: self.rect = self.image.get_rect(midbottom=(display_width-100, (display_height-30)/3))
            if plot == 2: self.rect = self.image.get_rect(midbottom=(display_width-100, (display_height-30)/2))
            if plot == 3: self.rect = self.image.get_rect(midbottom=(display_width-100, (display_height-30)/1.5))
            if plot == 4: self.rect = self.image.get_rect(midbottom=(display_width-100, (display_height-30)/1.2))
            if plot == 5: self.rect = self.image.get_rect(midbottom=(display_width-100, (display_height-30)))
        if lane == "left":
            if plot == 0: self.rect = self.image.get_rect(midbottom=(100, (display_height-30)/6))
            if plot == 1: self.rect = self.image.get_rect(midbottom=(100, (display_height-30)/3))
            if plot == 2: self.rect = self.image.get_rect(midbottom=(100, (display_height-30)/2))
            if plot == 3: self.rect = self.image.get_rect(midbottom=(100, (display_height-30)/1.5))
            if plot == 4: self.rect = self.image.get_rect(midbottom=(100, (display_height-30)/1.2))
            if plot == 5: self.rect = self.image.get_rect(midbottom=(100, (display_height-30)))   

class Goal(pygame.sprite.Sprite):
    def __init__(self, coords: tuple) -> None:
        super().__init__()
        # Loading Goal
        self.image = pygame.image.load(r"Game\img\goal\goal.png").convert_alpha()
        self.rect = self.image.get_rect(center=coords)
    
def displayScore() -> None:
    score_surf = data_font.render(f"Score:", True, "#ffffff")
    score_rect = score_surf.get_rect(center=(display_width/2, display_height/24))
    score2_surf = data_font.render(f"{score}", True, "#34febb")
    score2_rect = score_surf.get_rect(center=((display_width/2)+27.5, display_height/14))
    screen.blit(source=score_surf, dest=score_rect)
    screen.blit(source=score2_surf, dest=score2_rect)
    
def displayTimePlayed() -> None:
    global current_time
    current_time = pygame.time.get_ticks()//1000 - start_time
    text_surf = data_font.render("Time Played:", True, "#ffffff")
    text_rect = text_surf.get_rect(center=(display_width/2, display_height-100))
    screen.blit(source=text_surf, dest=text_rect)
    time_surf = data_font.render(f"{current_time} sec", True, "#34febb")
    time_rect = text_surf.get_rect(center=((display_width/2)+40, display_height-72.5))
    screen.blit(source=time_surf, dest=time_rect)
    
if __name__ == "__main__":
    # Game initialization
    pygame.init()

    # Display info
    display_dimensions = pygame.display.Info()
    display_width = display_dimensions.current_w
    display_height = display_dimensions.current_h
    screen = pygame.display.set_mode((display_width, display_height-60))
    display_width, display_height = screen.get_size()
    
    # Absolute Path
    abs_path = str(pathlib.Path().absolute())

    # Intro Screen Assets
    pygame.display.set_icon(pygame.image.load(abs_path + r"\Game\img\player\player.png"))
    pygame.display.set_caption("Square Bouncer")
    game_font = pygame.font.Font(abs_path + r"\Game\font\CascadiaCodePL-SemiBold.ttf", 50)
    data_font = pygame.font.Font(abs_path + r"\Game\font\CascadiaCodePL-SemiBold.ttf", 25)
    italicD_font = pygame.font.Font(abs_path + r"\Game\font\CascadiaCode-SemiBoldItalic.ttf", 20)

    # Config
    clock = pygame.time.Clock()
    intro_state = True
    change_goal_state = False
    game_active = False
    start_time = 0
    current_time = 0
    score = 0
    
    # Arduino initialization
    Ard = ardC.Ard()
    
    # Bg Music
    bg_music = pygame.mixer.Sound(abs_path + r"\Game\music\Beginning 2.mp3")
    bg_music.set_volume(0.5) #0.5
    bg_music.play(loops=(-1))
    bg_music_G = pygame.mixer.Sound(abs_path + r"\Game\music\Wait.mp3")
    bg_music_G.set_volume(0.5) #0.5

    #Intro Screen Assets
    logo_img = pygame.image.load(abs_path + r"\Game\img\player\_player.png").convert_alpha()
    logo_rect = logo_img.get_rect(center=(display_width/2, 375))
    
    # Asset initialization
    player = pygame.sprite.GroupSingle()
    square = pygame.sprite.GroupSingle()
    goal = pygame.sprite.GroupSingle()
    
    # Game Event Loop
    while True:
        screen.fill(color="#2b2d2e")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bg_music_G.stop()
                pygame.quit()
                sys.exit()
                                
            if not game_active and not intro_state:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    bg_music.stop()
                    bg_music_G.play(loops=(-1))
                    
                    # Starting Arduino thread
                    if Ard.arduino_connected:
                        time.sleep(1)
                        
                        startArdgetDatathread = th.Thread(target=lambda: Ard.getData())
                        startArdgetDatathread.daemon = True
                        startArdgetDatathread.start()
                        
                        # Asset initialization
                        player.add(Player())
                        goal.add(Goal(coords=(random.randint(300, display_width-300), random.randint(200, display_height-200))))
                        if Ard.arduino_data:
                            square.add(Square(lane=Ard.arduino_data[0], plot=Ard.arduino_data[1], sq_angle=Ard.arduino_data[2]))
                            Ard.arduino_data.clear()
                        
                        exit_text = italicD_font.render("Press 'Esc' key to return to home screen", True, "#fe6b31")
                        exit_text_rect = exit_text.get_rect(center=(display_width/2, display_height/10))
                        
                        # Start Timer
                        start_time = pygame.time.get_ticks()//1000
                    
                if not Ard.arduino_connected:
                    if event.type == pygame.KEYDOWN:
                        pygame.quit()
                        sys.exit()
                        
            if intro_state: 
                if event.type == pygame.KEYDOWN: intro_state = False
            
            if game_active:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_active = False
                    intro_state = True
                    bg_music_G.stop()
                    bg_music.play()
                                            
        # Main Game
        if game_active:                        
            # Player initialization
            player.draw(surface=screen)
            player.update()

            # asset_group initialization
            square.draw(surface=screen)
            square.update()
            goal.draw(surface=screen)
            goal.update()
            
            # Display info
            displayTimePlayed()
            displayScore()
            screen.blit(source=exit_text, dest=exit_text_rect)
            
            # Changing Square State
            if Ard.arduino_data:
                square.empty()
                square.add(Square(lane=Ard.arduino_data[0], plot=Ard.arduino_data[1], sq_angle=Ard.arduino_data[2]))
                Ard.arduino_data.clear()
            
            # Chaning Goal state
            if change_goal_state:
                goal.empty()
                goal.add(Goal(coords=(random.randint(400, display_width-400), random.randint(200, display_height-200))))
                change_goal_state = False
                
        # Intro Screen
        else:
            screen.fill(color="#20242c")
            
            # Intro Screen
            if intro_state:
                Intro = game_font.render("Square Bouncer!", True, "#6ee390")
                Intro_rect = Intro.get_rect(center=(display_width/2, 200))
                screen.blit(source=Intro, dest=Intro_rect)
                
                assetgrp_img = pygame.image.load(abs_path + r"\Game\img\game_icons.png").convert_alpha()
                assetgrp_rect = assetgrp_img.get_rect(center=(display_width/2, display_height/2.3))
                screen.blit(source=assetgrp_img,dest=assetgrp_rect)
                
                start_game_message = game_font.render("Press any key to continue", True, "#ffffff")
                start_game_message_rect = start_game_message.get_rect(center=(display_width/2, display_height/1.4))
                screen.blit(source=start_game_message, dest=start_game_message_rect)
                
                creator_name = italicD_font.render("By: M Vihaan, 8G", True, "#fe6b31")
                creator_rect = creator_name.get_rect(bottomleft=(display_width-220, display_height-30))
                screen.blit(source=creator_name, dest=creator_rect)
                
            # Entering game screen
            else:
                screen.fill(color="#20242c")
                try_connection_message = game_font.render("Tried to connect with Arduino", True, "#2176ed")
                try_connection_message_rect = try_connection_message.get_rect(center=(display_width/2, 150))
                screen.blit(source=try_connection_message, dest=try_connection_message_rect)

                if Ard.arduino_connected:
                    screen.blit(source=logo_img, dest=logo_rect)
                    
                    connected_message = game_font.render("Connected Successfully!", True, "#6ee390")
                    connected_message_rect = connected_message.get_rect(center=(display_width/2, 600))
                    screen.blit(source=connected_message, dest=connected_message_rect)

                    start_game_message = game_font.render("Press spacebar to start", True, "#ffffff")
                    start_game_message_rect = start_game_message.get_rect(center=(display_width/2, 700))
                    screen.blit(source=start_game_message, dest=start_game_message_rect)
                else:
                    screen.blit(source=logo_img, dest=logo_rect)
                    
                    connected_message = game_font.render("Couldnt Connect to Arduino!", True, "#ff0000")
                    connected_message_rect = connected_message.get_rect(center=(display_width/1.5, 600))
                    screen.blit(source=connected_message, dest=connected_message_rect)

                    exit_game_message = game_font.render("Press any key to exit", True, "#ffffff")
                    exit_game_message_rect = exit_game_message.get_rect(center=(display_width/2, 700))
                    screen.blit(source=exit_game_message, dest=exit_game_message_rect)

        pygame.display.update()
        clock.tick(120)