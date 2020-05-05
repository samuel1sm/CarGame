import os
import pygame
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
import random
from GameObjects import Car, Wall, Map
import math


class Game:
    def __init__(self, map):
        pygame.init()
        pygame.display.set_caption("Car tutorial")
        self.map = map
        self.screen = pygame.display.set_mode(map.screen_size)
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

        pos = map.initial_point

        car = Car(pos, car_image=car_image, scale_percent=scale_percent, collision_rects_distance=30)

        w, h = car_image.get_size()

        while not self.exit:
            self.screen.fill((0, 0, 0))

            dt = self.clock.get_time() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            pressed = pygame.key.get_pressed()

            map.draw_walls(self.screen)

            if car.activated:
                car.blit_rotate((w // 2, h // 2))

                car.change_angle(pressed, dt)

                car.distances = []
                for i, dp in enumerate(car.distance_rects):
                    for wall in self.map.wall_list:
                        if dp.rect.colliderect(wall.rect):
                            car.calculate_distace_to_wall(wall, i)
                            car.distance_rects[i].distance_from_colision_variable -= 1

                    if len(car.distances) != i+1:
                        car.distance_rects[i].reset_distance_from_colision()
                        car.distances.append(car.distance_rects[i].distance_from_colision_variable)

                for rec in car.collision_rects:
                    for wall in self.map.wall_list:
                        if rec.colliderect(wall.rect):
                            car.deactivate_car()
                            break

            # print(car.distances)

            car.show_image(self.screen)

            car.make_collision_recs()
            car.make_distance_recs()

            car.draw_car_rects(self.screen)

            w, h = car.car_image.get_size()

            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    map = Map("test_map_1.txt")
    game = Game(map)
    game.run()
