import pygame
import sys
import pathlib
import random
import threading as th
import time

import arduinoConfig as ardC

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load(abs_path + r"\Game\img\player\player.png").convert_alpha()
        self.rect = self.image.get_rect(center=(random.uniform(display_width/6.4, display_width-(display_width/6.4)), random.uniform(display_height/5.4, display_height-(display_height/5.4))))
        
        rand_xy = random.choice((2, -2))
        self.dx, self.dy = rand_xy, rand_xy

    def update(self) -> None:
        # Player movement
        self.rect.x += self.dx
        self.rect.y += self.dy
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
        if self.rect.top < 0: self.dy *= -1
        if self.rect.bottom > display_height: self.dy *= -1
        if self.rect.left < 0: self.dx *= -1
        if self.rect.right > display_width: self.dx *= -1
            
    def collMovement(self) -> None:
        self.rect.x -= self.dx
        self.dx *= -1
        self.rect.y -= self.dy
        self.dy *= -1

class Square(pygame.sprite.Sprite):
    def __init__(self, lane: str, plot: int) -> None:
        super().__init__()        
        # Loading Square
        self.image = pygame.image.load(abs_path + r"\Game\img\square\square.png")
        
        # Deploying the Square on the screen
        if lane == "right":
            if plot == 0: self.rect = self.image.get_rect(midbottom=(display_width/1.06, (display_height/1.0303030303)/6))
            if plot == 1: self.rect = self.image.get_rect(midbottom=(display_width/1.06, (display_height/1.0303030303)/3))
            if plot == 2: self.rect = self.image.get_rect(midbottom=(display_width/1.06, (display_height/1.0303030303)/2))
            if plot == 3: self.rect = self.image.get_rect(midbottom=(display_width/1.06, (display_height/1.0303030303)/1.5))
            if plot == 4: self.rect = self.image.get_rect(midbottom=(display_width/1.06, (display_height/1.0303030303)/1.2))
            if plot == 5: self.rect = self.image.get_rect(midbottom=(display_width/1.06, (display_height/1.0303030303)))
        if lane == "left":
            if plot == 0: self.rect = self.image.get_rect(midbottom=(display_width-(display_width/1.06), (display_height/1.0303030303)/6))
            if plot == 1: self.rect = self.image.get_rect(midbottom=(display_width-(display_width/1.06), (display_height/1.0303030303)/3))
            if plot == 2: self.rect = self.image.get_rect(midbottom=(display_width-(display_width/1.06), (display_height/1.0303030303)/2))
            if plot == 3: self.rect = self.image.get_rect(midbottom=(display_width-(display_width/1.06), (display_height/1.0303030303)/1.5))
            if plot == 4: self.rect = self.image.get_rect(midbottom=(display_width-(display_width/1.06), (display_height/1.0303030303)/1.2))
            if plot == 5: self.rect = self.image.get_rect(midbottom=(display_width-(display_width/1.06), (display_height/1.0303030303)))

class Goal(pygame.sprite.Sprite):
    def __init__(self, coords: tuple) -> None:
        super().__init__()
        # Loading Goal
        self.image = pygame.image.load(abs_path + r"\Game\img\goal\goal.png").convert_alpha()
        self.rect = self.image.get_rect(center=coords)
        
def loadAsset(mode: str, coords: tuple, img_loc: str, font, fcolor, text: str) -> None:
    if mode == "text":
        asset = font.render(text, True, fcolor)
        asset_rect = asset.get_rect(center=coords)
        screen.blit(source=asset, dest=asset_rect)
    if mode == "img":
        asset = pygame.image.load(img_loc).convert_alpha()
        asset_rect = asset.get_rect(center=coords)
        screen.blit(source=asset,dest=asset_rect)
        
def displayScore() -> None:
    loadAsset(mode="text", coords=(display_width/2, display_height/24), img_loc=None, font=data_font, fcolor="#ffffff", text="Score:")
    loadAsset(mode="text", coords=(display_width/2, display_height/14), img_loc=None, font=data_font, fcolor="#34febb", text=str(score))
    
