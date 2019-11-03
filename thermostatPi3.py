import kivy
kivy.require('1.11.1') 

from kivy.app import App
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class LoginScreen(GridLayout):    


        def __init__(self, **kwargs):
                super(LoginScreen, self).__init__(**kwargs)

                virtual_keyboard = GridLayout(cols=3)
                virtual_keyboard.add_widget(Button(text='1'))
                virtual_keyboard.add_widget(Button(text='2'))
                virtual_keyboard.add_widget(Button(text='3'))
                virtual_keyboard.add_widget(Button(text='4'))
                virtual_keyboard.add_widget(Button(text='5'))
                virtual_keyboard.add_widget(Button(text='6'))
                virtual_keyboard.add_widget(Button(text='7'))
                virtual_keyboard.add_widget(Button(text='8'))
                virtual_keyboard.add_widget(Button(text='9'))
                virtual_keyboard.add_widget(Button(text='-'))
                virtual_keyboard.add_widget(Button(text='0'))
                virtual_keyboard.add_widget(Button(text='-'))

                self.cols = 2
                self.add_widget(Label(text='thermostatPi\ninsert password to login'))
                self.password = TextInput(password=True, multiline=False)
                self.add_widget(self.password)
                self.add_widget(virtual_keyboard)
                self.add_widget(Button(text='Login'))

class thermostatPi3(App):



        def build(self):
                # Set app title
                self.title = 'thermostatPi3'
                # Set app screen dimensions
                Config.set('graphics', 'width', '480')
                Config.set('graphics', 'height', '320')
                # Uncomment in release stage
                #Config.set('graphics', 'borderless', '1')
 
                return LoginScreen()


if __name__ == '__main__':
        thermostatPi3().run()
