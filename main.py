#!/usr/bin/env python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.interface import FileForgeUI

if __name__ == "__main__":
    app = FileForgeUI()
    app.mainloop()