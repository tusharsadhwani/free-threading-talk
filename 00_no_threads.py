import time


def countdown(n):
    while n > 0:
        n -= 1


def main():
    print(f"Running 1 thread...")
    start = time.time()

    countdown(200_000_000)

    end = time.time()
    print(f"{end - start:.3} seconds.")


if __name__ == "__main__":
    main()
