import pygame
import os

WIDTH, HEIGHT = 800, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("space fight")

WHITE = (255, 255, 255)
BLACK = (10, 100, 120, 0.2)

BORDER = pygame.Rect(WIDTH / 2 - 2, 0, 4, HEIGHT)

FPS = 60
VEL = 2
SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40

# roating > scaling at proper size > adding image
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(
    pygame.transform.scale(
        pygame.image.load(os.path.join("Assets", "spaceship_yellow.png")),
        (SPACESHIP_WIDTH, SPACESHIP_HEIGHT),
    ),
    90,
)

# roating > scaling at proper size > adding image
RED_SPACESHIP_IMAGE = pygame.transform.rotate(
    pygame.transform.scale(
        pygame.image.load(os.path.join("Assets", "spaceship_red.png")),
        (SPACESHIP_WIDTH, SPACESHIP_HEIGHT),
    ),
    270,
)

SPACE_IMAGE = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT)
)


def draw_window(red, yellow):
    WIN.fill(WHITE)
    WIN.blit(SPACE_IMAGE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    WIN.blit(YELLOW_SPACESHIP_IMAGE, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP_IMAGE, (red.x, red.y))

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a]:  # left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d]:  # right
        yellow.x += VEL
    if keys_pressed[pygame.K_w]:  # up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s]:  # down
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT]:  # left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT]:  # right
        red.x += VEL
    if keys_pressed[pygame.K_UP]:  # up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN]:  # down
        red.y += VEL


def main():
    red = pygame.Rect(WIDTH - SPACESHIP_WIDTH, 0, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(0, 0, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()

        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        draw_window(red, yellow)

    pygame.quit()


if __name__ == "__main__":
    main()
