# ui.py

from direct.gui.OnscreenText import OnscreenText

class UI:
    def __init__(self):
        self.health_text = OnscreenText(text='Health: 100', pos=(-0.9, 0.8), scale=0.07)
        self.ammo_text = OnscreenText(text='Ammo: 30', pos=(-0.9, 0.7), scale=0.07)

    def draw_health_bar(self, health):
        self.health_text.setText(f'Health: {health}')

    def draw_ammo_count(self, ammo):
        self.ammo_text.setText(f'Ammo: {ammo}')

