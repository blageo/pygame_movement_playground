import pygame


class Block_Entity(pygame.sprite.Sprite):
    def __init__(self, groups, width, height):
        super().__init__(groups)
        self.speed = 0
        self.direction = 0
        self.image = pygame.Surface((width, height))
        self.image.fill("blue")
        self.rect = self.image.get_frect(topleft=(0, 0))

    def update(self, dt, all_sprites):
        pass


class Circle_Entity(pygame.sprite.Sprite):
    def __init__(self, groups, radius, init_speed, init_direction):
        super().__init__(groups)
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, (255, 0, 0), (radius, radius), radius)

        self.rect = self.image.get_rect()

        self.direction = self.direction = (
            init_direction.normalize()
            if init_direction.length() > 0
            else pygame.Vector2(1, 1)
        )
        self.speed = init_speed
        self.gravity = 2

    def update(self, dt, all_sprites):
        self.speed += self.gravity * dt
        self.rect.x += self.speed * self.direction.x * dt
        self.rect.y += self.speed * self.direction.y * dt
        self.handle_collision(all_sprites)

        if self.rect.left <= 0:
            self.rect.left = 0
            self.direction.x *= -1
        if self.rect.right >= 800:
            self.rect.right = 800
            self.direction.x *= -1

        if self.rect.top <= 0:
            self.rect.top = 0
            self.speed *= 0.8
            self.direction.y *= -1
        if self.rect.bottom >= 600:
            self.rect.bottom = 600
            self.speed *= 0.8
            self.direction.y *= -1

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def handle_collision(self, all_sprites):
        for sprite in all_sprites:
            if sprite == self:
                continue
            if pygame.sprite.collide_circle(self, sprite):
                self.bounce_off(sprite)

    def bounce_off(self, other):
        if isinstance(other, Circle_Entity):
            self.direction *= -1
            other.direction *= -1
        elif isinstance(other, Block_Entity):
            if abs(self.rect.bottom - other.rect.top) < self.radius:
                self.direction.y *= -1
            elif abs(self.rect.top - other.rect.bottom) < self.radius:
                self.direction.y *= -1
            elif abs(self.rect.right - other.rect.right) < self.radius:
                self.direction.x *= -1
            elif abs(self.rect.left - other.rect.left) < self.radius:
                self.direction.x *= -1


def click_to_spawn(all_sprites):
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Capture mouse speed and direction
    mouse_speed = pygame.mouse.get_rel()
    init_speed = max(abs(mouse_speed[0]), abs(mouse_speed[1]))
    init_direction = pygame.Vector2(mouse_speed[0], mouse_speed[1])
    if pygame.mouse.get_pressed()[0]:
        new_block = Block_Entity(all_sprites, 50, 50)
        new_block.rect.center = pygame.mouse.get_pos()
        all_sprites.add(new_block)
    elif pygame.mouse.get_pressed()[2]:
        new_circle = Circle_Entity(all_sprites, 25, init_speed, init_direction)
        new_circle.rect.center = (mouse_x, mouse_y)
        all_sprites.add(new_circle)


def clear_all_sprites(all_sprites):
    all_sprites.empty()


# NOTE: General Setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True
pygame.display.set_caption("Movement")
clock = pygame.time.Clock()

# NOTE: Entity Creation
all_sprites = pygame.sprite.Group()

click_event = pygame.event.custom_type()

while running:
    dt = clock.tick(60) / 1000

    # Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_to_spawn(all_sprites)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                clear_all_sprites(all_sprites)

    # update
    for sprite in all_sprites:
        sprite.update(dt, all_sprites)

    # draw game
    display_surface.fill("white")

    all_sprites.draw(display_surface)

    pygame.display.flip()

pygame.quit()
