import os
import pygame
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
import random
from GameObjects import Car, Wall
import math



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
        scale_percent = 0.5
        w, h = car_image.get_size()

        car_image = pygame.transform.scale(car_image, (int(w * scale_percent), int(h * scale_percent)))

        pos = (0, 0)

        car = Car(pos, car_image=car_image, scale_percent=scale_percent, distance_rects_distance=20)

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
            for wall in walls:
                pygame.draw.rect(self.screen, (255, 255, 255), wall.rect)
            if car.activated:
                car.blitRotate((w // 2, h // 2))

                car.change_angle(pressed, dt)

                for rec in car.collision_rects:
                    for wall in walls:
                        if rec.colliderect(wall.rect):
                            car.deactivate_car()
                            break

                for i, rec in enumerate(car.distance_rects):
                    for wall in walls:
                        # if i == 0:
                            if rec.colliderect(wall.rect):
                                car.calculate_distace_to_wall(wall,i)
                                # x, y = car.distance_points_x_y[i]
                                #
                                # ptl = wall.rect.topleft
                                # ptr = wall.rect.topright
                                # pbl = wall.rect.bottomleft
                                # pbr = wall.rect.bottomright
                                #
                                # p_array = [ptl, ptr, pbl, pbr]
                                #
                                # dist_array = []
                                #
                                # for point in p_array:
                                #     dist = math.sqrt((x - point[0]) ** 2 + (y - point[1]) ** 2)
                                #     dist_array.append((dist, point))
                                #
                                # dist_array.sort(key=lambda tup: tup[0])
                                #
                                # p1 = dist_array[0][1]
                                # p2 = dist_array[1][1]
                                #
                                # a = p1[1] - p2[1]
                                # b = p2[0] - p1[0]
                                # c = p1[0] * p2[1] - p2[0] * p1[1]
                                #
                                # dist = (abs(a * x + b * y + c)) / (math.sqrt(a ** 2 + b ** 2))



                            # break

            car.show_image(self.screen)

            # for rec in car.front_recs:

            # pygame.draw.rect(self.screen, (0, 255, 255), rec)

            car.make_collision_recs()
            car.make_distance_recs()

            for rec in car.collision_rects:
                pygame.draw.rect(self.screen, (0, 255, 255), rec)

            for rec in car.distance_rects:
                pygame.draw.rect(self.screen, (255, 0, 255), rec)

            w, h = car.car_image.get_size()

            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
