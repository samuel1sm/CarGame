from math import radians, sin, cos, sqrt
import copy
import pygame
from pygame.math import Vector2


class Car:
    class Ditance_Points():

        def __init__(self, distance_from_colision, tam):
            self.distance_from_colision_variable = distance_from_colision
            self.distance_from_colision_constant = distance_from_colision
            self.position = (0, 0)
            self.previous_position = (0, 0)
            self.rect = pygame.Rect(0, 0, tam[0], tam[1])

        def reset_distance_from_colision(self):
            self.distance_from_colision_variable = self.distance_from_colision_constant

        def compare_variable_constant_is_equals(self) -> bool:
            return self.distance_from_colision_variable == self.distance_from_colision_constant

        def draw_rect(self, screen):
            pygame.draw.rect(screen, (255, 0, 255), self.rect)

    def __init__(self, pos, car_image, angle=0.0, collision_rects_distance=20, scale_percent=0.5):
        self.position_absolute = Vector2(pos[0], pos[1])
        self.angle = angle
        self.left_origin = 0
        self.activated = True
        self.scale_percent = scale_percent
        self.colision_points_positions = [(collision_rects_distance,collision_rects_distance) for _ in range(5)]
        self.collision_rects = []
        self.max_distance = collision_rects_distance
        self.distance_rects = [
            Car.Ditance_Points(collision_rects_distance, (10 * self.scale_percent, 10 * self.scale_percent)) for _ in range(5)]
        self.car_center = (0,0)
        self.distances = [collision_rects_distance for _ in range(5)]
        self.car_image = car_image

        
    def calculate_new_position(self, values):

        new_angle = self.angle + values[0][0]

        new_position = (cos(radians(new_angle)) * values[0][1]* 1.5, sin(radians(new_angle) * -1) * values[0][1]* 1.5)
        
        return new_angle,new_position
        
    def set_new_infos(self, new_infos):
        self.angle = new_infos[0]
        self.position_absolute += new_infos[1]

    def make_collision_recs(self, position_absolute = None, angle = None):
        position_absolute = position_absolute if position_absolute != None else self.position_absolute
        angle = angle if angle != None else self.angle

        colision_points_positions = []
        aux = []
        collision_rects = []

        # center
        aux.append((int(position_absolute[0] + self.car_image.get_rect().width / 2),
                    int(position_absolute[1])))
        # left wheel
        aux.append((int(position_absolute[0] + self.car_image.get_rect().width / 2),
                    int(position_absolute[1]) + self.car_image.get_rect().height * 3 / 8))
        # right wheel

        aux.append((int(position_absolute[0] + self.car_image.get_rect().width / 2),
                    int(position_absolute[1]) - self.car_image.get_rect().height * 3 / 8))
        # left corner

        aux.append(
            (int(position_absolute[0] + self.car_image.get_rect().width * 3 / 8),
             int(position_absolute[1]) + self.car_image.get_rect().height / 2))
        # right corner
        aux.append(
            (int(position_absolute[0] + self.car_image.get_rect().width * 3 / 8),
             int(position_absolute[1]) - self.car_image.get_rect().height / 2))

        for cords in aux:
            circle_rotate_position = self.rotate(cords,position_absolute, angle)

            rec = pygame.Rect((int(circle_rotate_position[0]), int(circle_rotate_position[1])),
                              (10 * self.scale_percent, 10 * self.scale_percent))

            colision_points_positions.append((int(circle_rotate_position[0]), int(circle_rotate_position[1])))
            collision_rects.append(rec)
        

        return colision_points_positions,collision_rects
    
    def update_colision_points_info(self, new_info):
        self.colision_points_positions = new_info[0]
        self.collision_rects = new_info[1]

    def make_distance_recs(self, position_absolute = None, angle = None):
        distance_points_x_y = []
        position_absolute = position_absolute if position_absolute != None else self.position_absolute
        angle = angle if angle != None else self.angle
        

        # center
        distance_points_x_y.append(
            (int(position_absolute[0] + self.car_image.get_rect().width * 1 / 2 +
                 self.distance_rects[0].distance_from_colision_variable),
             int(position_absolute[1])))

        # left wheel
        distance_points_x_y.append((int(position_absolute[0] + self.car_image.get_rect().width * 1 / 2),
                                    int(position_absolute[1]) + self.car_image.get_rect().height * 1 / 2 +
                                    self.distance_rects[1].distance_from_colision_variable))

        # right wheel
        distance_points_x_y.append((int(position_absolute[0] + self.car_image.get_rect().width * 1 / 2),
                                    int(position_absolute[1]) - self.car_image.get_rect().height * 1 / 2 -
                                    self.distance_rects[2].distance_from_colision_variable))

        # left corner
        distance_points_x_y.append(
            (int(position_absolute[0] + self.car_image.get_rect().width * 1 / 2 +
                 self.distance_rects[3].distance_from_colision_variable),
             int(position_absolute[1]) + self.car_image.get_rect().height / 2
             + self.distance_rects[3].distance_from_colision_variable))

        # right corner
        distance_points_x_y.append(
            (int(position_absolute[0] + self.car_image.get_rect().width * 1 / 2 +
                 self.distance_rects[4].distance_from_colision_variable),
             int(position_absolute[1]) - self.car_image.get_rect().height / 2
             - self.distance_rects[4].distance_from_colision_variable))

        distance_rects = []


        for i, cords in enumerate(distance_points_x_y):
            ratated_position = self.rotate(cords,position_absolute, angle)

            rec = (int(ratated_position[0]), int(ratated_position[1]))
            distance_rects.append(copy.copy(self.distance_rects[i]))
            distance_rects[i].rect.topleft = rec
            distance_rects[i].previous_position = self.distance_rects[i].position
            distance_rects[i].position = ratated_position

        return distance_rects

    def update_distance_rect(self, new_info):
        self.distance_rects = new_info

    def player_control(self, pressed):
        if pressed[pygame.K_d]:
            self.angle -= 1
        elif pressed[pygame.K_a]:
            self.angle += 1

        if pressed[pygame.K_w] or pressed[pygame.K_s]:
            self.position_absolute += (cos(radians(self.angle)) * 2, sin(radians(self.angle) * -1) * 2)


    def rotate(self, cords, position, angle):

        value = (0, 0)

        ox, oy = position
        px, py = (cords[0] - value[0], cords[1] - value[1])

        angle = radians(angle)

        qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy)
        qy = oy + sin(angle) * (px - ox) * -1 + cos(angle) * (py - oy) * -1
        return qx, qy

    def blit_rotate(self, originPos):
        # calcaulate the axis aligned bounding box of the rotated image
        w, h = self.car_image.get_size()
        box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(self.angle) for p in box]
        min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

        # calculate the translation of the pivot
        pivot = pygame.math.Vector2(originPos[0], -originPos[1])
        pivot_rotate = pivot.rotate(self.angle)
        pivot_move = pivot_rotate - pivot
        self.car_center = pivot
        # calculate the upper left origin of the rotated image
        self.left_origin = (
            self.position_absolute[0] - originPos[0] + min_box[0] - pivot_move[0],
            self.position_absolute[1] - originPos[1] - max_box[1] + pivot_move[1])

        # get a rotated image

    def show_image(self, screen):
        rotated_image = pygame.transform.rotate(self.car_image, self.angle)
        screen.blit(rotated_image, self.left_origin)

    def deactivate_car(self):
        self.activated = False

    def draw_car_rects(self, screen):
        for rec in self.collision_rects:
            pygame.draw.rect(screen, (0, 255, 255), rec)

        for rec in self.distance_rects:
            rec.draw_rect(screen)


