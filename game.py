import time
import random

import pygame
from pygame.sprite import Sprite

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 700
GREY = (92, 91, 91)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (189, 174, 42)
RED = (255, 0, 0)


# define a BaseItem class
class BaseItem(Sprite):
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)


# This class is used to initialize and create window
class Game:
    window = None

    my_bullet_sound = None
    enemy1_explode_sound = None
    enemy2_explode_sound = None
    enemy3_explode_sound = None
    fire_bomb_sound = None
    get_bomb_sound = None
    get_heart_sound = None
    lose_heart_sound = None

    button_hover_sound = None
    button_pressed_sound = None

    hit_record_sound = None
    not_hit_record_sound = None

    start_hover_once = False
    bs_hover_once = False
    exit_hover_once = False

    def __init__(self):
        pass

    def create_game(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        pygame.display.init()
        Game.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption("Aircraft War")

        Game.my_bullet_sound = pygame.mixer.Sound("musics/my_bullet.wav")
        Game.enemy1_explode_sound = pygame.mixer.Sound("musics/enemy1_explode.wav")
        Game.enemy2_explode_sound = pygame.mixer.Sound("musics/enemy2_explode.wav")
        Game.enemy3_explode_sound = pygame.mixer.Sound("musics/enemy3_explode.wav")
        Game.fire_bomb_sound = pygame.mixer.Sound("musics/fire_bomb.wav")
        Game.get_bomb_sound = pygame.mixer.Sound("musics/get_bomb.wav")
        Game.get_heart_sound = pygame.mixer.Sound("musics/get_heart.wav")
        Game.lose_heart_sound = pygame.mixer.Sound("musics/lose_heart.wav")
        Game.lose_heart_sound.set_volume(0.7)

        Game.hit_record_sound = pygame.mixer.Sound("musics/hit_record.wav")
        Game.not_hit_record_sound = pygame.mixer.Sound("musics/not_hit_record.wav")

        Game.button_hover_sound = pygame.mixer.Sound("musics/button_hover.wav")
        Game.button_pressed_sound = pygame.mixer.Sound("musics/button_pressed.wav")


class Menu:

    def __init__(self):
        self.bg = ScrollBG(2)

        self.button_start = MenuButtons("Start", 25, BLACK, BLACK, 3, 140, 300)
        self.button_bs = MenuButtons("Best Score", 22, BLACK, BLACK, 3, 140, 400)
        self.button_exit = MenuButtons("Exit", 25, BLACK, BLACK, 3, 140, 500)
        self.button_start_hover = MenuButtons("Start", 30, WHITE, GREY, 0, 140, 300)
        self.button_bs_hover = MenuButtons("Best Score", 27, WHITE, GREY, 0, 140, 400)
        self.button_exit_hover = MenuButtons("Exit", 30, WHITE, GREY, 0, 140, 500)

    def create_menu(self):
        pygame.display.init()
        pygame.display.set_caption("Aircraft War")

        while True:
            self.bg.render()
            self.bg.scroll()

            self.check_button_hover()

            self.add_caption()

            self.get_event()
            pygame.display.update()  # Make the window updated


    def get_event(self):
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_start.detect_mouse_hover():
                    Game.button_pressed_sound.play()
                    pygame.time.wait(100)
                    MainGame().start_game()
                elif self.button_bs.detect_mouse_hover():
                    Game.button_pressed_sound.play()
                    pygame.time.wait(100)
                    BestScore().show_bg()
                elif self.button_exit.detect_mouse_hover():
                    with open('best_score.txt', 'w') as f:
                        f.write("0")
                    exit()

    def add_caption(self):
        # Add game caption
        Game.window.blit(self.create_text("AIRCRAFT", BLACK),
                         (30, 35))
        Game.window.blit(self.create_text("WAR", BLACK),
                         (140, 135))
        Game.window.blit(self.create_text("AIRCRAFT", GREY),
                         (35, 40))
        Game.window.blit(self.create_text("WAR", GREY),
                         (145, 140))

    # Add text
    def create_text(self, text, color):
        pygame.font.init()
        font = pygame.font.Font('fonts/zorque.otf', 85)
        text_surface = font.render(text, True, color)
        return text_surface

    # Check if the mouse is hovering over the button
    def check_button_hover(self):
        if self.button_start.detect_mouse_hover():
            self.button_start_hover.button_text()
            if not Game.start_hover_once:
                Game.button_hover_sound.play()
                Game.start_hover_once = True

        else:
            self.button_start.button_text()
            Game.start_hover_once = False

        if self.button_bs.detect_mouse_hover():
            self.button_bs_hover.button_text()
            if not Game.bs_hover_once:
                Game.button_hover_sound.play()
                Game.bs_hover_once = True
        else:
            self.button_bs.button_text()
            Game.bs_hover_once = False

        if self.button_exit.detect_mouse_hover():
            self.button_exit_hover.button_text()
            if not Game.exit_hover_once:
                Game.button_hover_sound.play()
                Game.exit_hover_once = True
        else:
            self.button_exit.button_text()
            Game.exit_hover_once = False


class ScrollBG:

    def __init__(self, speed):
        self.image = pygame.image.load("imgs/background.png")
        self.rect = self.image.get_rect()
        self.speed = speed
        self.pos_y1 = 0
        self.pos_y2 = -self.rect.height

    def scroll(self):
        self.pos_y1 += self.speed
        self.pos_y2 += self.speed
        if self.pos_y1 >= SCREEN_HEIGHT:
            self.pos_y1 = -self.rect.height
        if self.pos_y2 >= SCREEN_HEIGHT:
            self.pos_y2 = -self.rect.height

    def render(self):
        Game.window.blit(self.image, (0, self.pos_y1))
        Game.window.blit(self.image, (0, self.pos_y2))


class MenuButtons:
    def __init__(self, text, font_size, text_color, button_color, side_width, pos_x, pos_y):
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        self.button_color = button_color
        self.side_width = side_width
        self.pos_x = pos_x
        self.pos_y = pos_y

    def create_button(self):
        return pygame.draw.rect(Game.window, self.button_color, pygame.Rect(self.pos_x, self.pos_y, 200, 50),
                                self.side_width, 15)

    def create_text(self):
        pygame.font.init()
        font = pygame.font.Font('fonts/ghostclan.ttf', self.font_size)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.pos_x + 100, self.pos_y + 25))
        Game.window.blit(text_surface, text_rect)

    # combine create_button and create_text
    def button_text(self):
        self.create_button()
        self.create_text()

    def detect_mouse_hover(self):
        return self.create_button().collidepoint(pygame.mouse.get_pos())


