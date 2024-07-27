import pygame
import random
import sys
import os

# Ініціалізація Pygame
pygame.init()

# Налаштування екрану
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Україна відбиває напад")

# Колір
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# Завантаження зображень та музики
def load_image(name):
    return pygame.image.load(os.path.join('assets', name)).convert_alpha()


def load_sound(name):
    return pygame.mixer.Sound(os.path.join('assets', name))


def load_music(name):
    pygame.mixer.music.load(os.path.join('assets', name))


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


# Завантаження ресурсів
defender_img = load_image('defender.png')
attacker_img = load_image('attacker.png')
target_img = load_image('target.png')
background_img = load_image('background.webp')
explosion_img = load_image('explosion.png')
explosion_large_img = load_image('explosion_large.png')
bullet_img = load_image('bullet.png')


# Налаштування шрифта та музики
font = pygame.font.SysFont(None, 36)
button_font = pygame.font.SysFont(None, 48)
load_music('background_music.mp3')
pygame.mixer.music.set_volume(0.3)
hit_sound = load_sound('hit_sound.mp3')
explosion_sound = load_sound('explosion_sound.mp3')
bullet_sound = load_sound('hit_sound.mp3')
pygame.mixer.music.play(-1)  # Циклічне відтворення музики


# Клас для пострілів
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(bullet_img, (10, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 7

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


# Клас для захисника
class Defender(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(defender_img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 30)
        self.speed = 5
        self.health = 100

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.x = max(0, min(self.rect.x, WIDTH - 50))

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        bullet_sound.play()

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0


# Клас для атакуючих
class Attacker(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(attacker_img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 50)
        self.rect.y = -50
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.kill()


# Клас для цілей
class Target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(target_img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 50)
        self.rect.y = -50
        self.speed = random.randint(2, 4)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.kill()


# Клас для вибухів
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, large=False):
        super().__init__()
        self.image = pygame.transform.scale(
            explosion_large_img if large else explosion_img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.timer = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.timer > 500:
            self.kill()


# Клас для кнопок
class Button:
    def __init__(self, text, pos, size, bg_color, text_color):
        self.text = text
        self.pos = pos
        self.size = size
        self.bg_color = bg_color
        self.text_color = text_color
        self.rect = pygame.Rect(pos, size)
        self.hovered = False

    def draw(self, surface):
        color = YELLOW if self.hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect)
        draw_text(self.text, button_font, self.text_color, surface, self.rect.centerx, self.rect.centery)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.hovered and mouse_pressed[0]


# Головне меню
def main_menu():
    buttons = [
        Button('Почати гру', (WIDTH // 2 - 100, HEIGHT // 2 - 100), (200, 50), GREEN, BLACK),
        Button('Налаштування', (WIDTH // 2 - 100, HEIGHT // 2), (200, 50), GREEN, BLACK),
        Button('Інструкції', (WIDTH // 2 - 100, HEIGHT // 2 + 100), (200, 50), GREEN, BLACK),
        Button('Вийти', (WIDTH // 2 - 100, HEIGHT // 2 + 200), (200, 50), RED, BLACK)
    ]

    while True:
        screen.blit(background_img, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)
            if button.is_clicked(mouse_pos, mouse_pressed):
                if button.text == 'Почати гру':
                    return
                elif button.text == 'Налаштування':
                    settings_menu()
                elif button.text == 'Інструкції':
                    instructions_menu()
                elif button.text == 'Вийти':
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


# Налаштування меню
def settings_menu():
    while True:
        screen.fill(BLACK)
        draw_text('Налаштування (Натисніть ESC для повернення)', font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 100)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return


# Інструкції меню
def instructions_menu():
    while True:
        screen.fill(BLACK)
        draw_text('Інструкції (Натисніть ESC для повернення)', font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 100)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return


# Гра
def game_loop():
    global all_sprites, bullets

    all_sprites = pygame.sprite.Group()
    attackers = pygame.sprite.Group()
    targets = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    defender = Defender()
    all_sprites.add(defender)

    score = 0
    level = 1
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    defender.shoot()

        # Додаємо нових атакуючих та цілі
        if random.randint(1, 20) == 1 + level:
            attacker = Attacker()
            all_sprites.add(attacker)
            attackers.add(attacker)
        if random.randint(1, 30) == 1 + level:
            target = Target()
            all_sprites.add(target)
            targets.add(target)

        # Оновлюємо спрайти
        all_sprites.update()
        bullets.update()
        explosions.update()

        # Перевіряємо наявність зіткнень
        for bullet in pygame.sprite.groupcollide(bullets, targets, True, True):
            explosion = Explosion(bullet.rect.centerx, bullet.rect.centery, large=True)
            all_sprites.add(explosion)
            explosions.add(explosion)
            score += 10
            explosion_sound.play()

        for bullet in pygame.sprite.groupcollide(bullets, attackers, True, True):
            explosion = Explosion(bullet.rect.centerx, bullet.rect.centery)
            all_sprites.add(explosion)
            explosions.add(explosion)
            score += 5
            explosion_sound.play()

        if pygame.sprite.spritecollideany(defender, attackers):
            hit_sound.play()
            defender.take_damage(20)
            for attacker in pygame.sprite.spritecollide(defender, attackers, dokill=False):
                explosion = Explosion(attacker.rect.centerx, attacker.rect.centery)
                all_sprites.add(explosion)
                explosions.add(explosion)
                attacker.kill()

        if defender.health <= 0:
            draw_text(f"Гру програно! Рахунок: {score}", font, RED, screen, WIDTH // 2, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.wait(2000)
            return

        # Очищаємо екран
        screen.blit(background_img, (0, 0))

        # Малюємо спрайти
        all_sprites.draw(screen)
        bullets.draw(screen)

        # Малюємо рахунок
        draw_text(f"Рахунок: {score}", font, BLACK, screen, WIDTH // 2, 30)

        # Оновлюємо екран
        pygame.display.flip()
        clock.tick(30)

        # Збільшуємо рівень складності
        score += 1
        if score % 100 == 0:
            level += 1


# Головна функція
def main():
    while True:
        main_menu()
        game_loop()


if __name__ == "__main__":
    main()
