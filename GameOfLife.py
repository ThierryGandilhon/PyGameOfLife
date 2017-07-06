"""
    Game of Life
"""
import random
import numpy
import pygame
from pygame.locals import *


class Window(object):
    """ Class used to represent the window.
        Coordonates in pixels
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Board(object):
    """ Class used to represent the game board
        Coordinates in number of cells
    """
    def __init__(self, width, height, cell_size=5):
        """ Constructor
            Creates the bords and initialize the game system
        """
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.window = Window(width * cell_size, height * cell_size)

        self.grid = self.allocate_grid()

        pygame.init()
        self.display = pygame.display.set_mode((self.window.width, self.window.height))
        self.display.fill((255, 255, 255))
        pygame.display.set_caption('Game of Life')
        self.clock = pygame.time.Clock()

        self.range_width = range(self.width)
        self.range_height = range(self.height)
        self.range_neighbourhood_width = range(-1, 2)
        self.range_neighbourhood_height = range(-1, 2)

        self.fg_color = (255, 155, 0)
        self.bg_color = (255, 255, 255)
        self.grid_color = (0, 0, 0)

        self.populate()

    def allocate_grid(self):
        """ Allocates a new array that represents the cells board.
        """
        return numpy.zeros((self.width, self.height), dtype=numpy.dtype('int'))

    def populate(self):
        """ Initializes the board
            Uses a random generation of cells
        """
        for cell_x in self.range_width:
            for cell_y in self.range_height:
#                self.grid[cell_x, cell_y] = random.randint(0, 1)
                self.grid[cell_x, cell_y] = random.choice([0, 1])

    def display_cells(self):
        """ Displays the cells
        """
        for cell_x in self.range_width:
            for cell_y in self.range_height:
                if (self.grid[cell_x, cell_y] == 1):
                    pygame.draw.rect(self.display,
                                     self.fg_color,
                                     (cell_x * self.cell_size,
                                      cell_y * self.cell_size,
                                      self.cell_size,
                                      self.cell_size))
                else:
                    pygame.draw.rect(self.display,
                                     self.bg_color,
                                     (cell_x * self.cell_size,
                                      cell_y * self.cell_size,
                                      self.cell_size,
                                      self.cell_size))

    def display_grid(self):
        """ Display the grid
        """
        for cell_x in self.range_width:
            pygame.draw.line(self.display,
                             self.grid_color,
                             (cell_x * self.cell_size, 0),
                             (cell_x * self.cell_size, self.window.height))
        for cell_y in self.range_height:
            pygame.draw.line(self.display,
                             self.grid_color,
                             (0, cell_y * self.cell_size),
                             (self.window.width, cell_y * self.cell_size))

    def draw(self):
        """ Draws the full board
        """
        self.display_cells()
#        self.display_grid()

    def count_neighbours(self, cell):
        """ Counts the number of cells adajcent to a given one
            Uses Conway definition
        """
        neighbours = 0
        for delta_x in self.range_neighbourhood_width:
            for delta_y in self.range_neighbourhood_width:
                if delta_x == 0 and delta_y == 0:
                    continue
                neighbour_cell = (cell[0] + delta_x, cell[1] + delta_y)
                if (neighbour_cell[0] in self.range_width) and \
                    neighbour_cell[1] in self.range_height and \
                    self.grid[neighbour_cell[0], neighbour_cell[1]] == 1:
                    neighbours += 1
        return neighbours

    def compute_new_generation(self):
        """ Computes a new generation from the current board
        """
        new_grid = self.allocate_grid()
        for cell_x in self.range_width:
            for cell_y in self.range_height:
                nb_neighbours = self.count_neighbours((cell_x, cell_y))
                if self.grid[cell_x, cell_y] == 1:
                    if nb_neighbours < 2:
                        new_grid[cell_x, cell_y] = 0
                    elif nb_neighbours > 3:
                        new_grid[cell_x, cell_y] = 0
                    else:
                        new_grid[cell_x, cell_y] = 1
                else:
                    if nb_neighbours == 3:
                        new_grid[cell_x, cell_y] = 1
        self.grid = new_grid

def game_of_life(board, fps):
    """ Main function
    """
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit(0)

        board.compute_new_generation()
        board.draw()
        pygame.display.update()
        board.clock.tick(fps)



if __name__ == '__main__':
    game_of_life(Board(200, 100, 10), 20)
