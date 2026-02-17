"""番茄時鐘應用程式入口點。"""

import tkinter as tk

from src.app import PomodoroApp
from src.timer import Timer


def main() -> None:
    root = tk.Tk()
    timer = Timer()
    PomodoroApp(root, timer)
    root.mainloop()


if __name__ == "__main__":
    main()