class BestScore:
    return_hover_once = False
    start_hover_once = False

    def __init__(self):
        self.bg = ScrollBG(2)
        self.button_return = MenuButtons("Return", 25, BLACK, BLACK, 3, 25, 600)
        self.button_return_hover = MenuButtons("Return", 30, WHITE, GREY, 0, 25, 600)
        self.button_start = MenuButtons("Start", 25, BLACK, BLACK, 3, 255, 600)
        self.button_start_hover = MenuButtons("Start", 30, WHITE, GREY, 0, 255, 600)

    def show_bg(self):

        # MainGame.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption("Aircraft War Best Score")

        while True:
            self.bg.render()
            self.bg.scroll()
            Game.window.blit(self.create_text("Best Score", 'fonts/zorque.otf', 72, BLACK),
                             (25, 100))
            Game.window.blit(self.create_text("Best Score", 'fonts/zorque.otf', 72, GREY),
                             (30, 105))
            self.show_score()
            self.check_button_hover()
            self.get_event()
            pygame.display.update()  # Make the window updated

    def get_score(self):
        with open('best_score.txt', 'r') as f:
            return f.readline()



    def get_event(self):
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print('Move Up')
                elif event.key == pygame.K_DOWN:
                    print('Move Down')
                elif event.key == pygame.K_LEFT:
                    print('Move Left')
                elif event.key == pygame.K_RIGHT:
                    print('Move Right')
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_return.detect_mouse_hover():
                    Game.button_pressed_sound.play()
                    pygame.time.wait(100)
                    Menu().create_menu()
                elif self.button_start.detect_mouse_hover():
                    Game.button_pressed_sound.play()
                    pygame.time.wait(100)
                    MainGame().start_game()

    # Add the unchanging text
    def create_text(self, text, font, size, color):
        pygame.font.init()
        font = pygame.font.Font(font, size)
        text_surface = font.render(text, True, color)
        return text_surface

    # Add score
    def show_score(self):
        pygame.font.init()
        font = pygame.font.Font('fonts/ghostclan.ttf', 200)
        text_surface = font.render(self.get_score(), True, YELLOW)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        Game.window.blit(text_surface, text_rect)

    # Check if the mouse is hovering over the button
    def check_button_hover(self):

        if self.button_return.detect_mouse_hover():
            self.button_return_hover.button_text()
            if not BestScore.return_hover_once:
                Game.button_hover_sound.play()
                BestScore.return_hover_once = True
        else:
            self.button_return.button_text()
            BestScore.return_hover_once = False

        if self.button_start.detect_mouse_hover():
            self.button_start_hover.button_text()
            if not BestScore.start_hover_once:
                Game.button_hover_sound.play()
                BestScore.start_hover_once = True
        else:
            self.button_start.button_text()
            BestScore.start_hover_once = False


