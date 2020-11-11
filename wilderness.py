import random
import copy


class Tile:

    def __init__(self, symbol=None, color=None, bitmap=None):
        self.symbol = symbol
        self.color = color
        self.bitmap = bitmap


class Terrain(Tile):

    _next_id = 0

    def __init__(self, cost, symbol=None, color=None, bitmap=None):
        super().__init__(symbol, color, bitmap)
        self.cost = cost
        self.id = Terrain._next_id

        Terrain._next_id += 1


class TerrainObject:
    '''
        Marks a game object on the game board in a tile, hence it
        carries a x and y coordinates.
    '''
    
    def __init__(self, x, y, symbol=None, color=None, bitmap=None):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.color = color
        self.bitmap = bitmap


class Player(TerrainObject):

    def __init__(self, name, x=0, y=0):
        super().__init__(x, y, color='red')
        self.name = name
        self.score = 0
        self.steps = 0

    def __str__(self):
        return self.name

    def print_stats(self):
        print(u'%s [%s, %s].... score: %s' % (self.name, self.x, self.y, self.score))

    def try_move(self, dir):
        sx, sy = self.x, self.y
        if dir == 'up':
            sy = self.y - 1
        if dir == 'down':
            sy = self.y + 1
        if dir == 'right':
            sx = self.x + 1
        if dir == 'left':
            sx = self.x - 1

        # Note: Will only suggest new coordinates to caller
        return sx, sy

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def incr_score(self, delta_score):
        self.score += delta_score

    def incr_steps(self):
        self.steps += 1

class ExitPortal(TerrainObject):

    def __init__(self, x, y):
        super().__init__(x, y, color='black')


class GameMap:

    PLAINS = Terrain(0, ' ', '#edae28')
    FOREST = Terrain(3, 'F', '#167722')
    SWAMP = Terrain(7, 'S', '#846315')

    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows

        # Generate terrain
        terrain_selection_base = {
            self.SWAMP: 2,
            self.FOREST: 5,
            self.PLAINS: 8
        }
        self.terrain_selection = []

        # Prepare a bag of terrain to draw from when generating terrain
        for terrain, amount in terrain_selection_base.items():
            for i in range(0, amount):
                self.terrain_selection.append(terrain)

        # Terrain is a matrix (2x2 array)
        self._terrain = self._build_terrain()

        # Keep a copy of original
        self._original_terrain = copy.deepcopy(self._terrain)

        # Marker layers, markers keep their position on the object
        self.markers = []

        # exit marker
        exit_x = random.randint(int(3*cols/4), cols-1)
        exit_y = random.randint(int(3*rows/4), rows-1)
        self.exit_marker = ExitPortal(x=exit_x, y=exit_y)

        self.markers.append(self.exit_marker)

    def _get_random_terrain_tile(self):
        ti = random.randint(0, len(self.terrain_selection)-1)
        t = self.terrain_selection[ti]
        return Terrain(
            cost=t.cost,
            symbol=t.symbol,
            color=t.color,
            bitmap=t.bitmap
        )

    def _build_terrain(self):
        terrain_matrix = []
        # Note:
        #   Iterating over Cols (X) first and adding terrain to the row (Y)
        #   so we can access as m[x][y]

        for c in range(self.cols):
            col = []
            terrain_matrix.append(col)
            for r in range(self.rows):
                col.append(self._get_random_terrain_tile())

        return terrain_matrix

    def is_player_at_exit(self, player):
        return player.x == self.exit_marker.x and player.y == self.exit_marker.y

    def limit(self, v, max):
        if v < 0:
            return 0
        elif v >= max:
            return max
        else:
            return v

    def get_terrain_around(self, xr, yr, dist):
        matrix = []

        x1 = self.limit(xr - dist, self.cols)
        x2 = self.limit(xr + dist, self.cols)
        y1 = self.limit(yr - dist, self.rows)
        y2 = self.limit(yr + dist, self.rows)

        for xs in self._terrain[x1:x2]:
            matrix.append(xs[y1:y2])
        return matrix

    def get_cost(self, x, y):
        return self._terrain[x][y].cost

    def add_player_to_map(self, player):
        self.markers.append(player)

    def get_cord_and_cost(self, player, x, y):
        nx, ny = x, y

        if x < 0:
            nx = 0
        if y < 0:
            ny = 0
        if x >= (self.cols - 1):
            nx = self.cols - 1
        if y >= (self.rows - 1):
            ny = self.rows - 1

        # Valid move?
        if nx == x and ny == y:
            # If allowed to move, get score, and mark player in Maze
            cost = self.get_cost(nx, ny)
            player.x = nx
            player.y = ny
            print("Player at X=%s  Y=%s" % (player.x, player.y))
        else:
            cost = 0

        return nx, ny, cost


class Game:
    '''
        A simple maze game that can be tweaked and changed.

        Meant for testing and exploring RL algorithms

        https://blog.openai.com/openai-baselines-dqn/

    '''

    def __init__(self, game_map, players, vision=5):
        self.game_map = game_map
        self.players = players
        self.vision = vision

        for p in players:
            self.game_map.add_player_to_map(p)

    def player_action(self, player, action):
        # A player can only try to move, it may fail
        sx, sy = player.try_move(action)

        # Player suggest nex coordinates.. and terrain return new valid ones
        nx, ny, cost = self.game_map.get_cord_and_cost(player, sx, sy)
        player.set_pos(nx, ny)

        player.incr_score(cost)
        player.incr_steps()

        return cost
