import keyboard

def on_key_press(event):
    # Monitor key presses
    if event.name.isalpha():
        keyboard.send('backspace')  # Delete the key
    if event.name in ['shift', 'ctrl', 'alt']:
    	keyboard.release()

# Hook keyboard events
keyboard.on_press(on_key_press)
