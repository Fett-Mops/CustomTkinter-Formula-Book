import tkinter as tk
from tkinter import *
import json as js


   
class App():
   win = Tk()
   win.geometry("500x500")
   def __init__(self):
      super().__init__()
   
   def read_json(filename):
      with open (filename) as f:
         data = js.load(f)
         return data

   def write_json(data, filename): 
      with open (filename, 'w') as f:
         js.dump(data, f, indent=4)
   win.mainloop()
   

      







app = App()
