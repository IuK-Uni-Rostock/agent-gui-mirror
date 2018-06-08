#!/usr/bin/env python2

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

class DemonstratorGui(App):

    def build(self):
        return Button(text='hello world')

if __name__ == "__main__":
    DemonstratorGui().run()
