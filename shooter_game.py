import pygame
from pygame import *
from random import randint
import sys

pygame.init()
mixer.init()

try:
    mixer.music.load('space.ogg')
    mixer.music.play(-1) 
    fire_sound = mixer.Sound('fire.ogg')
except pygame.error as e:
    print(f"Ошибка загрузки звука: {e}")

img_back = "galaxy.jpg"
img_hero = "cocoa.png"
img_enemy = "komarik.png"
img_bullet = "bananchik.png"

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(pygame.image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.is_invincible = False

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx - 10, self.rect.top, 20, 20, 15)
        bullets.add(bullet)
        fire_sound.play()


class Enemy(GameSprite):
    def update(self):
        global missed
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = -50
            self.rect.x = randint(0, win_width - 50)
            missed += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


win_width = 700
win_height = 500
display.set_caption("Отрази вторжение солевых попрыгунов!")
window = display.set_mode((win_width, win_height))

try:
    background = transform.scale(pygame.image.load(img_back), (win_width, win_height))
except pygame.error as e:
    print(f"Ошибка загрузки фона: {e}")
    background = pygame.Surface((win_width, win_height))
    background.fill((0, 0, 0))  

player = Player(img_hero, win_width / 2 - 40, win_height - 100, 80, 100, 5)

enemies = sprite.Group()
for _ in range(5):
    enemy = Enemy(img_enemy, randint(0, win_width - 50), -50, 50, 50, randint(2, 4))
    enemies.add(enemy)

bullets = sprite.Group()

font.init()
font1 = font.SysFont("Arial", 36)

missed = 0
killed = 0

def show_stats():
    text1 = font1.render(f"Сбито: {killed}", True, (255, 255, 255))
    text2 = font1.render(f"Пропущено: {missed}", True, (255, 255, 255))
    window.blit(text1, (10, 10))
    window.blit(text2, (10, 50))

def show_result(message):
    window.blit(background, (0, 0))
    text = font1.render(message, True, (255, 255, 255))
    window.blit(text,
                (win_width / 2 - text.get_width() / 2,
                 win_height / 2 - text.get_height() / 2))
    display.update()
    pygame.time.wait(2000)

try:
    clock = pygame.time.Clock()
    run = True

    while run:
        for e in pygame.event.get():
            if e.type == QUIT:
                run = False
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    player.fire()

        window.blit(background, (0, 0))
        player.update()
        player.reset()

        enemies.update()
        enemies.draw(window)

        bullets.update()
        bullets.draw(window)

        for bullet in bullets:
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    bullet.kill()
                    enemy.rect.y = -50
                    enemy.rect.x = randint(0, win_width - 50)
                    killed += 1

        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                show_result("Вас съел комару!")
                run = False

        if missed >= 5:
            show_result("Вы были захвачены солевым попрыгуном!")
            run = False
        elif killed >= 10:
            show_result("Вы выжили! Вы отразили атаку.")
            run = False

        show_stats()

        display.update()
        clock.tick(60)

except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    mixer.music.stop()
    mixer.quit()
    pygame.display.quit()
    pygame.font.quit()
    pygame.quit()
    sys.exit()
