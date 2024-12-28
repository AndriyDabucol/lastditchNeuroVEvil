import pygame

pygame.init()


class Gamestate:
    scene = ''

class Fighter:
    name = 'Fighter'
    states = ['neutral', 'dodge-right', 'dodge-left', 'block', 'attack-right', 'attack-left']
    current_state = 'neutral'
    prev_state = ''
    health = 100
    opponent = 0

    def attack(self):
        if self.opponent.current_state == 'attack-right' and self.current_state == 'attack-left' and self.prev_state == 'dodge-left':
            self.opponent.health -= 10
            print(f'{self.opponent.name} was hit by {self.name}! 10 points damage!')
        elif self.opponent.current_state == 'attack-left' and self.current_state == 'attack-right' and self.prev_state == 'dodge-right':
            self.opponent.health -= 10
            print(f'{self.opponent.name} was hit by {self.name}! 10 points damage!')
        
        if self.opponent.current_state == 'block' or self.opponent.current_state == 'dodge-left' or self.opponent.current_state == 'dodge-right'

        




pygame.init()
screen = pygame.display.set_mode((256*2, 224*2))
world_surf = pygame.Surface((256,224))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    world_surf.fill("white")
    pygame.transform.scale2x(world_surf, screen)
    screen.blit(world_surf, (0,0))

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()