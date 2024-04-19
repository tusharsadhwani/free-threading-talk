import sys
import threading
import time

import pyfiglet
from pynput.keyboard import Listener, Key, KeyCode


fibonacci_message = ""
key = ""
done = threading.Event()


def fib(n):
    if n < 2:
        return 1

    return fib(n - 1) + fib(n - 2)


def calculate_fibonacci():
    global fibonacci_message
    fibonacci_message = "Calculating fib(37)..."
    result = fib(37)
    fibonacci_message = f"fib(37) is {result}"


def key_listener():
    def on_press(key_press):
        if key_press == Key.esc:
            done.set()
            return False  # break

        elif key_press == Key.space:
            global fibonacci_message
            threading.Thread(target=calculate_fibonacci).start()

        if isinstance(key_press, KeyCode):
            global key
            key = key_press.char.upper()

    listener = Listener(on_press=on_press, suppress=True)
    listener.start()
    listener.join()


def print_ui():
    while not done.is_set():
        # clear screen
        sys.stdout.write("\033[2J")

        if key == "":
            msg_lines = "\n\n\n\n\n\n\n\n\n\n\n"
        else:
            figlet_text = "\n" + pyfiglet.figlet_format(key, font="colossal")
            msg_lines = "\n".join(f"{line:^100}" for line in figlet_text.splitlines())

        sys.stdout.write(msg_lines)

        # print fib(37)
        sys.stdout.write(f"\n{fibonacci_message:^100}\n")

        # move cursor to top left corner
        sys.stdout.write("\033[H")
        sys.stdout.flush()

        # 10fps
        time.sleep(0.1)


def main():
    threads = [
        threading.Thread(target=key_listener),
        threading.Thread(target=print_ui),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
