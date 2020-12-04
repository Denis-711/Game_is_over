import pygame as pg


class Camera():
    def __init__(self, camera_func, size):
        self.rect = pg.Rect((0, 0), size)
        self.camera_func = camera_func
    
    def apply (self, target):
        return target.rect.move(self.rect.topleft)
    
    def update(self, target):
        self.rect = self.camera_func(self.rect, target.rect)


class Player(pg.sprite.Sprite):
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
        
        size = (84, 135) #размер героя соответсвует размеру его картинки
        self.image = pg.Surface(size)
        self.image = pg.image.load("sprites/GG.png")
        self.rect = pg.Rect(coords, (size))
        
        self.footing = 0
        self.move_dir = [0, 0]
        self.speed = speed
    
    def update(self, move_dir, objects):
        self.move_dir = move_dir
        self.speed[0] = 20 * self.move_dir[0]
        
        if(self.footing == 1):
            self.speed[1] = -40 * self.move_dir[1]
            self.footing = (self.move_dir[1] + 1) % 2
        if not self.footing:
            self.speed[1] += 2
        self.footing = 0
        self.rect.y += self.speed[1]
        self.check_collide(objects, (0, self.speed[1]))
        
        
        self.rect.x += self.speed[0]
        self.check_collide(objects,(self.speed[0], 0))
        print(self.speed)
         
    def check_collide(self, objects, velocity):  
        for obj in objects:
            if pg.sprite.collide_rect(self, obj):
               
                if (velocity[0] > 0):
                    self.rect.right = obj.rect.left 
                    self.speed[0] = 0
                    print('right')
                if(velocity[0] < 0):
                    self.rect.left = obj.rect.right 
                    self.speed[0] = 0
                    print('left')
                if (velocity[1] > 0):
                    self.rect.bottom = obj.rect.top 
                    self.speed[1] = 0
                    self.footing = 1
                    print('bottom')
                    
                if (velocity[1] < 0):
                    self.speed[1] = 0
                    print('top')
                    self.rect.top = obj.rect.bottom


class Brick(pg.sprite.Sprite):
    def __init__(self, coords):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((128, 64))
        self.image = pg.image.load("sprites/block_deck.png")
        self.rect = pg.Rect(coords, (128, 64))
        

class Manager():
    def __init__(self):
        self.move_dir = [0, 0]
        pg.init()
        level = [
                 "+                           +     +",
                 "+                           +     +",
                 "+                           +     +",
                 "+                     ++    +     +",
                 "+                           +     +",
                 "+                           +     +",
                 "+                           +     +",
                 "+              ++           +     +",
                 "+                           +     +",
                 "+                           +     +",
                 "+                    ++     +     +",
                 "+                           +     +",
                 "+         +               + +     +",
                 "+                           +     +",
                 "+              +            +     +",
                 "+                           +     +",
                 "+                   ++      +     +",
                 "+                           +     +",
                 "+                           +     +",
                 "+            ++             +     +",
                 "+                  +++      +     +",
                 "+                           +     +",
                 "+              +            +     +",
                 "+       +++                 +     +",
                 "+                           +     +",
                 "+++++++++++++++++++++++++++++++++++"]
        self.level_size = (len(level[0]) * 128, len(level) * 64)
        brick = Brick((len(level[0]) * 2, len(level) * 1))
        self.player = Player([300, 300], [0, 0])
        self.bricks = []
        self.game_objects = pg.sprite.Group()
        self.game_objects.add(self.player)
        for i in range(len(level)):
            for j in range(len(level[0])):
                if (level[i][j] == "+"):
                    brick = Brick([j * 128, i * 64])
                    self.game_objects.add(brick)
                    self.bricks.append(brick)
                              

        
        self.screen = pg.display.set_mode((1800, 900))
         
        self.camera = Camera(camera_configure, (len(level[0]) * 128, len(level) * 64)) 
        
        pg.display.set_caption("Game_is_over")    

    def handle_events(self, events):
        done = False
        for event in events:
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.move_dir[1] = 1
                if event.key == pg.K_a:
                    self.move_dir[0] = -1
                elif event.key == pg.K_d:
                    self.move_dir[0] = 1
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.move_dir[1] = 0
                if event.key == pg.K_a:
                    self.move_dir[0] = 0
                elif event.key == pg.K_d:
                    self.move_dir[0] = 0
        
        self.player.update(self.move_dir, self.bricks)
        self.game_objects.draw(self.screen)
        return done
        
    def process(self, events):
        done = self.handle_events(events)
        background = pg.Surface(self.level_size)
        background.fill((0, 0, 0))
        self.screen.blit(background, (0, 0))
        
        self.camera.update(self.player) 
        for obj in self.game_objects:
            self.screen.blit(obj.image, self.camera.apply(obj))
        pg.display.update()
        return done
        

def camera_configure(camera, target_rect):
    win_height = 900
    win_width = 1800
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
   
    
    
    

    return pg.Rect(l, t , w, h)      
