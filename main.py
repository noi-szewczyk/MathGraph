"""
Copyright© 2024 Artur Pozniak <noi.kucia@gmail.com> or <noiszewczyk@gmail.com>.
All rights reserved.
This program is released under license GPL-3.0-or-later

This file is part of MathGraph.
MathGraph is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

MathGraph is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with MathGraph.
If not, see <https://www.gnu.org/licenses/>.
"""

import json
import os.path

import arcade
import pyglet.image
from pyglet.window import ImageMouseCursor

from client import Client
from menu import MenuView


def game_configure(window: arcade.Window):
    """loading parameters from json configure file"""
    with open('config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)

    window.lobby = None  # contains Lobby class, if user in some of them

    window.SCREEN_WIDTH = config['SCREEN_WIDTH']
    window.SCREEN_HEIGHT = config['SCREEN_HEIGHT']
    window.FULLSCREEN_MODE = config['FULLSCREEN_MODE']
    window.SELECTED_MONITOR = config['SELECTED_MONITOR']

    window.GRAPH_BOTTOM_EDGE = window.SCREEN_HEIGHT / 4
    window.GRAPH_TOP_EDGE = window.SCREEN_HEIGHT - config['GRAPH_TOP_EDGE_OFFSET']

    window.GRAPH_BG_COLOR_HEX = config['GRAPH_BG_COLOR_HEX']
    window.GRAPH_LINES_COLOR_HEX = config['GRAPH_LINES_COLOR_HEX']

    if window.FULLSCREEN_MODE:
        if window.SELECTED_MONITOR > len(arcade.get_screens()):
            window.SELECTED_MONITOR = 1
        window.SCREEN_WIDTH, window.SCREEN_HEIGHT = arcade.get_display_size(window.SELECTED_MONITOR - 1)

        window.GRAPH_TOP_EDGE = window.SCREEN_HEIGHT - config['GRAPH_TOP_EDGE_OFFSET']
        window.GRAPH_BOTTOM_EDGE = window.SCREEN_HEIGHT / 4

        window.width = window.SCREEN_WIDTH
        window.title = 'MathGraph'
        window.height = window.SCREEN_HEIGHT
        window.set_fullscreen(True, arcade.get_screens()[window.SELECTED_MONITOR - 1])
    else:
        window.width = window.SCREEN_WIDTH
        window.title = 'MathGraph'
        window.height = window.SCREEN_HEIGHT

    window.scale = window.SCREEN_HEIGHT / 1080
    window.SCREEN_X_CENTER = window.SCREEN_WIDTH // 2
    window.SCREEN_Y_CENTER = window.SCREEN_HEIGHT // 2
    cursor = ImageMouseCursor(image=pyglet.image.load('textures/cursor.png'), hot_x=0, hot_y=32)
    window.set_mouse_cursor(cursor=cursor)
    window.client = Client()
    window.client.name = config['client_name']
    try:
        window.client.avatar = arcade.load_texture(config['client_avatar'])
    except FileNotFoundError:  # load standard file if specified avatar image file is missing
        window.client.avatar = arcade.load_texture('textures/default_avatar.jpg')


def main():
    """loading config to get settings,
    creating window  and then main menu view"""

    if not os.path.isfile('./config.json'):  # create new standard config file in case of its absence
        config = {
            "SCREEN_WIDTH": 1280,
            "SCREEN_HEIGHT": 720,
            "FULLSCREEN_MODE": 1,
            "SELECTED_MONITOR": 1,
            "GRAPH_TOP_EDGE_OFFSET": 25,
            "GRAPH_BG_COLOR_HEX": "#0b0112",
            "GRAPH_LINES_COLOR_HEX": "#6c31e0",
            "client_name": "User",
            "client_avatar": "textures/default_avatar.jpg"
        }
        with open('config.json', 'w') as file:
            json.dump(config, file, indent=4)

    math_graph = arcade.Window(antialiasing=True, vsync=True)
    game_configure(math_graph)
    menu_view = MenuView(math_graph)
    math_graph.show_view(menu_view)
    math_graph.run()


try:
    main()
except Exception as e:
    with open('crash_report.txt', 'w') as file:
        file.write(str(e))  # creating file with error
