#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math


class Vec2d:
    def __init__(self, *args):
        self.v = args[0], args[1]

    def __repr__(self):
        return 'Vector2D({}, {})'.format(self.v[0], self.v[1])

    def __setitem__(self, key, value):
        self.v[key] = value

    def __getitem__(self, item):
        return self.v[item]

    def __sub__(self, other):
        """"Returns the difference of two vectors."""
        return Vec2d(self.v[0] - other[0], self.v[1] - other[1])

    def __add__(self, other):
        """Returns the sum of two vectors."""
        return Vec2d(self.v[0] + other[0], self.v[1] + other[1])

    def __mul__(self, other):
        """Returns the result of multiplying vector on value."""
        return Vec2d(self.v[0] * other, self.v[1] * other)

    def len(self):
        """Returns the length of the vector."""
        return math.sqrt(self.v[0] * self.v[0] + self.v[1] * self.v[1])

    def int_pair(self):
        return self.v[0], self.v[1]


class Polyline:
    def __init__(self, points, width=3, color=(255, 255, 255)):
        self.points = points
        self.base_points = None
        self.width = width
        self.color = color

    def __repr__(self):
        return 'Polyline(length: {})'.format(len(self.points))

    def get_points(self, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.__get_point(i * alpha))
        return res

    def __get_point(self, alpha, deg=None):
        if deg is None:
            deg = len(self.base_points) - 1
        if deg == 0:
            return self.base_points[0]
        return (self.base_points[deg] * alpha) + (self.__get_point(alpha, deg - 1) * (1 - alpha))

    def draw_polyline(self):
        for p_n in range(-1, len(self.points) - 1):
            pygame.draw.line(gameDisplay, self.color,
                             (self.points[p_n][0], self.points[p_n][1]),
                             (self.points[p_n + 1][0], self.points[p_n + 1][1]), self.width)

    def draw_points(self):
        for p in self.points:
            pygame.draw.circle(gameDisplay, self.color,
                               (p[0], p[1]), self.width)

    def set_points(self, speeds):
        """Coordinates recalculation function"""
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + speeds[p]
            if self.points[p][0] > gameDisplay.get_size()[0] or self.points[p][0] < 0:
                speeds[p] = (- speeds[p][0], speeds[p][1])
            if self.points[p][1] > gameDisplay.get_size()[1] or self.points[p][1] < 0:
                speeds[p] = (speeds[p][0], -speeds[p][1])

    def draw_help(self):
        """Help window drawing function"""
        gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["Num+", "More points"])
        data.append(["Num-", "Less points"])
        data.append(["", ""])
        data.append([str(steps), "Current points"])

        pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


class Knot(Polyline):
    def __repr__(self):
        return 'Knot(length: {})'.format(len(self.points))

    def get_knot(self, count):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
            self.base_points = ptn

            res.extend(self.get_points(count))
        return res


if __name__ == "__main__":
    pygame.init()
    screen_dim = (800, 600)
    gameDisplay = pygame.display.set_mode(screen_dim)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    points = []
    speeds = []
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    points = []
                    speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                points.append(Vec2d(*event.pos))
                speeds.append((random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        polyline = Polyline(points)
        polyline.draw_points()
        knot = Knot(points, color=color)
        knot.points = knot.get_knot(steps)
        knot.draw_polyline()

        if not pause:
            polyline.set_points(speeds)
        if show_help:
            polyline.draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
