import pygame

pygame.init()

running = True

screen = pygame.display.set_mode((640, 480))

pygame.display.set_caption("Das ist ein sehr langer Titel, der eventuell die Größe des Fensters übersteigt, "
                           "aber das ist egal, denn es gibt keine Begrenzung für die Fenstertitellänge")

clock = pygame.time.Clock()

screen.fill((0, 0, 0))

pygame.draw.circle(pygame.display.get_surface(), (255, 0, 0), (640/2-32/2, 480/2-32/2), 32)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()