class MainGame:
    my_plane = None
    score = 0
    my_bomb_count = 0
    my_heart_count = 3
    enemy_plane_list = []

    my_weapon_list = []
    enemy3_bullet_list = []

    supply_list = []

    explode_list = []

    bullet_warning = False
    bomb_warning = False

    current_weapon_img = None

    pause = False

    def __init__(self):
        self.bg = ScrollBG(5)

        self.pause_or_resume_rect = pygame.image.load("imgs/pause_no.png").get_rect()
        self.pause_or_resume_rect.left = 400
        self.pause_or_resume_rect.top = 10

    def start_game(self):

        # MainGame.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption("Aircraft War Main Game")

        # Initialize my plane
        MainGame.my_plane = MyPlane(SCREEN_WIDTH / 2, 640)

        pygame.mixer.music.load("musics/bgm.ogg")
        pygame.mixer.music.play(-1)

        while True:
            # slow done
            time.sleep(0.02)  # unit is second

            # make scrolling background
            self.bg.render()
            if not MainGame.pause:
                self.bg.scroll()

            # monitor the event
            self.get_event()

            # display my plane
            MainGame.my_plane.display_plane()

            # display my weapons
            self.display_my_weapon()

            # create enemy planes
            if not MainGame.pause:
                rand_int1 = random.randint(1, 500)
                if rand_int1 <= 15:
                    self.create_enemy_plane()

            # display enemy planes
            self.display_enemy_plane()

            # display enemy bullets
            self.display_enemy_bullet()

            # create supplies
            if not MainGame.pause:
                rand_int2 = random.randint(1, 4000)
                if rand_int2 <= 10:
                    self.create_supply()

            # display supplies
            self.display_supply()

            # display explosion
            self.display_explosion()

            # display bomb label
            self.display_bomb_label()

            # display heart count
            self.display_heart()

            # display the score
            Game.window.blit(self.create_text("Score: {0}".format(MainGame.score), WHITE, 30), (10, 10))

            # display the warning
            self.display_warning()

            # display the pause/resume label
            self.display_pause_resume()

            # set up bomb count
            Game.window.blit(self.create_text("x " + str(MainGame.my_bomb_count), WHITE, 45), (100, 640))
            Game.window.blit(self.create_text("'s' to switch ", GREY, 10), (100, 685))

            # show the label of the current weapon
            self.display_current_weapon()

            # delete all dead (live = False) sprites
            self.delete_dead_sprites()

            pygame.display.flip()  # Make the window updated


    def get_event(self):
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.detect_mouse_hover(self.pause_or_resume_rect):
                    if not MainGame.pause:
                        pygame.mixer.pause()
                        pygame.mixer.music.pause()
                        MainGame.pause = True

                    elif MainGame.pause:
                        pygame.mixer.unpause()
                        pygame.mixer.music.unpause()
                        MainGame.pause = False

            # Enable my plane to shoot
            if event.type == pygame.KEYDOWN:

                if not MainGame.pause:
                    if event.key == pygame.K_SPACE:

                        # the number of bullets on screen <= 8 and the player chooses to shoot bullet
                        if len(MainGame.my_weapon_list) < 8 and MainGame.my_plane.weapon_is_bullet:
                            my_bullet = MyWeapon("my_bullet", MainGame.my_plane)
                            MainGame.my_weapon_list.append(my_bullet)
                            MainGame.bullet_warning = False
                            MainGame.bomb_warning = False

                            Game.my_bullet_sound.play()


                        # the number of bullets on screen > 8 and the player chooses to shoot bullet
                        elif len(MainGame.my_weapon_list) >= 8 and MainGame.my_plane.weapon_is_bullet:
                            MainGame.bullet_warning = True
                            MainGame.bomb_warning = False

                        # there is available bomb and the player chooses to fire the bomb
                        elif MainGame.my_bomb_count >= 1 and not MainGame.my_plane.weapon_is_bullet:
                            my_bomb = MyWeapon("bomb", MainGame.my_plane)
                            MainGame.my_weapon_list.append(my_bomb)
                            MainGame.my_bomb_count -= 1
                            MainGame.bullet_warning = False
                            MainGame.bomb_warning = False

                            Game.fire_bomb_sound.play()

                        # there is no available bomb and the player chooses to fire the bomb
                        elif MainGame.my_bomb_count < 1 and not MainGame.my_plane.weapon_is_bullet:
                            MainGame.bomb_warning = True
                            MainGame.bullet_warning = False

                    if event.key == pygame.K_s:
                        MainGame.my_plane.weapon_is_bullet = not MainGame.my_plane.weapon_is_bullet

        # Move my plane with the keyboard
        key_input = pygame.key.get_pressed()
        if not MainGame.pause:
            if key_input[pygame.K_UP]:
                MainGame.my_plane.direction = "UP"
                MainGame.my_plane.move()
            if key_input[pygame.K_DOWN]:
                MainGame.my_plane.direction = "DOWN"
                MainGame.my_plane.move()
            if key_input[pygame.K_LEFT]:
                MainGame.my_plane.direction = "LEFT"
                MainGame.my_plane.move()
            if key_input[pygame.K_RIGHT]:
                MainGame.my_plane.direction = "RIGHT"
                MainGame.my_plane.move()

    # delete all dead (live = False) sprites
    def delete_dead_sprites(self):
        sprite_list = [MainGame.my_weapon_list, MainGame.enemy_plane_list, MainGame.enemy3_bullet_list,
                       MainGame.supply_list, MainGame.explode_list]
        for sprite_group in sprite_list:
            for sprite in sprite_group:
                if not sprite.live:
                    sprite_group.remove(sprite)

    # Add text
    def create_text(self, text, color, size):
        pygame.font.init()
        font = pygame.font.Font('fonts/zorque.otf', size)
        text_surface = font.render(text, True, color)
        return text_surface

    def display_bomb_label(self):
        bomb_img = pygame.image.load("imgs/bomb_label.png")
        Game.window.blit(bomb_img, (20, 640))

    def display_warning(self):
        if MainGame.bullet_warning:
            Game.window.blit(self.create_text("MAX 8 BULLETS AT ONCE!", RED, 15), (10, 40))
        elif MainGame.bomb_warning:
            Game.window.blit(self.create_text("No AVAILABLE BOMB!", RED, 15), (10, 40))

    def display_heart(self):

        if MainGame.my_heart_count > 0:
            if MainGame.my_heart_count >= 3:  # the maximum amount of heart is 3
                MainGame.my_heart_count = 3
            dead_heart = pygame.image.load("imgs/dead_heart.png")
            alive_heart = pygame.image.load("imgs/heart.png")
            count = 0
            for i in range(3 - MainGame.my_heart_count):
                count += 1
                Game.window.blit(dead_heart, (280 + i * 60, 640))
            while count < 3:
                Game.window.blit(alive_heart, (280 + count * 60, 640))
                count += 1
        else:
            pygame.mixer.music.stop()
            GameOver().show_bg()

    def display_my_weapon(self):
        for my_weapon in MainGame.my_weapon_list:
            if my_weapon.type == "my_bullet":
                my_weapon.my_bullet_hit_enemy_plane()
            elif my_weapon.type == "bomb":
                my_weapon.fire_bomb()
            my_weapon.display_weapon()
            if not MainGame.pause:
                my_weapon.move()

    def create_enemy_plane(self):
        type_list = ["enemy1"] * 5 + ["enemy2"] * 2 + ["enemy3"]
        selected_type = random.choice(type_list)

        speed = random.randint(3, 6)

        if selected_type == "enemy1":
            image1 = pygame.image.load("imgs/enemy1.png")
            left = random.randint(0, SCREEN_WIDTH - image1.get_width())
            enemy = EnemyPlane(left, "enemy1", 1, speed)
            MainGame.enemy_plane_list.append(enemy)


        elif selected_type == "enemy2":
            image2 = pygame.image.load("imgs/enemy2.png")
            left = random.randint(0, SCREEN_WIDTH - image2.get_width())
            enemy = EnemyPlane(left, "enemy2", 2, speed)
            MainGame.enemy_plane_list.append(enemy)


        elif selected_type == "enemy3":
            image3 = pygame.image.load("imgs/enemy3.png")
            left = random.randint(0, SCREEN_WIDTH - image3.get_width())
            enemy = EnemyPlane(left, "enemy3", 2, speed)
            MainGame.enemy_plane_list.append(enemy)

    def display_enemy_plane(self):
        for enemy_plane in MainGame.enemy_plane_list:
            enemy_plane.enemy_plane_hit_my_plane()
            enemy_plane.display_plane()
            if not MainGame.pause:
                enemy_plane.move()

                if enemy_plane.type == "enemy3":
                    # shoot the bullet
                    enemy_bullet = enemy_plane.shot()
                    # if enemy_bullet is not none, append it to this enemy_plane's bullet list
                    if enemy_bullet:
                        MainGame.enemy3_bullet_list.append(enemy_bullet)

    def display_enemy_bullet(self):
        for enemy_bullet in MainGame.enemy3_bullet_list:
            enemy_bullet.enemy_bullet_hit_my_plane()
            enemy_bullet.display_bullet()
            if not MainGame.pause:
                enemy_bullet.move()

    def create_supply(self):
        if MainGame.my_heart_count >= 3:
            selected_type = "bomb"
        else:
            type_list = ["bomb", "heart"]
            selected_type = random.choice(type_list)

        if selected_type == "bomb":
            image1 = pygame.image.load("imgs/bomb_supply.png")
            left = random.randint(0, SCREEN_WIDTH - image1.get_width())
            supply = Supply(left, "bomb")
            MainGame.supply_list.append(supply)

        elif selected_type == "heart":
            image2 = pygame.image.load("imgs/heart_supply.png")
            left = random.randint(0, SCREEN_WIDTH - image2.get_width())
            supply = Supply(left, "heart")
            MainGame.supply_list.append(supply)

    def display_supply(self):
        for supply in MainGame.supply_list:
            supply.supply_hit_my_plane()
            supply.display_supply()
            if not MainGame.pause:
                supply.move()

    def display_explosion(self):
        for explode in MainGame.explode_list:
            explode.display_explosion()

    # show the label of the current weapon:
    def display_current_weapon(self):
        if MainGame.my_plane.weapon_is_bullet:
            Game.current_weapon_img = pygame.image.load("imgs/my_bullet.png")
            Game.window.blit(Game.current_weapon_img, (10, 60))
        elif not MainGame.my_plane.weapon_is_bullet:
            Game.current_weapon_img = pygame.image.load("imgs/bomb_label_small.png")
            Game.window.blit(Game.current_weapon_img, (5, 60))

    def display_pause_resume(self):
        image_rect = pygame.image.load("imgs/pause_no.png").get_rect()
        image_rect.left = 400
        image_rect.top = 10
        if not MainGame.pause:
            if self.detect_mouse_hover(image_rect):
                image = pygame.image.load("imgs/pause_hover.png")
            else:
                image = pygame.image.load("imgs/pause_no.png")
        elif MainGame.pause:
            if self.detect_mouse_hover(image_rect):
                image = pygame.image.load("imgs/resume_hover.png")
            else:
                image = pygame.image.load("imgs/resume_no.png")

        Game.window.blit(image, (image_rect.left, image_rect.top))

    def detect_mouse_hover(self, label_rect):
        return label_rect.collidepoint(pygame.mouse.get_pos())


