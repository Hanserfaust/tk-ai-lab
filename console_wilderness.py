import sys

from util import getChar

from wilderness import GameMap, Player, Game

# Game map settings
BUSH_PROBABILITY = 40
MAP_WIDTH = 20
MAP_HEIGTH = 20

# Player
PLAYER_VISION = 4

# Visualization
X_SCALE = 4
Y_SCALE = 2


class DQNEngine:
    pass


class ConsoleGame(Game):
    '''
        Game for UNIX console
    '''
    def __init__(self, game_map, players, x_scale, y_scale, vision=PLAYER_VISION,):
        super().__init__(game_map, players, vision)

        self.x_scale = x_scale
        self.y_scale = y_scale

    def console_print_tiles_at_scale(self, rows):

        for row in rows:
            for j in range(0, self.y_scale):
                for tile in row:
                    if tile:
                        for k in range(0, self.x_scale):
                            sys.stdout.write('%s' % tile.symbol)
                sys.stdout.write('\n')

    def console_print_around(self, xr, yr, dist):
        tile_rows = self.game_map.get_terrain_around(xr, yr, dist)
        self.console_print_tiles_at_scale(tile_rows)
        return tile_rows

    def show_terrain_for(self, player):
        return self.console_print_around(player.x, player.y, self.vision)


class HumanEngine:

    keyboard_to_action = {
        'w': 'up',
        's': 'down',
        'a': 'left',
        'd': 'right'
    }

    def run(self):

        print("Human Engine")
        print("------------------------------------")
        print("Hit 'x' to quit. Move with 'W A S D'")

        game_map = GameMap(MAP_WIDTH, MAP_HEIGTH)
        player1 = Player(u'Human One', int(MAP_WIDTH/2), int(MAP_HEIGTH/2))
        game = ConsoleGame(game_map, [player1], X_SCALE, Y_SCALE, PLAYER_VISION)

        # Show initial terrain
        game.show_terrain_for(player1)

        input_char = ''
        last_cost = 0

        while input_char != 'x' and last_cost != -1:
            print('\n')
            print('Map size: %s x %s, vision=%s' % (MAP_WIDTH, MAP_HEIGTH, PLAYER_VISION))
            print('---------------------------------------')
            player1.print_stats()

            # Keyboard input -> action
            input_char = getChar()
            action = self.keyboard_to_action.get(input_char, '')

            # Cost of moving into new terrain, mainly for determine exit condition
            last_cost = game.player_action(player1, action)

            # Determine what to do next by looking at this
            local_terrain = game.show_terrain_for(player1)

            # At this point, the "player" knows:
            #
            #  - cost of moving into last space
            #  - player location on map
            #  - surrounding terrain
            #    - can from this determine largest continous open chunk
            #    - cheapest way to exit (if visible)
            #  - own placement in surrounding terrain
            #  - total penalty

        if last_cost == -1:
            print("Game complete! %s score = %s" % (player1, player1.score))
        else:
            print("Game aborted!")


if __name__ == '__main__':

    print("Exploration game for DQN experimentation. Play game as:")
    print(" 1) Human player")
    print(" 2) Bot explorer")
    print(" 3) Current DQN algorithm")

    engine = getChar()

    if engine == '1':
        HumanEngine().run()
