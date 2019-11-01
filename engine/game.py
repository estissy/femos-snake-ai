from copy import deepcopy
from enum import Enum
from itertools import product
from math import ceil, sqrt, pow
from random import Random

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

    def __init__(self, width, height, phenotype, seed, game_representation_strategy,
                 snake_length=5, snack_eaten_points=1, moved_toward_snack_points=0.1,
                 moved_away_from_snack_points=-0.2, max_points_threshold=200):
        self.width = width
        self.height = height
        self.phenotype = phenotype
        self.seed = seed
        self.random_generator = Random(self.seed)
        self.game_representation_strategy = game_representation_strategy
        self.snack_perspective = None
        self.snack_eaten_points = snack_eaten_points
        self.moved_toward_snack_points = moved_toward_snack_points
        self.moved_away_from_snack_points = moved_away_from_snack_points
        self.max_points_threshold = max_points_threshold

        self.status = GameStatus.INITIALIZED
        self.snack = None
        self.snake = []
        self.score = 0
        self.direction = Direction.LEFT
        self.last_snack_distance = 0

        self.initialize_snake(snake_length)
        self.initialize_snack()
        self.initialize_last_snack_distance()

    def initialize_snake(self, snake_length=5):
        middle_x = ceil(self.width / 2)
        middle_y = ceil(self.height / 2)

        for index in range(snake_length):
            self.snake.append((middle_x + index, middle_y))

        self.snack_perspective = (middle_x + snake_length, middle_y)

    def initialize_snack(self):
        x_range = range(self.width)
        y_range = range(self.height)

        positions = product(x_range, y_range)
        available_positions = list(
            filter(lambda position: position not in self.snake, positions))
        self.snack = self.random_generator.choice(available_positions)

    def initialize_last_snack_distance(self):
        snake_head_position = self.get_snake_head_position()
        self.last_snack_distance = self.get_snake_snacks_distances(snake_head_position, self.snack)

    def get_snake_head_position(self):
        return self.snake[0]

    @staticmethod
    def get_snake_snacks_distances(snake_head_position, snack_position):
        coefficient1 = pow(snake_head_position[0] - snack_position[0], 2)
        coefficient2 = pow(snake_head_position[1] - snack_position[1], 2)
        return sqrt(coefficient1 + coefficient2)

    def move_forward(self, new_direction):
        head_position = self.get_snake_head_position()

        new_head_position = None
        new_tail = self.snake[:-1]
        new_snack_perspective_position = self.snake[-1]

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
        self.snack_perspective = new_snack_perspective_position

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
            elif selected_position == game.snack:
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
        return snake_head_position == self.snack

    @staticmethod
    def get_next_game(game):
        snake_head_position = game.get_snake_head_position()

        if game.score >= game.max_points_threshold:
            game.status = GameStatus.ENDED
            return game

        if game.is_snake_head_in_wall(snake_head_position):
            game.status = GameStatus.ENDED
            return game

        # Handle snake eating snack points
        new_snack_distance = Game.get_snake_snacks_distances(snake_head_position, game.snack)
        if game.is_snake_eating_snack(snake_head_position):
            game.score += game.snack_eaten_points
            game.initialize_snack()

            game.snake.append(game.snack_perspective)
        else:
            # Handle snake approach nearest snack
            if new_snack_distance < game.last_snack_distance:
                game.score += game.moved_toward_snack_points
            else:
                game.score += game.moved_away_from_snack_points

        game.last_snack_distance = new_snack_distance

        # Make decision
        game_state_representation = game.game_representation_strategy(game)
        prediction = Phenotype.get_prediction(game.phenotype, game_state_representation)
        new_direction = game.get_new_direction_from_prediction(prediction, game.direction)

        # Move forward
        game.move_forward(new_direction)

        # Update current direction
        game.direction = new_direction

        return deepcopy(game)

    @staticmethod
    def get_solved_game(game):
        tmp_game = game
        while tmp_game.status != GameStatus.ENDED:
            tmp_game = Game.get_next_game(tmp_game)

        return tmp_game
