import pygame
import os

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("space fight")

WHITE = (255, 255, 255)
BLACK = (10, 100, 120)
RED = (255, 0, 0)
YELLOW = (155, 155, 0)

BORDER = pygame.Rect(WIDTH // 2 - 1, 0, 2, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

FPS = 60
VEL = 5
BULLETS_VEL = 7
MAX_BULLETS = 30
SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

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


# drawing and objects on window
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # WIN.fill(WHITE)
    WIN.blit(SPACE_IMAGE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("health: " + str(yellow_health), 1, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width(), 0))
    WIN.blit(yellow_health_text, (0, 0))

    WIN.blit(YELLOW_SPACESHIP_IMAGE, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP_IMAGE, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


# handling yellow spacship's movement
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width + VEL < BORDER.x:  # right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # up
        yellow.y -= VEL
    if (
        keys_pressed[pygame.K_s] and yellow.y + yellow.height + VEL + 10 < HEIGHT
    ):  # down
        yellow.y += VEL


# handling red spacship's movement
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + SPACESHIP_WIDTH + VEL < WIDTH:  # right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + red.height + VEL + 10 < HEIGHT:  # down
        red.y += VEL


# handling bullets
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLETS_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLETS_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(
        draw_text,
        (
            WIDTH / 2 - draw_text.get_width() / 2,
            HEIGHT / 2 - draw_text.get_height() / 2,
        ),
    )
    pygame.display.update()
    pygame.time.delay(5000)


# main function
def main():
    red = pygame.Rect(
        WIDTH - SPACESHIP_WIDTH + 10,
        HEIGHT / 2 - SPACESHIP_HEIGHT / 2,
        SPACESHIP_WIDTH,
        SPACESHIP_HEIGHT,
    )
    yellow = pygame.Rect(
        10, HEIGHT / 2 - SPACESHIP_HEIGHT / 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT
    )
    winner_text = ""
    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width,
                        yellow.y + yellow.height // 2 - 2,
                        10,
                        5,
                    )
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        if red_health <= 0:
            winner_text = "YELLOW WINS!"

        if yellow_health <= 0:
            winner_text = "RED WINS!"

        if winner_text != "":
            draw_winner(winner_text)
            break  # someone won

        # print(red_bullets, yellow_bullets)
        keys_pressed = pygame.key.get_pressed()

        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()


if __name__ == "__main__":
    main()
