import pygame
from timer import Timer
import random
import math

pygame.mixer.init(44100, -16, 2, 2048) # (frequency, size, channels, buffer)


width = 160
height = 144
pygame.init()
screen = pygame.display.set_mode((width*4, height*4))
world_surf = pygame.Surface((width,height))
clock = pygame.time.Clock()
running = True

dt = clock.tick() / 1000 

gui = pygame.image.load('sprites/GUI_fight1.png').convert_alpha()
text_font = pygame.font.SysFont(None, 14)

on_main_menu = True
endscreen = False


music = pygame.mixer.Sound('neurovevil.ogg')
music.set_volume(0.5)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, False, text_col)

    world_surf.blit(img, (x, y))



class Gamestate:
    scene = ''

class Fighter:
    def __init__(self, name):

        self.name = name
    
    states = ['neutral', 'dodge', 'block', 'attack']
    current_state = states[0]
    prev_state = ''
    health = 100
    energy = 100
    opponent = 0

    curr_text = ''

    def change_current_text(self, text):
        self.curr_text = text
            


class Neuro(Fighter):

    cooldown_time = 1000
    cooldown_timer = Timer(1000)
    cooldown_timer.activate()

    regenerate_timer = Timer(3000)
    health = 100

    gui_pos = pygame.Vector2(0, 0)
    gui_shake = 0

    got_hit = False

    sprites = {
        'neutral_hands_sprites' : pygame.image.load('sprites/neuro3.png').convert_alpha(),
        'attack_hands_sprites' : pygame.image.load('sprites/neuro4.png').convert_alpha(),
        'block_hands_sprites' :  pygame.image.load('sprites/neuro5.png').convert_alpha()
    }
    current_sprite =  sprites['neutral_hands_sprites']

    hands_pos = pygame.Vector2( width/2 - 54, 60)

    

    def attack(self):
        op_state = self.opponent.current_state 
        curr_state = self.current_state
        prev_state = self.prev_state

        if not self.cooldown_timer.finished:
            return
        
        self.current_sprite = self.sprites['attack_hands_sprites']

        self.energy -= 10
        if op_state == 'neutral' and self.cooldown_timer.finished:
            self.cooldown_timer.duration = self.cooldown_time
            self.cooldown_timer.activate() 

            self.opponent.fight_or_flight()
            

        

        '''

        if op_state == 'attack' and curr_state == 'attack' and prev_state == 'dodge' and self.cooldown_timer.finished:
            self.cooldown_timer.duration = self.cooldown_time
            self.cooldown_timer.activate() 

            self.opponent.take_damage(dmg_amount=10, enrgy_dplted=5)
            
            print(f'{self.opponent.name} was hit by {self.name}! 10 points damage!')
        
        if op_state == 'dodge' and self.cooldown_timer.finished:
            self.cooldown_timer.duration = self.cooldown_time + 500
            self.cooldown_timer.activate()

            print(f'{self.opponent.name} dodged!')

        '''



            
    def update(self):
        self.cooldown_timer.update()
        self.regenerate_timer.update()

        if not self.regenerate_timer.active:
            self.regenerate_timer.duration = 4000
            self.regenerate_timer.activate()
            if self.health < 100:
                self.health += 2



        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.current_state = self.states[3]
            self.attack()

        if self.cooldown_timer.finished:
            self.current_state = 'neutral'
        
        if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
            self.current_state = 'block'
            print('block')

        if self.got_hit == True:
            self.gui_shake += 0.8
            self.gui_pos.y += math.sin(self.gui_shake) * 2
            if self.gui_shake >= (math.pi*8):
                self.gui_pos.y = 0
                self.gui_shake = 0
                self.got_hit = False

        if self.current_state == 'neutral':
            self.current_sprite = self.sprites['neutral_hands_sprites']
        elif self.current_state == 'block':
            self.current_sprite = self.sprites['block_hands_sprites']

        world_surf.blit(self.current_sprite, (self.hands_pos.x, self.hands_pos.y))
        world_surf.blit(gui, (self.gui_pos.x, self.gui_pos.y))

        draw_text(str(self.health), text_font, 'black', 122, 128)
        

        
    
    def take_damage(self, dmg_amount, flashes):

        if self.current_state == 'block':
            dmg_amount -= 8
        self.health -= dmg_amount


        # self.flashes = flashes
        self.got_hit = True

        #print(f'Neuro - Damage taken: {dmg_amount}, energy_drained: {enrgy_dplted}')
    



