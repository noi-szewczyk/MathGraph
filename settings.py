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

from arcade import gui, Text, set_background_color, color, View, load_texture
from UIFixedElements import *


class SettingsView(View):
    def __init__(self, game):
        super().__init__(game)
        set_background_color(color.COOL_BLACK)
        self.manager = gui.UIManager()
        self.manager.enable()
        self.text_to_draw = []
        with open('config.json', 'r') as file:
            self.param_height = json.load(file)['SCREEN_HEIGHT']
        self.add_ui()

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def add_ui(self):
        self.text_to_draw.clear()
        self.manager.clear()
        ui_anchor = gui.UIAnchorLayout()
        text_size = int(32 * self.window.scale)
        vertical_offset = int(25 * self.window.scale)
        text_color = (128, 245, 255)

        # adding title text
        self.text_to_draw.append(Text('settings', color=text_color, font_size=text_size * 2,
                                      font_name='Arial', anchor_y='top', start_x=self.window.width // 2,
                                      start_y=int(0.95 * self.window.height), anchor_x='center'
                                      )
                                 )
        # adding restart warning text
        self.text_to_draw.append(Text(
            'All changes require manual restart to escape bugs and to become applied', color=(128, 245, 255),
            font_size=text_size, anchor_x='center',
            font_name='Arial', anchor_y='bottom', start_x=self.window.width // 2,
            start_y=int(0.02 * self.window.height)
        )
        )

        # loading essential textures
        switch_texture = load_texture('textures/square_checkBox_empty.png')
        switch_texture_pressed = load_texture('textures/square_checkBox_pressed.png')
        exit_button_texture = load_texture('textures/LobbyExitButton.png')
        exit_button_texture_hovered = load_texture('textures/LobbyExitButton_hovered.png')
        exit_button_scale = 0.9 * self.window.scale
        switch_scale = 0.25 * self.window.scale

        # adding fullscreen mode switcher
        self.full_screen_switch = FixedUITextureToggle(
            off_texture=switch_texture, on_texture=switch_texture_pressed, value=self.window.FULLSCREEN_MODE,
            width=int(switch_scale * switch_texture.width), height=int(switch_scale * switch_texture.height)
        )
        ui_anchor.add(self.full_screen_switch, anchor_x='right', anchor_y='top',
                      align_x=int(-self.full_screen_switch.width - 0.53 * self.window.width),
                      align_y=int(-0.05 * self.window.height - 2 * text_size - 3 * vertical_offset))
        self.text_to_draw.append(
            Text(
                'full screen mode', start_x=self.window.width - int(
                    self.full_screen_switch.width + 0.53 * self.window.width - 25 * self.window.scale),
                start_y=self.window.height + int(-0.05 * self.window.height - 2 * text_size - 3 * vertical_offset -
                                                 self.full_screen_switch.height / 2), anchor_x='left',
                anchor_y='center',
                font_name='Arial', font_size=text_size, color=text_color
            )
        )

        @self.full_screen_switch.event('on_change')
        def change_full_screen(event):
            self.window.FULLSCREEN_MODE = 0 if self.window.FULLSCREEN_MODE else 1
            with open('config.json', 'r') as file:
                config = json.load(file)
            config['FULLSCREEN_MODE'] = self.window.FULLSCREEN_MODE
            with open('config.json', 'w') as file:
                json.dump(config, file, indent=4)
            self.full_screen_switch.value = self.window.FULLSCREEN_MODE
            self.add_ui()

        # adding resolution select
        self.text_to_draw.append(
            Text(
                'select window resolution:', start_x=self.window.width // 2,
                start_y=self.window.height + int(-0.05 * self.window.height - 2 * text_size - 5 * vertical_offset -
                                                 self.full_screen_switch.height), anchor_x='center',
                anchor_y='top', font_name='Arial', font_size=text_size, color=text_color
            )
        )

        # 1280x720
        self.text_to_draw.append(
            Text(
                '1280x720', start_x=self.window.width // 2 - int(250 * self.window.scale),
                start_y=self.window.height + int(-0.05 * self.window.height - 3 * text_size - 6 * vertical_offset -
                                                 self.full_screen_switch.height), anchor_x='center',
                anchor_y='top', font_name='Arial', font_size=text_size // 2, color=text_color
            )
        )
        self.resolution_1280x720 = FixedUITextureToggle(
            off_texture=switch_texture, on_texture=switch_texture_pressed, value=self.param_height == 720,
            width=int(switch_scale * 0.8 * switch_texture.width), height=int(switch_scale * 0.8 * switch_texture.height)
        )
        self.resolution_1280x720.disabled = self.full_screen_switch.value
        ui_anchor.add(self.resolution_1280x720, anchor_x='center', anchor_y='top',
                      align_x=-int(250 * self.window.scale),
                      align_y=int(-0.05 * self.window.height - 3.5 * text_size - 7 * vertical_offset -
                                  self.full_screen_switch.height))

        @self.resolution_1280x720.event('on_change')
        def change_resolution(event):
            with open('config.json', 'r') as file:
                config = json.load(file)
            config['SCREEN_HEIGHT'] = 720
            self.param_height = 720
            config['SCREEN_WIDTH'] = 1280
            with open('config.json', 'w') as file:
                json.dump(config, file, indent=4)
            self.resolution_1280x720.disabled = True
            self.add_ui()

        # 1600x900
        self.text_to_draw.append(
            Text(
                '1600x900', start_x=self.window.width // 2 - int(125 * self.window.scale),
                start_y=self.window.height + int(
                    -0.05 * self.window.height - 3 * text_size - 6 * vertical_offset -
                    self.full_screen_switch.height), anchor_x='center',
                anchor_y='top', font_name='Arial', font_size=text_size // 2, color=text_color
            )
        )
        self.resolution_1600x900 = FixedUITextureToggle(
            off_texture=switch_texture, on_texture=switch_texture_pressed,
            value=self.param_height == 900,
            width=int(switch_scale * 0.8 * switch_texture.width),
            height=int(switch_scale * 0.8 * switch_texture.height)
        )
        self.resolution_1600x900.disabled = self.full_screen_switch.value
        ui_anchor.add(self.resolution_1600x900, anchor_x='center', anchor_y='top',
                      align_x=-int(125 * self.window.scale),
                      align_y=int(-0.05 * self.window.height - 3.5 * text_size - 7 * vertical_offset -
                                  self.full_screen_switch.height))

        @self.resolution_1600x900.event('on_change')
        def change_resolution(event):
            with open('config.json', 'r') as file:
                config = json.load(file)
            config['SCREEN_HEIGHT'] = 900
            self.param_height = 900
            config['SCREEN_WIDTH'] = 1600
            with open('config.json', 'w') as file:
                json.dump(config, file, indent=4)
            self.resolution_1600x900.disabled = True
            self.add_ui()

        # 1920x1080
        self.text_to_draw.append(
            Text(
                '1920x1080', start_x=self.window.width // 2 + int(0 * self.window.scale),
                start_y=self.window.height + int(
                    -0.05 * self.window.height - 3 * text_size - 6 * vertical_offset -
                    self.full_screen_switch.height), anchor_x='center',
                anchor_y='top', font_name='Arial', font_size=text_size // 2, color=text_color
            )
        )
        self.resolution_1920x1080 = FixedUITextureToggle(
            off_texture=switch_texture, on_texture=switch_texture_pressed,
            value=self.param_height == 1080,
            width=int(switch_scale * 0.8 * switch_texture.width),
            height=int(switch_scale * 0.8 * switch_texture.height)
        )
        self.resolution_1920x1080.disabled = self.resolution_1920x1080.value or self.full_screen_switch.value
        ui_anchor.add(self.resolution_1920x1080, anchor_x='center', anchor_y='top',
                      align_x=+int(0 * self.window.scale),
                      align_y=int(-0.05 * self.window.height - 3.5 * text_size - 7 * vertical_offset -
                                  self.full_screen_switch.height))

        @self.resolution_1920x1080.event('on_change')
        def change_resolution(event):
            with open('config.json', 'r') as file:
                config = json.load(file)
            config['SCREEN_HEIGHT'] = 1080
            self.param_height = 1080
            config['SCREEN_WIDTH'] = 1920
            with open('config.json', 'w') as file:
                json.dump(config, file, indent=4)
            self.resolution_1920x1080.disabled = True
            self.add_ui()

        # 2560x1440
        self.text_to_draw.append(
            Text(
                '2560x1440', start_x=self.window.width // 2 + int(125 * self.window.scale),
                start_y=self.window.height + int(
                    -0.05 * self.window.height - 3 * text_size - 6 * vertical_offset -
                    self.full_screen_switch.height), anchor_x='center',
                anchor_y='top', font_name='Arial', font_size=text_size // 2, color=text_color
            )
        )
        self.resolution_2560x1440 = FixedUITextureToggle(
            off_texture=switch_texture, on_texture=switch_texture_pressed,
            value=self.param_height == 1440,
            width=int(switch_scale * 0.8 * switch_texture.width),
            height=int(switch_scale * 0.8 * switch_texture.height)
        )
        self.resolution_2560x1440.disabled = self.resolution_2560x1440.value or self.full_screen_switch.value
        ui_anchor.add(self.resolution_2560x1440, anchor_x='center', anchor_y='top',
                      align_x=+int(125 * self.window.scale),
                      align_y=int(-0.05 * self.window.height - 3.5 * text_size - 7 * vertical_offset -
                                  self.full_screen_switch.height))

        @self.resolution_2560x1440.event('on_change')
        def change_resolution(event):
            with open('config.json', 'r') as file:
                config = json.load(file)
            config['SCREEN_HEIGHT'] = 1440
            self.param_height = 1440
            config['SCREEN_WIDTH'] = 2560
            with open('config.json', 'w') as file:
                json.dump(config, file, indent=4)
            self.resolution_2560x1440.disabled = True
            self.add_ui()

        # 3840x2160
        self.text_to_draw.append(
            Text(
                '3840x2160', start_x=self.window.width // 2 + int(250 * self.window.scale),
                start_y=self.window.height + int(
                    -0.05 * self.window.height - 3 * text_size - 6 * vertical_offset -
                    self.full_screen_switch.height), anchor_x='center',
                anchor_y='top', font_name='Arial', font_size=text_size // 2, color=text_color
            )
        )
        self.resolution_3840x2160 = FixedUITextureToggle(
            off_texture=switch_texture, on_texture=switch_texture_pressed,
            value=self.param_height == 2160,
            width=int(switch_scale * 0.8 * switch_texture.width),
            height=int(switch_scale * 0.8 * switch_texture.height)
        )
        self.resolution_3840x2160.disabled = self.resolution_3840x2160.value or self.full_screen_switch.value
        ui_anchor.add(self.resolution_3840x2160, anchor_x='center', anchor_y='top',
                      align_x=+int(250 * self.window.scale),
                      align_y=int(-0.05 * self.window.height - 3.5 * text_size - 7 * vertical_offset -
                                  self.full_screen_switch.height))

        @self.resolution_3840x2160.event('on_change')
        def change_resolution(event):
            with open('config.json', 'r') as file:
                config = json.load(file)
            config['SCREEN_HEIGHT'] = 2160
            self.param_height = 2160
            config['SCREEN_WIDTH'] = 3840
            with open('config.json', 'w') as file:
                json.dump(config, file, indent=4)
            self.resolution_3840x2160.disabled = True
            self.add_ui()

        # adding exit settings button
        exit_button = FixedUITextureButton(texture=exit_button_texture,
                                           width=int(
                                               exit_button_scale * exit_button_texture.width),
                                           height=int(
                                               exit_button_scale * exit_button_texture.height),
                                           texture_hovered=
                                           exit_button_texture_hovered)
        exit_button.on_click = self.go_back
        ui_anchor.add(exit_button, anchor_y='bottom',
                      align_y=int(0.02 * self.window.height + 2 * vertical_offset + text_size))

        self.manager.add(ui_anchor)

    def go_back(self, event):
        from menu import  MenuView
        view = MenuView(self.window)
        self.window.show_view(view)

    def on_draw(self):
        self.clear()
        arcade.start_render()

        # drawing text
        for text in self.text_to_draw:
            text.draw()

        # drawing GUI
        self.manager.draw()

        arcade.finish_render()
