from copy import deepcopy

from femos.core import get_number_of_nn_weights
from femos.genotypes import SimpleGenotype
from femos.phenotypes import Phenotype

from engine.game import Game, Direction, GameStatus


def test_game_initialization():
    def game_representation_strategy(game):
        return Game.get_full_game_representation_strategy(game)

    snake_length = 5
    width = 32
    height = 18
    seed = 777

    input_nodes = width * height + 4
    hidden_layer_nodes = [64]
    output_nodes = 3
    number_of_nn_weights = get_number_of_nn_weights(input_nodes, hidden_layer_nodes, output_nodes)
    weight_lower_threshold = -1
    weight_upper_threshold = 1

    sample_genotype = SimpleGenotype.get_random_genotype(number_of_nn_weights, weight_lower_threshold,
                                                         weight_upper_threshold)
    sample_phenotype = Phenotype(sample_genotype.weights, input_nodes, hidden_layer_nodes, output_nodes)

    sample_game = Game(width, height, sample_phenotype, seed, game_representation_strategy, snake_length)

    assert len(sample_game.snake) == snake_length

    correct_snake_blocks = [(16, 9), (17, 9), (18, 9), (19, 9), (20, 9)]
    assert sample_game.snake == correct_snake_blocks
    assert sample_game.snack_perspective == (21, 9)

    assert sample_game.snack not in correct_snake_blocks
    assert 0 <= sample_game.snack[0] <= width
    assert 0 <= sample_game.snack[1] <= height

    another_game = Game(width, height, sample_phenotype, seed, game_representation_strategy, snake_length)
    assert sample_game.snack == another_game.snack


