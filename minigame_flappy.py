import pygame as pg
import random


class Hurt(pg.sprite.Sprite):
    """
    Класс игрока.
    Наследуется от pygame.sprite.Sprite и имеет станадартные атрибуты:
    image - поверхность с изображением персонажа
    rect - прямоугольник соотвествующий физической модели
           игрока в игровом простарнстве.

    Атрибуты реакция на команды:
    move_dir - массив из двух чисел, первое отвечает за движение
               по горизонтали(1 - двигаться вправо, -1 - двигаться влево,
               0 - не двигаться по горизонтали), второе отвечает за прыжок
               (1 - выполнить прыжок, 0 -не выполнять прыжок).

    Атрибуты движения:
    speed - текущая скорость передвижения в виде массива из проекций на оси

    Атрибуты взаимодействия с блоками:
    footing - если 1, то герой находится ногами на блоке в данный момент
              если 0, то герой не имеет опоры в данный момент
    """

    def __init__(self, coords, speed):
        """
        Функция инициализирует объект игрока.
        Ключевые аргументы:
        coords - начальные координаты положения(массив из 2 чисел)
        speed - начальная скорость движения(массив из 2 чисел)
        """
        pg.sprite.Sprite.__init__(self)

        size = (32, 27)  # размер героя соответсвует размеру его картинки
        self.image = pg.Surface(size)
        self.image = pg.image.load("sprites/hurt.png")
        self.rect = pg.Rect(coords, (size))
        self.life = True

        self.move_dir = [0, 0]
        self.speed = speed

    def update(self, move_dir, objects, screen_height=600):
        self.move_dir = move_dir
        self.speed[0] = 20 * self.move_dir[0]
        self.speed[1] = -5 * self.move_dir[1]
        if self.rect.centery >= screen_height // 12:
            self.speed[1] += 0.5
        self.rect.y += self.speed[1]
        self.check_collide(objects, (0, self.speed[1]))

        self.rect.x += self.speed[0]
        self.check_collide(objects, (self.speed[0], 0))


    def check_collide(self, objects, velocity,
                      screen_height=600, hurt_height=32):
        for obj in objects:
            for sprite in obj.sprites1:
                if pg.sprite.collide_rect(self, sprite):
                    self.life = False
                    if (velocity[0] > 0):
                        self.rect.right = sprite.rect.left
                        self.speed[0] = 0
                    if (velocity[0] < 0):
                        self.rect.left = sprite.rect.right
                        self.speed[0] = 0
                    if (velocity[1] > 0):
                        self.rect.bottom = sprite.rect.top
                        self.speed[1] = 0
                    if (velocity[1] < 0):
                        self.speed[1] = 0
                        self.rect.top = sprite.rect.bottom
            for sprite in obj.sprites2:
                if pg.sprite.collide_rect(self, sprite):
                    self.life = False
                    if (velocity[0] > 0):
                        self.rect.right = sprite.rect.left
                        self.speed[0] = 0
                    if (velocity[0] < 0):
                        self.rect.left = sprite.rect.right
                        self.speed[0] = 0
                    if (velocity[1] > 0):
                        self.rect.bottom = sprite.rect.top
                        self.speed[1] = 0
                    if (velocity[1] < 0):
                        self.speed[1] = 0
                        self.rect.top = sprite.rect.bottom

        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.y >= screen_height - hurt_height:
            self.rect.y = screen_height - hurt_height


class ClawUp(pg.sprite.Sprite):
    def __init__(self, coords):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((64, 64))
        self.image = pg.image.load("sprites/dragon_claw_up.png")
        self.rect = pg.Rect(coords, (64, 64))


class ClawDown(pg.sprite.Sprite):
    def __init__(self, coords):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((64, 64))
        self.image = pg.image.load("sprites/dragon_claw_down.png")
        self.rect = pg.Rect(coords, (64, 64))


class Arm(pg.sprite.Sprite):
    def __init__(self, coords):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((64, 128))
        self.image = pg.image.load("sprites/full_dragon_arm.png")
        self.rect = pg.Rect(coords, (64, 128))


