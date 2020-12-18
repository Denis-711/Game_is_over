import pygame as pg
import yaml
import random
import os
import pyganim


class Dyna_obj(pg.sprite.Sprite):
    def __init__(self, coords, speed, size, image_file):
        pg.sprite.Sprite.__init__(self)

        # извлечение анимаций
        anim_files = []
        for i in os.walk(image_file):
            anim_files.append(i)
        anim_atack = []
        anim_jump = []
        anim_stand = []
        anim_delay = 1
        atack_delay = 300
        for adress, dirs, files in anim_files:
            if (adress == image_file + "/atack"):
                for one_file in files:
                    anim_atack.append(
                        (str(adress + "/" + one_file), atack_delay))
            if (adress == image_file + "/jump"):
                for one_file in files:
                    anim_jump.append(
                        (str(adress + "/" + one_file), anim_delay))

            if (adress == image_file + "/stand"):
                for one_file in files:
                    anim_stand.append(
                        (str(adress + "/" + one_file), anim_delay))
            

        self.anim_atack = pyganim.PygAnimation(anim_atack)
        self.anim_atack.play()
        self.anim_jump = pyganim.PygAnimation(anim_jump)
        self.anim_jump.play()
        self.anim_stand = pyganim.PygAnimation(anim_stand)
        self.anim_stand.play()

        self.image = pg.Surface(size[1])
        self.rect = pg.Rect(coords, (size[0]))
        
        self.atack = False
        self.atack_started = False
        self.atack_period = atack_delay
         
        self.health = 200
        self.life = True 
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

    def check_spikes(self, objects):
        max_dist = 400
        if type(self) == Player:
            for obj in objects:
                if abs(obj.rect.x - self.rect.x) < max_dist:
                    if pg.sprite.collide_rect(self, obj):
                        time = pg.time.get_ticks()
                        if obj.active :
                            obj.kill(self, time)
                        else:
                            obj.triggering()
    
    def check_enemies(self, enemies):
        max_dist = 400                  
        for enemy in enemies:
            if (abs(enemy.rect.x - self.rect.x) < max_dist):
                if pg.sprite.collide_rect(self, enemy) and self.atack:
                    time = pg.time.get_ticks()
                    if(time - self.time_atack > 0.9 * self.atack_period):
                        damage = 200
                        enemy.get_damage(damage)
            if type(self) == Enemy:
                if pg.sprite.collide_rect(self, enemy) and not self.atack:
                    self.activate_atack()
              
    def get_damage(self, damage):
        self.health -= damage;
    
    def activate_atack(self):
        self.atack = True
        self.time_atack = pg.time.get_ticks()
        self.atack_started = True


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
    Наследуется от Dyna_obj и имеет станадартные атрибуты:
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
        size_mod = (89, 120)  # размер героя соответсвует размеру его картинки
        size_pic = (125, 120)
        size = (size_mod, size_pic)
        
        image_file = "sprites/sprites_beta/GG"
        Dyna_obj.__init__(self, coords, speed, size, image_file)
        self.health = 1000

    def update(self, move_dir, atack_command, objects, spikes):
        #взаимодествие с блоками
        self.move_dir = move_dir
        self.speed[0] = 40 * self.move_dir[0]

        if (self.move_dir[1] == 1 and self.footing):
            self.image.fill((0, 0, 0))
            self.image.set_colorkey((0, 0, 0))
            self.anim_jump.blit(self.image, (0, 0))

        if (self.move_dir[1] == 0 and self.footing):
            self.image.fill((0, 0, 0))
            self.image.set_colorkey((0, 0, 0))
            self.anim_stand.blit(self.image, (0, 0))

        if self.footing:
            self.speed[1] = -80 * self.move_dir[1]
            self.footing = (self.move_dir[1] + 1) % 2
        if not self.footing:
            self.speed[1] += 10
        self.footing = 0
        self.rect.y += self.speed[1]
        self.check_spikes(spikes)                      # взаимодествие с шипами
        self.check_collide(objects, (0, self.speed[1]))

        self.rect.x += self.speed[0]
        self.check_collide(objects, (self.speed[0], 0))
        
        #активация атаки
        if not self.atack and atack_command:
            self.activate_atack()
        #атака
        if self.atack:
            time = pg.time.get_ticks()
            flag = time - self.time_atack < self.atack_period
            if(flag and self.atack_started):
                self.atack_started = True
                self.image.fill((0, 0, 0))
                self.image.set_colorkey((0, 0, 0))
                self.anim_atack.blit(self.image, (0, 0))
                self.anim_atack.stop()
                self.anim_atack.play()
            if (time - self.time_atack > self.atack_period):
                self.atack = False
                self.time_atack = time
                self.atack_started = False
        if self.health < 0:
            self.life = False
        
                
