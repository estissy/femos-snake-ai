import argparse
from multiprocessing import Pool
from random import Random
from statistics import mean

from femos.core import get_number_of_nn_weights, get_evolved_population
from femos.genotypes import UncorrelatedNStepSizeGenotype
from femos.phenotypes import Phenotype
from femos.selections import get_n_size_tournament_parent_selection, get_age_based_offspring_selection

from engine.game import Game

# Parsing command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--game_board_width", help="Width of the snake game board.", type=int, default=36)
parser.add_argument("--game_board_height", help="Height of the snake game board.", type=int, default=18)
parser.add_argument("--seed", help="Selected integer value for experiments recurrence.", type=int, default=777)
parser.add_argument("--initial_snake_length", help="Initial snake length in new game.", type=int, default=5)
parser.add_argument("--hidden_layer_nodes", help="List of nodes in hidden layers", type=list, default=[64])
parser.add_argument("--weight_lower_threshold", help="Lower threshold value of ann weights", type=float, default=-1.0)
parser.add_argument("--weight_upper_threshold", help="Upper threshold value of ann weights", type=float, default=1.0)
parser.add_argument("--mutation_step_size_lower_threshold",
                    help="Lower threshold value for genotype mutation step size",
                    type=float, default=-0.2)
parser.add_argument("--mutation_step_size_upper_threshold",
                    help="Upper threshold value for genotype mutation step size",
                    type=float, default=0.2)
parser.add_argument("--population_size", help="Number of individuals in population", type=int, default=20)
parser.add_argument("--tournament_size", help="Number of individuals to rival in tournament selection", type=int,
                    default=3)
parser.add_argument("--epochs", help="Number of epochs", type=int, default=1000)
parser.add_argument("--tau1", help="Mutation operator parameter - tau1", type=float, default=0.001)
parser.add_argument("--tau2", help="Mutation operator parameter - tau2", type=float, default=0.01)
parser.add_argument("--snack_eaten_points", help="Number of points assigned when snake eat snack", type=float,
                    default=1.0)
parser.add_argument("--moving_toward_snack_points", help="Number of points assigned when snake is moving toward snack",
                    type=float, default=0.1)
parser.add_argument("--moving_away_snack_points", help="Number of points assigned when snake is moving away of snack",
                    type=float, default=-0.2)
parser.add_argument("--max_points_threshold", help="Number of points to end game even if snake still plays.",
                    type=float,
                    default=10.0)
parser.add_argument("--same_environment", help="Use the same environment for every individual in population",
                    action="store_true")

args = parser.parse_args()

input_nodes = args.game_board_width * args.game_board_height + 4
output_nodes = 3
number_of_nn_weights = get_number_of_nn_weights(input_nodes, args.hidden_layer_nodes, output_nodes)

genotypes = UncorrelatedNStepSizeGenotype.get_random_genotypes(args.population_size, number_of_nn_weights,
                                                               args.weight_lower_threshold, args.weight_upper_threshold,
                                                               args.mutation_step_size_lower_threshold,
                                                               args.mutation_step_size_upper_threshold)

random_generator = Random(args.seed)


def phenotype_strategy(genotype):
    return Phenotype(genotype.weights, input_nodes, args.hidden_layer_nodes, output_nodes)


def evaluation_strategy(phenotypes):
    game_board_widths = [args.game_board_width] * args.population_size
    game_board_heights = [args.game_board_height] * args.population_size

    if args.same_environment:
        evaluation_random_seed = random_generator.randint(1, 1000000)
        seeds = [evaluation_random_seed] * args.population_size
    else:
        seeds = list(map(lambda index: random_generator.randint(1, 1000000), range(args.population_size)))

    game_representation_strategies = [Game.get_full_game_representation_strategy] * args.population_size
    initial_snake_lengths = [args.initial_snake_length] * args.population_size
    snack_eaten_points = [args.snack_eaten_points] * args.population_size
    moving_toward_snack_points = [args.moving_toward_snack_points] * args.population_size
    moving_away_snack_points = [args.moving_away_snack_points] * args.population_size
    max_points_thresholds = [args.max_points_threshold] * args.population_size
    arguments = list(zip(game_board_widths, game_board_heights, phenotypes, seeds, game_representation_strategies,
                         initial_snake_lengths, snack_eaten_points, moving_toward_snack_points,
                         moving_away_snack_points, max_points_thresholds))

    initialized_games = list(map(lambda game_arguments: Game(*game_arguments), arguments))

    with Pool() as p:
        solved_games = p.map(Game.get_solved_game, initialized_games)

    phenotype_values = list(map(lambda solved_game: solved_game.score, solved_games))

    print(mean(phenotype_values), max(phenotype_values))
    return phenotype_values


def parent_selection_strategy(phenotypes_values):
    return get_n_size_tournament_parent_selection(phenotypes_values, args.tournament_size, args.population_size)


def mutation_strategy(genotype):
    return UncorrelatedNStepSizeGenotype.get_mutated_genotype(genotype, args.tau1, args.tau2)


def offspring_selection_strategy(parents, updated_parents):
    return get_age_based_offspring_selection(parents, updated_parents)


evolved_population = get_evolved_population(genotypes, phenotype_strategy, evaluation_strategy,
                                            parent_selection_strategy, mutation_strategy, offspring_selection_strategy,
                                            args.epochs)
