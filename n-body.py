import pygame
import pygame.gfxdraw
from pygame.locals import *
from math import sqrt, atan2, degrees, cos, sin, radians

pygame.init()

size = width, height = 900, 900

screen = pygame.display.set_mode(size)

GREY = 39, 69, 99

frames = 0

class Ball(pygame.sprite.Sprite):
    def __init__(self, (x, y), radius, mass, color, speed=(0,0)):
        pygame.sprite.Sprite.__init__(self)

        BALL_IMG = pygame.Surface((2*radius, 2*radius), pygame.SRCALPHA)

        #ball = pygame.draw.circle(screen, color, ball_position, 20)
        pygame.gfxdraw.aacircle(BALL_IMG, radius, radius, radius-1, color)
        pygame.gfxdraw.filled_circle(BALL_IMG, radius, radius, radius-1, color)
        
        self.mSpeed = speed
        self.x = x
        self.y = y
        self.delta_x = 0
        self.delta_y = 0
        self.mass = mass
        self.radius = radius
        self.image = BALL_IMG
        self.rect = self.image.get_rect(center=(150, 200))
        self.trail = []

        
    
    def move(self):
        self.x += self.mSpeed[0]
        self.y += self.mSpeed[1]
        if frames % 20 == 0:
            self.trail.append((int(self.x + self.radius), int(self.y + self.radius)))

    def constrainedMove(self, position, radius, print_flag=False):
        self.x += self.mSpeed[0]
        self.y += self.mSpeed[1]
        if abs(self.x - position[0]) <= self.radius and abs(self.y - position[1]) <= self.radius:
            self.speed = (-self.mSpeed[0], -self.mSpeed[1])
        if frames % 20 == 0:
            self.trail.append((int(self.x + self.radius), int(self.y + self.radius)))
        if print_flag:
            print("constrained move speed: {}".format(self.mSpeed))

    def drawTrail(self, surface, color):
        for point in self.trail:
            pygame.draw.circle(surface, color, point, 0)
    
    def trimNthTrail(self, n):
        self.trail = self.trail[::n]

    def getUnitVector(self, position):
        x_vector = 0
        y_vector = 0

        if position[0] > self.x:
            x_vector = 1
        else:
            x_vector = -1
        
        if position[1] > self.y:
            y_vector = 1
        else:
            y_vector = -1
        
        return (x_vector, y_vector)

    def applyGravity(self, position, mass, grav_mod, print_flag=False):
        if print_flag: print(self.mSpeed)
        GRAV_CONST = 6.67 * 10 ** -11
        unit_vector = self.getUnitVector(position)
        self.delta_x = 0
        self.delta_y = 0

        
        radius = sqrt(abs(position[0] - self.x)**2 + abs(position[1] - self.y) **2)

        g_vector = grav_mod * ((GRAV_CONST * mass) / radius ** 2)

        y_vector = self.y - position[1]
        x_vector = self.x - position[0]

        angle_between_rads = atan2(y_vector, x_vector)

        angle_between_degrees = degrees(angle_between_rads)

        if angle_between_degrees == 0 or angle_between_degrees == 180:
            if print_flag: print("Horizontally Aligned")
            self.delta_x = g_vector * unit_vector[0]
            self.delta_y = 0
        elif angle_between_degrees == 90 or angle_between_degrees == 270:
            if print_flag: print("Vertically Aligned")
            self.delta_x = 0
            self.delta_y = g_vector * unit_vector[1]
        else:
            if print_flag: print("Any Other Alignment")
            active_angle = angle_between_degrees % 90
            active_angle_rads = radians(active_angle)
            
            y_component = g_vector * sin(active_angle_rads)
            self.delta_y = y_component * unit_vector[1]
            if print_flag: print(self.delta_y)

            x_component = g_vector * cos(active_angle_rads)
            self.delta_x = x_component * unit_vector[0]
            if print_flag: print(self.delta_x)

        if print_flag:
            print('-------------------------------')
            print(frames)
            print(self.delta_x, self.delta_y)
            print(self.mSpeed)
            print(self.delta_x + self.mSpeed[0] > self.delta_x)
            print('-------------------------------')

        self.mSpeed = (self.mSpeed[0] + self.delta_x, self.mSpeed[1] + self.delta_y)

    def checkCollision(self, bounds):
        if self.x <= 0 or self.x >= bounds[0]:
            if self.x <= 0: 
                self.x = 1 
            elif self.x >= bounds[0]: 
                self.x = bounds[0]-self.radius
            self.mSpeed = (-self.mSpeed[0], self.mSpeed[1])
        if self.y <= 0 or self.y >= bounds[1]:
            if self.y <= 0: 
                self.y = 1 
            elif self.y >= bounds[1]:
                self.y = bounds[1]-self.radius
            self.mSpeed = (-self.mSpeed[1], self.mSpeed[1])

    def draw (self, surface):
        surface.blit(self.image, (self.x, self.y))

ball = Ball((width/4, width/4), 15, 2*10**11, (0, 255, 0), (.075, -.15))

ball2 = Ball((width - width/4, height - height/4), 15, 2*10**11, (0, 0, 255), (-.075, .15))

ball3 = Ball((width/2, height/2), 15, 2*10**11, (255, 0, 0))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    screen.fill((0, 0, 0))

    entities = [ball, ball2, ball3]

    for entity in entities:
        for body in entities:
            if body != entity:
                print('sumting')
                entity.applyGravity((body.x, body.y), body.mass, 1)
                entity.move()
                entity.drawTrail(screen, (255, 255, 255))
            else:
                entity.draw(screen)
    
    pygame.display.update()

    frames += 1