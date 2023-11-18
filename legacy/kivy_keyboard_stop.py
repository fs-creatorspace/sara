from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window

class MyKeyboardApp(App):
    def build(self):
        self.label = Label(text="Press a key!")
        Window.bind(on_key_down=self.on_keyboard_down)
        return self.label

    def on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):

        if text == 'w':     #start Conversation
            self.label.text = "This is the start of your Conversation"
            
        if text == 's':     # stop conversation
            self.label.text = "Conversation stopped"

if __name__ == '__main__':
    MyKeyboardApp().run()