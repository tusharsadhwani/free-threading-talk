import asyncio
import sys

from prompt_toolkit.input import create_input
from prompt_toolkit.keys import Keys
import pyfiglet

fibonacci_message = ""
key = ""
cancelled = asyncio.Event()


def fib(n):
    if n < 2:
        return 1

    return fib(n - 1) + fib(n - 2)


def calculate_fibonacci():
    global fibonacci_message
    fibonacci_message = "Calculating fib(37)..."
    result = fib(37)
    fibonacci_message = f"fib(37) is {result}"


async def key_listener():
    input = create_input()

    def keys_ready():
        for key_press in input.read_keys():
            if key_press.key == Keys.Escape:
                cancelled.set()

            elif key_press.key == " ":
                calculate_fibonacci()

            global key
            key = str(key_press.key).upper()
            if not len(key) == 1:
                key = ""

    with input.raw_mode():
        with input.attach(keys_ready):
            await cancelled.wait()


async def print_ui():
    while True:
        # clear screen
        sys.stdout.write("\033[2J")

        if cancelled.is_set():
            raise asyncio.CancelledError

        if key == "":
            msg_lines = "\n\n\n\n\n\n\n\n\n\n\n"
        else:
            figlet_text = "\n" + pyfiglet.figlet_format(key, font="colossal")
            msg_lines = "\n".join(f"{line:^100}" for line in figlet_text.splitlines())

        sys.stdout.write(msg_lines)

        # print fib(40)
        sys.stdout.write(f"\n{fibonacci_message:^100}")

        # move cursor to top left corner
        sys.stdout.write("\033[H")
        sys.stdout.flush()

        # 10fps
        await asyncio.sleep(0.1)


async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(key_listener())
            tg.create_task(print_ui())
    except asyncio.CancelledError:
        pass


if __name__ == "__main__":
    asyncio.run(main())
