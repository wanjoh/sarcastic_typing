from pynput import keyboard
from pynput.keyboard import KeyCode, Key, Controller

mocking: bool = False
binds: list[set[Key | KeyCode]] = [{Key.alt_l, KeyCode.from_char('m')}, {Key.alt_l, KeyCode.from_char('M')}]
pressed: set[Key | KeyCode] = set()  # current pressed buttons
controller = Controller()
debug = False


def toggle_mocking():
    global mocking
    mocking = not mocking
    print(f"mocking is {'on' if mocking else 'off'}")


def on_press(key):

    if any([key in bind for bind in binds]):
        pressed.add(key)
    if pressed in binds:
        toggle_mocking()
        pressed.remove(key)

    if mocking and hasattr(key, 'char') and key.char.isalpha():
        controller.press(Key.caps_lock)
        controller.release(Key.caps_lock)

    if debug:
        print(pressed)


def on_release(key):
    if key in pressed:
        pressed.remove(key)

    if debug:
        print(pressed)


if __name__ == '__main__':
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
