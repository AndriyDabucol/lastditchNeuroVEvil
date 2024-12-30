from pygame.time import get_ticks

class Timer:

    def __init__(self, duration):
        self.duration = duration
        self.start_time = 0
        self.loop = False
        self.func = False
        self.active = False
        self.finished = False

    def activate(self):
        self.active = True
        self.finished = False
        self.start_time = get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0
    
    def timeout(self):
        self.finished = True
        self.active = False
        if self.loop: 
            self.activate()

        if self.func:
            return self.func()
        else:
            return True

    def update(self):
        if self.active:
            current_time = get_ticks()
            if current_time - self.start_time >= self.duration:
                self.timeout()



