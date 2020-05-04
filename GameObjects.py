import random
from math import copysign, degrees, radians, sin, cos

import pygame
from pygame.math import Vector2


class Car:
    def __init__(self, pos, car_image, angle=0.0, distance_rects_distance=20, scale_percent=0.5):
        self.position_absolute = Vector2(pos[0], pos[1])

        self.angle = angle
        self.left_origin = 0
        self.activated = True
        self.scale_percent = scale_percent
        self.distance_points_x_y = []
        self.collision_rects = []
        self.distance_rects = []
        self.distance_rects_distance = distance_rects_distance
        self.car_image = car_image

    def make_collision_recs(self):
        self.distance_points_x_y = []

        aux = []

        self.collision_rects = []

        aux.append((int(self.position_absolute[0] + self.car_image.get_rect().width / 2),
                                         int(self.position_absolute[1])))

        aux.append((int(self.position_absolute[0] + self.car_image.get_rect().width / 2),
                                         int(self.position_absolute[1]) + self.car_image.get_rect().height * 3 / 8))

        aux.append((int(self.position_absolute[0] + self.car_image.get_rect().width / 2),
                                         int(self.position_absolute[1]) - self.car_image.get_rect().height * 3 / 8))

        aux.append(
            (int(self.position_absolute[0] + self.car_image.get_rect().width * 3 / 8),
             int(self.position_absolute[1]) + self.car_image.get_rect().height / 2))

        aux.append(
            (int(self.position_absolute[0] + self.car_image.get_rect().width * 3 / 8),
             int(self.position_absolute[
                     1]) - self.car_image.get_rect().height / 2))

        for cords in aux:
            circle_rotate_position = self.rotate(cords)

            rec = pygame.Rect((int(circle_rotate_position[0]), int(circle_rotate_position[1])),
                              (10 * self.scale_percent, 10 * self.scale_percent))

            self.distance_points_x_y.append ((int(circle_rotate_position[0]), int(circle_rotate_position[1])))
            self.collision_rects.append(rec)

        # return rec

        # pygame.draw.rect(screen, color, rec)

    def make_distance_recs(self):
        distance_points_x_y = []
        self.distance_rects = []

        distance_points_x_y.append(
            (int(self.position_absolute[0] + self.car_image.get_rect().width / 2 + self.distance_rects_distance),
             int(self.position_absolute[1])))

        distance_points_x_y.append((int(self.position_absolute[0] + self.car_image.get_rect().width * 3 / 8),
                                    int(self.position_absolute[1]) + self.car_image.get_rect().height * 3 / 8 +
                                    self.distance_rects_distance))

        distance_points_x_y.append((int(self.position_absolute[0] + self.car_image.get_rect().width * 3 / 8),
                                    int(self.position_absolute[1]) - self.car_image.get_rect().height * 3 / 8 -
                                    self.distance_rects_distance))

        distance_points_x_y.append(
            (int(self.position_absolute[0] + self.car_image.get_rect().width * 3 / 8 + self.distance_rects_distance),
             int(self.position_absolute[
                     1]) + self.car_image.get_rect().height / 2 + self.distance_rects_distance))

        distance_points_x_y.append(
            (int(self.position_absolute[0] + self.car_image.get_rect().width * 3 / 8 + self.distance_rects_distance),
             int(self.position_absolute[
                     1]) - self.car_image.get_rect().height / 2 - self.distance_rects_distance))

        for cords in distance_points_x_y:
            ratated_position = self.rotate(cords)

            rec = pygame.Rect((int(ratated_position[0]), int(ratated_position[1])),
                              (10 * self.scale_percent, 10 * self.scale_percent))

            self.distance_rects.append(rec)

        # return rec

        # pygame.draw.rect(screen, color, rec)

    def change_angle(self, pressed, dt):
        if pressed[pygame.K_d]:
            self.angle -= 1
        elif pressed[pygame.K_a]:
            self.angle += 1

        if pressed[pygame.K_w] or pressed[pygame.K_s]:
            self.position_absolute += (cos(radians(self.angle)) * 2, sin(radians(self.angle) * -1) * 2)

    def rotate(self, cords):

        value_ang = self.angle if self.angle < 0 else self.angle

        value = (5, 0) if (value_ang % 360 >= 260 and value_ang % 360 < 360) else (5, 0) if (
                value_ang % 360 >= 0 and value_ang % 360 < 25) else (0, 0)

        ox, oy = self.position_absolute
        px, py = (cords[0] - value[0], cords[1] - value[1])

        angle = radians(self.angle)

        qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy)
        qy = oy + sin(angle) * (px - ox) * -1 + cos(angle) * (py - oy) * -1
        return qx, qy

    def blitRotate(self, originPos):
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


class Wall(object):

    def __init__(self, pos, tam=(10, 20)):
        self.rect = pygame.Rect(pos[0], pos[1], tam[0], tam[1])
        # self.rect.center = pos
