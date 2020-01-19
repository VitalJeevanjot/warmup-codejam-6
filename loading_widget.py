import random

from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.logger import Logger



class LoadingWidget(Widget):
    def set_alpha_channel(self, opacity):
        self.color = [self.color[i] for i in range(3)] + [opacity]


class LoadingWidgets(Widget):
    child_number = NumericProperty()

    def __init__(self, **kwargs):
        super(LoadingWidgets, self).__init__(**kwargs)
        Logger.info(f'Loading widgets pos: {self.pos}, size: {self.size}')
        self.child_number = kwargs.get('child_number', 5)
        for i in range(1, self.child_number + 1):
            widget = LoadingWidget()
            widget.opacity = 0
            widget.set_alpha_channel(i/4)
            Logger.info(f'Widget #{i} pos: {widget.pos}, size: {widget.size}')
            self.add_widget(widget)
        self.anims = []
        self.animating = False

    def on_pos(self, width, height):
        Logger.info(f'Loading widgets pos changed: {self.pos}, size: {self.size}')
        for widget in self.children:
            widget.pos = self.pos

    def on_size(self, width, height):
        Logger.info(f'Loading widgets size changed: {self.pos}, size: {self.size}')
        for widget in self.children:
            widget.size = [self.height, self.height]

    def start(self):
        i = 1
        self.animating = True
        for widget in self.children:
            widget.opacity = 100
            anim = Animation(x=self.pos[0] + self.width, y=self.pos[1],
                             duration=self._anim_duration(i), t='in_circ') + \
                Animation(x=self.pos[0], y=self.pos[1],
                          duration=self._anim_duration(i), t='in_circ')
            anim.bind(on_complete=self._on_complete)
            anim.repeat = True
            self.anims.append(anim)
            anim.start(widget)
            i += 1

    def stop(self):
        for anim in self.anims:
            anim.repeat = False
        self.animating = False

    def _on_complete(self, animation, widget):
        if not self.animating:
            widget.opacity = 0
            widget.pos = self.pos

    def _anim_duration(self, i):
        return i/(self.child_number ^ 2) + 0.5
