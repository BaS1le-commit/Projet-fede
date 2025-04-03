import os
import sys
import threading
from src.interface import App
from src.clavier import ClavierController


if __name__ == "__main__":
    app = App()

    clavier_thread = threading.Thread(target=ClavierController(app), daemon=True)
    clavier_thread.start()

    app.mainloop()