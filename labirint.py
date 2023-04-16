# Разработай свою игру в этом файле!
from pygame import *
pyinstaller --onefile labirint.py
window = display.set_mode((1200, 800))
clock = time.Clock()
                           
hp = 3
collect_coins = 0
shoot_timer = 0


class Hero(sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__()
        self.image = image.load(img)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def show(self):
        window.blit(self.image, self.rect)

    def control(self):
        global hp, game, collect_coins
        keyboard = key.get_pressed()
        if keyboard[K_w] and self.rect.y > 0:
            self.rect.y -= 5
            if sprite.spritecollide(self, walls, False):
                self.rect.y += 5
        if keyboard[K_s] and self.rect.bottom < 800:
            self.rect.y += 5
            if sprite.spritecollide(self, walls, False):
                self.rect.y -= 5
        if keyboard[K_d] and self.rect.right < 1200:
            self.rect.x += 5
            if sprite.spritecollide(self, walls, False):
                self.rect.x -= 5
        if keyboard[K_a] and self.rect.x > 0:
            self.rect.x -= 5
            if sprite.spritecollide(self, walls, False):
                self.rect.x += 5
        if self.rect.colliderect(e1.rect) or self.rect.colliderect(e2.rect):  # касание врага
            hp -= 1
            if hp == 0:
                game = 0
            self.rect.x = 100
            self.rect.y = 200
        if self.rect.colliderect(heal.rect):  # касание аптечки
            hp += 1
            heal.rect.x = -1000
        for i in coins.sprites():  # касание монетки
            if self.rect.colliderect(i.rect):
                i.rect.x = -1000
                collect_coins += 1
                if collect_coins == 3:
                    finish.rect.x = 1100

    def resize(self, w, h):
        self.image = transform.scale(self.image, (w, h))
        x, y = self.rect.x, self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Enemy(Hero):
    def __init__(self, img, x, y, steps, speed):
        super().__init__(img, x, y)
        self.steps = steps
        self.distance = 0
        self.side = 1
        self.speed = speed
        # 1  направо
        # -1 налево

    def move(self):
        self.rect.x += self.side * self.speed  # движение

        self.distance += 1  # записывает сколько прошел

        if self.distance == self.steps:  # проверяет, не пора ли развернуться
            self.distance = 0
            self.side = -self.side


class Bullet(Hero):
    def __init__(self, img, x, y, x_direction, y_direction):
        super().__init__(img, x, y)
        self.x_direction = x_direction
        self.y_direction = y_direction

    def move(self):
        self.rect.x += self.x_direction
        self.rect.y += self.y_direction


e1 = Enemy('enemy.png', 550, 500, 120, 5)
e1.resize(100, 70)

e2 = Enemy('enemy.png', 150, 200, 120, 5)
e2.resize(100, 70)

player = Hero('mario.png', 100, 200)
player.resize(50, 50)

s1 = Hero('brick.png', 100, 300)
s2 = Hero('brick.png', 200, 300)
s3 = Hero('brick.png', 300, 300)
s4 = Hero('brick.png', 400, 300)
s7 = Hero('brick.png', 900, 300)
s8 = Hero('brick.png', 800, 300)
s5 = Hero('brick.png', 400, 400)
s6 = Hero('brick.png', 800, 200)
s9 = Hero('brick.png', 400, 500)
s10 = Hero('brick.png', 1000, 300)
walls = sprite.Group()
walls.add(s1, s2, s3, s4, s5, s6, s7, s8, s9, s10)
for i in walls:
    i.resize(130, 130)

heal = Hero('heal.png', 200, 500)
heal.resize(70, 70)

finish = Hero('portal.png', -1100, 600)
finish.resize(100, 100)

c1 = Hero('money.png', 1000, 200)
c2 = Hero('money.png', 1000, 600)
c3 = Hero('money.png', 200, 600)
coins = sprite.Group()
coins.add(c1, c2, c3)
for i in coins.sprites():
    i.resize(70, 70)

fon = image.load('fon.png')
fon = transform.scale(fon, (1200, 800))

heart = image.load('heart.png')
heart = transform.scale(heart, (50, 50))

turret = Hero('tyrel.png', 100, 600)
turret.resize(100, 100)

bullets = sprite.Group()

game = 1
while game == 1:
    window.blit(fon, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            game = 2

    if player.rect.colliderect(finish.rect):
        game = 3

    player.control()
    player.show()

    walls.draw(window)
    coins.draw(window)
    bullets.draw(window)
    for b in bullets.sprites():
        b.move()
    for b in bullets.sprites():
        if b.rect.x > 1300 or b.rect.x < -100:
            bullets.remove(b)
        if b.rect.y > 900 or b.rect.y < -100:
            bullets.remove(b)
        if b.rect.colliderect(player.rect):
            bullets.remove(b)
            hp -= 1
            if hp == 0:
                game = 0
            player.rect.x = 100
            player.rect.y = 200

    e1.move()
    e1.show()
    e2.move()
    e2.show()
    turret.show()
    shoot_timer += 1
    if shoot_timer == 100:
        shoot_timer = 0
        b = Bullet('fire.png', turret.rect.x, turret.rect.y, 10, 0)
        b.resize(50, 50)
        bullets.add(b)
    heal.show()
    finish.show()
    for i in range(hp):
        window.blit(heart, (20 + 50*i, 20))

    display.update()
    clock.tick(60)

window.blit(fon, (0, 0))
font.init()
shrift = font.Font(None, 60)
if game == 0:
    lose_text = shrift.render('Игра окончена. Ты проиграл', True, (0, 0, 0))
    window.blit(lose_text, (400, 350))
    display.update()
    while True:
        for e in event.get():
            if e.type == QUIT:
                exit()
        clock.tick(60)
if game == 3:
    win_text = shrift.render('Игра окончена. Ты победил', True, (0, 0, 0))
    window.blit(win_text, (350, 350))
    display.update()
    while True:
        for e in event.get():
            if e.type == QUIT:
                exit()
        clock.tick(60)

