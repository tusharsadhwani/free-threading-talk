import asyncio
import sys

import httpx
from prompt_toolkit.input import create_input
from prompt_toolkit.keys import Keys
import pyfiglet

progress = 0
key_pressed = ""
download_done = asyncio.Event()


async def download_file():
    url = "https://ash-speed.hetzner.com/100MB.bin"
    # 10mb file in case the internet is too slow
    # url = "https://freetestdata.com/wp-content/uploads/2022/02/Free_Test_Data_10MB_MP4.mp4"

    async with httpx.AsyncClient().stream("GET", url) as response:
        total_size = int(response.headers["content-length"])
        downloaded = 0
        with open("/tmp/downloaded.bin", "wb") as f:
            async for chunk in response.aiter_bytes():
                f.write(chunk)
                downloaded += len(chunk)
                global progress
                progress = int(downloaded / total_size * 100)


async def key_listener():
    input = create_input()

    def keys_ready():
        for key_press in input.read_keys():
            if key_press.key == Keys.ControlC:
                download_done.set()
                continue

            global key_pressed
            key_pressed = str(key_press.key).upper()
            if not len(key_pressed) == 1:
                key_pressed = ""

    with input.raw_mode():
        with input.attach(keys_ready):
            await download_done.wait()


async def print_ui():
    while True:
        # clear screen
        sys.stdout.write("\033[2J")

        # print the latest key pressed
        if download_done.is_set():
            exit_msg = "Press again to cancel download..."
            msg_lines = f"\n\n\n\n\n{exit_msg:^100}\n\n\n\n\n\n"
        elif key_pressed == "":
            msg_lines = "\n\n\n\n\n\n\n\n\n\n\n"
        else:
            figlet_text = "\n" + pyfiglet.figlet_format(key_pressed, font="colossal")
            msg_lines = "\n".join(f"{line:^100}" for line in figlet_text.splitlines())

        sys.stdout.write(msg_lines)

        # Show download progress
        progress_bar = "#" * progress + "-" * (100 - progress)
        sys.stdout.write("\r[%s] %d%%" % (progress_bar, progress))

        # move cursor to top left corner
        sys.stdout.write("\033[H")
        sys.stdout.flush()
        # 20fps
        await asyncio.sleep(0.05)


async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(key_listener())
            tg.create_task(download_file())
            tg.create_task(print_ui())
    except asyncio.CancelledError:
        pass


if __name__ == "__main__":
    asyncio.run(main())