class Evil(Fighter):

    cooldown_time = random.randint(2000, 6000)
    cooldown_timer = Timer(cooldown_time)
    cooldown_timer.activate()

    regenerate_timer = Timer(1500)

    defensive_duration = 1000
    offensive_duration = random.randint(1000, 3000)
    rtrn_neutral_timer = Timer(0)

    flash_timer = Timer(200)

    pos = pygame.Vector2((width / 2 -32, height/2 - 32))

    sprites = {
        'neutral': pygame.image.load('sprites/evil-neuro1.png').convert_alpha(),
        'blank': pygame.image.load('sprites/transparent.png').convert_alpha()
    }

    current_sprite = sprites['neutral']
    flashes = 0
    anim_speed = 2

    bob = 0
    bob_freq= 0.1
    shake = 0

    time_before_freak = 1200

    show_dodge = False

    

    def update(self):
        self.rtrn_neutral_timer.update()
        self.cooldown_timer.update()
        self.flash_timer.update()
        self.regenerate_timer.update()

        if not self.regenerate_timer.active:
            self.regenerate_timer.duration = 1500
            self.regenerate_timer.activate()
            if self.health < 100:
                self.health += 2

        if not self.rtrn_neutral_timer.active:
            self.current_state = 'neutral'

            self.cooldown_timer.duration = random.randint(2000, 6000)
            self.cooldown_timer.activate()

        

        if self.current_state == 'neutral':
            self.bob += self.bob_freq
            self.pos.y += math.sin(self.bob) / 5 
            if self.bob >= (math.pi*2):
                self.bob = 0

        draw_text(str(self.health), text_font, 'black', 20, 20)

        

        self.flash()
        self.dodge_anim()
        world_surf.blit(self.current_sprite, (self.pos.x, self.pos.y))


    
    def fight_or_flight(self):
        self.rtrn_neutral_timer.duration = self.defensive_duration
        self.rtrn_neutral_timer.activate()

        self.prev_state = self.current_state

        self.current_state = self.states[random.randint(0,2)]

        print(f'currently in {self.current_state}')

        if self.current_state == self.states[0]:
            
            self.take_damage(5,8)

            self.change_current_text(f'{self.name} was hit by {self.opponent.name}! 10 points damage and 5 points of energy depleted!')
        
        if self.current_state == self.states[2]:
            self.opponent.energy -= 5
            self.take_damage(dmg_amount=2, flashes=4)
            self.change_current_text(f'{self.name} blocked and only sustained 2 points of damage! {self.name} lost 15 points of energy!')

        if self.current_state == self.states[1]:
            self.show_dodge = True
            self.energy -= 10
            self.change_current_text(f'{self.name} dodged and sustained no damage! {self.name} lost 10 points of energy!')

        

        

    def attack(self):
        self.opponent.take_damage(10, 0)
        

    def flash(self):
        if self.flashes > 0 and not self.flash_timer.active:
            self.flash_timer.duration = 50
            self.flash_timer.activate()

            if self.current_sprite == self.sprites['neutral']:
                self.current_sprite = self.sprites['blank']
            elif self.current_sprite == self.sprites['blank']:
                self.current_sprite = self.sprites['neutral']
            self.flashes -= 1
    
    def dodge_anim(self):
        if self.show_dodge:
            self.shake += 0.1
            self.pos.x += math.sin(self.shake) * 3
            if self.shake >= (math.pi*2):
                self.prev_state = self.current_state
                self.shake = 0
                self.pos.x = width /2 -32
                self.show_dodge = False
                self.attack()
            
    
    def take_damage(self, dmg_amount, flashes):
        self.health -= dmg_amount

        self.flashes = flashes
        

        # print(f'Damage taken: {dmg_amount}, energy_drained: {enrgy_dplted}')




neuro = Neuro(name="Neuro")
evil = Evil(name="Evil-Neuro")


neuro.opponent = evil
evil.opponent = neuro

initialize = False
press_cooldown = Timer(1000)

menus_initial = False

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    world_surf.fill("white")

    press_cooldown.update()

    if on_main_menu:
        press_cooldown.activate()
        world_surf.blit(pygame.image.load('sprites/GUI_fight3.png').convert_alpha(), (0, 0))

        initialize = False
       

        music.stop()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] :
            on_main_menu = False
    elif endscreen:
        
        world_surf.blit(pygame.image.load('sprites/GUI_fight2.png').convert_alpha(), (0, 0))

        music.stop()
        keys = pygame.key.get_pressed()

        draw_text('SHIFT', text_font, 'white', 10, 100)
        if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
            endscreen = False
            on_main_menu = True
    else:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        
        if not initialize:
            music.play(loops=-1)
            music_playing = True

            neuro = Neuro(name="Neuro")
            evil = Evil(name="Evil-Neuro")


            neuro.opponent = evil
            evil.opponent = neuro

            initialize = True


            


        # fill the screen with a color to wipe away anything from last frame
        
        
        
        # RENDER YOUR GAME HERE
        
        evil.update()
        neuro.update()

        if neuro.health <= 0:
            on_main_menu = True

        if evil.health <= 0:
            endscreen = True

        neuro.opponent = evil
        evil.opponent = neuro
        #current_text = neuro.curr_text
        # flip() the display to put your work on screen
        #draw_text(current_text, text_font, 'black', 5, 115)
        

    pygame.transform.scale_by(world_surf, 4, screen)
    
    pygame.display.flip()

    

    clock.tick(60)  # limits FPS to 60

pygame.quit()