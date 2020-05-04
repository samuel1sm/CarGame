import os
import pygame
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
import random
from GameObjects import Car, Wall
import math


def rotate(origin, point, angle):
    value_ang = angle if angle < 0 else angle

    value = (5, 0) if (value_ang % 360 >= 260 and value_ang % 360 < 360) else (5, 0) if (
            value_ang % 360 >= 0 and value_ang % 360 < 25) else (0, 0)

    ox, oy = origin
    px, py = (point[0] - value[0], point[1] - value[1])

    angle = radians(angle)

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) * -1 + math.cos(angle) * (py - oy) * -1
    return qx, qy

    # rotate and blit the image

    # draw rectangle around the image
    # pygame.draw.rect(surf, (255, 0, 0), (*origin, *rotated_image.get_size()), 2)


def make_recs(screen, car, cords, color):
    circle_rotate_position = rotate(car.position_absolute,
                                    cords, car.angle)

    rec = pygame.Rect((int(circle_rotate_position[0]), int(circle_rotate_position[1])), (10, 10))

    return rec

    # pygame.draw.rect(screen, color, rec)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car tutorial")
        width = 1280
        height = 720
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "imgs/carro_feio.png")
        car_image = pygame.image.load(image_path)
        # car_image = pygame.Surface((128, 64))

        pos = (0, 0)

        car = Car(pos, car_image=car_image)

        walls = []
        walls.append(Wall((600, 600), (128, 64)))
        walls.append(Wall((500, 500), (50, 50)))
        walls.append(Wall((100, 100), (50, 50)))

        w, h = car_image.get_size()

        while not self.exit:
            self.screen.fill((0, 0, 0))

            dt = self.clock.get_time() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            pressed = pygame.key.get_pressed()

            if car.activated:
                car.blitRotate( (w // 2, h // 2))

                car.change_angle(pressed, dt)

                for rec in car.front_recs:
                    for wall in walls:
                        if rec.colliderect(wall):
                            car.deactivate_car()
                            break

            car.show_image(self.screen)


            for wall in walls:
                pygame.draw.rect(self.screen, (255, 255, 255), wall.rect)
                # for rec in car.front_recs:

                # pygame.draw.rect(self.screen, (0, 255, 255), rec)

            car.make_recs()

            for rec in car.front_recs:
                for wall in walls:
                    if rec.colliderect(wall):
                        print("bateu")

            for rec in car.front_recs:
                pygame.draw.rect(self.screen, (0, 255, 255), rec)

            w, h = car.car_image.get_size()

            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