def test_snake_moves():
    def game_representation_strategy(game):
        return Game.get_full_game_representation_strategy(game)

    snake_length = 5
    width = 32
    height = 18

    input_nodes = width * height + 4
    hidden_layer_nodes = [64]
    output_nodes = 3
    number_of_nn_weights = get_number_of_nn_weights(input_nodes, hidden_layer_nodes, output_nodes)
    weight_lower_threshold = -1
    weight_upper_threshold = 1

    sample_genotype = SimpleGenotype.get_random_genotype(number_of_nn_weights, weight_lower_threshold,
                                                         weight_upper_threshold)
    sample_phenotype = Phenotype(sample_genotype.weights, input_nodes, hidden_layer_nodes, output_nodes)
    sample_game = Game(width, height, sample_phenotype, 777, game_representation_strategy, snake_length)

    # Test snake going LEFT and changed to LEFT
    game_copy = deepcopy(sample_game)
    game_copy.move_forward(Direction.LEFT)
    correct_snake_blocks = [(15, 9), (16, 9), (17, 9), (18, 9), (19, 9)]
    assert game_copy.snake == correct_snake_blocks
    assert len(game_copy.snake) == snake_length

    # Test snake going LEFT and changed to RIGHT
    game_copy = deepcopy(sample_game)
    game_copy.move_forward(Direction.RIGHT)
    correct_snake_blocks = [(15, 9), (16, 9), (17, 9), (18, 9), (19, 9)]
    assert game_copy.snake == correct_snake_blocks
    assert len(game_copy.snake) == snake_length

    # Test snake going LEFT and changed to UP
    game_copy = deepcopy(sample_game)
    game_copy.move_forward(Direction.UP)
    correct_snake_blocks = [(16, 8), (16, 9), (17, 9), (18, 9), (19, 9)]
    assert game_copy.snake == correct_snake_blocks
    assert len(game_copy.snake) == snake_length

    # Test snake going LEFT and changed to DOWN
    game_copy = deepcopy(sample_game)
    game_copy.move_forward(Direction.DOWN)
    correct_snake_blocks = [(16, 10), (16, 9), (17, 9), (18, 9), (19, 9)]
    assert game_copy.snake == correct_snake_blocks
    assert len(game_copy.snake) == snake_length

    # Test snake going RIGHT and changed to LEFT
    game_copy = deepcopy(sample_game)

    # Set up snake rotated to RIGHT
    game_copy.snake = [(20, 9), (19, 9), (18, 9), (17, 9), (16, 9)]
    game_copy.direction = Direction.RIGHT

    correct_snake_blocks = [(21, 9), (20, 9), (19, 9), (18, 9), (17, 9)]
    game_copy.move_forward(Direction.LEFT)
    assert game_copy.snake == correct_snake_blocks
    assert len(game_copy.snake) == snake_length

    # Test snake going RIGHT and changed to RIGHT
    game_copy = deepcopy(sample_game)

    # Set up snake rotated to RIGHT
    game_copy.snake = [(20, 9), (19, 9), (18, 9), (17, 9), (16, 9)]
    game_copy.direction = Direction.RIGHT

    correct_snake_blocks = [(21, 9), (20, 9), (19, 9), (18, 9), (17, 9)]
    game_copy.move_forward(Direction.RIGHT)
    assert game_copy.snake == correct_snake_blocks
    assert len(game_copy.snake) == snake_length

    # Test snake going RIGHT and changed to UP
    game_copy = deepcopy(sample_game)

    # Set up snake rotated to RIGHT
    game_copy.snake = [(20, 9), (19, 9), (18, 9), (17, 9), (16, 9)]
    game_copy.direction = Direction.RIGHT

    correct_snake_blocks = [(20, 8), (20, 9), (19, 9), (18, 9), (17, 9)]
    game_copy.move_forward(Direction.UP)
    assert game_copy.snake == correct_snake_blocks
    assert len(game_copy.snake) == snake_length

    # Test snake going RIGHT and changed to DOWN
    game_copy = deepcopy(sample_game)

    # Set up snake rotated to RIGHT
    game_copy.snake = [(20, 9), (19, 9), (18, 9), (17, 9), (16, 9)]
    game_copy.direction = Direction.RIGHT

    correct_snake_blocks = [(20, 10), (20, 9), (19, 9), (18, 9), (17, 9)]
    game_copy.move_forward(Direction.DOWN)
    assert game_copy.snake == correct_snake_blocks
    assert len(game_copy.snake) == snake_length

    # Test snake going UP and changed to LEFT
    game_copy = deepcopy(sample_game)

    # Set up snake rotated to UP
    game_copy.snake = [(16, 9), (16, 8), (16, 7), (16, 6), (16, 5)]
    game_copy.direction = Direction.UP

    correct_snake_blocks = [(15, 9), (16, 9), (16, 8), (16, 7), (16, 6)]
    game_copy.move_forward(Direction.LEFT)
    assert game_copy.snake == correct_snake_blocks
    assert len(game_copy.snake) == snake_length

    # Test snake going UP and changed to RIGHT
    game_copy = deepcopy(sample_game)

    # Set up snake rotated to UP
    game_copy.snake = [(16, 5), (16, 6), (16, 7), (16, 8), (16, 9)]
    game_copy.direction = Direction.UP

    correct_snake_blocks = [(17, 5), (16, 5), (16, 6), (16, 7), (16, 8)]
    game_copy.move_forward(Direction.RIGHT)
    assert game_copy.snake == correct_snake_blocks
    assert len(game_copy.snake) == snake_length

    # Test snake going UP and changed to UP
    game_copy = deepcopy(sample_game)

    # Set up snake rotated to UP
    game_copy.snake = [(16, 5), (16, 6), (16, 7), (16, 8), (16, 9)]
    game_copy.direction = Direction.UP

    correct_snake_blocks = [(16, 4), (16, 5), (16, 6), (16, 7), (16, 8)]
    game_copy.move_forward(Direction.UP)
    assert game_copy.snake == correct_snake_blocks
    assert len(game_copy.snake) == snake_length

    # Test snake going UP and changed to DOWN
    game_copy = deepcopy(sample_game)

    # Set up snake rotated to UP
    game_copy.snake = [(16, 5), (16, 6), (16, 7), (16, 8), (16, 9)]
    game_copy.direction = Direction.UP

    correct_snake_blocks = [(16, 4), (16, 5), (16, 6), (16, 7), (16, 8)]
    game_copy.move_forward(Direction.DOWN)
    assert game_copy.snake == correct_snake_blocks
    assert len(game_copy.snake) == snake_length

    # Test snake going DOWN and changed to LEFT
    game_copy = deepcopy(sample_game)

    # Set up snake rotated DOWN
    game_copy.snake = [(16, 9), (16, 8), (16, 7), (16, 6), (16, 5)]
    game_copy.direction = Direction.DOWN

    correct_snake_blocks = [(15, 9), (16, 9), (16, 8), (16, 7), (16, 6)]
    game_copy.move_forward(Direction.LEFT)
    assert game_copy.snake == correct_snake_blocks
    assert len(game_copy.snake) == snake_length

    # Test snake going DOWN and changed to RIGHT
    game_copy = deepcopy(sample_game)

    # Set up snake rotated DOWN
    game_copy.snake = [(16, 9), (16, 8), (16, 7), (16, 6), (16, 5)]
    game_copy.direction = Direction.DOWN

    correct_snake_blocks = [(17, 9), (16, 9), (16, 8), (16, 7), (16, 6)]
    game_copy.move_forward(Direction.RIGHT)
    assert game_copy.snake == correct_snake_blocks
    assert len(game_copy.snake) == snake_length

    # Test snake going DOWN and changed to UP
    game_copy = deepcopy(sample_game)

    # Set up snake rotated DOWN
    game_copy.snake = [(16, 9), (16, 8), (16, 7), (16, 6), (16, 5)]
    game_copy.direction = Direction.DOWN

    correct_snake_blocks = [(16, 10), (16, 9), (16, 8), (16, 7), (16, 6)]
    game_copy.move_forward(Direction.UP)
    assert game_copy.snake == correct_snake_blocks
    assert len(game_copy.snake) == snake_length

    # Test snake going DOWN and changed to DOWN
    game_copy = deepcopy(sample_game)

    # Set up snake rotated DOWN
    game_copy.snake = [(16, 9), (16, 8), (16, 7), (16, 6), (16, 5)]
    game_copy.direction = Direction.DOWN

    correct_snake_blocks = [(16, 10), (16, 9), (16, 8), (16, 7), (16, 6)]
    game_copy.move_forward(Direction.DOWN)
    assert game_copy.snake == correct_snake_blocks
    assert len(game_copy.snake) == snake_length


