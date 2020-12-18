import pygame as pg
import classes
import mini_game_ball as mg1
import minigame_flappy as mg2

mng = classes.Manager(True)
clock = pg.time.Clock()
victory = False

while(mng.playing and not victory):
    done = False
    mng.setting()
    while not done and not victory:
        if mng.playing:
            if(mng.final):
                clock.tick(1)
                if(mg1.mini_balls()):
                    clock.tick(1)
                    if(mg2.mini_flappy()):
                        victory = True
            else:
                clock.tick(120)
                done = mng.process(pg.event.get())
            pg.display.update()
        else:
            pg.QUIT()

if victory:
    image = pg.image.load("sprites/sprites_beta/final.jpg", "RGB")
    imageRect = image.get_rect()
    imageRect.center = (600, 300)
    mng.screen.fill((0, 0, 0))
    mng.screen.blit(image, imageRect)
pg.display.update()
time = pg.time.get_ticks()
while(pg.time.get_ticks() - time < 2000):
    
    clock.tick(120)
    
pg.QUIT()
print('game over')
