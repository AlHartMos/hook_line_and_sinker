# To install pygame in a conda environment
    # conda create -n mygame python=3.12
    # conda activate mygame
    # conda install -c conda-forge pygame
import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()