class GameOver:
    exit_hover_once = False
    replay_hover_once = False

    def __init__(self):
        self.bg = ScrollBG(2)
        self.button_exit = MenuButtons("Exit", 25, BLACK, BLACK, 3, 25, 600)
        self.button_exit_hover = MenuButtons("Exit", 30, WHITE, GREY, 0, 25, 600)
        self.button_replay = MenuButtons("Replay", 25, BLACK, BLACK, 3, 255, 600)
        self.button_replay_hover = MenuButtons("Replay", 30, WHITE, GREY, 0, 255, 600)
        self.update()


    def show_bg(self):

        pygame.display.set_caption("Aircraft War Game Over")

        while True:
            self.bg.render()
            self.bg.scroll()
            Game.window.blit(self.create_text("Game Over", 'fonts/zorque.otf', 72, BLACK),
                             (25, 100))
            Game.window.blit(self.create_text("Game Over", 'fonts/zorque.otf', 72, GREY),
                             (30, 105))

            self.show_best_score()
            self.show_player_score()
            self.check_button_hover()
            self.get_event()
            pygame.display.update()  # Make the window updated

    def get_score(self):
        with open('best_score.txt', 'r') as f:
            return f.readline()



    def get_event(self):
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_exit.detect_mouse_hover():
                    exit()
                elif self.button_replay.detect_mouse_hover():
                    Game.button_pressed_sound.play()
                    pygame.time.wait(100)
                    self.reset()
                    MainGame().start_game()

    # Add the unchanging text
    def create_text(self, text, font, size, color):
        pygame.font.init()
        font = pygame.font.Font(font, size)
        text_surface = font.render(text, True, color)
        return text_surface

    # Add score
    def show_best_score(self):
        pygame.font.init()
        font = pygame.font.Font('fonts/ghostclan.ttf', 50)
        text_surface = font.render("Best:  " + self.get_score(), True, YELLOW)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, (SCREEN_HEIGHT - 100) / 2))
        Game.window.blit(text_surface, text_rect)

    # Show the player's score
    def show_player_score(self):
        pygame.font.init()
        font = pygame.font.Font('fonts/ghostclan.ttf', 40)
        if MainGame.score > int(self.get_score()):
            text_surface = font.render("Your Score:  " + str(MainGame.score), True, YELLOW)

        else:
            text_surface = font.render("Your Score:  " + str(MainGame.score), True, WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, (SCREEN_HEIGHT + 100) / 2))
        Game.window.blit(text_surface, text_rect)

    # Check if the mouse is hovering over the button
    def check_button_hover(self):

        if self.button_exit.detect_mouse_hover():
            self.button_exit_hover.button_text()
            if not BestScore.return_hover_once:
                Game.button_hover_sound.play()
                BestScore.return_hover_once = True
        else:
            self.button_exit.button_text()
            BestScore.return_hover_once = False

        if self.button_replay.detect_mouse_hover():
            self.button_replay_hover.button_text()
            if not BestScore.start_hover_once:
                Game.button_hover_sound.play()
                BestScore.start_hover_once = True
        else:
            self.button_replay.button_text()
            BestScore.start_hover_once = False

    # update the best score:
    def update(self):
        if MainGame.score > int(self.get_score()):
            Game.hit_record_sound.play()
            with open('best_score.txt', 'w') as f:
                f.write(str(MainGame.score))
        else:
            Game.not_hit_record_sound.play()

    # Reset variables to replay the game
    def reset(self):
        MainGame.my_plane = None
        MainGame.score = 0
        MainGame.my_bomb_count = 0
        MainGame.my_heart_count = 3
        MainGame.enemy_plane_list = []

        MainGame.my_weapon_list = []
        MainGame.enemy3_bullet_list = []

        MainGame.supply_list = []

        MainGame.explode_list = []

        MainGame. ullet_warning = False
        MainGame.bomb_warning = False

        MainGame.current_weapon_img = None

        MainGame.pause = False

