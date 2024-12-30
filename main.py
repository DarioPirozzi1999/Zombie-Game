import pygame
import random
import time

pygame.init()

screen_width = 900
screen_height = 700
screen = pygame.display.set_mode([screen_width, screen_height])

lives = 3
score = 0
level = 1
font = pygame.font.Font(None, 36)
level_time_limit = 20  # Time limit for each level in seconds

pygame.display.set_caption("Zombie Game")
clock = pygame.time.Clock()

def set_background(image):
    bg = pygame.image.load(image)
    bg = pygame.transform.scale(bg, [screen_width, screen_height])
    screen.blit(bg, (0, 0))


class CrossHair(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("CrossHair.png")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Zombies(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()



zombies_list = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
crosshair = CrossHair()
all_sprites.add(crosshair)

img = ["Zombie.png", "FlagZombie.png", "CaveZombie.png"]


def spawn_zombies(level):
    zombies_list.empty()
    for i in range(level * 5):
        spawn = Zombies(random.choice(img))
        spawn.rect.x = random.randrange(200, 700)
        spawn.rect.y = random.randrange(100, 700)
        zombies_list.add(spawn)
        all_sprites.add(spawn)



spawn_zombies(level)


running = True
start_time = time.time()

while running:
    screen.fill((0, 0, 0))
    set_background("Background.png")

   
    elapsed_time = time.time() - start_time
    remaining_time = max(0, level_time_limit - int(elapsed_time))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
           
            hits = [z for z in zombies_list if z.rect.collidepoint(event.pos)]
            for hit in hits:
                zombies_list.remove(hit)
                all_sprites.remove(hit)
                score += 10

   
    all_sprites.update()

    
    all_sprites.draw(screen)

    
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    level_text = font.render(f"Level: {level}", True, (255, 255, 255))
    timer_text = font.render(f"Time Left: {remaining_time}s", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))
    screen.blit(level_text, (10, 90))
    screen.blit(timer_text, (10, 130))

    
    if remaining_time == 0:
        lives -= 1
        if lives == 0:
            running = False  
        else:
            
            spawn_zombies(level)
            start_time = time.time() 

    
    if len(zombies_list) == 0:
        level += 1
        spawn_zombies(level)
        start_time = time.time()  

    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()