class Wall(object):
    def __init__(self, pos, tam=(10, 20)):
        self.rect = pygame.Rect(pos[0], pos[1], tam[0], tam[1])
        # self.rect.center = pos


class Map:
    def __init__(self, file_name):
        with open(f"maps/{file_name}", 'r') as f:
            line = f.readline().split(",")
            self.initial_point = (int(line[1]), int(line[2]))
            line = f.readline().split(",")
            self.wall_size = (int(line[1]), int(line[2]))
            line = f.readline().split(",")
            self.wall_color = (int(line[1]), int(line[2]), int(line[3]))
            line = f.readline().split(",")
            self.final_color = (int(line[1]), int(line[2]), int(line[3]))
            line = f.readline().split(",")
            self.screen_size = (int(line[1]), int(line[2]))
            line = f.readline().split(",")
            self.screen_color = (int(line[1]), int(line[2]), int(line[3]))

            self.wall_list = []


            for j, line in enumerate(f.readlines()):
                for i, obj in enumerate(line.split(",")):
                    if obj == "w":
                        self.wall_list.append(Wall((self.wall_size[0] * i, self.wall_size[1] * j), self.wall_size))
                    elif obj == "f":
                         self.final_position_rect = Wall((self.wall_size[0] * i, self.wall_size[1] * j), self.wall_size)
                         self.final_position = (self.wall_size[0] * i, self.wall_size[1] * j)

    def draw_walls(self, screen):
        for wall in self.wall_list:
            pygame.draw.rect(screen, self.wall_color, wall.rect)

        pygame.draw.rect(screen, self.final_color, self.final_position_rect.rect)

    def calculate_distances(self, rects):
        distance = []

        new_position = []
        # print(rects[0] == test)
        for i, dp in enumerate(rects):
            dp = copy.copy(dp)
            new_position.append(dp)
            for wall in self.wall_list:
                if dp.rect.colliderect(wall.rect):
                    new_position[i].distance_from_colision_variable -= 1

                    dist = new_position[i].distance_from_colision_variable
                    if dist < 0:
                        dist = 0
                
                    distance.append(dist)
                            
                    break


            if len(distance) != i + 1:
                if not new_position[i].compare_variable_constant_is_equals():
                    new_position[i].distance_from_colision_variable += 1
                dist = new_position[i].distance_from_colision_variable
                if dist < 0:
                    dist = 0
            
                distance.append(dist)

        return distance, new_position


        
