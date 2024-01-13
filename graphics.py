import pygame as pg
import math
pg.init()

WIDTH, HEIGHT = 1000,1000
WIN = pg.display.set_mode((WIDTH, HEIGHT)) #creates a sort of canvas

WHITE = (255,255,255)
pg.display.set_caption("Rocket Sim") #this is like the title of the app, similar to HTMLs title
rocketIMG = pg.image.load("pic/rocket.png").convert_alpha()
ROCKET_HEIGHT = 100
ROCKET_WIDTH = 50
ROCKET_IMAGE = pg.transform.scale(rocketIMG, (ROCKET_WIDTH, ROCKET_HEIGHT))

groundImg = pg.image.load('pic/ground.png').convert()
skyImg = pg.image.load('pic/sky.png').convert_alpha()
spaceImg = pg.image.load('pic/space.png').convert_alpha()

groundImg = pg.transform.scale(groundImg, (WIDTH, HEIGHT))
skyImg = pg.transform.scale(skyImg, (WIDTH, HEIGHT))
spaceImg = pg.transform.scale(spaceImg, (WIDTH, HEIGHT))

current_bg = groundImg

rocket_img = pg.image.load('pic/rocket.png').convert_alpha()
rocket_rect = rocket_img.get_rect(center=(WIDTH/2, HEIGHT - ROCKET_HEIGHT))

class Rocket(pg.sprite.Sprite):
    def __init__(self, velocity):
        super().__init__()
        self.image = rocket_img
        self.rect = rocket_rect
        self.oVelocity = velocity
        self.nVelocity = self.oVelocity
        self.acc = (-.05, -.05)
        self.prev = ""
        self.mask = pg.mask.from_surface(self.image)  # For pixel-perfect collision detection
    def updatePos(self, keys):
        self.accFun(keys)
    def accFun(self, keys):
        if keys[pg.K_w]:
            self.nVelocity[1] += self.acc[1]
            self.rect.y += self.nVelocity[1]
        if(keys[pg.K_d]):
            self.nVelocity[0] += self.acc[0]
            self.rect.x -= self.nVelocity[0]
        if(keys[pg.K_a]):
            self.nVelocity[0] += self.acc[0]
            self.rect.x += self.nVelocity[0]
        if(keys[pg.K_s]):
            self.nVelocity[1] += self.acc[1]
            self.rect.y -= self.nVelocity[1]
    def resetFun(self, keys):
        if(keys != self.prev):
            self.nVelocity = list(self.oVelocity)
        self.prev = keys
    def draw(self, surface):
        surface.blit(self.image, self.rect)

rocket = Rocket([-1, -1])


def main(): #this is basically a inf loop we need to run our code constantly to ensure our window doesnt close instantly after running it.
    run = True
    global current_bg
    clock = pg.time.Clock() #regulates framerate
    pg.time.delay(500)
    while run: #inf while loop
        clock.tick(60) #max "fps"
        WIN.fill((0,0,0))
        for event in pg.event.get(): #for any event that the user does, wheter that be a keystroke or mouse click, check it
            if event.type == pg.QUIT: #if the user clicks on the x on the window
                run = False #run is set to false to exit the inf while loop
        keys = pg.key.get_pressed()
        rocket.draw(WIN)
        rocket.resetFun(keys)
        rocket.updatePos(keys)
        if rocket_rect.y < HEIGHT / 2:
            current_bg = skyImg
        if rocket_rect.y < HEIGHT / 4:
            current_bg = spaceImg
        WIN.blit(current_bg, (0, 0))
        WIN.blit(ROCKET_IMAGE, rocket_rect)
        pg.display.update()
    pg.quit() #stops the program
    
if __name__ == "__main__":
    main()