class MyPlane(BaseItem):

    def __init__(self, left, top):
        self.images = [
            pygame.image.load("imgs/my_plane1.png"),
            pygame.image.load("imgs/my_plane2.png")
        ]

        self.image = self.images[0]

        self.rect = self.images[0].get_rect()
        # The moving direction of my plane
        self.direction = "UP"
        # set up the left and top
        self.rect.left = left - self.images[0].get_width() / 2  # locate my plane in the center
        self.rect.top = top - self.images[0].get_height()
        # The speed of my plane
        self.speed = 10
        # life
        self.life = 3

        self.weapon_is_bullet = True

        self.type = "my_plane"

        self.anim1 = True

    def move(self):
        # determine the direction of my plane to move

        if self.direction == "UP":
            if self.rect.top >= 0:
                self.rect.top -= self.speed
        elif self.direction == "DOWN":
            if self.rect.top + self.image.get_height() < 640:
                self.rect.top += self.speed
        elif self.direction == "LEFT":
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == "RIGHT":
            if self.rect.left + self.image.get_width() < SCREEN_WIDTH:
                self.rect.left += self.speed

    def display_plane(self):
        if self.anim1:
            self.image = self.images[0]
            if not MainGame.pause:
                self.anim1 = False
            Game.window.blit(self.image, self.rect)

        else:
            self.image = self.images[1]
            if not MainGame.pause:
                self.anim1 = True
            Game.window.blit(self.image, self.rect)


