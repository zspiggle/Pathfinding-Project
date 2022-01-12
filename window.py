import tkinter as tk





class Window(tk.Frame):

  def __init__(self):
    super().__init__()

    self.initUI()


  def initUI(self):
    self.master.title("Pathfinding")
    self.pack(fill=tk.BOTH, expand=1)

    canvas = tk.Canvas(self)
    canvas.create_rectangle(30, 10, 120, 80,
        outline="#fb0", fill="#fb0")
    canvas.create_rectangle(150, 10, 240, 80,
        outline="#f50", fill="#f50")
    canvas.create_rectangle(270, 10, 370, 80,
        outline="#05f", fill="#05f")
    canvas.pack(fill=tk.BOTH, expand=1)


def main():
  root = tk.Tk()
  win = Window()
  root.geometry("400x100+300+300")
  root.mainloop()


if __name__ == '__main__':
    main()