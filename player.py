import random

import arcade

from client import Client


class Player:

    def __init__(self, computer_player: bool = True, client : Client = None, left_player=True,name : str = None):
        self.alive = True
        self.computer_player = computer_player
        self.left_player = left_player
        # keep player Client object with all information about user to display
        if client:
            self.client = client
        else:
            self.client = Client()
            if name: self.client.name=name
        # graphic coordinates of player
        self.x = None
        self.y = None

    def create_sprite(self, window):
        """this method must be called after creation of the game to create the sprite,
        bc it's cordinates depends on game parameters"""

        self.texture_left, self.texture_right = arcade.load_texture_pair('textures/player_sprite.png')
        self.texture_left_dead, self.texture_right_dead = arcade.load_texture_pair('textures/player_sprite_dead.png')

        GRAPH_TOP_EDGE = window.GRAPH_TOP_EDGE
        GRAPH_BOTTOM_EDGE = window.GRAPH_BOTTOM_EDGE
        GRAPH_LEFT_EDGE = int(
            window.SCREEN_WIDTH - (GRAPH_TOP_EDGE - GRAPH_BOTTOM_EDGE) * window.lobby.game.proportion_x2y) // 2
        GRAPH_RIGHT_EDGE = window.SCREEN_WIDTH - GRAPH_LEFT_EDGE
        player_scale = 0.35
        while True:
            if self.left_player:
                rand_x = random.randint(
                    int(GRAPH_LEFT_EDGE + self.texture_left.width * player_scale / 2 * window.scale),
                    int(window.SCREEN_X_CENTER - self.texture_left.width * player_scale / 2 * window.scale))
            else:
                rand_x = random.randint(
                    int(window.SCREEN_X_CENTER + self.texture_left.width * player_scale / 2 * window.scale),
                    int(GRAPH_RIGHT_EDGE - self.texture_left.width * player_scale / 2 * window.scale))
            rand_y = random.randint(int(GRAPH_BOTTOM_EDGE + 10 * window.scale
                                        + self.texture_left.width * player_scale / 2 * window.scale),
                                    int(GRAPH_TOP_EDGE - 10 * window.scale
                                        - self.texture_left.width * player_scale / 2 * window.scale))
            self.sprite = arcade.Sprite(self.texture_left if self.left_player else self.texture_right,
                                        scale=player_scale * window.scale, center_x=rand_x, center_y=rand_y)
            if (not window.lobby.game.players_sprites_list) or \
                    (not arcade.check_for_collision_with_list(self.sprite, window.lobby.game.players_sprites_list)):
                break
        self.x = (self.sprite.center_x - window.SCREEN_X_CENTER) * window.lobby.game.x_edge * 2 / (
                GRAPH_RIGHT_EDGE - GRAPH_LEFT_EDGE)
        self.y = (self.sprite.center_y - (GRAPH_TOP_EDGE + GRAPH_BOTTOM_EDGE) / 2) * window.lobby.game.y_edge * 2 / (
                GRAPH_TOP_EDGE - GRAPH_BOTTOM_EDGE)

        window.lobby.game.players_sprites_list.append(self.sprite)
        window.lobby.game.players_sprites_list.initialize()  # to avoid lags during first drawing

        # adding nick text object only once here
        self.nick  = arcade.Text(self.client.name, start_x=self.sprite.center_x
                                           , start_y=self.sprite.bottom, anchor_y='top', anchor_x='center',
                                           font_size=14 * window.scale, color=arcade.color.WHITE)
