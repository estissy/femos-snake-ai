from copy import deepcopy
from enum import Enum
from itertools import product
from math import ceil
from random import sample

from femos.phenotypes import Phenotype
from numpy import argmax


class GameStatus(Enum):
    INITIALIZED = 1
    PENDING = 2
    ENDED = 3


class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class Prediction(Enum):
    ROTATE_LEFT = 1
    ROTATE_RIGHT = 2
    KEEP_DIRECTION = 3


class Game:

    def __init__(self, width, height, phenotype, seed, game_representation_strategy, number_of_snacks=1,
                 snake_length=5):
        self.width = width
        self.height = height
        self.phenotype = phenotype
        self.seed = seed
        self.number_of_snacks = number_of_snacks
        self.game_representation_strategy = game_representation_strategy

        self.status = GameStatus.INITIALIZED
        self.snacks = []
        self.snake = []
        self.score = 0
        self.direction = Direction.LEFT

        self.initialize_snake(snake_length)
        self.initialize_snacks()

    def initialize_snake(self, snake_length=5):
        middle_x = ceil(self.width / 2)
        middle_y = ceil(self.height / 2)

        for index in range(snake_length):
            self.snake.append((middle_x + index, middle_y))

    def initialize_snacks(self):
        x_range = range(self.width)
        y_range = range(self.height)

        positions = product(x_range, y_range)
        available_positions = list(
            filter(lambda position: position not in self.snake and position not in self.snacks, positions))
        snacks_to_initialize = self.number_of_snacks - len(self.snacks)
        new_random_snacks = sample(available_positions, snacks_to_initialize)

        self.snacks += new_random_snacks

    def get_snake_head_position(self):
        return self.snake[0]

    def move_forward(self, new_direction):
        head_position = self.get_snake_head_position()

        new_head_position = None
        new_tail = self.snake[:-1]

        # Handle inadequate move. As result snake is moving in the same direction.
        if self.direction == Direction.LEFT and (new_direction == Direction.LEFT or new_direction == Direction.RIGHT):
            new_head_position = (head_position[0] - 1, head_position[1])

        if self.direction == Direction.RIGHT and (new_direction == Direction.LEFT or new_direction == Direction.RIGHT):
            new_head_position = (head_position[0] + 1, head_position[1])

        if self.direction == Direction.UP and (new_direction == Direction.UP or new_direction == Direction.DOWN):
            new_head_position = (head_position[0], head_position[1] - 1)

        if self.direction == Direction.DOWN and (new_direction == Direction.UP or new_direction == Direction.DOWN):
            new_head_position = (head_position[0], head_position[1] + 1)

        # Handle real direction changes.
        if (self.direction == Direction.LEFT or self.direction == Direction.RIGHT) and new_direction == Direction.UP:
            new_head_position = (head_position[0], head_position[1] - 1)

        if (self.direction == Direction.LEFT or self.direction == Direction.RIGHT) and new_direction == Direction.DOWN:
            new_head_position = (head_position[0], head_position[1] + 1)

        if (self.direction == Direction.UP or self.direction == Direction.DOWN) and new_direction == Direction.LEFT:
            new_head_position = (head_position[0] - 1, head_position[1])

        if (self.direction == Direction.UP or self.direction == Direction.DOWN) and new_direction == Direction.RIGHT:
            new_head_position = (head_position[0] + 1, head_position[1])

        self.snake = [new_head_position] + new_tail

    @staticmethod
    def get_full_game_representation_strategy(game):
        range_x = range(game.width)
        range_y = range(game.height)

        positions = list(product(range_x, range_y))

        game_representation = []

        # Encode game board
        for selected_position in positions:

            if selected_position in game.snake:
                game_representation.append(1)
            elif selected_position in game.snacks:
                game_representation.append(-1)
            else:
                game_representation.append(0)

        # Encode current direction
        if game.direction == Direction.LEFT:
            game_representation += [1, 0, 0, 0]
        elif game.direction == Direction.RIGHT:
            game_representation += [0, 1, 0, 0]
        elif game.direction == Direction.UP:
            game_representation += [0, 0, 1, 0]
        else:
            game_representation += [0, 0, 0, 1]

        return game_representation

    @staticmethod
    def get_new_direction_from_prediction(prediction, current_direction):
        best_decision = argmax(prediction)
        parsed_prediction = None

        if best_decision == 0:
            parsed_prediction = Prediction.ROTATE_RIGHT
        elif best_decision == 1:
            parsed_prediction = Prediction.ROTATE_LEFT
        else:
            parsed_prediction = Prediction.KEEP_DIRECTION

        # Handle new direction while parsed_prediction is "KEEP DIRECTION".
        if parsed_prediction == Prediction.KEEP_DIRECTION and current_direction == Direction.LEFT:
            return Direction.LEFT

        if parsed_prediction == Prediction.KEEP_DIRECTION and current_direction == Direction.RIGHT:
            return Direction.RIGHT

        if parsed_prediction == Prediction.KEEP_DIRECTION and current_direction == Direction.UP:
            return Direction.UP

        if parsed_prediction == Prediction.KEEP_DIRECTION and current_direction == Direction.DOWN:
            return Direction.DOWN

        # Handle new direction while parsed_prediction is "ROTATE LEFT"
        if parsed_prediction == Prediction.ROTATE_LEFT and current_direction == Direction.LEFT:
            return Direction.DOWN

        if parsed_prediction == Prediction.ROTATE_LEFT and current_direction == Direction.RIGHT:
            return Direction.UP

        if parsed_prediction == Prediction.ROTATE_LEFT and current_direction == Direction.UP:
            return Direction.LEFT

        if parsed_prediction == Prediction.ROTATE_LEFT and current_direction == Direction.DOWN:
            return Direction.RIGHT

        # Handle new direction while parsed_prediction is "ROTATE RIGHT"
        if parsed_prediction == Prediction.ROTATE_RIGHT and current_direction == Direction.LEFT:
            return Direction.UP

        if parsed_prediction == Prediction.ROTATE_RIGHT and current_direction == Direction.RIGHT:
            return Direction.DOWN

        if parsed_prediction == Prediction.ROTATE_RIGHT and current_direction == Direction.UP:
            return Direction.RIGHT

        if parsed_prediction == Prediction.ROTATE_RIGHT and current_direction == Direction.DOWN:
            return Direction.DOWN

    def is_snake_head_in_wall(self, snake_head_position):
        if snake_head_position[0] < 0 or snake_head_position[0] >= self.width or snake_head_position[1] < 0 or \
                snake_head_position[1] >= self.height:
            return True
        elif snake_head_position in self.snake[1:]:
            return True
        else:
            return False

    def is_snake_eating_snack(self, snake_head_position):
        if snake_head_position in self.snacks:
            return True
        else:
            return False

    @staticmethod
    def get_next_game(game):
        snake_head_position = game.get_snake_head_position()

        if game.is_snake_head_in_wall(snake_head_position):
            game.status = GameStatus.ENDED
            return game

        if game.is_snake_eating_snack(snake_head_position):
            game.score += 1
            game.snacks.remove(snake_head_position)
            game.initialize_snacks()

        # Make decision
        game_state_representation = game.game_representation_strategy(game)
        prediction = Phenotype.get_prediction(game.phenotype, game_state_representation)
        new_direction = game.get_new_direction_from_prediction(prediction, game.direction)

        # Move forward
        game.move_forward(new_direction)

        # Update current direction
        game.direction = new_direction
        snake_head_position = game.get_snake_head_position()

        return deepcopy(game)

    def run(self):

        while 1:
            snake_head_position = self.get_snake_head_position()

            if self.is_snake_head_in_wall(snake_head_position):
                self.status = GameStatus.ENDED
                return self

            if self.is_snake_eating_snack(snake_head_position):
                self.score += 1
                self.snacks.remove(snake_head_position)
                self.initialize_snacks()

            # Make decision
            game_state_representation = self.game_representation_strategy(self)
            prediction = Phenotype.get_prediction(self.phenotype, game_state_representation)
            new_direction = self.get_new_direction_from_prediction(prediction, self.direction)

            # Move forward
            self.move_forward(new_direction)

            # Update current direction
            self.direction = new_direction
