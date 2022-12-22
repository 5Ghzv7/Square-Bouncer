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
        self.rect = self.image.get_rect(center=(display_width-100, display_height-100))

        self.dx = random.choice((-1, 1))
        self.dy = random.choice((-2, -1, 1, 2))

    def update(self) -> None:
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.top < 0:
            self.dy *= -1
        if self.rect.bottom > display_height:
            self.dy *= -1
        if self.rect.left < 0:
            self.dx *= -1
        if self.rect.right > display_width:
            self.dx *= -1

        # Collision with Polygon
        global score
        collision = pygame.sprite.spritecollideany(sprite=player.sprite, group=asset_group)
        if collision != None:
            self.rect.x -= self.dx
            self.dx *= -1
            self.dx += random.choice((0, 1))
            self.rect.y -= self.dy
            self.dy *= -1
            self.dy += random.choice((0, 1))
            score += 1

class Square(pygame.sprite.Sprite):
    def __init__(self, lane: str) -> None:
        super().__init__()

        # Loading Sprite
        self.image = pygame.image.load(r"Game\img\square\square.png").convert_alpha()
        if lane == "right":
            self.rect = self.image.get_rect(center=(display_width-100, display_height-100))
        if lane == "left":
            self.rect = self.image.get_rect(center=(100, display_height-100))

class Goal(pygame.sprite.Sprite):
    def __init__(self, lane: str) -> None:
        super().__init__()
        self.image = pygame.image.load(r"Game\img\goal\goal.png").convert_alpha()
        self.rect = self.image.get_rect(center=(display_width/2, display_height/2))

def displayTimePlayed() -> None:
    current_time = pygame.time.get_ticks() // 1000 - start_time
    text_surf = data_font.render("Time Played:", True, "#ffffff")
    text_rect = text_surf.get_rect(center=(display_width/16, display_height/24))
    time_surf = data_font.render(f"{current_time} sec", True, "#01e3f2")
    time_rect = text_surf.get_rect(center=(display_width/16, display_height/14))
    screen.blit(source=text_surf, dest=text_rect)
    screen.blit(source=time_surf, dest=time_rect)
    
def displayScore() -> None:
    score_surf = data_font.render(f"{score}", True, "#fe1db4")
    score_rect = score_surf.get_rect(center=(display_width-60, display_height/24))
    screen.blit(source=score_surf, dest=score_rect)
    screen.blit(source=score_surf, dest=score_rect)

if __name__ == "__main__":
    # Game initialization
    pygame.init()

    # Display info
    display_dimensions = pygame.display.Info()
    display_width = display_dimensions.current_w
    display_height = display_dimensions.current_h
    screen = pygame.display.set_mode((display_width, display_height-59))
    display_width, display_height = screen.get_size()
    
    # Absolute Path
    abs_path = str(pathlib.Path().absolute())

    # Intro Screen Assets
    pygame.display.set_icon(pygame.image.load(abs_path + r"\Game\img\player\player.png"))
    pygame.display.set_caption("Square Bouncer")
    game_font = pygame.font.Font(abs_path + r"\Game\font\CascadiaCodePL-SemiBold.ttf", 50)
    data_font = pygame.font.Font(abs_path + r"\Game\font\CascadiaCodePL-SemiBold.ttf", 25)

    # Config
    clock = pygame.time.Clock()
    game_active = False
    start_time = 0
    score = 0
    
    # Arduino initialization
    Ard = ardC.Ard()
    
    # Bg Music
    bg_music = pygame.mixer.Sound(abs_path + r"\Game\music\Beginning 2.mp3")
    bg_music.play(loops=(-1))
    bg_music_G = pygame.mixer.Sound(abs_path + r"\Game\music\Wait.mp3")

    #Intro Screen Assets
    logo_img = pygame.image.load(abs_path + r"\Game\img\player\_player.png").convert_alpha()
    logo_rect = logo_img.get_rect(center=(display_width/2, 375))

    # Game Event Loop
    while True:
        screen.fill(color="#2b2d2e")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bg_music_G.stop()
                pygame.quit()
                sys.exit()
                                
            if not game_active:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = pygame.time.get_ticks()//1000
                    bg_music.stop()
                    bg_music_G.play(loops=(-1))
                    
                    # Starting Arduino thread
                    if Ard.arduino_connected:
                        time.sleep(1)
                        
                        startArdgetDatathread = th.Thread(target=lambda: Ard.getData())
                        startArdgetDatathread.daemon = True
                        startArdgetDatathread.start()
                        
                    # Asset initialization
                    player = pygame.sprite.GroupSingle()
                    player.add(Player())

                    # Polygons (obstacles)
                    asset_group = pygame.sprite.Group()
                    asset_group.add(Square(lane="left"), Goal(lane="left"))
                    
                if not Ard.arduino_connected:
                    if event.type == pygame.KEYDOWN:
                        pygame.quit()
                        sys.exit()
                                            
        # Main Game
        if game_active:                        
            # Player initialization
            player.draw(surface=screen)
            player.update()

            # asset_group initialization
            asset_group.draw(surface=screen)
            asset_group.update()
            
            # Display info
            displayTimePlayed()
            displayScore()
            
            print(Ard.arduino_data)
        # Intro Screen
        else:
            screen.fill(color="#20242c")
            screen.blit(source=logo_img, dest=logo_rect)

            try_connection_message = game_font.render("Tried to connect with Arduino...", True, "#2176ed")
            try_connection_message_rect = try_connection_message.get_rect(center=(display_width/2, 150))
            screen.blit(source=try_connection_message, dest=try_connection_message_rect)

            if Ard.arduino_connected:
                connected_message = game_font.render("Connected Successfully", True, "#6ee390")
                connected_message_rect = try_connection_message.get_rect(center=(display_width/1.725, 600))
                screen.blit(source=connected_message, dest=connected_message_rect)

                start_game_message = game_font.render("Press spacebar to start", True, "#ffffff")
                start_game_message_rect = start_game_message.get_rect(center=(display_width/2, 700))
                screen.blit(source=start_game_message, dest=start_game_message_rect)
            else:
                connected_message = game_font.render("Couldnt Connect to Arduino...", True, "#ff0000")
                connected_message_rect = try_connection_message.get_rect(center=(display_width/1.875, 600))
                screen.blit(source=connected_message, dest=connected_message_rect)

                start_game_message = game_font.render("Press any key to exit", True, "#ffffff")
                start_game_message_rect = start_game_message.get_rect(center=(display_width/2, 700))
                screen.blit(source=start_game_message, dest=start_game_message_rect)
                
            """connected_message = game_font.render("Connected Successfully", True, "#6ee390")
            connected_message_rect = try_connection_message.get_rect(center=(display_width/1.725, 600))
            screen.blit(source=connected_message, dest=connected_message_rect)

            start_game_message = game_font.render("Press spacebar to start", True, "#ffffff")
            start_game_message_rect = start_game_message.get_rect(center=(display_width/2, 700))
            screen.blit(source=start_game_message, dest=start_game_message_rect)"""

        pygame.display.update()
        clock.tick(60)