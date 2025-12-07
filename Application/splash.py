from kivymd.uix.screen import MDScreen
class Splash(MDScreen):
    def on_enter(self):
        self.ids.progress.start()