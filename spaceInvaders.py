import pygame
from pygame import mixer
import random

mixer.init() 
mixer.music.load("assets/fundo.wav") 
mixer.music.set_volume(0.7) 
mixer.music.play() 

def abrirArquivo():
    abrir = open("logins.txt", "a")
    abrir.close()

def gravarArquivo():
    arquivo = open("logins.txt","a")
    linhasParaOArquivo = ["Nome: ", nome," - E-mail: ", email + "\n"]
    for lnh in linhasParaOArquivo:
        arquivo.write(lnh)
    arquivo.close()

nome = str(input('Digite seu nome: '))
confEmail = False
while confEmail == False:
    email = str(input('Digite seu e-mail: '))
    if '@' in email and '.' in email:
        try:
            gravarArquivo()
            confEmail = True
        except:
            abrirArquivo()
    else:
        print("E-mail inválido")

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

tempo = pygame.time.Clock()
fps = 60

largura = 600
altura = 800

screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Space Invanders')

gameEvents = pygame.event

font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)
font50 = pygame.font.SysFont('Constantia', 50)

explosion_fx = pygame.mixer.Sound("assets/explosion.wav")
explosion_fx.set_volume(0.25)

explosion2_fx = pygame.mixer.Sound("assets/explosion2.wav")
explosion2_fx.set_volume(0.25)

laser_fx = pygame.mixer.Sound("assets/laser.wav")
laser_fx.set_volume(0.25)

linhas = 5
colunas = 5
alien_pausa = 1000
alien_ultimo_tiro = pygame.time.get_ticks()
contagem = 3
ultima_contagem = pygame.time.get_ticks()
game_over = 0

red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

bg = pygame.image.load("assets/bg.png")

def draw_bg():
    screen.blit(bg, (0, 0))

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

class Nave(pygame.sprite.Sprite):
    def __init__(self, x, y, vida):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vida_inicial = vida
        self.vida_restante = vida
        self.ultimo_tiro = pygame.time.get_ticks()

    def update(self):
        velocidade = 8
        pausa = 500 
        game_over = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= velocidade
        if key[pygame.K_RIGHT] and self.rect.right < largura:
            self.rect.x += velocidade

        tempo_agora = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and tempo_agora - self.ultimo_tiro > pausa:
            laser_fx.play()
            bullet = Balas(self.rect.centerx, self.rect.top)
            bullet_grupo.add(bullet)
            self.ultimo_tiro = tempo_agora

        self.mask = pygame.mask.from_surface(self.image)

        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.vida_restante > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.vida_restante / self.vida_inicial)), 15))
        elif self.vida_restante <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_grupo.add(explosion)
            self.kill()
            game_over = -1
        return game_over

class Balas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_grupo, True):
            self.kill()
            explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_grupo.add(explosion)

class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/alien" + str(random.randint(1, 5)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction

class Alien_Balas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        if self.rect.top > altura:
            self.kill()
        if pygame.sprite.spritecollide(self, nave_grupo, False, pygame.sprite.collide_mask):
            self.kill()
            explosion2_fx.play()
            nave.vida_restante -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_grupo.add(explosion)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, tamanho):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"assets/exp{num}.png")
            if tamanho == 1:
                img = pygame.transform.scale(img, (20, 20))
            if tamanho == 2:
                img = pygame.transform.scale(img, (40, 40))
            if tamanho == 3:
                img = pygame.transform.scale(img, (160, 160))

            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0


    def update(self):
        explosion_speed = 3
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

nave_grupo = pygame.sprite.Group()
bullet_grupo = pygame.sprite.Group()
alien_grupo = pygame.sprite.Group()
alien_bullet_grupo = pygame.sprite.Group()
explosion_grupo = pygame.sprite.Group()


def create_aliens():
    for row in range(linhas):
        for item in range(colunas):
            alien = Aliens(100 + item * 100, 100 + row * 70)
            alien_grupo.add(alien)
create_aliens()

nave = Nave(int(largura / 2), altura - 100, 3)
nave_grupo.add(nave)

def main_menu():
    while True:
        screen.blit(bg, (0, 0))
        draw_text('MENU', font50, white, int(largura / 2 - 80), int(altura / 2))
        draw_text('ENTER : INICIAR', font40, white, int(largura / 2 - 150), int(altura / 2 + 60))
        draw_text('ESC : SAIR', font40, white, int(largura / 2 - 93), int(altura / 2 + 100))

        for event in gameEvents.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                run = True
                return run
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
        pygame.display.update()

main_menu()


run = True

while run:
    tempo.tick(fps)

    draw_bg()

    if contagem == 0:
        tempo_agora = pygame.time.get_ticks()

        if tempo_agora - alien_ultimo_tiro > alien_pausa and len(alien_bullet_grupo) < 5 and len(alien_grupo) > 0:
            attacking_alien = random.choice(alien_grupo.sprites())
            alien_bullet = Alien_Balas(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            alien_bullet_grupo.add(alien_bullet)
            alien_ultimo_tiro = tempo_agora

        if len(alien_grupo) == 0:
            game_over = 1

        if game_over == 0:
            game_over = nave.update()

            bullet_grupo.update()
            alien_grupo.update()
            alien_bullet_grupo.update()
        else:
            if game_over == -1:
                draw_text('VOCÊ PERDEU!', font40, white, int(largura / 2 - 130), int(altura / 2 + 50))
            if game_over == 1:
                draw_text('VOCÊ GANHOU!', font40, white, int(largura / 2 - 140), int(altura / 2 + 50))

    if contagem > 0:
        draw_text('PREPARE-SE!', font40, white, int(largura / 2 - 110), int(altura / 2 + 50))
        draw_text(str(contagem), font40, white, int(largura / 2 - 10), int(altura / 2 + 100))
        count_timer = pygame.time.get_ticks()
        if count_timer - ultima_contagem > 1000:
            contagem -= 1
            ultima_contagem = count_timer

    explosion_grupo.update()

    nave_grupo.draw(screen)
    bullet_grupo.draw(screen)
    alien_grupo.draw(screen)
    alien_bullet_grupo.draw(screen)
    explosion_grupo.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
