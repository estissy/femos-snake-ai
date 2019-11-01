from sys import exit

import pygame
from femos.core import get_number_of_nn_weights
from femos.genotypes import UncorrelatedNStepSizeGenotype
from femos.phenotypes import Phenotype

from engine.game import Game

game_board_width = 36
game_board_height = 18
seed = 777
number_of_snacks = 5
initial_snake_length = 6

input_nodes = game_board_width * game_board_height + 4
hidden_layer_nodes = [64]
output_nodes = 3
number_of_nn_weights = get_number_of_nn_weights(input_nodes, hidden_layer_nodes, output_nodes)
weight_lower_threshold = -1
weight_upper_threshold = 1
mutation_step_size_lower_threshold = -0.3
mutation_step_size_upper_threshold = 0.3

genotype = UncorrelatedNStepSizeGenotype.get_random_genotype(number_of_nn_weights, weight_lower_threshold,
                                                             weight_upper_threshold,
                                                             mutation_step_size_lower_threshold,
                                                             mutation_step_size_upper_threshold)
phenotype = Phenotype.get_phenotype_from_genotype(genotype, input_nodes, hidden_layer_nodes, output_nodes)

game = Game(game_board_width, game_board_height, phenotype, seed, Game.get_full_game_representation_strategy,
            initial_snake_length)

pygame.init()

scale = 24
game_screen_width = game_board_width * scale
game_screen_height = game_board_height * scale
background_color = (255, 255, 255)
snake_color = (0, 255, 0)
snack_color = (255, 0, 0)
delay = 150

screen = pygame.display.set_mode((game_screen_width, game_screen_height))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # Print game
    screen.fill(background_color)

    for index, selected_snake_block in enumerate(game.snake):
        block_alpha = 255 / (index + 1)

        snake_block = pygame.Surface((1 * scale, 1 * scale))
        snake_block.set_alpha(block_alpha)
        snake_block.fill(snake_color)
        top_x = selected_snake_block[0] * scale
        top_y = selected_snake_block[1] * scale
        screen.blit(snake_block, (top_x, top_y))

    for selected_snack_block in game.snacks:
        snack_block = pygame.Surface((1 * scale, 1 * scale))
        snack_block.fill(snack_color)
        top_x = selected_snack_block[0] * scale
        top_y = selected_snack_block[1] * scale
        screen.blit(snack_block, (top_x, top_y))

    pygame.display.update()
    pygame.time.wait(delay)

    game = Game.get_next_game(game)
