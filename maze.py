from pygame import *
font.init()
font1 = font.SysFont('Times New Roman', 70)
win = font1.render(
    'Great Job', True, (255, 215, 0)
)
lose = font1.render(
    'LAAAME', True, (255, 0, 0)
)
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

kick = mixer.Sound('kick.ogg')
money = mixer.Sound('money.ogg')



#создай окно игры
window = display.set_mode((700, 500))
display.set_caption('Лабиринт')

#классы
class GameSprite(sprite.Sprite):
    def __init__(self, filename, w, h, speed, x, y):
        super().__init__()
        self.image = transform.scale(
            image.load(filename),
            (w, h)
        )
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y -=10
        elif keys_pressed[K_s] and self.rect.y < 440:
            self.rect.y +=10
        elif keys_pressed[K_a] and self.rect.x > -1:
            self.rect.x -=10
        elif keys_pressed[K_d] and self.rect.x < 640:
            self.rect.x +=10

class Enemy(GameSprite):
    direction = 'left'
    speed = 1
    def update(self):
        if self.rect.x <= 470:
            self.direction = 'right'
        elif self.rect.x >= 700 - 65:
            self.direction = 'left'

        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, w, h, color, x, y):
        super().__init__()
        self.image = Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#персонажи и объекты
player = Player('hero.png', 65, 65, 15, 50, 400)
enemy = Enemy('cyborg.png', 65, 65, 8, 400, 220)
treasure = GameSprite('treasure.png', 65, 65, 15, 620, 420)
wall1 = Wall(60, 130, (0,0,0), 200, 300)
wall2 = Wall(130, 60, (0,0,0), 200, 300)
wall3 = Wall(130, 60, (0,0,0), 300, 300)
wall4 = Wall(60, 130, (0,0,0), 420, 250)
wall5 = Wall(60, 130, (0,0,0), 420, 150)
wall6 = Wall(60, 130, (0,0,0), 420, 100)
wall7 = Wall(130, 60, (0,0,0), 420, 100)
wall8 = Wall(60, 130, (0,0,0), 200, 370)
wall9 = Wall(60, 130, (0,0,0), 500, 100)

walls = sprite.Group()
walls.add(wall1, wall2, wall3, wall4, wall5, wall6, wall7, wall8, wall9)

#задай фон сцены
background = transform.scale(
    image.load('background.jpg'),
    (700, 500)
)
game = True
finish = False

clock = time.Clock()
FPS = 60

#игровой цикл
while game:
    if finish == False:
        window.blit(background, (0, 0))
        wall1.draw_wall()
        wall2.draw_wall()
        wall3.draw_wall()
        wall4.draw_wall()
        wall5.draw_wall()
        wall6.draw_wall()
        wall7.draw_wall()
        wall8.draw_wall()
        wall9.draw_wall()
        player.reset()
        player.update()
        enemy.reset()
        enemy.update()
        treasure.reset()

        if len(sprite.spritecollide(player, walls, False)) > 0:
            player.rect.x = 50
            player.rect.y = 400
        elif sprite.collide_rect(player, treasure):
            window.blit(win, (200, 200))
            finish = True
            money.play()
        elif sprite.collide_rect(player, enemy):
            window.blit(lose, (200, 200))
            finish = True
            kick.play()

        

    for e in event.get():
        if e.type == QUIT:
            game = False
    display.update()
    clock.tick(FPS)