class Enemy(Dyna_obj):
    def __init__(self, coords, speed):
        self.max_dist = 700  # определяет доступную зону

        self.spawn_coord = coords
        size_mod = (127, 120)  # размер героя соответсвует размеру его картинки
        size_pic = (127, 120)
        size = (size_mod, size_pic)
        image_file = "sprites/sprites_beta/enemy_1"
        Dyna_obj.__init__(self, coords, speed, size, image_file)

    def update(self, objects):
        if (self.rect.x > self.spawn_coord[0] + self.max_dist):
            self.move_dir[0] = -1
        if (self.rect.x < self.spawn_coord[0] - self.max_dist):
            self.move_dir[0] = 1
        if (self.speed[0] == 0):
            self.move_dir[0] = random.randint(-1, 1)
        self.speed[0] = 30 * self.move_dir[0]            

        if (self.move_dir[1] == 0 and self.footing):
            self.image.fill((0, 0, 0))
            self.image.set_colorkey((0, 0, 0))
            self.anim_stand.blit(self.image, (0, 0))

        if not self.footing:
            self.speed[1] += 4
        self.footing = 0
        self.rect.y += self.speed[1]
        self.check_collide(objects, (0, self.speed[1]))

        self.rect.x += self.speed[0]
        self.check_collide(objects, (self.speed[0], 0))
        
        #атака
        if self.atack:
            time = pg.time.get_ticks()
            flag = time - self.time_atack < self.atack_period
            if(flag and self.atack_started):
                self.atack_started = True
                self.image.fill((0, 0, 0))
                self.image.set_colorkey((0, 0, 0))
                self.anim_atack.blit(self.image, (0, 0))
                self.anim_atack.stop()
                self.anim_atack.play()
            if (time - self.time_atack > self.atack_period):
                self.atack = False
                self.time_atack = time
                self.atack_started = False
        if self.health <= 0:
            self.life = False



class Brick(Static_obj):
    def __init__(self, coords):
        size = (128, 64)
        image_file = "sprites/block_deck.png"
        Static_obj.__init__(self, coords, size, image_file)


class BlockSpikes(pg.sprite.Sprite):
    def __init__(self, coords):
        pg.sprite.Sprite.__init__(self)
        size = (128, 64)
        image_file = "sprites/sprites_beta/spike"
        self.image = pg.Surface(size)
        self.rect = pg.Rect(coords, (size))
        self.active = False
        self.time = 0
        self.active_time = 1000
        anim_files = []
        for i in os.walk(image_file):
            anim_files.append(i)
        anim_spike = []
        anim_stand = []
        anim_delay = 3
        for adress, dirs, files in anim_files:
            if (adress == image_file + "/anim"):
                for one_file in files:
                    anim_spike.append(
                        (str(adress + "/" + one_file), anim_delay))
        for adress, dirs, files in anim_files:
            if (adress == image_file + "/stand"):
                for one_file in files:
                    anim_stand.append(
                        (str(adress + "/" + one_file), anim_delay))
        self.anim_spike = pyganim.PygAnimation(anim_spike)
        self.anim_spike.play()
        self.anim_stand = pyganim.PygAnimation(anim_stand)
        self.anim_stand.play()

    def triggering(self):
        time = pg.time.get_ticks()
        if not self.active:
            self.active = True
            self.time = time

    def update(self):
        if self.active:
            time = pg.time.get_ticks()
            flag = time - self.time > self.active_time * 0.33
            flag = flag and time - self.time < self.active_time *0.66
            if(flag):
                self.image.fill((0, 0, 0))
                self.image.set_colorkey((0, 0, 0))
                self.anim_spike.blit(self.image, (0, 0))
            if (time - self.time > self.active_time):
                self.active = False
                self.time = time
        else:
            self.image.fill((0, 0, 0))
            self.image.set_colorkey((0, 0, 0))
            self.anim_stand.blit(self.image, (0, 0))

    def kill(self, person, time):
        flag = time - self.time > self.active_time * 0.33
        flag = flag and time - self.time < self.active_time *0.66
        if flag:
            person.get_damage(100)
        
		
