import pygame as pg
import classes
import mini_game_ball as mg1
import minigame_flappy as mg2

mng = classes.Manager(True)
clock = pg.time.Clock()


while(mng.playing):
    done = False
    mng.setting()
    while not done:
        if mng.playing:
            if(mng.final):
                clock.tick(1)
                
                if(mg1.mini_balls()):
                    clock.tick(1)
                    if(mg2.mini_flappy()):
                        print("WIN")
                        pg.QUIT()
            else:
                clock.tick(120)
                done = mng.process(pg.event.get())
            pg.display.update()
        else:
            pg.QUIT()
        
        

print('game over')
