import pygame

class Food(pygame.sprite.Sprite):
    loc = (0,0)
    RADIUS = 3
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([self.RADIUS*2,self.RADIUS*2])
        self.rect = pygame.draw.circle(self.image, (0,0,0), self.loc, self.RADIUS)
        
    def setLocation(self, loc):
        self.loc = loc
        
    def update(self):
        self.rect.center = self.loc