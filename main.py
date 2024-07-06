import pygame


class Block_Entity(pygame.sprite.Sprite):
    def __init__(self, groups, width, height):
        super().__init__(groups)
        self.direction = pygame.Vector2()
        self.speed = 0
        self.image = pygame.Surface((width, height))
        self.image.fill("blue")
        self.rect = self.image.get_frect(topleft=(0, 0))

    def update(self, dt):
        self.direction.x = 0.5
        self.direction.y = 1

        self.rect.center += self.direction * self.speed * dt


class Circle_Entity(pygame.sprite.Sprite):
    def __init__(self, groups, radius):
        super().__init__(groups)
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, (255, 0, 0), (radius, radius), radius)

        self.rect = self.image.get_rect()

        self.direction = pygame.Vector2(1, 1)
        self.speed = 200
        self.gravity = 2

    def update(self, dt):
        self.speed += self.gravity * dt
        self.rect.x += self.speed * self.direction.x * dt
        self.rect.y += self.speed * self.direction.y * dt

        if self.rect.left <= 0:
            self.rect.left = 0
            self.direction.x *= -1
        if self.rect.right >= 800:
            self.rect.right = 800
            self.direction.x *= -1

        if self.rect.top <= 0:
            self.rect.top = 0
            self.speed *= -0.8
            self.direction.y *= -1
        if self.rect.bottom >= 600:
            self.rect.bottom = 600
            self.speed *= -0.8
            self.direction.y *= -1

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def click_to_spawn(all_sprites):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        new_block = Block_Entity(all_sprites, 50, 50)
        new_block.rect.center = pygame.mouse.get_pos()
    elif pygame.mouse.get_pressed()[2]:
        new_circle = Circle_Entity(all_sprites, 25)
        new_circle.rect.center = (mouse_x, mouse_y)


# NOTE: General Setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True
pygame.display.set_caption("Movement")
clock = pygame.time.Clock()

# NOTE: Entity Creation
all_sprites = pygame.sprite.Group()
blocky_boy = Block_Entity(all_sprites, 100, 50)
circle_entity = Circle_Entity(all_sprites, 25)
all_sprites.add(circle_entity)

click_event = pygame.event.custom_type()

while running:
    dt = clock.tick(60) / 1000

    # Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_to_spawn(all_sprites)

    # update
    all_sprites.update(dt)

    # draw game
    display_surface.fill("white")

    all_sprites.draw(display_surface)

    pygame.display.flip()

pygame.quit()
