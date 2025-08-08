# XO — Styled Tic Tac Toe

This project creates a styled Tic-Tac-Toe (XO) desktop app using Python + tkinter.

## What is included
- `xo_game_styled.py` — the Python source for the game
- `assets/game_icon.ico` — icon used for the app (generated or extracted)
- GitHub Actions workflow to build a Windows .exe automatically

## Build locally (Windows)
1. Install Python 3.11 and ensure `python` and `pip` are in PATH.
2. Install PyInstaller: `pip install pyinstaller pillow`
3. From project root, run:
   ```
   pyinstaller --onefile --windowed --icon=assets/game_icon.ico xo_game_styled.py --name "XO_Styled"
   ```
4. Find the exe in `dist\XO_Styled.exe` and share it.

## Build automatically via GitHub Actions (recommended)
1. Create a new GitHub repository.
2. Push all files in this folder to the `main` branch of the repo.
3. Go to **Actions** tab on GitHub; the workflow `Build Windows EXE` will run on push or you can trigger it manually.
4. After the workflow finishes, download the artifact `XO_Styled_windows_exe` which contains `XO_Styled.exe`.

## Notes
- The AI uses minimax and is hard to beat.
- Make sure you have rights to distribute any assets combined into the build.
- If you'd like additional styling, sounds, or packaging (installer, code signing), tell me and I can add it.
