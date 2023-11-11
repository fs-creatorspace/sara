import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock

class TypewriterLabel(Label):
    def animate_text(self, text):
        self.displayed_text = ''
        self.full_text = text
        Clock.schedule_interval(self.add_character, 0.1)

    def add_character(self, _):
        if len(self.displayed_text) < len(self.full_text):
            self.displayed_text += self.full_text[len(self.displayed_text)]
            self.text = self.displayed_text
        else:
            return False

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='horizontal')
        self.image = Image(source='img/image.jpg', allow_stretch=True, keep_ratio=True)  # replace with your image file path
        layout.add_widget(self.image)
        right_layout = BoxLayout(orientation='vertical')
        self.label = TypewriterLabel()
        self.button = Button(text='Write Text', on_press=self.write_text)
        right_layout.add_widget(self.label)
        right_layout.add_widget(self.button)
        layout.add_widget(right_layout)
        return layout

    def write_text(self, _):
        self.label.animate_text('Lorem ipsum dolor sit amet')

if __name__ == '__main__':
    MyApp().run()