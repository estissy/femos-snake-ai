from multiprocessing import Pool
from random import Random

from femos.parser import handle_evolution_run

from engine.game import Game

# Game arguments
GAME_BOARD_WIDTH = 18
GAME_BOARD_HEIGHT = 18
SEED = 777
INITIAL_SNAKE_LENGTH = 5
SAME_ENVIRONMENT = False

SNACK_EATEN_POINTS = 4
MOVING_TOWARD_SNACK_POINTS = 0.1
MOVING_AWAY_SNACK_POINTS = -0.2
MAX_POINTS_THRESHOLD = 10
MIN_POINTS_THRESHOLD = -10
INPUT_NODES = 8
OUTPUT_NODES = 3

random_generator = Random(SEED)

def evaluation_strategy(phenotypes):
    population_size = len(phenotypes)
    game_board_widths = [GAME_BOARD_WIDTH] * population_size
    game_board_heights = [GAME_BOARD_HEIGHT] * population_size

    if SAME_ENVIRONMENT:
        evaluation_random_seed = random_generator.randint(1, 1000000)
        seeds = [evaluation_random_seed] * population_size
    else:
        seeds = list(map(lambda index: random_generator.randint(1, 1000000), range(population_size)))

    game_representation_strategies = [Game.get_feature_based_game_representation_strategy] * population_size 
    initial_snake_lengths = [INITIAL_SNAKE_LENGTH] * population_size
    snack_eaten_points = [SNACK_EATEN_POINTS] * population_size
    moving_toward_snack_points = [MOVING_TOWARD_SNACK_POINTS] * population_size
    moving_away_snack_points = [MOVING_AWAY_SNACK_POINTS] * population_size
    max_points_thresholds = [MAX_POINTS_THRESHOLD] * population_size
    min_points_thresholds = [MIN_POINTS_THRESHOLD] * population_size
    arguments = list(zip(game_board_widths, game_board_heights, phenotypes, seeds, game_representation_strategies,
                         initial_snake_lengths, snack_eaten_points, moving_toward_snack_points,
                         moving_away_snack_points, max_points_thresholds, min_points_thresholds))

    initialized_games = list(map(lambda game_arguments: Game(*game_arguments), arguments))

    with Pool() as p:
        solved_games = p.map(Game.get_solved_game, initialized_games)

    phenotype_values = list(map(lambda solved_game: solved_game.score, solved_games))

    return phenotype_values


evolved_population = handle_evolution_run(INPUT_NODES, OUTPUT_NODES, evaluation_strategy)
