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
import string
import sys

import arcade
import pyglet.image
from pyglet.window import ImageMouseCursor
from arcade import Window, get_screens, get_display_size, load_texture, load_texture_pair

from UIFixedElements import FixedUITextureToggle, FixedUITextureButton, AdvancedUIInputText
from client import Client
from menu import MenuView

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)


def game_configure(window: Window):
    """loading parameters from json configure file"""

    if getattr(sys, 'frozen', False):
        config_path = os.path.dirname(sys.executable)+'/config.json'
    else:
        config_path = 'config.json'
    with open(config_path, 'r', encoding='utf-8') as file:
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
        if window.SELECTED_MONITOR > len(get_screens()):
            window.SELECTED_MONITOR = 1
        window.SCREEN_WIDTH, window.SCREEN_HEIGHT = get_display_size(window.SELECTED_MONITOR - 1)

        window.GRAPH_TOP_EDGE = window.SCREEN_HEIGHT - config['GRAPH_TOP_EDGE_OFFSET']
        window.GRAPH_BOTTOM_EDGE = window.SCREEN_HEIGHT / 4

        window.width = window.SCREEN_WIDTH
        window.title = 'MathGraph'
        window.height = window.SCREEN_HEIGHT
        window.set_fullscreen(True, get_screens()[window.SELECTED_MONITOR - 1])
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
        window.client.avatar = load_texture(config['client_avatar'])
    except FileNotFoundError:  # load standard file if specified avatar image file is missing
        window.client.avatar = load_texture('textures/default_avatar.jpg')


def preload_textures():
    load_texture('textures/user_avatar.jpg')
    load_texture('textures/default_avatar.jpg')
    load_texture('textures/GameBackground_4k.jpg')
    load_texture('textures/bottom_panel_4k.jpg')
    load_texture('textures/MainMenuBackgroundLogo.png')
    load_texture('textures/Settings_button_2048.png')
    load_texture('textures/Lobby_BG_4k.jpg')
    load_texture_pair('textures/player_sprite.png')
    load_texture_pair('textures/player_sprite_dead.png')
    load_texture('textures/fire_button.png')
    load_texture('textures/fire_button_hovered.png')
    load_texture('textures/fire_button_disabled.png')
    load_texture('textures/fire_button_pressed.png')
    load_texture('textures/LobbyExitButton.png')
    load_texture('textures/LobbyExitButton_hovered.png')
    load_texture('textures/square_checkBox_pressed.png')
    load_texture('textures/square_checkBox_empty.png')
    load_texture('textures/skip_vote_button.png')
    load_texture('textures/skip_vote_button_hovered.png')
    load_texture('textures/LobbyPlayButton.png')
    load_texture('textures/LobbyPlayButton_hovered.png')
    load_texture('textures/LobbyAddBotButton.png')
    load_texture('textures/LobbyAddBotButton_hovered.png')
    load_texture('textures/LobbySettingsBox.png')
    load_texture('textures/CheckBoxBlue_empty.png')
    load_texture('textures/CheckBoxBlue_pressed.png')


def preload_texts(window):
    arcade.load_font('resources/Raleway.ttf')  # this font is used in lobby
    arcade.draw_text(string.ascii_letters, 0, 0)  # force font init (fixes lag on first text draw)
    arcade.draw_text(string.ascii_letters, 0, 0, font_size=int(14 * window.scale))
    arcade.draw_text(string.ascii_letters, 0, 0, font_size=int(72 * window.scale), multiline=False,
                     color=(128, 245, 255, 255))
    arcade.draw_text(string.ascii_letters, 0, 0, font_name='Arial')


def preload_UI(window):
    checkbox_scale = 0.25 * window.scale
    checkbox_empty_texture = load_texture('textures/CheckBoxBlue_empty.png')
    checkbox_pressed_texture = load_texture('textures/CheckBoxBlue_pressed.png')
    vote_button_texture = load_texture('textures/skip_vote_button.png')
    vote_button_texture_hovered = load_texture('textures/skip_vote_button_hovered.png')
    vote_button_scale = 0.675 * window.scale
    FixedUITextureToggle(on_texture=checkbox_pressed_texture,
                         off_texture=checkbox_empty_texture,
                         value=False, width=checkbox_empty_texture.width * checkbox_scale,
                         height=checkbox_empty_texture.height * checkbox_scale)
    FixedUITextureButton(width=int(vote_button_texture.width * vote_button_scale),
                         height=int(vote_button_texture.height * vote_button_scale),
                         texture=vote_button_texture,
                         texture_hovered=vote_button_texture_hovered)
    formula_input_height = int(window.GRAPH_BOTTOM_EDGE - 5 - 95 * window.scale)
    formula_input_width = window.SCREEN_WIDTH / 2.88
    AdvancedUIInputText(text='formula', font_size=int(18 * window.scale),
                        text_color=(255, 255, 255),
                        multiline=True, width=formula_input_width,
                        height=formula_input_height)

    close_texture = load_texture('textures/avatar_close_32px.png')
    close_texture_hovered = load_texture('textures/avatar_close_32px_hovered.png')
    swap_button_texture = load_texture('textures/team_swap_32px.png')

    FixedUITextureButton(texture=close_texture,
                         width=int(32 * window.scale),
                         height=int(32 * window.scale),
                         texture_hovered=close_texture_hovered)
    FixedUITextureButton(texture=swap_button_texture,
                         width=int(32 * window.scale),
                         height=int(32 * window.scale))


def main():
    """loading config to get settings,
    creating window  and then main menu view"""

    if getattr(sys, 'frozen', False):
        config_path = os.path.dirname(sys.executable)+'/config.json'
    else:
        config_path = 'config.json'

    if not os.path.isfile(config_path):  # create new standard config file in case of its absence
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
        with open(config_path, 'w') as file:
            json.dump(config, file, indent=4)

    math_graph = Window(antialiasing=True, vsync=True)
    game_configure(math_graph)
    menu_view = MenuView(math_graph)
    math_graph.show_view(menu_view)

    preload_textures()  # caching textures before run
    preload_texts(math_graph)  # glyphs building
    preload_UI(math_graph)  # caching UI elements

    math_graph.run()


try:
    main()
except Exception as e:
    if getattr(sys, 'frozen', False):
        report_path = os.path.dirname(sys.executable)+'/crash_report.txt'
    else:
        report_path = 'crash_report.txt'
    with open(report_path, 'w') as file:
        file.write(str(e))  # creating file with error
