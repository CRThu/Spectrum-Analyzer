rmdir /s /q App
pyinstaller --distpath=./App/dist --workpath=./App/build --specpath=./App --clean --onedir --windowed --name=GUI gui_main.py