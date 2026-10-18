
import time
import pygame
import numpy as np

pygame.init()

# Colours
COLOUR_BG = (10, 10, 10)
COLOUR_GRID = (40, 40, 40)
COLOUR_DIE_NEXT = (170, 170, 170)
COLOUR_ALIVE_NEXT = (255, 255, 255)

# Window settings
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")


# Update cells
def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros_like(cells)

    for row, col in np.ndindex(cells.shape):
        # Count living neighbours
        alive = np.sum(
            cells[max(0, row - 1):row + 2,
                  max(0, col - 1):col + 2]
        ) - cells[row, col]

        colour = COLOUR_BG

        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    colour = COLOUR_DIE_NEXT
            else:
                updated_cells[row, col] = 1
                colour = COLOUR_ALIVE_NEXT

        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    colour = COLOUR_ALIVE_NEXT

        pygame.draw.rect(
            screen,
            colour,
            (col * size, row * size, size - 1, size - 1)
        )

    return updated_cells


def main():
    running = False
    clock = pygame.time.Clock()

    cells = np.zeros((HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE))

    screen.fill(COLOUR_GRID)
    update(screen, cells, CELL_SIZE)
    pygame.display.flip()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running

                elif event.key == pygame.K_c:
                    cells = np.zeros_like(cells)
                    running = False

        # Draw cells with the mouse while paused
        if not running and pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            col = pos[0] // CELL_SIZE
            row = pos[1] // CELL_SIZE

            if 0 <= row < cells.shape[0] and 0 <= col < cells.shape[1]:
                cells[row, col] = 1

        # Clear and redraw the screen
        screen.fill(COLOUR_GRID)

        if running:
            cells = update(screen, cells, CELL_SIZE, with_progress=True)
        else:
            update(screen, cells, CELL_SIZE)

        pygame.display.flip()

        if running:
            time.sleep(0.001)


if __name__ == "__main__":
    main()
