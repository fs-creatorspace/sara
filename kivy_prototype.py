import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label

class GIFChangerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Initial GIF and label
        self.initial_gif = Image(source="./img/initial.gif")  
        self.layout.add_widget(self.initial_gif)

        self.label = Label(text="Initial Value")
        self.layout.add_widget(self.label)

        # Button to change GIF and value
        self.button = Button(text="Change GIF and Value")
        self.button.bind(on_press=self.on_button_click)
        self.layout.add_widget(self.button)

        return self.layout

    def on_button_click(self, instance):
        # Change the GIF and label text
        self.initial_gif.source = "./img/changed.gif" 
        self.label.text = "New Value"

if __name__ == '__main__':
    GIFChangerApp().run()
