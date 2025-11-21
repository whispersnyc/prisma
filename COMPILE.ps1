# Sample build command for PyInstaller to create a self-extracting executable
./.venv/Scripts/pyinstaller --noconfirm --onedir --name "Prismo" --clean --add-data "./resources;resources/" "./main.py"