class EnemyPlane(BaseItem):

    def __init__(self, left, type, life, speed):
        self.type = type
        self.image = pygame.image.load("imgs/" + self.type + ".png")
        self.rect = self.image.get_rect()

        # set up the left and top
        self.rect.left = left
        self.rect.top = 0 - self.rect.height
        # The speed of enemy plane
        self.speed = speed

        # life
        self.life = life

        self.live = True

    def move(self):
        if self.rect.top <= SCREEN_HEIGHT:
            self.rect.top += self.speed
        else:
            self.live = False

    def display_plane(self):
        if self.type == "enemy2" or self.type == "enemy3":
            if self.life == 2:
                pygame.draw.rect(Game.window, RED, pygame.Rect(self.rect.left, self.rect.top - 5, self.rect.width, 5))
                pygame.draw.rect(Game.window, BLACK, pygame.Rect(self.rect.left, self.rect.top - 5, self.rect.width, 5),
                                 1)
            elif self.life == 1:
                if self.type == "enemy2":
                    self.image = pygame.image.load("imgs/enemy2_explode1.png")
                elif self.type == "enemy3":
                    self.image = pygame.image.load("imgs/enemy3_explode1.png")
                pygame.draw.rect(Game.window, RED,
                                 pygame.Rect(self.rect.left, self.rect.top - 5, self.rect.width / 2, 5))
                pygame.draw.rect(Game.window, WHITE,
                                 pygame.Rect(self.rect.left + self.rect.width / 2, self.rect.top - 5,
                                             self.rect.width / 2, 5))
                pygame.draw.rect(Game.window, BLACK, pygame.Rect(self.rect.left, self.rect.top - 5, self.rect.width, 5),
                                 1)
        Game.window.blit(self.image, self.rect)

    def shot(self):
        num = random.randint(1, 1000)
        if num < 20:
            return EnemyBullet(self)

    def enemy_plane_hit_my_plane(self):
        if pygame.sprite.collide_mask(self, MainGame.my_plane):
            MainGame.my_heart_count -= 1

            enemy_plane_explode = Explode(self)
            my_plane_explode = Explode(MainGame.my_plane)
            MainGame.explode_list.append(enemy_plane_explode)
            MainGame.explode_list.append(my_plane_explode)
            self.live = False
            MainGame.my_plane = MyPlane(SCREEN_WIDTH / 2, 640)

            if MainGame.my_heart_count >=1:
                Game.lose_heart_sound.play()


