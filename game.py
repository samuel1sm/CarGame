import os
import pygame
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
import random
from GameObjects import Car, Wall, Map
import math
from CarAi import CarAi

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
        if not os.path.exists("episodes"):
            os.mkdir("episodes")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "imgs/carro_feio.png")
        car_image = pygame.image.load(image_path)
        # car_image = pygame.Surface((128, 64))
        scale_percent = 0.5
        w, h = car_image.get_size()

        car_image = pygame.transform.scale(car_image, (int(w * scale_percent), int(h * scale_percent)))

        pos = self.map.initial_point

        car = Car(pos, car_image=car_image, scale_percent=scale_percent, collision_rects_distance=30)

        w, h = car_image.get_size()

        carai = CarAi(5)

        episode = 0
        while not self.exit:
            self.screen.fill((0, 0, 0))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            pressed = pygame.key.get_pressed()

            map.draw_walls(self.screen)

            if car.activated:
                car.blit_rotate((w // 2, h // 2))


                movement = carai.predict(car.distances, car.max_distance)
                # print(valor)
                # car.player_control(pressed)
                new_info = car.calculate_new_position(movement)
                car.set_new_infos(new_info)
                
                new_info = car.make_collision_recs()
                car.update_colision_points_info(new_info)
                new_info = car.make_distance_recs()
                car.update_distance_rect(new_info)

                distance, new_position = self.map.calculate_distances(car.distance_rects)
                car.distances =distance
                car.distance_rects = new_position

                next_state_movement = carai.predict(car.distances, car.max_distance)
                new_angle,new_position = car.calculate_new_position(next_state_movement)
                new_position = car.position_absolute + new_position 
                distance_rects = car.make_distance_recs(new_position,new_angle)
                distance, _ = self.map.calculate_distances(distance_rects)

                carai.car_train((car.distances, car.position_absolute), (distance_rects, new_position))

                if episode % 20 == 0:
                    carai.model.save("episodes/ai_car_{}.h5".format(episode))
                    lista =  os.listdir("episodes")
                    if len(lista) == 40:
                        os.remove(f"episodes/{lista[0]}") 
                episode += 1

                for rec in car.collision_rects:
                    for wall in self.map.wall_list:
                        if rec.colliderect(wall.rect):
                            car = Car(pos, car_image=car_image, scale_percent=scale_percent, collision_rects_distance=30)

                            break

            car.show_image(self.screen)
            # print(car.distances)
            
            car.draw_car_rects(self.screen)
            w, h = car.car_image.get_size()

            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    map = Map("test_map_1.txt")
    game = Game(map)
    game.run()
