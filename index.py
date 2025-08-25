import pygame, random, sys

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Magnetic Field Dodge")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 36)

player = pygame.Rect(300, 200, 20, 20)

fields = [pygame.Rect(random.randint(0, 550), random.randint(0, 350), 40, 40)]
field_speeds = [(random.choice([-2, 2]), random.choice([-2, 2]))]

score = 0
speed = 5
running = True

start_ticks = pygame.time.get_ticks()
last_spawn_time = 0
grace_period = 3
max_fields = 35

def spawn_fields(n):
    new_fields = []
    new_speeds = []
    for _ in range(n):
        while True:
            x = random.randint(0, 550)
            y = random.randint(0, 350)
            rect = pygame.Rect(x, y, 40, 40)
            if rect.colliderect(player.inflate(200, 200)):
                continue
            new_fields.append(rect)
            new_speeds.append((random.choice([-2, 2]), random.choice([-2, 2])))
            break
    return new_fields, new_speeds

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player.x -= speed
    if keys[pygame.K_RIGHT]: player.x += speed
    if keys[pygame.K_UP]: player.y -= speed
    if keys[pygame.K_DOWN]: player.y += speed

    player.x = max(0, min(player.x, 580))
    player.y = max(0, min(player.y, 380))

    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    score = seconds

    if seconds % 5 == 0 and seconds != last_spawn_time and len(fields) < max_fields:
        last_spawn_time = seconds
        count_new = min(len(fields), max_fields - len(fields))
        new_fields, new_speeds = spawn_fields(count_new)
        fields.extend(new_fields)
        field_speeds.extend(new_speeds)

    for i, f in enumerate(fields):
        dx, dy = field_speeds[i]
        f.x += dx
        f.y += dy

        if f.left <= 0 or f.right >= 600:
            field_speeds[i] = (-dx, dy)
        if f.top <= 0 or f.bottom >= 400:
            field_speeds[i] = (dx, -dy)

        if seconds > grace_period and player.colliderect(f):
            print("Game Over! Final Score:", score)
            running = False

    screen.fill((255,255,255))
    pygame.draw.rect(screen, (0, 0, 255), player)

    for f in fields:
        pygame.draw.rect(screen, (255, 0, 0), f)

    text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    if seconds <= grace_period:
        warn = font.render("INVINCIBLE!", True, (0, 200, 0))
        screen.blit(warn, (230, 10))

    count_text = font.render(f"Fields: {len(fields)}", True, (200, 0, 0))
    screen.blit(count_text, (450, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
