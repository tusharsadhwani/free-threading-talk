import multiprocessing
import time


def countdown(n):
    while n > 0:
        n -= 1


def main():
    print(f"Running 4 processes...")
    start = time.time()

    procs = []
    for _ in range(4):
        proc = multiprocessing.Process(target=countdown, args=(50_000_000,))
        procs.append(proc)

    for proc in procs:
        proc.start()
    for proc in procs:
        proc.join()

    end = time.time()
    print(f"{end - start:.3} seconds.")


if __name__ == "__main__":
    main()
