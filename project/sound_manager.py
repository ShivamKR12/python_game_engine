# sound_manager.py

from direct.showbase.ShowBase import AudioManager

class SoundManager:
    def __init__(self):
        self.audio_manager = AudioManager()
        self.sounds = {}
        self.music = None

    def load_sounds(self, sound_files):
        for name, file in sound_files.items():
            self.sounds[name] = self.audio_manager.loadSfx(file)

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()

    def play_music(self, file, loop=True):
        self.music = self.audio_manager.loadMusic(file)
        if loop:
            self.music.setLoop(True)
        self.music.play()