class MyWeapon(BaseItem):
    def __init__(self, type, plane):
        self.plane = plane
        self.type = type

        self.image = pygame.image.load("imgs/" + type + ".png")
        self.rect = self.image.get_rect()

        # Set up the initial position of my bullet
        self.rect.left = plane.rect.left + plane.rect.width / 2 - self.rect.width / 2
        self.rect.top = plane.rect.top - self.rect.height

        if self.type == "my_bullet":
            self.speed = 6

        elif self.type == "bomb":
            self.speed = 15

        self.live = True

    def move(self):
        if self.rect.top + self.rect.height > 0:
            self.rect.top -= self.speed
        else:
            self.live = False

    def display_weapon(self):
        Game.window.blit(self.image, self.rect)

    def my_bullet_hit_enemy_plane(self):
        for enemy_plane in MainGame.enemy_plane_list:
            if pygame.sprite.collide_mask(enemy_plane, self):
                if enemy_plane.life == 1:
                    self.live = False
                    enemy_plane.live = False
                    explode = Explode(enemy_plane)
                    MainGame.explode_list.append(explode)
                    if enemy_plane.type == "enemy1":
                        MainGame.score += 1
                        Game.enemy1_explode_sound.play()
                    else:
                        MainGame.score += 2
                        if enemy_plane.type == "enemy2":
                            Game.enemy2_explode_sound.play()
                        elif enemy_plane.type == "enemy3":
                            Game.enemy3_explode_sound.play()
                else:
                    self.live = False
                    enemy_plane.life -= 1

                    if enemy_plane.type == "enemy2":
                        Game.enemy2_explode_sound.play()
                    elif enemy_plane.type == "enemy3":
                        Game.enemy3_explode_sound.play()

    def fire_bomb(self):
        for enemy_plane in MainGame.enemy_plane_list:
            if enemy_plane.rect.top >= self.rect.top:
                enemy_plane.live = False
                explode = Explode(enemy_plane)
                MainGame.explode_list.append(explode)

                # add score based on enemy plane type
                if enemy_plane.type == "enemy1":
                    MainGame.score += 1
                elif enemy_plane.type == "enemy2":
                    MainGame.score += 2
        for supply in MainGame.supply_list:
            if supply.rect.top >= self.rect.top:
                supply.live = False
        for enemy3_bullet in MainGame.enemy3_bullet_list:
            if enemy3_bullet.rect.top >= self.rect.top:
                enemy3_bullet.live = False


