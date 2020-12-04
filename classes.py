import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self, coords, speed):
        self.move_dir = [0, 0]
        pg.sprite.Sprite.__init__(self)
        self.speed = speed
        self.image = pg.Surface((20, 30))
        self.image.fill((255, 0, 0))
        self.rect = pg.Rect(coords, (20, 30))
        self.footing = 0
    
    def update(self, move_dir, objects):
        self.move_dir = move_dir
        self.speed[0] = 5 * self.move_dir[0]
        
        if(self.footing == 1):
            self.speed[1] = -20 * self.move_dir[1]
            self.footing = (self.move_dir[1] + 1) % 2
        if not self.footing:
            self.speed[1] += 1
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
        self.image = pg.Surface((20, 20))
        self.image.fill((0, 0, 255))
        self.rect = pg.Rect(coords, (20, 20))
        

class Manager():
    def __init__(self):
        self.move_dir = [0, 0]
        pg.init()
        level = [
                 "++++++++++++++++++++++++++++++++++++++++",
                 "+                                      +",
                 "+                                      +",
                 "+                                      +",
                 "+                                      +",
                 "+                             +++++    +",
                 "+                                      +",
                 "+                                      +",
                 "+                                      +",
                 "+            +++                       +",
                 "+                                      +",
                 "+                                      +",
                 "+                                      +",
                 "+                                      +",
                 "+                           +++        +", 
                 "+                                      +",
                 "+                                      +",
                 "+                                      +",
                 "+                                      +",
                 "++++++++++++++++++++++++++++++++++++++++"]
        brick = Brick([20, 20])
        self.player = Player([100, 100], [0, 0])
        self.bricks = []
        self.game_objects = pg.sprite.Group()
        self.game_objects.add(self.player)
        for i in range(20):
            for j in range(40):
                if (level[i][j] == "+"):
                    brick = Brick([j * 20, i * 20])
                    self.game_objects.add(brick)
                    self.bricks.append(brick)
                              

        
        self.screen = pg.display.set_mode((800, 800))
        
        pg.display.set_caption("Game_is_over")    

    def handle_events(self, events):
        done = False
        for event in events:
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.move_dir[1] = 1
                if event.key == pg.K_LEFT:
                    self.move_dir[0] = -1
                elif event.key == pg.K_RIGHT:
                    self.move_dir[0] = 1
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    self.move_dir[1] = 0
                if event.key == pg.K_LEFT:
                    self.move_dir[0] = 0
                elif event.key == pg.K_RIGHT:
                    self.move_dir[0] = 0
        
        self.player.update(self.move_dir, self.bricks)
        self.game_objects.draw(self.screen)
        return done
        
    def process(self, events):
        done = self.handle_events(events)
        background = pg.Surface((800, 800))
        background.fill((0, 0, 0))
        self.screen.blit(background, (0, 0)) 
        self.game_objects.draw(self.screen)
        return done
        
        
    
