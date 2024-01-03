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
"""This file is used bc  in arcade3.0.0.dev26 there are
    still many bugs with UIInputText, UITextureButton and UITextureToggle and it doesn't work
    great:
        combinations such as ctrl+x doesn't work for Input,
        old textures are not cleared in buttons and toggles 
    so it's temporary feature I hope
"""

from arcade.gui import UIEvent, UIInputText, UIKeyEvent, Surface, UITextureButton, UITextureToggle
from arcade.types import RGBOrA255, RGB
from pyglet.text.caret import Caret
from pyglet.text.document import AbstractDocument
import pyglet.text
import pyperclip
import arcade.key
from typing import Optional


class FixedUITextureButton(UITextureButton):

    def do_render(self, surface: Surface):
        self.prepare_render(surface)

        style = self.get_current_style()

        # update label
        self.apply_style(style)

        current_state = self.get_current_state()
        current_texture = self._textures.get(current_state)
        if current_texture:
            surface.clear()
            surface.draw_texture(0, 0, self.content_width, self.content_height, current_texture)


class AdvancedUIInputText(UIInputText):

    def __init__(
            self,
            x: float = 0,
            y: float = 0,
            width: float = 100,
            height: float = 24,
            text: str = "",
            font_name=("Arial",),
            font_size: float = 12,
            text_color: RGBOrA255 = (0, 0, 0, 255),
            multiline=False,
            caret_color: RGB = (0, 0, 0),
            size_hint=None,
            size_hint_min=None,
            size_hint_max=None,
            **kwargs,
    ):
        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height,
            size_hint=size_hint,
            size_hint_min=size_hint_min,
            size_hint_max=size_hint_max,
            **kwargs,
        )

        self.last_event = None
        self._active = False
        self._text_color = text_color if len(text_color) == 4 else (*text_color, 255)
        self.doc: AbstractDocument = pyglet.text.decode_text(text)
        self.doc.set_style(0, len(text),
                           dict(font_name=font_name, font_size=font_size, color=self._text_color),
                           )

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.doc, width - self.LAYOUT_OFFSET, height, multiline=multiline)
        self.layout.x += self.LAYOUT_OFFSET
        self.caret = Caret(self.layout, color=(3, 11, 163, 255))
        self.caret.visible = True
        self.caret.PERIOD = 0.2
        self._blink_state = self._get_caret_blink_state()

    def on_event(self, event: UIEvent) -> Optional[bool]:
        if isinstance(event, UIKeyEvent):
            if self.last_event:
                self.last_event = None
                return super().on_event(event)
            document: AbstractDocument = self.layout.document
            if event.symbol == arcade.key.X and event.modifiers & arcade.key.MOD_CTRL:
                # Copy
                text = document.text[self.layout.selection_start:self.layout.selection_end]
                pyperclip.copy(text)
                # Delete
                self.caret.on_text_motion(motion=arcade.key.MOTION_DELETE)
                self.last_event = True

            elif event.symbol == arcade.key.C and event.modifiers & arcade.key.MOD_CTRL:
                # Copy
                text = document.text[self.layout.selection_start:self.layout.selection_end]
                pyperclip.copy(text)
                self.last_event = True

            elif event.symbol == arcade.key.V and event.modifiers & arcade.key.MOD_CTRL:
                # Paste
                text = pyperclip.paste()
                self.caret.on_text(text)
                self.last_event = True

            elif event.symbol == arcade.key.A and event.modifiers & arcade.key.MOD_CTRL:
                # selecting whole text
                self.caret.move_to_point(0, 1000)
                self.caret._mark = 0
                self.caret.select_to_point(4000, -1000)
                self.last_event = True

        return super().on_event(event)


class FixedUITextureToggle(UITextureToggle):

    def do_render(self, surface: Surface):
        self.prepare_render(surface)
        tex = self.normal_on_tex if self.value else self.normal_off_tex
        if self.pressed:
            tex = self.pressed_on_tex if self.value else self.pressed_off_tex
        elif self.hovered:
            tex = self.hover_on_tex if self.value else self.hover_off_tex
        surface.clear()
        surface.draw_texture(0, 0, self.content_width, self.content_height, tex)
