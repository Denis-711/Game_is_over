import random
import pygame
import math


class GameHandler:
    def __init__(self):
        """
        Создание констант игры, и объектов игры.
        """
        self.FPS = 30
        self.screen_height = 600
        self.screen_width = 600
        self.level = 1
        self.screen = pygame.display.set_mode((self.screen_width,
                                               self.screen_height))
        self.max_quantity = 10
        self.spawn_time = 400
        self.time_of_prev_spawn = 0
        self.time_of_kill = 0
        self.direction = 360
        self.speed_max = 10
        self.speed_min = 2
        self.radius = 30
        self.rotationalspeed = 15
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.counter = 0
        self.final_start = True
        self.start = True
        self.end = False
        self.pause = False
        self.finished = False
        self.time_pause = 0
        self.pool = []
        self.death = False
        self.clock = pygame.time.Clock()
        self.win = False
        self.RED = (255, 0, 0)


class Ball(GameHandler):
    """
    Первый тип игровой цели - шарик, за попадание в него получаешь 1 очко.
    """

    def __init__(self):
        """
        Параметры наследумеые из класса BaseTarget и инициализация параметра
        радиус отвечаещего за радиус круга, символизирующего шарик.
        """
        super().__init__()
        self.x = random.randint(self.screen_width * 0.15 + self.radius,
                                self.screen_width * 0.85 - self.radius)
        self.y = random.randint(self.screen_height * 0.15 + self.radius,
                                self.screen_height * 0.85 - self.radius)
        self.velocity = [
            random.randint(self.speed_min, self.level * self.speed_max),
            random.randint(0, self.direction)]
        self.color = self.WHITE
        self.radius = self.radius
        

    def move_xy(self):
        """
        Отвечает за измененине координат.
        """
        if self.x >= self.screen_width * 0.85 or self.x <= self.screen_width * 0.15:
            self.velocity[1] = 180 - self.velocity[1]
        elif self.y >= self.screen_height * 0.85 or self.y <= self.screen_height * 0.15:
            self.velocity[1] *= -1
        self.x = self.x + int(self.velocity[0]
                              * math.cos(math.pi * self.velocity[1] / 180))
        self.y = self.y - int(self.velocity[0]
                              * math.sin(math.pi * self.velocity[1] / 180))

    def draw(self):
        """
        Функция рисует на игровом экране объект.
        """
        pygame.draw.circle(self.screen, self.color, (self.x, self.y),
                           self.radius)

    def kill(self):
        """
        Закрашивает объект черным цветом.
        """
        pygame.draw.circle(self.screen, self.BLACK, (self.x, self.y),
                           self.radius)

    def move(self):
        """
        Отвечает за передвижение объекта.
        """
        self.kill()
        self.move_xy()
        self.draw()

    def check(self, x, y):
        """
        Проверка попадания. x, y - координаты точки проверки.
        """
        if (self.x - x) ** 2 + (self.y - y) ** 2 <= self.radius ** 2:
            return True
        else:
            return False


def mini_balls():
    GH = GameHandler()


    while not GH.finished:
        if(GH.final_start):
            GH.time_of_prev_spawn = pygame.time.get_ticks()
            GH.time_of_kill = pygame.time.get_ticks()
            GH.final_start = False
        GH.clock.tick(GH.FPS)
        time = pygame.time.get_ticks()
        if not GH.end:
            for ball in GH.pool:
                ball.move()
                pygame.display.update()
            if (time - GH.time_of_prev_spawn >= GH.spawn_time) and \
                    (GH.counter < 10):
                unit = Ball()
                GH.pool.append(unit)
                GH.time_of_prev_spawn = time
                GH.counter += 1
                pygame.display.update()
            if time - GH.time_of_kill > 4 * GH.spawn_time:
                GH.end = True
                del GH.pool[:]
                GH.screen.fill(GH.BLACK)
                GH.death = True
                GH.screen.fill(GH.RED)
                GH.finished = True
                pygame.display.update()
            if GH.counter == 10 and len(GH.pool) == 0 and not GH.end:
                GH.screen.fill(GH.WHITE)
                GH.end = True
                GH.finished = True
                GH.win = True
                pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GH.finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i, ball in enumerate(GH.pool):
                    if ball.check(x, y):
                        ball.kill()
                        GH.time_of_kill = pygame.time.get_ticks()
                        GH.pool.pop(i)
    return GH.win

