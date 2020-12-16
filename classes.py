import pygame as pg
import yaml
import random

class Dyna_obj(pg.sprite.Sprite):
    def __init__(self, coords, speed, size, image_file):
        pg.sprite.Sprite.__init__(self)
        
        self.image = pg.Surface(size)
        self.image = pg.image.load(image_file)
        self.rect = pg.Rect(coords, (size))
        
        self.footing = 0
        self.move_dir = [0, 0]
        self.speed = speed
    
    def check_collide(self, objects, velocity):
        #максимальная дальность взаимодействия
        max_dist = 400                    
        for obj in objects:
            if (abs(obj.rect.x - self.rect.x) < max_dist):
                if pg.sprite.collide_rect(self, obj):
               
                    if (velocity[0] > 0):
                        self.rect.right = obj.rect.left 
                        self.speed[0] = 0
                    
                    if(velocity[0] < 0):
                        self.rect.left = obj.rect.right 
                        self.speed[0] = 0
                  
                    if (velocity[1] > 0):
                        self.rect.bottom = obj.rect.top 
                        self.speed[1] = 0
                        self.footing = 1
                   
                    if (velocity[1] < 0):
                        self.speed[1] = 0
                        self.rect.top = obj.rect.bottom


class Static_obj(pg.sprite.Sprite):
    def __init__(self, coords, size, image_file):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((size))
        self.image = pg.image.load(image_file)
        self.rect = pg.Rect(coords, (size))


class Camera():
    def __init__(self, camera_func, full_size, win_size):
        self.win_size = win_size
        self.rect = pg.Rect((0, 0), full_size)
        self.camera_func = camera_func
    
    def apply(self, target):
        return target.rect.move(self.rect.topleft)
    
    def update(self, target):
        self.rect = self.camera_func(self.rect, target.rect, self.win_size)


class Player(Dyna_obj):
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
        size = (79, 127)  # размер героя соответсвует размеру его картинки
        image_file = "sprites/GG.png"
        Dyna_obj.__init__(self, coords, speed, size, image_file)
        
    def update(self, move_dir, objects):
        self.move_dir = move_dir
        self.speed[0] = 50 * self.move_dir[0]
        
        if (self.footing == 1):
            self.speed[1] = -40 * self.move_dir[1]
            self.footing = (self.move_dir[1] + 1) % 2
        if not self.footing:
            self.speed[1] += 2
        self.footing = 0
        self.rect.y += self.speed[1]
        self.check_collide(objects, (0, self.speed[1]))

        self.rect.x += self.speed[0]
        self.check_collide(objects, (self.speed[0], 0))
        print(self.speed)


class Enemy(Dyna_obj):
    def __init__(self, coords, speed):
        self.max_dist = 700              #определяет доступную зону
        self.spawn_coord = coords
        size = (0.75 * 129,127)
        image_file = "Minotaur.png"
        Dyna_obj.__init__(self, coords, speed, size, image_file)
    
    def update(self, objects):
        if (self.rect.x > self.spawn_coord[0] + self.max_dist):
            self.move_dir[0] = -1
        if (self.rect.x < self.spawn_coord[0] - self.max_dist):
            self.move_dir[0] = 1
        if (self.speed[0] == 0):
            self.move_dir[0] = random.randint(-1, 1)
        self.speed[0] = 30 * self.move_dir[0]
        
        if not self.footing:
            self.speed[1] += 4
        self.footing = 0
        self.rect.y += self.speed[1]
        self.check_collide(objects, (0, self.speed[1]))

        self.rect.x += self.speed[0]
        self.check_collide(objects, (self.speed[0], 0))
        print(self.speed)
        

class Brick(pg.sprite.Sprite):
    def __init__(self, coords):
        size = (128, 64)
        image_file = "sprites/block_deck.png"
        Static_obj.__init__(self, coords, size, image_file)
       

class Manager():
    def __init__(self):
        brick_size = (128, 64)   #размер обычного блока
        win_size = (900, 1800)   #размер игрового окна
        k = 1                    #регулирование дальности прорисовки
        
        self.max_dist = k * (win_size[0]**2 + win_size[1]**2)**0.5        
        self.move_dir = [0, 0]
        pg.init()
        with open('platform.yaml') as f:  # открытие файла ямл, где хранятся данные о расположении блоков
            level = yaml.safe_load(f)

        self.level_size = (len(level[0]) * brick_size[0], len(level) * brick_size[1])
        brick = Brick((len(level[0]) * 2, len(level) * 1))
        self.bricks = []
        self.enemies = []
        self.game_objects = pg.sprite.Group()
        for i in range(len(level)):
            for j in range(len(level[0])):
                if (level[i][j] == "+"):
                    brick = Brick([j * brick_size[0], i * brick_size[1]])
                    self.game_objects.add(brick)
                    self.bricks.append(brick)
                if (level[i][j] == "0"):
                    spawn_coords = [j * brick_size[0], i * brick_size[1]]
                if (level[i][j] == "1"):
                    enemy_coord = [j * brick_size[0], i * brick_size[1]]
                    enemy = Enemy(enemy_coord, [0, 0])
                    self.game_objects.add(enemy)
                    self.enemies.append(enemy)
                              
        self.player = Player(spawn_coords, [0, 0])
        self.game_objects.add(self.player)
        self.screen = pg.display.set_mode((1800, 900))
         
        self.camera = Camera(camera_configure, (len(level[0]) * brick_size[0],
                                                len(level) * brick_size[1]), win_size)
        
        pg.display.set_caption("Game_is_over")    

    def handle_events(self, events):
        done = False
        for event in events:
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.move_dir[1] += 1
                if event.key == pg.K_a:
                    self.move_dir[0] += -1
                elif event.key == pg.K_d:
                    self.move_dir[0] += 1
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.move_dir[1] = 0
                if event.key == pg.K_a:
                    self.move_dir[0] -= -1
                elif event.key == pg.K_d:
                    self.move_dir[0] -= 1
        
        self.player.update(self.move_dir, self.bricks)
        return done
        
    def process(self, events):
        done = self.handle_events(events)
        
        for enemy in self.enemies:
            enemy.update(self.bricks)
        background = pg.Surface(self.level_size)
        background.fill((0, 0, 0))
        self.screen.blit(background, (0, 0))
        
        self.camera.update(self.player) 
        for obj in self.game_objects:
            dist_x = (self.player.rect.x - obj.rect.x)
            dist_y = (self.player.rect.y - obj.rect.y)
            dist = (dist_y**2 + dist_x**2)**(0.5)
            
            if(dist < self.max_dist):
                self.screen.blit(obj.image, self.camera.apply(obj))
        pg.display.update()
        return done
        

def camera_configure(camera, target_rect, win_size):
    win_height = win_size[0]
    win_width = win_size[1]
    l = target_rect.left
    t = target_rect.top
    w = camera.width
    h = camera.height

    l, t = -l+win_width/ 2, -t + target_rect.height

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-win_width), l)   # Не движемся дальше правой границы
    
    """
    Если игрок внизу, то камера ориентируется по уровню пола,
    если игрок далеко от низа, то камера ориентируется так,
    чтобы игрок был вверху экрана
    """
    t = max(t, -camera.height + win_height) 
    
    return pg.Rect(l, t, w, h)