def test_get_full_game_representation_strategy():
    def game_representation_strategy(game):
        return Game.get_full_game_representation_strategy(game)

    snake_length = 3
    width = 8
    height = 8
    input_nodes = width * height + 4
    hidden_layer_nodes = [64]
    output_nodes = 3
    number_of_nn_weights = get_number_of_nn_weights(input_nodes, hidden_layer_nodes, output_nodes)
    weight_lower_threshold = -1
    weight_upper_threshold = 1

    sample_genotype = SimpleGenotype.get_random_genotype(number_of_nn_weights, weight_lower_threshold,
                                                         weight_upper_threshold)
    sample_phenotype = Phenotype(sample_genotype.weights, input_nodes, hidden_layer_nodes, output_nodes)
    sample_game = Game(width, height, sample_phenotype, 777, game_representation_strategy, snake_length)

    game_representation = Game.get_full_game_representation_strategy(sample_game)
    assert len(game_representation) == 8 * 8 + 4
    assert game_representation[36] == 1
    assert game_representation[44] == 1
    assert game_representation[52] == 1


def test_snake_points_assignment():
    def game_representation_strategy(game):
        return Game.get_full_game_representation_strategy(game)

    snake_length = 5
    width = 32
    height = 18
    snack_eaten_points = 2

    input_nodes = width * height + 4
    hidden_layer_nodes = [64]
    output_nodes = 3
    number_of_nn_weights = get_number_of_nn_weights(input_nodes, hidden_layer_nodes, output_nodes)
    weight_lower_threshold = -1
    weight_upper_threshold = 1

    sample_genotype = SimpleGenotype.get_random_genotype(number_of_nn_weights, weight_lower_threshold,
                                                         weight_upper_threshold)
    sample_phenotype = Phenotype(sample_genotype.weights, input_nodes, hidden_layer_nodes, output_nodes)

    sample_game = Game(width, height, sample_phenotype, 777, game_representation_strategy, snake_length,
                       snack_eaten_points)

    # Hack snack position
    # Initial snake blocks are [(16, 9), (17, 9), (18, 9), (19, 9), (20, 9)]
    # So we put snack on snake head
    sample_game.snack = (16, 9)

    next_game_object = Game.get_next_game(sample_game)

    assert next_game_object.score == snack_eaten_points
    assert next_game_object.snack != (16, 9)
    assert next_game_object.snack is not None
    assert len(next_game_object.snake) == snake_length + 1
    assert next_game_object.snack_perspective is not None


def test_game_max_points_threshold():
    def game_representation_strategy(game):
        return Game.get_full_game_representation_strategy(game)

    snake_length = 5
    width = 32
    height = 18
    snack_eaten_points = 2

    input_nodes = width * height + 4
    hidden_layer_nodes = [64]
    output_nodes = 3
    number_of_nn_weights = get_number_of_nn_weights(input_nodes, hidden_layer_nodes, output_nodes)
    weight_lower_threshold = -1
    weight_upper_threshold = 1
    max_points_threshold = 200
    min_points_threshold = -10

    sample_genotype = SimpleGenotype.get_random_genotype(number_of_nn_weights, weight_lower_threshold,
                                                         weight_upper_threshold)
    sample_phenotype = Phenotype(sample_genotype.weights, input_nodes, hidden_layer_nodes, output_nodes)

    sample_game = Game(width, height, sample_phenotype, 777, game_representation_strategy, snake_length,
                       snack_eaten_points, max_points_threshold=max_points_threshold,
                       min_points_threshold=min_points_threshold)
    sample_game.score = 200

    next_game_state = Game.get_next_game(sample_game)
    assert next_game_state.status == GameStatus.ENDED

    next_game_state.score = -10
    next_game_state = Game.get_next_game(next_game_state)
    assert next_game_state.status == GameStatus.ENDED