def displayTimePlayed() -> None:
    global current_time
    current_time = pygame.time.get_ticks()//1000 - start_time
    text_surf = data_font.render("Time Played:", True, "#ffffff")
    text_rect = text_surf.get_rect(center=(display_width/2, display_height/1.10869565217))
    screen.blit(source=text_surf, dest=text_rect)
    time_surf = data_font.render(f"{current_time} sec", True, "#34febb")
    time_rect = text_surf.get_rect(center=(display_width/1.92, display_height/1.07196029777))
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
    fps = 120
    
    # Arduino initialization
    Ard = ardC.Ard()
    
    # Bg Music
    bg_music = pygame.mixer.Sound(abs_path + r"\Game\music\Beginning 2.mp3")
    bg_music.set_volume(0.5)
    bg_music.play(loops=(-1))
    bg_music_G = pygame.mixer.Sound(abs_path + r"\Game\music\Wait.mp3")
    bg_music_G.set_volume(0.5)
    
    # Asset initialization
    player = pygame.sprite.GroupSingle()
    square = pygame.sprite.GroupSingle()
    goal = pygame.sprite.GroupSingle()
    
    # Game Event Loop
    while True:
        screen.fill(color="#2b2d2e")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Stopping game
                bg_music_G.stop()
                pygame.quit()
                sys.exit()
                                
            if not game_active and not intro_state:
                # Starting Game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    bg_music.stop()
                    bg_music_G.play(loops=(-1))
                    
                    # Arduino detection
                    if Ard.arduino_connected:
                        if not Ard.arduinoSerial.is_open: Ard.arduinoSerial.open()
                        time.sleep(1)
                        
                        # Starting Arduino thread
                        ArdgetDatathread = th.Thread(target=lambda: Ard.getData())
                        ArdgetDatathread.daemon = True
                        ArdgetDatathread.start()
                        
                        # Asset initialization
                        player.add(Player())
                        goal.add(Goal(coords=(random.uniform(display_width/6.4, display_width-(display_width/6.4)), random.uniform(display_height/5.1, display_height-(display_height/5.1)))))
                        if Ard.arduino_data:
                            square.add(Square(lane=Ard.arduino_data[0], plot=Ard.arduino_data[1]))
                            Ard.arduino_data.clear()
                        
                        # Exit message initialization
                        exit_text = italicD_font.render("Press 'Esc' key to return to home screen", True, "#fe6b31")
                        exit_text_rect = exit_text.get_rect(center=(display_width/2, display_height/10))
                        
                        # Start Timer
                        start_time = pygame.time.get_ticks()//1000
                    
                # Exitting game
                if not Ard.arduino_connected:
                    if event.type == pygame.KEYDOWN:
                        pygame.quit()
                        sys.exit()
            
            # Exitting Welcome screen            
            if intro_state: 
                if event.type == pygame.KEYDOWN: intro_state = False
            
            # Resseting game
            if game_active:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # Changing config
                    intro_state = True
                    change_goal_state = False
                    game_active = False
                    start_time = 0
                    current_time = 0
                    score = 0
                    
                    # Stopping bg tasks
                    bg_music_G.stop()
                    bg_music.play()
                    Ard.arduinoSerial.close()
                                            
        # Main Game
        if game_active:                        
            # Player initialization
            player.draw(surface=screen)
            player.update()

            # Square and Goal initialization
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
                square.add(Square(lane=Ard.arduino_data[0], plot=Ard.arduino_data[1]))
                Ard.arduino_data.clear()
            
            # Chaning Goal state
            if change_goal_state:
                goal.empty()
                goal.add(Goal(coords=(random.uniform(display_width/6.4, display_width-(display_width/6.4)), random.uniform(display_height/5.1, display_height-(display_height/5.1)))))
                change_goal_state = False
                
        # Intro Screen
        else:
            # Background
            screen.fill(color="#20242c")
            
            # Intro Screen
            if intro_state:
                # Displaying messages
                loadAsset(mode="text", coords=(display_width/2, display_height/5.4), img_loc=None, font=game_font, fcolor="#6ee390", text="Square Bouncer!")
                loadAsset(mode="img", coords=(display_width/2, display_height/2.3), img_loc=abs_path+r"\Game\img\game_icons.png", font=None, fcolor=None, text=None)
                loadAsset(mode="text", coords=(display_width/2, display_height/1.4), img_loc=None, font=game_font, fcolor="#ffffff", text="Press any key to continue")
                loadAsset(mode="text", coords=(display_width/1.06666666667, display_height-(display_height/30)), img_loc=None, font=italicD_font, fcolor="#fe6b31", text="By: M Vihaan, 8G")
                
            # Entering game screen
            else:
                # Background
                screen.fill(color="#20242c")                
                loadAsset(mode="img", coords=(display_width/2, display_height/2.88), img_loc=abs_path+r"\Game\img\player\_player.png", font=None, fcolor=None, text=None)

                # Displaying messages
                loadAsset(mode="text", coords=(display_width/2, display_height/6.8), img_loc=None, font=game_font, fcolor="#2176ed", text="Tried to connect with Arduino")
                if Ard.arduino_connected:
                    loadAsset(mode="text", coords=(display_width/2, display_height/1.7), img_loc=None, font=game_font, fcolor="#6ee390", text="Connected Successfully!")
                    loadAsset(mode="text", coords=(display_width/2, display_height/1.45714285714), img_loc=None, font=game_font, fcolor="#ffffff", text="Press spacebar to start")
                else:
                    loadAsset(mode="text", coords=(display_width/2, display_height/1.7), img_loc=None, font=game_font, fcolor="#FF0000", text="Couldnt Connect to Arduino!")
                    loadAsset(mode="text", coords=(display_width/2, display_height/1.45714285714), img_loc=None, font=game_font, fcolor="#ffffff", text="Press any key to exit")

        pygame.display.update()
        clock.tick(fps)