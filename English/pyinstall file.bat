del /s /q ".\Crossword puzzle.exe"
"%pyinstaller%" -w --icon="Endlish Helper\icon.ico" --key 101108 -F "Endlish Helper\Crossword puzzle.py"
rd /s /q __pycache__
rd /s /q build
rd /s /q dist
"Crossword puzzle.spec"
"%pyinstaller%" "Crossword puzzle.spec"
copy /Y "dist\Crossword puzzle.exe" "Crossword puzzle.exe"
del "Crossword puzzle.spec"
rd /s /q __pycache__
rd /s /q build
rd /s /q dist
rd /s /q "Endlish Helper\__pycache__"