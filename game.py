import pygame
from pygame import (K_DOWN, K_LEFT, K_ESCAPE, K_RIGHT, K_UP, K_SPACE)

pygame.init()
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
all_objects = pygame.sprite.Group()
bullets = pygame.sprite.Group()


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
    SHOOTBULLET = pygame.USEREVENT + 2
    pygame.time.set_timer(CUPHEADSHOOT, 120)
    pygame.time.set_timer(SHOOTBULLET, 120)
    background = pygame.image.load("images/sky.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    clouds = pygame.image.load("images/clouds.png")
    clouds = pygame.transform.scale(clouds, (SCREEN_WIDTH, SCREEN_HEIGHT))
    clouds2 = pygame.image.load("images/clouds2.png")
    clouds2 = pygame.transform.scale(clouds2, (SCREEN_WIDTH, SCREEN_HEIGHT))
    mountains = pygame.image.load("images/mountain.png")
    mountains = pygame.transform.scale(mountains, (SCREEN_WIDTH + 1000, SCREEN_HEIGHT))
    running = True
    x = 1
    image_of_shooting = pygame.image.load(f"images/CupheadShoot/{x}.png")
    is_shooting = False
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
                image_of_shooting = pygame.image.load(f"images/CupheadShoot/{x}.png")
                x += 1
                if x == 5:
                    x = 1
            elif event.type == SHOOTBULLET and key_pressed[K_SPACE]:
                is_shooting = True
                bullet = Bullet()
                bullet.rect.x = plane.rect.x + plane.rect.width * 4 / 5 + 4
                bullet.rect.y = plane.rect.y + plane.rect.height / 3 + 17
        if not key_pressed[K_SPACE]:
            is_shooting = False
        for object in all_objects:
            screen.blit(object.surf, object.rect)
        for bullet in bullets:
            bullet.move()
        plane.move(key_pressed)
        all_objects.update()
        if is_shooting:
            screen.blit(image_of_shooting,
                        (plane.rect.x + plane.rect.width * 4 / 5 + 4, plane.rect.y + plane.rect.height / 3))
        pygame.display.flip()

    pygame.quit()


run_game()
