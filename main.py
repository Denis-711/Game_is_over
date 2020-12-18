import pygame as pg
import classes

mng = classes.Manager(True)
clock = pg.time.Clock()


while(mng.playing):
    done = False
    mng.setting()
    while not done:
        clock.tick(120)
        if mng.playing:
            done = mng.process(pg.event.get())
            pg.display.update()
        else:
            pg.QUIT()

print('game over')
