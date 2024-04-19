import multiprocessing

items = []


def append_items():
    items.append("Spam")
    items.append("Eggs")
    items.append("Bacon")


def main():
    print(f"Running 4 processes...")

    procs = []
    for _ in range(4):
        proc = multiprocessing.Process(target=append_items)
        procs.append(proc)

    for proc in procs:
        proc.start()
    for proc in procs:
        proc.join()

    print("Items:", items)


if __name__ == "__main__":
    main()
