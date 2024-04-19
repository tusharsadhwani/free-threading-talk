import threading
import time


def countdown(n):
    while n > 0:
        n -= 1


def main():
    print(f"Running 4 threads...")
    start = time.time()

    threads = []
    for _ in range(4):
        thread = threading.Thread(target=countdown, args=(50_000_000,))
        threads.append(thread)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    end = time.time()
    print(f"{end - start:.3} seconds.")


if __name__ == "__main__":
    main()
