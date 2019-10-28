from copy import deepcopy

from femos.phenotypes import Phenotype

from src.game import Game, Direction


def test_game_initialization():
    sample_phenotype = Phenotype

    def game_representation_strategy(game):
        return Game.get_full_game_representation_strategy(game)

    snake_length = 5
    number_of_snacks = 3
    width = 32
    height = 18
    sample_game = Game(width, height, sample_phenotype, 777, game_representation_strategy, number_of_snacks,
                       snake_length)

    assert len(sample_game.snake) == snake_length

    correct_snake_blocks = [(16, 9), (17, 9), (18, 9), (19, 9), (20, 9)]
    assert sample_game.snake == correct_snake_blocks
    assert len(sample_game.snacks) == number_of_snacks

    for selected_snack in sample_game.snacks:
        assert selected_snack not in correct_snake_blocks
        assert 0 <= selected_snack[0] <= width
        assert 0 <= selected_snack[1] <= height


def test_snake_moves():
    sample_phenotype = Phenotype

    def game_representation_strategy(game):
        return Game.get_full_game_representation_strategy(game)

    snake_length = 5
    number_of_snacks = 3
    width = 32
    height = 18
    sample_game = Game(width, height, sample_phenotype, 777, game_representation_strategy, number_of_snacks,
                       snake_length)

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
    sample_phenotype = Phenotype

    def game_representation_strategy(game):
        return Game.get_full_game_representation_strategy(game)

    snake_length = 3
    number_of_snacks = 3
    width = 8
    height = 8
    sample_game = Game(width, height, sample_phenotype, 777, game_representation_strategy, number_of_snacks,
                       snake_length)
    print(sample_game.snake)

    game_representation = Game.get_full_game_representation_strategy(sample_game)
    print(game_representation)
    assert len(game_representation) == 8 * 8 + 4
    assert game_representation[36] == 1
    assert game_representation[44] == 1
    assert game_representation[52] == 1
