import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.app import JKBApp

if __name__ == "__main__":
    app = JKBApp()
    app.mainloop()