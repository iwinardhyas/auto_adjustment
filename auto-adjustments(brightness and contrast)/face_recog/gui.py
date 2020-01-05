from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
# from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.filechooser import FileChooser
from os.path import sep, expanduser, isdir, dirname


# Boxlayout is the App class

class BoxLayoutDemo(App):
    # def load_from_filechooser(self, filechooser):
    #     self.load(filechooser.path, filechooser.selection)
    def load(path, selection):
        print(path,  selection)

    def build(self):

        # superBox        = BoxLayout(orientation='vertical')
        superBox        = FloatLayout()


        horizontalBox   = FloatLayout()
        widget_image    = Button(text="tes",size_hint=(.5, .25),pos=(0, 0))
        button1         = Button(text="one",size_hint=(.5, .25),pos=(100, 100))
        button1.bind(on_release = load(FileChooser.path, FileChooser.selection))
        # button2         = Button(text="two")
        # button3         = Button(text="tes")
        horizontalBox.add_widget(button1)
        horizontalBox.add_widget(widget_image)
        # horizontalBox.add_widget(button2)
        # horizontalBox.add_widget(button3)
   

        # verticalBox     = BoxLayout(orientation='vertical')
        # button3         = Button(text="Three")
        # button4         = Button(text="Four")
        # verticalBox.add_widget(button3)
        # verticalBox.add_widget(button4)

   
        superBox.add_widget(horizontalBox)
        # superBox.add_widget(verticalBox)

   
        return superBox

    # def buildlayout(self):
    #     superbox = FloatLayout(size=(300, 300))
    #     button = Button(text="Hello world")
    #     # layout.add_widget(button)
    #     superbox.add_widget(button)
    #     return superbox
   

 

# Instantiate and run the kivy app

if __name__ == '__main__':

    BoxLayoutDemo().run()