class EnemyBullet(BaseItem):
    def __init__(self, plane):
        self.plane = plane

        self.image = pygame.image.load("imgs/enemy_bullet.png")
        self.rect = self.image.get_rect()
        # Set up the initial position of my bullet
        self.rect.left = plane.rect.left + plane.rect.width / 2 - self.rect.width / 2
        self.rect.top = plane.rect.top + plane.rect.height

        self.speed = 6

        self.live = True

    def move(self):
        if self.rect.top < SCREEN_HEIGHT:
            self.rect.top += self.speed
        else:
            self.live = False

    def display_bullet(self):
        Game.window.blit(self.image, self.rect)

    def enemy_bullet_hit_my_plane(self):
        if pygame.sprite.collide_mask(MainGame.my_plane, self):
            MainGame.my_heart_count -= 1
            explode = Explode(MainGame.my_plane)
            MainGame.explode_list.append(explode)
            self.live = False
            MainGame.my_plane = MyPlane(SCREEN_WIDTH / 2, 640)

            if MainGame.my_heart_count >= 1:
                Game.lose_heart_sound.play()


class Supply(BaseItem):
    def __init__(self, left, type):
        self.type = type
        self.image = pygame.image.load("imgs/" + self.type + "_supply.png")
        self.rect = self.image.get_rect()

        # set up the left and top
        self.rect.left = left
        self.rect.top = 0 - self.rect.height
        self.speed = 20

        self.live = True

    def move(self):
        if self.rect.top <= SCREEN_HEIGHT:
            self.rect.top += self.speed
        else:
            self.live = False

    def display_supply(self):
        Game.window.blit(self.image, self.rect)

    def supply_hit_my_plane(self):
        if pygame.sprite.collide_mask(self, MainGame.my_plane):
            if self.type == "bomb":
                MainGame.my_bomb_count += 1
                Game.get_bomb_sound.play()
            elif self.type == "heart":
                MainGame.my_heart_count += 1
                Game.get_heart_sound.play()
            self.live = False


class Explode:
    def __init__(self, plane):
        # The explosion position is determined by the current bullet hitting the plane position
        self.rect = plane.rect
        if plane.type == "enemy1":
            self.images = [
                pygame.image.load('imgs/enemy1_explode1.png'),
                pygame.image.load('imgs/enemy1_explode2.png'),
                pygame.image.load('imgs/enemy1_explode3.png'),
                pygame.image.load('imgs/enemy1_explode4.png')
            ]
        elif plane.type == "enemy2":
            self.images = [
                pygame.image.load('imgs/enemy2_explode2.png'),
                pygame.image.load('imgs/enemy2_explode3.png'),
                pygame.image.load('imgs/enemy2_explode4.png')
            ]
        elif plane.type == "enemy3":
            self.images = [
                pygame.image.load('imgs/enemy3_explode2.png'),
                pygame.image.load('imgs/enemy3_explode3.png'),
                pygame.image.load('imgs/enemy3_explode4.png'),
                pygame.image.load('imgs/enemy3_explode5.png'),
                pygame.image.load('imgs/enemy3_explode6.png')
            ]
        elif plane.type == "my_plane":
            self.images = [
                pygame.image.load('imgs/my_plane_explode1.png'),
                pygame.image.load('imgs/my_plane_explode2.png'),
                pygame.image.load('imgs/my_plane_explode3.png'),
                pygame.image.load('imgs/my_plane_explode4.png')

            ]
        self.step = 0
        self.image = self.images[self.step]
        self.live = True

    def display_explosion(self):
        if self.step < len(self.images):
            self.image = self.images[self.step]
            if not MainGame.pause:
                self.step += 1

            Game.window.blit(self.image, self.rect)
        else:
            self.live = False


if __name__ == "__main__":
    Game().create_game()
    Menu().create_menu()
