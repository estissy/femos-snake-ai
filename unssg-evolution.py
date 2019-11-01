from statistics import mean

from femos.core import get_number_of_nn_weights, get_evolved_population
from femos.genotypes import UncorrelatedNStepSizeGenotype
from femos.phenotypes import Phenotype
from femos.selections import get_two_size_tournament_parent_selection, get_age_based_offspring_selection

from engine.game import Game

game_board_width = 36
game_board_height = 18
seed = 777
initial_snake_length = 5

input_nodes = game_board_width * game_board_height + 4
hidden_layer_nodes = [64]
output_nodes = 3
number_of_nn_weights = get_number_of_nn_weights(input_nodes, hidden_layer_nodes, output_nodes)
weight_lower_threshold = -1
weight_upper_threshold = 1
mutation_step_size_lower_threshold = -0.3
mutation_step_size_upper_threshold = 0.3
population_size = 20
epochs = 1000
tau1 = 0.001
tau2 = 0.01

genotypes = UncorrelatedNStepSizeGenotype.get_random_genotypes(population_size, number_of_nn_weights,
                                                               weight_lower_threshold, weight_upper_threshold,
                                                               mutation_step_size_lower_threshold,
                                                               mutation_step_size_upper_threshold)


def phenotype_strategy(genotype):
    return Phenotype(genotype.weights, input_nodes, hidden_layer_nodes, output_nodes)


def evaluation_strategy(phenotypes):
    phenotype_values = []

    for selected_phenotype in phenotypes:
        game = Game(game_board_width, game_board_height, selected_phenotype, seed,
                    Game.get_full_game_representation_strategy, initial_snake_length)
        game.evaluate_phenotype()
        phenotype_values.append(game.score)

    print(mean(phenotype_values), max(phenotype_values))
    return phenotype_values


def parent_selection_strategy(phenotypes_values):
    return get_two_size_tournament_parent_selection(phenotypes_values, population_size)


def mutation_strategy(genotype):
    return UncorrelatedNStepSizeGenotype.get_mutated_genotype(genotype, tau1, tau2)


def offspring_selection_strategy(parents, updated_parents):
    return get_age_based_offspring_selection(parents, updated_parents)


evolved_population = get_evolved_population(genotypes, phenotype_strategy, evaluation_strategy,
                                            parent_selection_strategy, mutation_strategy, offspring_selection_strategy,
                                            epochs)
