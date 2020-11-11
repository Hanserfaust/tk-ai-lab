import sys

from tkinter import Tk, Canvas, mainloop, ALL, Label

from tkinter.messagebox import showinfo

from wilderness import GameMap, Player, Game

import baselines

# Game map settings
MAP_WIDTH = 10
MAP_HEIGTH = 10

# Player
PLAYER_VISION = 100

# TK
DEFAULT_TILE_SIZE = 30

CANVAS_WIDTH = 1000
CANVAS_HEIGTH = 1000
CANVAS_OFFSET = 0 #int(CANVAS_WIDTH/2) - PLAYER_VISION * DEFAULT_TILE_SIZE


class TkGame(Game):

    tile_size = DEFAULT_TILE_SIZE

    keyboard_to_action = {
        'w': 'up',
        's': 'down',
        'a': 'left',
        'd': 'right'
    }

    def __init__(self, game_map, players, vision=PLAYER_VISION):
        super().__init__(game_map, players, vision)

        root = Tk()
        # Label(root, text="Red Sun", bg="red", fg="white").pack()

        self.canvas = Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGTH)
        self.canvas.pack()

        self.input_enabled = False

    def evaluate(self):
        # Evaluate game state
        if self.game_map.is_player_at_exit(self.players[0]):
            self.input_enabled = False
            showinfo("Exit found!", "Player found exit after %s steps. \n\nTotal penalty = %s" % (self.players[0].steps, self.players[0].score))
            sys.exit()

    def render(self):
        self.canvas.delete(ALL)

        for p in self.players:
            game.show_terrain_for(p)

        self.draw_markers(self.game_map.markers)

        self.draw_panel()

    def tk_display_around(self, xr, yr, dist):
        terrain_matrix = self.game_map.get_terrain_around(xr, yr, dist)

        self.draw_terrain_matrix(terrain_matrix)

        return terrain_matrix

    def show_terrain_for(self, player):
        return self.tk_display_around(player.x, player.y, self.vision)

    def draw_terrain_matrix(self, terrain_matrix):

        for i in range(len(terrain_matrix)):
            for j in range(len(terrain_matrix[i])):
                terrain = terrain_matrix[i][j]

                x1 = i * self.tile_size + CANVAS_OFFSET
                y1 = j * self.tile_size + CANVAS_OFFSET

                x2 = (i+1) * self.tile_size + CANVAS_OFFSET
                y2 = (j+1) * self.tile_size + CANVAS_OFFSET

                # x1,y1,x2,y2
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=terrain.color)

    def draw_markers(self, markers):

        for marker in markers:
            x1 = marker.x * self.tile_size + CANVAS_OFFSET
            y1 = marker.y * self.tile_size + CANVAS_OFFSET

            x2 = (marker.x+1) * self.tile_size + CANVAS_OFFSET
            y2 = (marker.y+1) * self.tile_size + CANVAS_OFFSET

            # x1,y1,x2,y2
            self.canvas.create_oval(x1, y1, x2, y2, fill=marker.color)

    def draw_panel(self):
        self.canvas.create_text(920, 100, text="Penalty: %s" % self.players[0].score)

    def draw_game_end_text(self):
        self.canvas.create_text(920, 200, text="Exit found!")

    def draw_map(self):
        self.draw_terrain_matrix(self.game_map._terrain)

    #
    # Event handlers
    #
    ################################
    def callback_Button_1(self, event):
        self.canvas.focus_set()
        print("clicked at", event.x, event.y)

    def callback_Key(self, event):
        print("Pressed char = %s" % event.char)

        action = self.keyboard_to_action.get(event.char, None)

        if not action or not self.input_enabled:
            return

        self.player_action(player1, action)

        self.evaluate()

        self.render()

    def configure_inputs(self):
        self.canvas.bind("<Key>", self.callback_Key)

        self.canvas.bind("<Button-1>", self.callback_Button_1)

        self.canvas.pack()


if __name__ == '__main__':

    game_map = GameMap(MAP_WIDTH, MAP_HEIGTH)
    player1 = Player(u'Human One', 0, 0)
    game = TkGame(game_map, [player1], PLAYER_VISION)

    # Show initial terrain

    input_char = ''
    last_cost = 0

    game.configure_inputs()

    game.render()

    game.input_enabled = True

    mainloop()