class FullArm():
    def __init__(self, screen_height=600, screen_width=1200,
                 claw_height=64, claw_width=64, velocity=10):
        self.space = random.randint(claw_height, screen_height - claw_height)
        self.velocity = velocity
        self.life = True
        self.x1 = -claw_width + 100
        self.x2 = screen_width - 100
        self.n_down = (self.space - claw_height) // (claw_height * 2) + 2
        self.n_up = (screen_height - self.space - claw_height * 2) \
                    // (claw_height * 2) + 2
        self.sprites1 = pg.sprite.Group()
        self.sprites1.add(ClawDown([self.x1, self.space - claw_height // 2]))
        self.sprites1.add(ClawUp([self.x1, self.space + claw_height * 3 // 2]))
        for i in range(self.n_down):
            self.sprites1.add(Arm([self.x1,
                                  self.space - claw_height * (2 * i + 2.5)]))
        for i in range(self.n_up):
            self.sprites1.add(Arm([self.x1,
                                  self.space + claw_height * (2 * i + 2.5)]))
        self.sprites2 = pg.sprite.Group()
        self.sprites2.add(ClawDown([self.x2, self.space - claw_height // 2]))
        self.sprites2.add(ClawUp([self.x2, self.space + claw_height * 3 // 2]))
        for i in range(self.n_down):
            self.sprites2.add(Arm([self.x2,
                                  self.space - claw_height * (2 * i + 2.5)]))
        for i in range(self.n_up):
            self.sprites2.add(Arm([self.x2,
                                  self.space + claw_height * (2 * i + 2.5)]))

    def move(self, velocity):
        for obj in self.sprites1:
            obj.rect = obj.rect.move(velocity, 0)
        for obj in self.sprites2:
            obj.rect = obj.rect.move(-velocity, 0)

    def draw(self, screen):
        self.sprites1.draw(screen)
        self.sprites2.draw(screen)
        if pg.sprite.collide_rect(self.sprites1.sprites()[0],
                                  self.sprites2.sprites()[0]):
            self.life = False




class Manager_of_flappy():
    def __init__(self):
        self.move_dir = [0, 0]
        pg.init()
        self.player = Hurt([600, 300], [0, 0])
        self.obstacles = []
        self.game_objects = pg.sprite.Group()
        self.game_objects.add(self.player)
        self.screen = pg.display.set_mode((1200, 600))
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)
        self.time_of_spawn = 1500
        self.time_of_prev_spawn = 0
        self.counter = 0
        pg.display.update()


    def handle_events(self, events):
        done = False
        if self.player.life:
            for event in events:
                if event.type == pg.QUIT:
                    done = True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_w:
                        self.move_dir[1] += 1
                    elif event.key == pg.K_s:
                        self.move_dir[1] += -1
                if event.type == pg.KEYUP:
                    if event.key == pg.K_w:
                        self.move_dir[1] -= 1
                    elif event.key == pg.K_s:
                        self.move_dir[1] -= -1

        else:
            done = True

        self.player.update(self.move_dir, self.obstacles)

        pg.display.update()

        return done

    def process(self, events):
        done = self.handle_events(events)
        time = pg.time.get_ticks()
        self.screen.fill(self.BLACK)
        self.game_objects.draw(self.screen)

        if time - self.time_of_prev_spawn >= self.time_of_spawn \
                and self.counter < 6:
            self.time_of_prev_spawn = time
            self.obstacles.append(FullArm())
            self.counter += 1

        if self.counter > 0 and len(self.obstacles) == 0:
            self.screen.fill(self.WHITE)

        for i, obj in enumerate(self.obstacles):
            obj.move(5)
            obj.draw(self.screen)
            if not obj.life:
                self.obstacles.pop(i)

        pg.display.update()
        return done


mngf = Manager_of_flappy()
clock = pg.time.Clock()
done = False

while not done:
    clock.tick(60)
    done = mngf.process(pg.event.get())
    pg.display.update()

mngf.screen.fill(mngf.RED)
pg.display.update()
done = False
counter = 0
print('game over')