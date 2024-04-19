import concurrent.futures
import time

x = 0


def increment():
    global x
    for _ in range(10_000_000):
        x += 1


def main():
    start = time.time()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for _ in range(4):
            executor.submit(increment)

    end = time.time()

    print(f"{x = :_}")
    print(f"Time taken: {end - start:.3f} seconds")


if __name__ == "__main__":
    main()
