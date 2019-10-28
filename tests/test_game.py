from femos.phenotypes import Phenotype

from src.game import Game


def test_game_initialization():
    sample_phenotype = Phenotype

    def game_representation_strategy(game):
        return Game.get_full_game_representation_strategy(game)

    snake_length = 5
    number_of_snacks = 3
    width = 32
    height = 18
    sample_game = Game(32, 18, sample_phenotype, 777, game_representation_strategy, number_of_snacks, snake_length)

    assert len(sample_game.snake) == snake_length

    correct_snake_blocks = [(16, 9), (17, 9), (18, 9), (19, 9), (20, 9)]
    assert sample_game.snake == correct_snake_blocks
    assert len(sample_game.snacks) == number_of_snacks

    for selected_snack in sample_game.snacks:
        assert selected_snack not in correct_snake_blocks
        assert 0 <= selected_snack[0] <= width
        assert 0 <= selected_snack[1] <= height