class Manager():
    def __init__(self):
        brick_size = (128, 64)  # размер обычного блока
        win_size = (900, 1800)  # размер игрового окна
        k = 1  # регулирование дальности прорисовки

        self.max_dist = k * (win_size[0] ** 2 + win_size[1] ** 2) ** 0.5
        self.move_dir = [0, 0]
        self.atack_command = False
        pg.init()
        with open(
                'platform.yaml') as f:  # открытие файла ямл, где хранятся данные о расположении блоков
            level = yaml.safe_load(f)

        self.level_size = (
        len(level[0]) * brick_size[0], len(level) * brick_size[1])
        brick = Brick((len(level[0]) * 2, len(level) * 1))
        self.bricks = []
        self.enemies = []
        self.spikes = []
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
                if (level[i][j] == "-"):
                    block_spikes = BlockSpikes([j * brick_size[0],
                                                i * brick_size[1]])
                    self.game_objects.add(block_spikes)
                    self.spikes.append(block_spikes)

        self.player = Player(spawn_coords, [0, 0])
        self.game_objects.add(self.player)
        self.screen = pg.display.set_mode((1800, 900))

        self.camera = Camera(camera_configure, (len(level[0]) * brick_size[0],
                                                len(level) * brick_size[1]),
                             win_size)

        pg.display.set_caption("Game_is_over")
        pg.font.init()
        self.font = pg.font.Font('freesansbold.ttf', 32)
        self.hurt_image = pg.image.load("sprites/hurt.png", "RGBA")
        self.hurt_image = pg.transform.scale(self.hurt_image, (128, 108))
        self.hurt_imageRect = self.hurt_image.get_rect()
        self.hurt_imageRect.center = (100, 100)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 51, 51)

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
            if event.type == pg.MOUSEBUTTONDOWN:
                self.atack_command = True
        self.player.update(self.move_dir, self.atack_command, self.bricks + self.spikes, self.spikes)
        self.atack_command = False
        return done

    def process(self, events):
        done = self.handle_events(events)

        for enemy in self.enemies:
            if enemy.life == False:
	            enemy.kill()
	            self.enemies.remove(enemy)
            enemy.update(self.bricks + self.spikes)
        for spike in self.spikes:
            spike.update()
        
        self.player.check_enemies(self.enemies)
        for enemy in self.enemies:
            enemy.check_enemies([self.player])
        
        background = pg.Surface(self.level_size)
        background.fill((0, 0, 0))
        self.screen.blit(background, (0, 0))

        self.camera.update(self.player)
        for obj in self.game_objects:
            dist_x = (self.player.rect.x - obj.rect.x)
            dist_y = (self.player.rect.y - obj.rect.y)
            dist = (dist_y ** 2 + dist_x ** 2) ** (0.5)

            if (dist < self.max_dist):
                self.screen.blit(obj.image, self.camera.apply(obj))
        text = self.font.render(str(self.player.health),
                                True, self.WHITE, self.RED)
        textRect = text.get_rect()
        textRect.center = (100, 100)
        self.screen.blit(self.hurt_image, self.hurt_imageRect)
        self.screen.blit(text, textRect)
        pg.display.update()
        return done


def camera_configure(camera, target_rect, win_size):
    win_height = win_size[0]
    win_width = win_size[1]
    l = target_rect.left
    t = target_rect.top
    w = camera.width
    h = camera.height

    l, t = -l + win_width / 2, -t + target_rect.height

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - win_width),
            l)  # Не движемся дальше правой границы

    """
    Если игрок внизу, то камера ориентируется по уровню пола,
    если игрок далеко от низа, то камера ориентируется так,
    чтобы игрок был вверху экрана
    """
    t = max(t, -camera.height + win_height)

    return pg.Rect(l, t, w, h)
