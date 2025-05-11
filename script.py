# Name: KeyboardManager
# Description: A utility to filter keyboard input
# Author: KeyOnTheBoard
# Version: 1.0.0

import time
from pynput.keyboard import Listener, Key, Controller

def sanitize_input(key):
    try:
        if hasattr(key, 'char') and key.char.isalpha():  # Only letters
            keyboard.press(Key.backspace)
            keyboard.release(Key.backspace)
            time.sleep(0.01)  # Small delay to avoid flooding
    except AttributeError:
        pass

if __name__ == "__main__":
    keyboard = Controller()
    print("Keyboard sanitizer running (Ctrl+C to exit)...")
    with Listener(on_press=sanitize_input) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            print("\nExiting safely.")
