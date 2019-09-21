import kivy
from kivy.app import App
from kivy.uix.label import Widget
from kivy.graphics import Rectangle
from kivy.graphics import Color
    
class Touch(Widget):
    def __init__(self, **kwargs):
        super(Touch, self).__init__(**kwargs)

        with self.canvas:
            x = 0
            y = 0
            for i in range(4):
                for i in range(4):
                    Color(0,1,1, 0.4, mode='rgba')
                    self.rect = Rectangle(pos=(x,y), size = (75,75))
                    x += 150
                x = 0
                y += 150
            x = 75
            y = 75
            for i in range(4):
                for i in range(4):
                    Color(0,1,1, 0.4, mode='rgba')
                    self.rect = Rectangle(pos=(x,y), size = (75,75))
                    x += 150
                x = 75
                y += 150

            x = 75
            y = 0
            for i in range(4):
                for i in range(4):
                    Color(1,1,1, 0.8, mode='rgba')
                    self.rect = Rectangle(pos=(x,y), size = (75,75))
                    x += 150
                x = 75
                y += 150
            x = 0
            y = 75
            for i in range(4):
                for i in range(4):
                    Color(1,1,1, 0.8, mode='rgba')
                    self.rect = Rectangle(pos=(x,y), size = (75,75))
                    x += 150
                x = 0
                y += 150

           
               
                
                
  
            
            
            #Color(1,1,1, 0.7, mode='rgba')
            #self.rect = Rectangle(pos=(50,0), size = (50,50) )

    def on_touch_down(self, touch):
       # self.rect.pos = (touch.pos[0] -25 , touch.pos[1] -20)
       pass

    def on_touch_move(self, touch):
       #  self.rect.pos = (touch.pos[0] -25 , touch.pos[1] -20)
       pass


class MyApp(App):
    def build(self):
        return Touch()


if __name__ == "__main__":
    MyApp().run()

