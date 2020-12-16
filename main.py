import pygame as pg
import classes

mng = classes.Manager()
clock = pg.time.Clock()
done = False

while not done:
    clock.tick(120)
    done = mng.process(pg.event.get())
    pg.display.update()

print('game over')
