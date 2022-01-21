import tkinter as tk
from app import Window
from field import Tile

def draw_tile(w):
  w.canvas.create_rectangle(30, 10, 120, 80, outline="#fb0", fill="#fb0")

def main():
  root = tk.Tk()
  win = Window()

  root.geometry("400x100+300+300")
  root.mainloop()

  root.after(100, draw_tile, win) #needs to be threaded
                                  #https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop has threading example


if __name__ == '__main__':
    main()