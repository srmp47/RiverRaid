import pygame
from pygame import (K_DOWN, K_LEFT, K_RIGHT, K_UP, K_SPACE, K_TAB, K_r)

pygame.init()
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
all_objects = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bombs = pygame.sprite.Group()


class Plane(pygame.sprite.Sprite):
    def __init__(self):
        super(Plane, self).__init__()
        self.surf = pygame.image.load("images/blue_plane.png")
        self.rect = self.surf.get_rect()
        self.speed = 50
        all_objects.add(self)

    def move(self, key_pressed):
        if key_pressed[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if key_pressed[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if key_pressed[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if key_pressed[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = SCREEN_HEIGHT
        if self.rect.bottom < 0:
            self.rect.bottom = 0


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Bullet, self).__init__()
        self.surf = pygame.image.load("images/bullet.png")
        self.rect = self.surf.get_rect()
        self.speed = 35
        all_objects.add(self)
        bullets.add(self)

    def move(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()


class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        super(Bomb, self).__init__()
        bomb_image = pygame.image.load("images/bomb.png")
        bomb_image = pygame.transform.scale(bomb_image, (40, 40))
        self.surf = bomb_image
        self.x_speed = 35
        self.y_speed = 0
        self.x_acceleration = 2
        self.y_acceleration = 4
        self.rect = self.surf.get_rect()
        all_objects.add(self)
        bombs.add(self)

    def move(self):
        self.rect.move_ip(self.x_speed, self.y_speed)
        self.x_speed += self.x_acceleration
        self.y_speed += self.y_acceleration
        if self.rect.left > SCREEN_WIDTH:
            self.kill()


# class Bird(pygame.sprite.Sprite):
#     def __init__(self):
#         super(Bird, self).__init__()
#         self.num = 1
#         self.surf = pygame.image.load(f"{self.num}.png")
#         self.rect = self.surf.get_rect()
#     def  update(self):
#         self.num += 1
#         if self.num == 7:
#             self.num = 1
#         self.surf = pygame.image.load(f"{self.num}.png")
#     def shoot(self):


def run_game():
    plane = Plane()
    CUPHEADSHOOT = pygame.USEREVENT + 1
    SHOOTBULLETANDBOMB = pygame.USEREVENT + 2
    CONVERTTOROCKET = pygame.USEREVENT + 3
    pygame.time.set_timer(CUPHEADSHOOT, 120)
    pygame.time.set_timer(SHOOTBULLETANDBOMB, 120)
    pygame.time.set_timer(CONVERTTOROCKET, 130)
    background = pygame.image.load("images/sky.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    clouds = pygame.image.load("images/clouds.png")
    clouds = pygame.transform.scale(clouds, (SCREEN_WIDTH, SCREEN_HEIGHT))
    clouds2 = pygame.image.load("images/clouds2.png")
    clouds2 = pygame.transform.scale(clouds2, (SCREEN_WIDTH, SCREEN_HEIGHT))
    mountains = pygame.image.load("images/mountain.png")
    mountains = pygame.transform.scale(mountains, (SCREEN_WIDTH + 1000, SCREEN_HEIGHT))
    running = True
    number_of_shooting = 1
    image_of_shooting = pygame.image.load(f"images/CupheadShoot/{number_of_shooting}.png")
    number_of_converting_to_rocket = 1
    image_of_converting_to_rocket = pygame.image.load(f"images/convert_to_rocket{number_of_converting_to_rocket}.png")
    is_shooting = False
    is_converting_to_rocket = False
    mode = "bullet"
    clock = pygame.time.Clock()
    pygame.display.flip()
    clock.tick(30)
    while running:
        screen.blit(background, (0, 0))
        screen.blit(clouds, (0, 0))
        screen.blit(clouds2, (0, 0))
        screen.blit(mountains, (0, 0))
        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            elif event.type == CUPHEADSHOOT and is_shooting:
                image_of_shooting = pygame.image.load(f"images/CupheadShoot/{number_of_shooting}.png")
                number_of_shooting += 1
                if number_of_shooting == 5:
                    number_of_shooting = 1
            elif event.type == SHOOTBULLETANDBOMB and key_pressed[K_SPACE]:
                is_shooting = True
                if mode == "bullet":
                    bullet = Bullet()
                    bullet.rect.x = plane.rect.x + plane.rect.width * 4 / 5 + 4
                    bullet.rect.y = plane.rect.y + plane.rect.height / 3 + 17
                elif mode == "bomb":
                    bomb = Bomb()
                    bomb.rect.x = plane.rect.x + plane.rect.width * 4 / 5 + 4
                    bomb.rect.y = plane.rect.y + plane.rect.height / 3 + 17
            elif event.type == CONVERTTOROCKET and is_converting_to_rocket:
                number_of_converting_to_rocket += 1
                if number_of_converting_to_rocket != 6:
                    image_of_converting_to_rocket = pygame.image.load(f"images/convert_to_rocket{number_of_converting_to_rocket}.png")
                else:
                    number_of_converting_to_rocket = 1
                    is_converting_to_rocket = False

        if not key_pressed[K_SPACE]:
            is_shooting = False
        if key_pressed[K_TAB]:
            if mode == "bullet":
                mode = "bomb"
            else:
                mode = "bullet"
        if key_pressed[K_r] and not is_converting_to_rocket:
            is_converting_to_rocket = True
        for object in all_objects:
            screen.blit(object.surf, object.rect)
        if is_converting_to_rocket:
            screen.blit(image_of_converting_to_rocket,
                        (plane.rect.x - plane.rect.width / 2, plane.rect.y - plane.rect.height / 2))
        for bullet in bullets:
            bullet.move()
        for bomb in bombs:
            bomb.move()
        plane.move(key_pressed)
        all_objects.update()
        if is_shooting:
            screen.blit(image_of_shooting,
                        (plane.rect.x + plane.rect.width * 4 / 5 + 4, plane.rect.y + plane.rect.height / 3))
        pygame.display.flip()

    pygame.quit()


run_game()
