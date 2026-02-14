# 🎨 Advanced Logo Generator

A powerful Python-based tool for generating modern, harmonious logos with a sleek, dark-themed GUI.

![Logo Generator GUI](random_logo.png)

## 🚀 Quick Start (Windows)

The easiest way to run the application is using the provided batch file:

1.  Open the project folder.
2.  Double-click **`run_gui.bat`**.

This will automatically set up the virtual environment, install dependencies, and launch the GUI.

## ✨ Features

- **Batch Generation**: Creates 5 unique variations every time you click generate.
- **Carousel Navigation**: Effortlessly browse through generated logos with "Next" and "Previous" buttons.
- **Custom Text**: Enter your brand name directly into the GUI.
- **Harmonious Colors**: Uses triadic, analogous, and monochromatic rules for professional aesthetics.
- **Multiple Templates**: Includes Hexagon Tech, Shield Badge, Minimal Circle, and more.

## 🛠️ Manual Installation

If you prefer to set up the environment yourself:

1.  **Clone/Copy** the project directory.
2.  **Create a Virtual Environment**:
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Install Dependencies**:
    ```powershell
    pip install gizeh numpy Pillow cairosvg pycairo
    ```
4.  **Cairo Binaries (Critical)**:
    - This project bundles `libcairo-2.dll` and its dependencies in the root folder.
    - The script uses `os.add_dll_directory()` to ensure these are loaded correctly on Windows.

## 🖥️ Usage

### Running the GUI
```powershell
.\venv\Scripts\activate
python gui.py
```

### Running the CLI (Random Generator)
```powershell
.\venv\Scripts\activate
$env:LOGO_CHOICE='2'
python logo_generator.py
```

## 🏗️ Technical Stack

- **Graphics**: [Gizeh](https://github.com/Zulko/gizeh) (Cairo-based)
- **GUI**: Tkinter (Standard Python GUI)
- **Image Processing**: Pillow (PIL)
- **Math**: NumPy

## 📝 License
MIT
a
