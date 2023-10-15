import os
import subprocess
from pathlib import Path
import nicegui

cmd = [
    "C:\\Users\\Owner\\src\\budgettrackingapp\\venv\\Scripts\\python.exe",
    "-m",
    "PyInstaller",
    "main.py",  # your main file with ui.run()
    "-i",  # For the App Icon
    "C:\\Users\\Owner\\src\\budgettrackingapp\\assets\\budgeting.ico",
    "--name",
    "BudgetingApp",  # name of your app
    "--onefile",
    "--windowed",  # prevent console appearing, only use with ui.run(native=True, ...)
    "--add-data",
    f"{Path(nicegui.__file__).parent}{os.pathsep}nicegui",
]
subprocess.call(cmd)
