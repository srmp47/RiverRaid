import pygame
import random
from pygame import (K_DOWN, K_LEFT, K_RIGHT, K_UP, K_SPACE, K_TAB, K_r, K_c)

pygame.init()
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
all_objects = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bombs = pygame.sprite.Group()
sparrows = pygame.sprite.Group()
destroying_sparrows = pygame.sprite.Group()


class Plane(pygame.sprite.Sprite):
    def __init__(self):
        super(Plane, self).__init__()
        self.surf = pygame.image.load("images/blue_plane.png")
        self.rect = self.surf.get_rect()
        self.speed = 50
        self.number_of_change_image = 10
        self.is_destroying = False
        all_objects.add(self)
        self.is_rocket = False

    def move(self, key_pressed):
        if not self.is_rocket and not self.is_destroying:
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
        elif self.is_rocket and not self.is_destroying:
            self.rect.move_ip(self.speed, 0)
            if self.rect.left > SCREEN_WIDTH:
                self.surf = pygame.image.load("images/blue_plane.png")
                self.rect.x = SCREEN_WIDTH / 4
                self.rect.y = SCREEN_HEIGHT / 2
                self.is_rocket = False

    def destroy(self):
        self.is_destroying = True
        self.number_of_change_image = 10

    def chang_image(self):
        if self.number_of_change_image == 1:
            self.surf = pygame.image.load("images/blue_plane.png")
            self.rect.x = SCREEN_WIDTH / 4
            self.rect.y = SCREEN_HEIGHT / 2
            self.is_destroying = False
            self.is_rocket = False
        else:
            self.number_of_change_image -= 1
            self.surf = pygame.image.load(f"images/destroy_rocket{self.number_of_change_image}.png")


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
        self.x_speed = 20
        self.y_speed = 0
        self.x_acceleration = 1
        self.y_acceleration = 2
        self.rect = self.surf.get_rect()
        all_objects.add(self)
        bombs.add(self)

    def move(self):
        self.rect.move_ip(self.x_speed, self.y_speed)
        self.x_speed += self.x_acceleration
        self.y_speed += self.y_acceleration
        if self.rect.left > SCREEN_WIDTH:
            self.kill()


class Sparrow(pygame.sprite.Sprite):
    def __init__(self, color):
        super(Sparrow, self).__init__()
        self.color = color
        self.surf = pygame.image.load(f"images/MiniBossFly/{self.color}/1.png")
        self.rect = self.surf.get_rect()
        self.speed = 8
        self.image_number = 0
        self.image_number_of_destroying = 0
        self.is_destroying = False
        sparrows.add(self)
        all_objects.add(self)

    def move(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

    def change_image(self):
        if not self.is_destroying:
            self.image_number += 1
            if self.image_number > 4:
                self.image_number = 1
            self.surf = pygame.image.load(f"images/MiniBossFly/{self.color}/{self.image_number}.png")
        else:
            self.image_number_of_destroying += 1
            if self.image_number_of_destroying == 7:
                self.kill()
            else:
                self.surf = pygame.image.load(
                    f"images/destroy_{self.color}_sparrow{self.image_number_of_destroying}.png")

    def destroy(self):
        self.is_destroying = True
        sparrows.remove(self)
        destroying_sparrows.add(self)


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
    CREATESPARROW = pygame.USEREVENT + 4
    CHANGEIMAGEOFSPARROW = pygame.USEREVENT + 5
    CHANGEIMAGEOFSTROYINGSPARROW = pygame.USEREVENT + 6
    CHANGEIMAGEOFSTROYINGSPLANE = pygame.USEREVENT + 7
    pygame.time.set_timer(CUPHEADSHOOT, 120)
    pygame.time.set_timer(SHOOTBULLETANDBOMB, 120)
    pygame.time.set_timer(CONVERTTOROCKET, 130)
    pygame.time.set_timer(CREATESPARROW, 10000)
    pygame.time.set_timer(CHANGEIMAGEOFSPARROW, 300)
    pygame.time.set_timer(CHANGEIMAGEOFSTROYINGSPARROW, 100)
    pygame.time.set_timer(CHANGEIMAGEOFSTROYINGSPLANE, 180)
    background = pygame.image.load("images/sky.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
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
    # clock = pygame.time.Clock()
    # pygame.display.flip()
    # clock.tick(60)
    while running:
        screen.blit(background, (0, 0))
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
                if 1 <= number_of_converting_to_rocket <= 5:
                    image_of_converting_to_rocket = pygame.image.load(
                        f"images/convert_to_rocket{number_of_converting_to_rocket}.png")
                    plane.surf = pygame.image.load(f"images/rocket{number_of_converting_to_rocket}.png")
                elif 5 < number_of_converting_to_rocket <= 10:
                    plane.surf = pygame.image.load(f"images/rocket{number_of_converting_to_rocket}.png")
                else:
                    number_of_converting_to_rocket = 1
                    is_converting_to_rocket = False
                    plane.is_rocket = True
            elif event.type == CREATESPARROW:
                sparrow1 = Sparrow("yellow")
                sparrow2 = Sparrow("purple")
                sparrow3 = Sparrow("yellow")
                sparrow4 = Sparrow("purple")
                y = random.randint(sparrow1.rect.height, SCREEN_HEIGHT - sparrow1.rect.height)
                sparrow1.rect.x = SCREEN_WIDTH + sparrow1.rect.width
                sparrow1.rect.y = y
                sparrow2.rect.x = SCREEN_WIDTH + 2 * sparrow1.rect.width + 40
                sparrow2.rect.y = y
                sparrow3.rect.x = SCREEN_WIDTH + 3 * sparrow1.rect.width + 80
                sparrow3.rect.y = y
                sparrow4.rect.x = SCREEN_WIDTH + 4 * sparrow1.rect.width + 120
                sparrow4.rect.y = y
            elif event.type == CHANGEIMAGEOFSPARROW:
                for sparrow in sparrows:
                    sparrow.change_image()
            elif event.type == CHANGEIMAGEOFSTROYINGSPARROW:
                for sparrow in destroying_sparrows:
                    sparrow.change_image()
            elif event.type == CHANGEIMAGEOFSTROYINGSPLANE and plane.is_destroying:
                plane.chang_image()

        if not key_pressed[K_SPACE]:
            is_shooting = False
        if key_pressed[K_c]:
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
            hit_sparrows = pygame.sprite.spritecollide(bullet, sparrows, False)
            for sparrow in hit_sparrows:
                sparrow.destroy()
                bullet.kill()
                break
        for bomb in bombs:
            bomb.move()
            bomb.move()
            hit_sparrows = pygame.sprite.spritecollide(bomb, sparrows, False)
            for sparrow in hit_sparrows:
                sparrow.destroy()
                bomb.kill()
                break
        for sparrow in sparrows:
            sparrow.move()
        plane.move(key_pressed)
        if plane.is_rocket:
            hit_objects = pygame.sprite.spritecollide(plane, all_objects, False)
            for object in hit_objects:
                if not isinstance(object, Plane):
                    plane.destroy()
                    if isinstance(object, Sparrow):
                        for sparrow in sparrows:
                            sparrow.destroy()
                    break

        all_objects.update()
        if is_shooting:
            screen.blit(image_of_shooting,
                        (plane.rect.x + plane.rect.width * 4 / 5 + 4, plane.rect.y + plane.rect.height / 3))
        pygame.display.flip()

    pygame.quit()


run_game()
