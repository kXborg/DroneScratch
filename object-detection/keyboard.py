import pygame

def init():
    pygame.init()
    window = pygame.display.set_mode((500, 500))


def getKey(keyname):
    ans = False
    for event in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(keyname))
    if keyInput[myKey]:
        ans = True
    
    pygame.display.update()
    return ans


if __name__ == '__main__':
    init()