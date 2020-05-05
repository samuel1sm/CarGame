import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("My first game")
clock = pygame.time.Clock()

loop = True
press = False
while loop:
    try:
        # pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

        px, py = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed() == (1, 0, 0):
            pygame.draw.rect(screen, (128, 128, 128), (px, py, 10, 10))

        if event.type == pygame.MOUSEBUTTONUP:
            press == False
        pygame.display.update()
        clock.tick(1000)
    except Exception as e:
        print(e)
        pygame.quit()

pygame.quit()